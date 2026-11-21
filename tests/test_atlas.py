"""Regression tests for paper provenance, typed facet tags and public routing."""
import copy
import json
import sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from atlas import load_atlas, build_papers_index, build_paper_detail
from build_site import data, article_url, html_page


def fixture_data():
    cats, posts, map_data = data(ROOT)
    papers, taxonomy = load_atlas(ROOT, posts, map_data)
    return posts, map_data, papers, taxonomy


def test_all_questions_have_stable_unique_paper_identity_and_tags():
    posts, knowledge, papers, taxonomy = fixture_data()
    assert len(posts) >= 132 and len(papers) >= 25
    assert sum(p['status'] == 'published' for p in posts) >= 126
    assert len({(p["paper_id"], p["question_number"]) for p in posts}) == len(posts)
    assert all(p["facets"]["concept"] for p in posts if p["status"] == "published")
    assert set(d["id"] for d in taxonomy["dimensions"]) == {"concept", "method", "visual"}
    assert "vector" in {tag for p in posts for tag in p["facets"]["concept"]}


def test_compilation_is_sixteen_distinct_paper_excerpts_with_same_source():
    posts, _, papers, _ = fixture_data()
    extracted = [p for p in posts if p["slug"].startswith("shanghai-2024-geometry-")]
    assert len(extracted) == 16
    assert len({p["paper_id"] for p in extracted}) == 16
    assert {p["question_number"] for p in extracted} == {20}
    registry = {p["id"]: p for p in papers}
    assert {registry[p["paper_id"]]["source_id"] for p in extracted} == {"shanghai-2024-geometry-compilation"}
    assert all(registry[p["paper_id"]]["kind"] == "exam-excerpt" for p in extracted)


def test_paper_page_orders_questions_and_never_links_to_draft():
    posts, _, papers, taxonomy = fixture_data()
    paper = next(p for p in papers if p["id"] == "jianping-2021-mock-03")
    page = build_paper_detail(paper, posts, taxonomy, "https://example.com/math-posts/", html_page, article_url)
    published = [p for p in posts if p["paper_id"] == paper["id"] and p["status"] == "published"]
    assert f"已公开 {len(published)} / 原卷 21 题" in page
    assert page.index("第 1 题") < page.index("第 2 题") < page.index("第 21 题")
    q20 = next(p for p in posts if p["slug"] == "jianping-2021-q20")
    if q20["status"] == "draft":
        assert "第 20 题" in page and "暂未公开" in page
        assert article_url(q20) not in page
    else:
        assert article_url(q20) in page
    assert "user-uploaded" in page


def test_paper_registry_does_not_fabricate_total_question_count():
    posts, _, papers, taxonomy = fixture_data()
    paper = next(p for p in papers if p["id"] == "yangpu-2023-mock")
    assert paper["total_questions"] is None
    detail = build_paper_detail(paper, posts, taxonomy, "https://example.com/math-posts/", html_page, article_url)
    assert "原卷总题数未登记" in detail
    assert "第 10 题" in detail and "尚未收录" not in detail
    listing = build_papers_index(papers, posts, "https://example.com/math-posts/", html_page)
    assert "/papers/" in listing
    assert "2023 届上海市杨浦区高三一模" in listing


def test_reject_unknown_typed_tag_and_duplicate_original_number():
    posts, km, papers, _ = fixture_data()
    fake = copy.deepcopy(posts)
    fake[0]["facets"]["concept"].append("invented-tag")
    with pytest.raises(AssertionError, match="Unknown concept"):
        load_atlas(ROOT, fake, km)
    fake = copy.deepcopy(posts)
    fake[1]["question_number"] = fake[0]["question_number"]
    with pytest.raises(AssertionError, match="Duplicate original"):
        load_atlas(ROOT, fake, km)


def test_vector_analytic_geometry_and_fill_in_can_be_composed():
    posts, *_ = fixture_data()
    filtered = [p for p in posts if p["status"] == "published"
                and p["category"] == "fill-in"
                and "vector" in p["facets"]["concept"]]
    assert filtered
    assert all(p["paper_id"] and p["question_number"] >= 1 for p in filtered)


def test_skill_stepper_example_is_accessible_without_javascript():
    skill = ROOT / "skills/math-visual-posts"
    demo = (skill / "assets/templates/stepwise-vector-example.html").read_text("utf-8")
    script = (skill / "assets/js/stepwise-solution.js").read_text("utf-8")
    svg = (skill / "assets/examples/vector-length.svg").read_text("utf-8")
    assert demo.count("data-solution-step>") == 3
    assert 'data-stepper-controls hidden' in demo
    assert 'aria-live="polite"' in demo
    assert 'display="block"' in demo and "MathML" in demo
    assert "step.hidden = !showAll" in script
    assert "controls.hidden = false" in script
    assert "<title" in svg and "<desc" in svg and 'viewBox="0 0 480 360"' in svg
    assert "A (1,2)" in svg and "B (4,6)" in svg and "Δx=3" in svg and "Δy=4" in svg


