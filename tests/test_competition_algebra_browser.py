"""Rendered MathML, SVG and interaction checks in real offline Chromium."""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
DIR=ROOT/"specials"/"algebra-structures"


def test_algebra_12_pages_4_browser_sizes_and_mathml():
    pages=sorted(DIR.glob("[0-9][0-9]-*.html"))
    assert len(pages)==12
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True)
        try:
            for width,height in [(1440,900),(768,1024),(390,844),(360,800)]:
                tab=browser.new_page(viewport={"width":width,"height":height})
                errors=[]
                tab.on("pageerror",lambda err: errors.append(str(err)))
                for article in pages:
                    tab.goto(article.as_uri(),wait_until="load",timeout=40000)
                    tab.wait_for_selector("[data-algebra-lesson] [data-metric]",timeout=15000)
                    before=tab.locator("[data-stage] svg").evaluate("(el)=>el.outerHTML")
                    tab.locator("input[type=range]").evaluate(
                        "(el)=>{el.value='81';el.dispatchEvent(new Event('input',{bubbles:true}))}"
                    )
                    after=tab.locator("[data-stage] svg").evaluate("(el)=>el.outerHTML")
                    assert before!=after,f"Slider inert: {article.name}, {width}px"
                    assert tab.locator("[data-state]").inner_text().startswith("参数 81%")
                    status=tab.evaluate("""() => {
                      const m=[...document.querySelectorAll('math')];
                      const f=[...document.querySelectorAll('figure svg')];
                      const fr=[...document.querySelectorAll('mfrac')];
                      return {
                        overflow:document.documentElement.scrollWidth>innerWidth+1,
                        math:m.length>6 && m.every(el=>el.namespaceURI==='http://www.w3.org/1998/Math/MathML'
                          && el.getBoundingClientRect().width>0 && el.getBoundingClientRect().height>0),
                        figs:f.length===5 && f.every(el=>el.getBoundingClientRect().width>0
                          && el.getBoundingClientRect().height>0),
                        fractions:fr.every(el=>{
                           if(el.children.length!==2)return false;
                           const top=el.children[0].getBoundingClientRect(),bottom=el.children[1].getBoundingClientRect();
                           return top.width>0&&bottom.width>0&&top.top<bottom.top;
                        }),
                        matrices:[...document.querySelectorAll('mtable')].every(el=>
                          el.getBoundingClientRect().width>0 && el.getBoundingClientRect().height>0)
                      }
                    }""")
                    assert not status["overflow"],f"Horizontal overflow {article.name} {width}px"
                    assert status["math"],f"MathML namespace/visibility {article.name} {width}px"
                    assert status["figs"],f"SVG visibility {article.name} {width}px"
                    assert status["fractions"],f"Fraction stack wrong {article.name} {width}px"
                    assert status["matrices"],f"Matrix layout wrong {article.name} {width}px"
                    assert not errors,f"JS errors {article.name} {width}px: {errors}"
                tab.close()
            # Offline/no-script version still retains its educational content and static SVG.
            tab=browser.new_page(viewport={"width":390,"height":844},java_script_enabled=False)
            tab.goto((DIR/"04-lagrange-interpolation.html").as_uri())
            assert tab.locator("math").count()>=7
            assert tab.locator("figure svg").count()==5
            assert tab.locator("h1").is_visible()
            tab.close()
            # Print must retain mathematical objects and not depend on live JS.
            tab=browser.new_page()
            tab.emulate_media(media="print")
            tab.goto((DIR/"10-fibonacci-matrix.html").as_uri())
            assert tab.locator("math mtable").count()>0
            assert tab.locator("figure svg").count()==5
            tab.close()
        finally:
            browser.close()
