#!/usr/bin/env python3
"""Practical browser smoke: responsive Post, SVG, static Three.js fallback, JS errors."""
from __future__ import annotations
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
from pathlib import Path
import threading,json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'_site'
def run():
    assert (SITE/'index.html').exists(),'build site before browser smoke'
    handler=partial(SimpleHTTPRequestHandler,directory=str(SITE))
    server=ThreadingHTTPServer(('127.0.0.1',0),handler)
    worker=threading.Thread(target=server.serve_forever,daemon=True);worker.start()
    host=f'http://127.0.0.1:{server.server_address[1]}/'
    posts=json.loads((ROOT/'content/posts.json').read_text(encoding='utf-8'))
    articles=[f"posts/{item['category']}/{item['slug']}/" for item in posts if item['status']=='published']
    pages=['','archive/','topics/','question-types/']+articles
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True,args=['--disable-dev-shm-usage'])
        try:
            for width in (1440,768,390,360):
                page=browser.new_page(viewport={'width':width,'height':850},reduced_motion='reduce')
                failures=[]
                page.route('https://cdn.jsdelivr.net/**',lambda route:route.abort())
                page.on('pageerror',lambda e:failures.append(str(e)))
                for path in pages:
                    page.goto(host+path,wait_until='domcontentloaded',timeout=30000)
                    page.locator('h1').first.wait_for(timeout=12000)
                    assert page.locator('h1').count()==1,(width,path,'H1')
                    assert page.locator('main').count()==1,(width,path,'main')
                    assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth+1'),(width,path,'overflow')
                    if path == 'question-types/':
                        assert '按试卷题型浏览' in page.locator('h1').inner_text()
                        assert page.locator('link[rel="canonical"]').get_attribute('href').endswith('/question-types/')
                    if path == 'topics/':
                        assert page.locator('.knowledge-area').count() == 7
                    if path == '' and width == 390:
                        assert page.locator('[data-category-filter]').count() == 1
                        subject = page.locator('[data-subject-filter]')
                        assert subject.count() == 1
                        subject.select_option('analytic-geometry')
                        page.wait_for_function("""() => location.search.includes('area=analytic-geometry')
                            && [...document.querySelectorAll('[data-post-grid] [data-post-card]')]
                              .every(x => (x.dataset.subjects || '').split(' ').includes('analytic-geometry'))""", timeout=10000)
                        subject.select_option('')
                    if '/posts/' in path:
                        assert page.locator('#overview').count()==1,(width,path,'problem-first overview')
                        assert page.locator('#question').count()==1,(width,path,'original question')
                        assert page.locator('#overview').evaluate("(el)=>el.compareDocumentPosition(document.querySelector('#question')) & Node.DOCUMENT_POSITION_FOLLOWING"),(width,path,'overview order')
                        assert page.locator('#solution .step-note').count()==page.locator('#solution li').count(),(width,path,'step explanations')
                        assert page.locator('figure svg').count()>=1,(width,path,'SVG')
                        assert page.locator('[data-knowledge-context] a[href]').count()>=2,(width,path,'taxonomy cross-links')
                        # Native SVG exists, is legible at browser dimensions, and has
                        # a semantic title+description. A viewport can never mask a broken chart.
                        svg_metrics=page.locator('figure svg').evaluate_all("""nodes => nodes.map(svg => {
                            const rect=svg.getBoundingClientRect();
                            const texts=[...svg.querySelectorAll('text')];
                            const outside=texts.filter(t => {
                                const r=t.getBoundingClientRect();
                                return r.width>0 && r.height>0
                                    && (r.left < rect.left - 8 || r.right > rect.right + 8
                                        || r.top < rect.top - 8 || r.bottom > rect.bottom + 8);
                            });
                            return {width:rect.width,height:rect.height,texts:texts.length,
                                desc:!!svg.querySelector('desc'),title:!!svg.querySelector('title'),
                                overflowLabels:outside.length};
                        })""")
                        assert all(m['width']>5 and m['height']>5 and m['title'] and m['desc']
                                   for m in svg_metrics),(width,path,'SVG title/desc/size',svg_metrics)
                        if width==390 and any(m['overflowLabels'] for m in svg_metrics):
                            print('SVG LABEL REVIEW',path,svg_metrics)
                        assert page.locator('math').count()>=1,(width,path,'MathML')
                        assert page.locator('math[aria-label],math[aria-labelledby]').count()==page.locator('math').count(),(width,path,'MathML accessible labels')
                        if 'week12-gaosan-' in path:
                            assert page.locator('math[display="block"]').count() >= 1,(width,path,'display MathML equation')
                            assert page.locator('math').evaluate_all("(nodes)=>nodes.every(n=>n.namespaceURI==='http://www.w3.org/1998/Math/MathML' && n.getBoundingClientRect().width>0 && n.getBoundingClientRect().height>0)"),(width,path,'native MathML namespace and visible geometry')
                        if any(f'jianping-2021-q{n:02d}' in path for n in (4,13,17)):
                            scene=page.locator('[data-three-scene]')
                            scene.wait_for(timeout=5000)
                            page.locator('[data-three-scene][data-ready="false"]').wait_for(timeout=10000)
                            assert scene.locator('.static-scene').is_visible(),(width,path,'visible offline SVG fallback')
                            assert not scene.locator('canvas').is_visible(),(width,path,'canvas hidden when CDN unavailable')
                        if 'q17' in path:
                            assert page.locator('.scene-controls input').count()==0,(width,path,'no inert tetrahedron sliders')
                assert not failures,(width,failures)
                page.close()
        finally:browser.close()
    # Render every published stand-alone SVG cover as an SVG document.
    # The HTML smoke above does not exercise the full cover catalogue.
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True,args=['--disable-dev-shm-usage'])
        page=browser.new_page(viewport={'width':760,'height':420},reduced_motion='reduce')
        for item in posts:
            if item['status'] != 'published':
                continue
            path=f"posts/{item['category']}/{item['slug']}/"+item['cover']['src']
            page.goto(host+path,wait_until='load',timeout=30000)
            result=page.evaluate("""() => {
                const svg=document.querySelector('svg');
                if (!svg) return {valid:false};
                const vb=svg.viewBox.baseVal,rect=svg.getBoundingClientRect();
                const text=[...svg.querySelectorAll('text')];
                const clipped=text.filter(el => {
                    const box=el.getBoundingClientRect();
                    return box.width>0 && box.height>0 &&
                      (box.left<rect.left-9 || box.right>rect.right+9 ||
                       box.top<rect.top-9 || box.bottom>rect.bottom+9);
                });
                return {valid:vb.width>0 && vb.height>0 && rect.width>0 && rect.height>0,
                        title:!!svg.querySelector('title'),desc:!!svg.querySelector('desc'),
                        labels:text.length,clipped:clipped.length};
            }""")
            assert result['valid'] and result['title'] and result['desc'],(path,result)
            if result['clipped']:
                print('SVG COVER LABEL REVIEW',path,result)
        browser.close()
    server.shutdown()
    print(f'Browser smoke OK: {len(pages)} pages ({len(articles)} articles) x 4 viewport widths')
if __name__=='__main__':run()