def test_2023_jiading_second_batch_appears_under_one_school_paper():
    posts, _, papers, taxonomy = fixture_data()
    record = next(p for p in papers if p['id'] == 'jiading-2023-mock')
    items = sorted([p for p in posts if p['paper_id'] == record['id']],
                   key=lambda p: p['question_number'])
    question_numbers = [p['question_number'] for p in items]
    assert set(range(11,21)).issubset(question_numbers)
    assert question_numbers == sorted(question_numbers)
    assert record['total_questions'] is None
    detail = build_paper_detail(record, posts, taxonomy, 'https://example.com/math-posts/', html_page, article_url)
    assert detail.index('第 11 题') < detail.index('第 20 题')
    assert '原卷总题数未登记' in detail

def test_all_132_questions_keep_original_titles_and_source_pages():
    posts, _, _, _ = fixture_data()
    assert len({p['slug'] for p in posts}) == len(posts)
    assert all(p.get('title') and p.get('source_pages') and p.get('tags') for p in posts)
    assert all(p.get('question_number') and p.get('paper_id') for p in posts)
    for p in posts:
        assert p['facets']['concept'], p['slug']


def test_no_public_route_for_draft_only_exam_excerpt():
    posts, _, papers, _ = fixture_data()
    draft_only = next(p for p in papers if p["id"] == "shanghai-2024-er-mo-fengxian")
    assert not any(p["paper_id"] == draft_only["id"] and p["status"] == "published" for p in posts)
    from build_site import ROOT
    # The build produces public_papers and excludes this record from route generation.
    source = (ROOT / "scripts/build_site.py").read_text("utf-8")
    assert "public_papers=" in source and "for paper in public_papers" in source


def test_huangpu_focus_vertex_language_is_mathematically_correct():
    posts, _, _, _ = fixture_data()
    p = next(p for p in posts if p["slug"] == "shanghai-2024-geometry-huangpu-q20")
    assert "共焦" not in p["title"] and "双曲线顶点" in p["title"]
    article = ROOT / "posts" / p["category"] / p["slug"]
    html = (article / "index.html").read_text("utf-8")
    svg = (article / "assets/cover.svg").read_text("utf-8")
    assert "共焦" not in html and "共焦" not in svg
    assert "椭圆焦点" in svg and "双曲线顶点" in svg


def test_never_publish_explicitly_unverified_source_glyph():
    posts, _, _, _ = fixture_data()
    item=next(p for p in posts if p['slug']=='songjiang-2023-mock-q16')
    assert item['status']=='draft'
    evidence=json.loads((ROOT/'posts'/item['category']/item['slug']/'evidence.json').read_text('utf-8'))
    assert evidence['qa']['source_checked'] is False
    assert '缺失' in evidence['editorial_note']


def test_verified_number_shape_visualization_facets_are_grounded_in_svg():
    posts, _, _, _ = fixture_data()
    by_slug={p['slug']:p for p in posts}
    for slug,method,visual,title in (
        ('jianping-2021-q02','coordinate-method','coordinate-plane','参数方程消元为直线'),
        ('jianping-2021-q03','number-shape','feasible-region','半平面约束的最近点'),
        ('jianping-2021-q08','number-shape','coordinate-plane','奇函数与平行四边形'),
    ):
        p=by_slug[slug]
        assert method in p['facets']['method'] and visual in p['facets']['visual']
        svg=(ROOT/'posts'/p['category']/p['slug']/p['cover']['src']).read_text('utf-8')
        assert title in svg
    p=by_slug['jiading-2023-q19']
    assert 'optimization' in p['facets']['concept']
    assert 'probability-statistics' not in p['facets']['concept']


def test_skill_gates_follow_actual_execution_order():
    skill=(ROOT/'skills/math-visual-posts/SKILL.md').read_text("utf-8")
    gates=["Gate 0", "Gate 1", "Gate 1.5", "Gate 2", "Gate 2.5",
           "Gate 3", "Gate 4", "Gate 5", "Gate 6", "Gate 7", "Gate 7.5", "Gate 8"]
    positions=[skill.index("## "+g+"：") for g in gates]
    assert positions==sorted(positions)
    for name in ("student-solution-design","visualization-by-problem-type","taxonomy-and-tags","exam-provenance-schema"):
        assert "references/"+name+".md" in skill


def test_source_document_registry_matches_all_paper_references():
    posts, _, papers, _ = fixture_data()
    sources=json.loads((ROOT/'content/source_documents.json').read_text('utf-8'))['documents']
    by_id={src['id']:src for src in sources}
    assert len(sources)>=10
    assert len(by_id)==len(sources)
    assert all(p['source_id'] in by_id and p['source_title']==by_id[p['source_id']]['title'] for p in papers)
    assert all(src['access']=='user-uploaded' and src['public_url'] is None for src in sources)
    excerpt=[p for p in papers if p['kind']=='exam-excerpt'
             and p['source_id']=='shanghai-2024-geometry-compilation']
    assert len(excerpt)==16 and len({p['source_id'] for p in excerpt})==1
