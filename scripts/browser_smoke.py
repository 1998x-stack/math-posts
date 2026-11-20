#!/usr/bin/env python3
"""Practical browser smoke: responsive Post, SVG, static Three.js fallback, JS errors."""
from __future__ import annotations
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
from pathlib import Path
import threading
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'_site'
def run():
    assert (SITE/'index.html').exists(),'build site before browser smoke'
    handler=partial(SimpleHTTPRequestHandler,directory=str(SITE))
    server=ThreadingHTTPServer(('127.0.0.1',0),handler)
    worker=threading.Thread(target=server.serve_forever,daemon=True);worker.start()
    host=f'http://127.0.0.1:{server.server_address[1]}/'
    pages=['','archive/','topics/','posts/fill-in/jianping-2021-q04/','posts/multiple-choice/jianping-2021-q13/','posts/worked-solutions/jianping-2021-q17/','posts/worked-solutions/jianping-2021-q21/']
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True,args=['--disable-dev-shm-usage'])
        try:
            for width in (1440,768,390,360):
                page=browser.new_page(viewport={'width':width,'height':850},reduced_motion='reduce')
                failures=[]
                page.on('pageerror',lambda e:failures.append(str(e)))
                for path in pages:
                    page.goto(host+path,wait_until='domcontentloaded',timeout=30000)
                    page.locator('h1').first.wait_for(timeout=12000)
                    assert page.locator('h1').count()==1,(width,path,'H1')
                    assert page.locator('main').count()==1,(width,path,'main')
                    assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth+1'),(width,path,'overflow')
                    if '/posts/' in path:
                        assert page.locator('figure svg').count()>=1,(width,path,'SVG')
                        assert page.locator('math').count()>=1,(width,path,'MathML')
                        if 'q04' in path or 'q13' in path or 'q17' in path:
                            assert page.locator('.static-scene svg').count()>=1,(width,path,'3D static fallback')
                assert not failures,(width,failures)
                page.close()
        finally:browser.close()
    server.shutdown()
    print('Browser smoke OK: 7 pages x 4 viewport widths')
if __name__=='__main__':run()
