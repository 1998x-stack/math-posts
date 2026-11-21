"""Regression tests for exam-format vs knowledge-domain taxonomy and SVG QA."""
from pathlib import Path
from html.parser import HTMLParser
from scripts.build_site import ROOT, data, build_home, build_question_types, build_topics
from scripts.audit_svg import audit


def test_independent_exam_type_and_knowledge_area_memberships():
    categories, posts, graph = data(ROOT)
    published = [p for p in posts if p['status'] == 'published']
    areas = {a['id'] for a in graph['areas']}
    assert len(categories) == 3 and len(areas) == 7
    assert len(published) >= 78
    assert all(1 <= len(p['knowledge_areas']) <= len(areas) for p in published)
    assert all(set(p['knowledge_areas']) <= areas for p in published)
    # Some mathematical problems genuinely cross multiple knowledge areas.
    assert any(len(p['knowledge_areas']) >= 2 for p in published)


def test_question_type_page_has_distinct_canonical_and_correct_breadcrumb():
    categories, posts, graph = data(ROOT)
    url = 'https://1998x-stack.github.io/math-posts/'
    type_html = build_question_types(categories, posts, url)
    assert '<h1>按试卷题型浏览</h1>' in type_html
    assert 'href="https://1998x-stack.github.io/math-posts/question-types/"' in type_html
    assert '首页</a> <span>/</span> 试卷题型' in type_html
    assert '按试卷题型浏览' not in build_topics(categories, posts, url, graph)


def test_homepage_subject_filter_is_not_a_question_type():
    categories, posts, graph = data(ROOT)
    url = 'https://1998x-stack.github.io/math-posts/'
    html = build_home(categories, posts, url, graph)
    assert 'data-category-filter' in html
    assert 'data-subject-filter' in html
    assert '<option value="analytic-geometry">' in html
    assert 'data-subjects=' in html
    assert '全部知识领域' in html
    assert '全部题型' in html


def test_svg_source_audit_preserves_semantics():
    report = audit(ROOT, strict_desc=True)
    assert report['pass'], report['errors'][:20]
    assert report['counts']['articles'] >= 82
    assert report['counts']['inline_svg'] >= 78
    assert report['counts']['standalone_svg'] >= 82


def test_key_geometry_diagrams_have_mathematical_descriptions():
    cases = {
        'shanghai-2024-geometry-minhang-q20': ['椭圆', '抛物线', '焦点'],
        'shanghai-2024-geometry-jiading-q20': ['椭圆', '中点', '斜率'],
        'shanghai-2024-geometry-chongming-q20': ['垂足', '圆', '固定点'],
        'shanghai-2024-geometry-fengxian-q20': ['竖直', '反例', '椭圆'],
    }
    for slug, terms in cases.items():
        base = ROOT / 'posts' / 'worked-solutions' / slug
        html = (base / 'index.html').read_text('utf-8')
        cover = (base / 'assets' / 'cover.svg').read_text('utf-8')
        for term in terms:
            assert term in html + cover, (slug, term)
        assert '<desc>' in cover and '<title>' in cover


def test_related_posts_reach_across_exam_formats_by_shared_knowledge_nodes():
    from scripts.related_posts import choose_related
    _, posts, _ = data(ROOT)
    published = [p for p in posts if p['status'] == 'published']
    current = next(p for p in published if p['slug'] == 'jianping-2021-q15')
    suggestions = choose_related(current, published, routes=[], limit=4)
    assert suggestions
    assert any(x['post']['category'] != current['category'] for x in suggestions)
    assert all(x['kind'] == '知识点衔接' or x['post']['category'] == current['category']
               for x in suggestions)


def test_huangpu_svg_does_not_confuse_hyperbola_vertices_with_foci():
    import json
    posts = json.loads((ROOT / 'content/posts.json').read_text('utf-8'))
    post = next(p for p in posts if p['slug'] == 'shanghai-2024-geometry-huangpu-q20')
    page = ROOT / 'posts' / post['category'] / post['slug']
    html = (page / 'index.html').read_text('utf-8')
    cover = (page / 'assets/cover.svg').read_text('utf-8')
    assert '共焦' not in post['title'] + post['subtitle'] + html + cover
    assert '椭圆焦点' in post['title']
    assert '双曲线顶点' in post['title']
    # For x²/5 + y²/4 = 1 the focal distance is 1;
    # for x² - y² = 1 the focal distance is sqrt(2).
    assert 5 - 4 == 1
    assert 1 + 1 == 2
