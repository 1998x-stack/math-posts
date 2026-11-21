from pathlib import Path
from scripts.audit_svg import audit

ROOT=Path(__file__).resolve().parents[1]


def test_all_registered_article_svgs_have_valid_structure_and_references():
    report=audit(ROOT,strict_desc=False)
    assert report['pass'],report['errors'][:30]
    assert report['counts']['articles']>=132
    assert report['counts']['standalone_svg']>=132


def test_high_risk_2024_geometry_diagrams_have_specific_descriptions():
    cases={
        'shanghai-2024-geometry-minhang-q20':['椭圆','抛物线','焦点'],
        'shanghai-2024-geometry-jiading-q20':['椭圆','中点','斜率'],
        'shanghai-2024-geometry-chongming-q20':['垂足','圆','固定点'],
        'shanghai-2024-geometry-fengxian-q20':['竖直','反例','椭圆'],
        'shanghai-2024-geometry-huangpu-q20':['椭圆焦点','双曲线顶点'],
    }
    for slug,terms in cases.items():
        page=ROOT/'posts'/'worked-solutions'/slug
        html=(page/'index.html').read_text('utf-8')
        cover=(page/'assets/cover.svg').read_text('utf-8')
        for term in terms:
            assert term in html+cover,(slug,term)
        assert '<title' in cover and '<desc' in cover,slug
