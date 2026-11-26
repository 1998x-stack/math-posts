"""Actual Chromium smoke tests for the 12-lesson geometry special.

Each page must render from local files (no CDN) at desktop/tablet/mobile widths,
change a mathematical SVG when its control changes, and preserve native MathML.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
SERIES=ROOT/"specials"/"geometry-transformations"


def test_all_geometry_lessons_in_actual_browser():
    pages=sorted(SERIES.glob("[0-9][0-9]-*.html"))
    assert len(pages)==12
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        try:
            for width,height in [(1440,900),(768,1024),(390,844),(360,800)]:
                tab=browser.new_page(viewport={"width":width,"height":height})
                errors=[]
                tab.on("pageerror",lambda ex: errors.append(str(ex)))
                for article in pages:
                    tab.goto(article.as_uri(),wait_until="load",timeout=25000)
                    tab.wait_for_selector("[data-geom-lesson] [data-metric]",timeout=10000)
                    before=tab.locator("[data-stage] svg").evaluate("(el)=>el.outerHTML")
                    tab.locator("input[type=range]").evaluate(
                        "(el)=>{el.value='79';el.dispatchEvent(new Event('input',{bubbles:true}))}"
                    )
                    after=tab.locator("[data-stage] svg").evaluate("(el)=>el.outerHTML")
                    assert before!=after, f"SVG not updated: {article.name} at {width}px"
                    assert tab.locator("[data-status]").inner_text().startswith("参数 79%")
                    result=tab.evaluate("""() => ({
                      overflow:document.documentElement.scrollWidth>innerWidth+1,
                      math:[...document.querySelectorAll('math')].every(
                        m=>m.namespaceURI==='http://www.w3.org/1998/Math/MathML'&&
                        m.getBoundingClientRect().width>0&&m.getBoundingClientRect().height>0
                      ),
                      figs:[...document.querySelectorAll('figure svg')].every(
                        s=>s.getBoundingClientRect().width>0&&s.getBoundingClientRect().height>0
                      )
                    })""")
                    assert not result["overflow"],f"horizontal overflow: {article.name} {width}px"
                    assert result["math"],f"MathML render/namespace: {article.name} {width}px"
                    assert result["figs"],f"SVG render failure: {article.name} {width}px"
                    assert not errors,f"JavaScript errors: {article.name} {width}px {errors}"
                tab.close()
        finally:
            browser.close()
