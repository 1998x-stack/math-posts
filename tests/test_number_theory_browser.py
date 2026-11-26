"""Real Chromium tests for all 12 offline number-theory articles at 4 widths."""
from pathlib import Path
from playwright.sync_api import sync_playwright

SERIES=Path(__file__).resolve().parents[1]/'specials'/'number-theory'


def test_all_number_theory_pages_render_and_interact():
    articles=sorted(SERIES.glob('[0-9][0-9]-*.html'))
    assert len(articles)==12
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True, args=['--disable-dev-shm-usage'])
        try:
            for width,height in ((1440,900),(768,1024),(390,844),(360,800)):
                tab=browser.new_page(viewport={'width':width,'height':height},reduced_motion='reduce')
                errors=[]
                tab.on('pageerror',lambda e:errors.append(str(e)))
                for article in articles:
                    errors.clear()
                    tab.goto(article.as_uri(),wait_until='load',timeout=30000)
                    tab.locator('math').first.wait_for(timeout=10000)
                    assert tab.locator('math').count()==6,(article,width)
                    assert tab.locator('figure svg').count()==4,(article,width)
                    before=tab.locator('[data-visual] svg').evaluate('(e)=>e.outerHTML')
                    slider=tab.locator('[data-nt] input[type=range]')
                    original=slider.input_value()
                    minimum=slider.get_attribute('min')
                    maximum=slider.get_attribute('max')
                    target=minimum if minimum!=original else maximum
                    slider.evaluate('(node,v)=>{node.value=v;node.dispatchEvent(new Event("input",{bubbles:true}))}',target)
                    after=tab.locator('[data-visual] svg').evaluate('(e)=>e.outerHTML')
                    assert before!=after,(article,width,'SVG did not change')
                    assert tab.locator('[data-value]').inner_text()==target
                    result=tab.evaluate('''() => ({
                      overflow: document.documentElement.scrollWidth>innerWidth+1,
                      math: [...document.querySelectorAll('math')].every(m=>
                        m.namespaceURI==='http://www.w3.org/1998/Math/MathML' &&
                        m.getBoundingClientRect().width>0 && m.getBoundingClientRect().height>0),
                      frac: [...document.querySelectorAll('math mfrac')].every(f=>{
                        const [num,den]=f.children;
                        return num && den && num.getBoundingClientRect().bottom <= den.getBoundingClientRect().top+2;
                      }),
                      svg: [...document.querySelectorAll('figure svg')].every(s=>
                        s.getBoundingClientRect().width>0 && s.getBoundingClientRect().height>0),
                      visible: [...document.querySelectorAll('math')].every(m=>m.getClientRects().length>0)
                    })''')
                    assert not result['overflow'],(article,width,'document overflow')
                    assert result['math'] and result['visible'],(article,width,'MathML not rendered')
                    assert result['frac'],(article,width,'MathML fraction not stacked')
                    assert result['svg'],(article,width,'SVG size zero')
                    assert not errors,(article,width,errors)
                tab.close()
        finally:
            browser.close()
