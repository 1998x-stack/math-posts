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
    assert len(posts) >= 82 and len(papers) == 24
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
    assert "已公开 20 / 原卷 21 题" in page
    assert page.index("第 1 题") < page.index("第 2 题") < page.index("第 21 题")
    assert "第 20 题" in page and "暂未公开" in page
    assert article_url(next(p for p in posts if p["slug"] == "jianping-2021-q20")) not in page
    assert "user-uploaded" in page


def test_paper_registry_does_not_fabricate_total_question_count():
    posts, _, papers, taxonomy = fixture_data()
    paper = next(p for p in papers if p["id"] == "yangpu-2023-mock")
    assert paper["total_questions"] is None
    detail = build_paper_detail(paper, posts, taxonomy, "https://example.com/math-posts/", html_page, article_url)
    assert "原卷总题数未登记" in detail
    assert "第 5 题" in detail and "第 6 题" not in detail
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
