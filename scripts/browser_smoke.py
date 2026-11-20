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
    pages=['','archive/','topics/']+articles
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
                    if '/posts/' in path:
                        assert page.locator('#overview').count()==1,(width,path,'problem-first overview')
                        assert page.locator('#question').count()==1,(width,path,'original question')
                        assert page.locator('#overview').evaluate("(el)=>el.compareDocumentPosition(document.querySelector('#question')) & Node.DOCUMENT_POSITION_FOLLOWING"),(width,path,'overview order')
                        assert page.locator('#solution .step-note').count()==page.locator('#solution li').count(),(width,path,'step explanations')
                        assert page.locator('figure svg').count()>=1,(width,path,'SVG')
                        assert page.locator('math').count()>=1,(width,path,'MathML')
                        assert page.locator('math[aria-label],math[aria-labelledby]').count()==page.locator('math').count(),(width,path,'MathML accessible labels')
                        if any(f'q{n:02d}' in path for n in (4,13,17)):
                            scene=page.locator('[data-three-scene]')
                            scene.wait_for(timeout=5000)
                            page.locator('[data-three-scene][data-ready="false"]').wait_for(timeout=10000)
                            assert scene.locator('.static-scene').is_visible(),(width,path,'visible offline SVG fallback')
                            assert not scene.locator('canvas').is_visible(),(width,path,'canvas hidden when CDN unavailable')
                        if 'q17' in path:
                            assert page.locator('.scene-controls input').count()==0,(width,path,'no inert tetrahedron sliders')
                        if page.locator('body[data-visual-first="true"]').count():
                            assert page.locator('#overview figure.problem-visual').count()>=1,(width,path,'problem visual')
                            assert page.locator('#solution figure.step-visual').count()>=2,(width,path,'step visuals')
                            assert page.locator('#answer figure.conclusion-visual').count()>=1,(width,path,'conclusion visual')
                            assert page.locator('math.math-inline').count()>=8,(width,path,'inline MathML coverage')
                            assert page.locator('figure.visual-figure svg title').count()==page.locator('figure.visual-figure').count(),(width,path,'SVG titles')
                            assert page.locator('figure.visual-figure svg desc').count()==page.locator('figure.visual-figure').count(),(width,path,'SVG descriptions')
                            math_visible=page.locator('math.math-inline').evaluate_all("(els)=>els.every(el=>{const r=el.getBoundingClientRect();return r.width>0&&r.height>0})")
                            assert math_visible,(width,path,'MathML must render with visible geometry')
                            residual=page.evaluate("""() => {
                                const clone=document.body.cloneNode(true);
                                clone.querySelectorAll('math,svg,script,style,code,pre,noscript').forEach(el=>el.remove());
                                const text=clone.innerText||'';
                                const patterns=[
                                  /(?<![\\w])(?:[A-Za-z][A-Za-z0-9₀-₉]*)(?:\\([^()\\n]{1,24}\\))?\\s*(?:=|≤|≥|<|>)\\s*[-−]?\\s*(?:\\d+(?:\\.\\d+)?|[A-Za-z(])/u,
                                  /(?<![\\w])[A-Z]\\s*\\([^()\\n]*,[^()\\n]*\\)/u,
                                  /(?<![\\w])[A-Za-z][A-Za-z0-9₀-₉]*[²³⁴]/u,
                                  /(?<![\\w])\\d+\\s*\\/\\s*\\d+(?![\\w])/u,
                                  /(?<![\\w])[A-Z]{1,3}\\s*(?:∥|⊥)\\s*(?:[A-Z]{1,3}|平面)/u,
                                  /(?<![\\w])[A-Za-z][A-Za-z0-9₀-₉]*\\s*(?:·|×)\\s*[A-Za-z]/u
                                ];
                                return patterns.map(re=>text.match(re)?.[0]).filter(Boolean);
                            }""")
                            assert not residual,(width,path,'unrendered formula candidates',residual)
                assert not failures,(width,failures)
                page.close()
        finally:browser.close()
    server.shutdown()
    print(f'Browser smoke OK: {len(pages)} pages ({len(articles)} articles) x 4 viewport widths')
if __name__=='__main__':run()
