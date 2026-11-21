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
    papers=json.loads((ROOT/'content/papers.json').read_text(encoding='utf-8'))
    public_papers=[paper for paper in papers if any(
        item['paper_id']==paper['id'] and item['status']=='published' for item in posts
    )]
    paper_paths=[f"papers/{paper['id']}/" for paper in public_papers]
    pages=['','archive/','topics/','question-types/','papers/']+paper_paths+articles
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
                    if path.startswith('papers/') and path != 'papers/':
                        assert page.locator('.paper-question').count() >= 1,(width,path,'paper entries')
                        assert page.locator('.paper-question-number').evaluate_all(
                            "(nodes)=>nodes.every(n=>/^第 \\d+ 题$/.test(n.textContent.trim()))"
                        ),(width,path,'original numbering')
                        for draft in (x for x in posts if x['status']=='draft'):
                            assert page.locator(f'a[href*="{draft["slug"]}"]').count()==0,(width,path,'draft link exposed')
                    if '/posts/' in path:
                        assert page.locator('#overview').count()==1,(width,path,'problem-first overview')
                        assert page.locator('#question').count()==1,(width,path,'original question')
                        assert page.locator('#overview').evaluate("(el)=>el.compareDocumentPosition(document.querySelector('#question')) & Node.DOCUMENT_POSITION_FOLLOWING"),(width,path,'overview order')
                        assert page.locator('#solution .step-note').count()==page.locator('#solution li').count(),(width,path,'step explanations')
                        assert page.locator('figure svg').count()>=1,(width,path,'SVG')
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
                # Actual facet interactions (not only static HTML) plus browser Back.
                if width in (1440,390):
                    page.goto(host,wait_until='domcontentloaded')
                    page.locator('[data-facet-filter="concept"]').select_option('vector')
                    page.locator('[data-category-filter]').select_option('fill-in')
                    page.locator('[data-facet-filter="paper"]').select_option('yangpu-2023-mock')
                    page.wait_for_function(
                        "() => document.querySelector('[data-visible-count]')?.textContent.includes('全库')",
                        timeout=15000
                    )
                    cards=page.locator('[data-post-grid] .index-card')
                    assert cards.count()>=1,(width,'vector+fill-in+yangpu returned no results')
                    assert page.url.find('concept=vector')!=-1 and page.url.find('paper=yangpu-2023-mock')!=-1
                    assert cards.all_text_contents() and all('杨浦' in t for t in cards.all_text_contents())
                    page.go_back(wait_until='domcontentloaded')
                    assert page.locator('[data-facet-filter="paper"]').input_value()=='', (width,'Back did not restore paper filter')
                    assert page.locator('[data-category-filter]').input_value()=='fill-in'
                    page.locator('[data-facet-filter="paper"]').select_option('derivative-classics-collection')
                    assert page.locator('[data-no-results]').is_visible(),(width,'zero-result feedback')
                    page.locator('[data-filter-reset]').click()
                    assert page.locator('[data-facet-filter="concept"]').input_value()==''
                    assert page.locator('[data-category-filter]').input_value()==''
                assert not failures,(width,failures)
                page.close()
        finally:browser.close()
    server.shutdown()
    print(f'Browser smoke OK: {len(pages)} pages ({len(articles)} articles, {len(public_papers)} public papers) x 4 viewport widths + facet navigation')
if __name__=='__main__':run()
