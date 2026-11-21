"""Validated, source-faithful multi-facet taxonomy and paper browsing.

One question has one canonical post URL. Paper pages are projections over the
manifest, not duplicated question content. Drafts never become public links.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from html import escape as H
import json
import re
from pathlib import Path

SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
KINDS = {"exam", "exam-excerpt", "worksheet", "problem-set"}
AXES = ("concept", "method", "visual")
TYPE_LABELS = {
    "fill-in": "填空题", "multiple-choice": "选择题",
    "worked-solutions": "解答题",
}


def load_atlas(root: Path, posts: list, knowledge_map: dict):
    """Fail closed on taxonomy/exam identity mistakes and draft contamination."""
    papers = json.loads((root / "content/papers.json").read_text(encoding="utf-8"))
    taxonomy = json.loads((root / "content/taxonomy.json").read_text(encoding="utf-8"))
    assert isinstance(papers, list) and papers, "Paper registry must be non-empty"
    assert taxonomy.get("version") == 1
    dims = taxonomy.get("dimensions", [])
    assert [d.get("id") for d in dims] == list(AXES), "Unexpected facet dimensions"
    tags = {}
    for dim in dims:
        entries = dim.get("tags", [])
        ids = [t["id"] for t in entries]
        assert ids and len(ids) == len(set(ids)), "Duplicate taxonomy tag"
        assert all(SLUG.fullmatch(t["id"]) and t.get("title") for t in entries)
        tags[dim["id"]] = set(ids)
        for t in entries:
            assert isinstance(t.get("aliases", []), list), t
    paper_ids = set()
    for paper in papers:
        pid = paper.get("id", "")
        assert SLUG.fullmatch(pid) and pid not in paper_ids, "Invalid/duplicate paper ID"
        paper_ids.add(pid)
        assert paper.get("kind") in KINDS, pid
        assert paper.get("source_access") == "user-uploaded", pid
        assert paper.get("source_id") and paper.get("source_title"), pid
        assert paper.get("title") and paper.get("exam_type"), pid
        assert paper.get("school") is None or isinstance(paper["school"], str), pid
        assert paper.get("region") is None or isinstance(paper["region"], str), pid
        assert paper.get("year") is None or (isinstance(paper["year"], int) and 1900 <= paper["year"] <= 2100), pid
        total = paper.get("total_questions")
        assert total is None or (isinstance(total, int) and total > 0), pid
    mapped = {
        slug for area in knowledge_map.get("areas", [])
        for node in area.get("subtopics", [])
        for slug in node.get("posts", [])
    }
    seen = set()
    for post in posts:
        slug = post["slug"]
        assert post.get("paper_id") in paper_ids, f"Missing paper identity: {slug}"
        number = post.get("question_number")
        assert isinstance(number, int) and number >= 1, f"Invalid original question number: {slug}"
        key = (post["paper_id"], number)
        assert key not in seen, f"Duplicate original question number in paper: {key}"
        seen.add(key)
        total = next(p["total_questions"] for p in papers if p["id"] == post["paper_id"])
        assert total is None or number <= total, f"Question beyond known paper total: {slug}"
        facets = post.get("facets")
        assert isinstance(facets, dict) and set(facets) == set(AXES), f"Invalid facets: {slug}"
        for axis in AXES:
            values = facets[axis]
            assert isinstance(values, list) and len(values) == len(set(values)), f"Duplicate {axis}: {slug}"
            assert all(isinstance(v, str) and v in tags[axis] for v in values), f"Unknown {axis}: {slug}"
        source=root / "posts" / post["category"] / slug / "evidence.json"
        assert source.is_file(), f"Missing per-question provenance: {slug}"
        provenance=json.loads(source.read_text(encoding="utf-8"))
        assert provenance.get("source", {}).get("question")==number, f"Evidence question mismatch: {slug}"
        assert provenance.get("source", {}).get("pages")==post.get("source_pages"), f"Evidence pages mismatch: {slug}"
        assert "official" in provenance.get("answer", {}), f"Missing official-answer provenance field: {slug}"
        if post["status"] == "published":
            assert slug in mapped, f"No knowledge-map entry: {slug}"
            assert facets["concept"], f"Published post without concept tag: {slug}"
            assert provenance.get("qa", {}).get("source_checked") is not False, f"Unverified source published: {slug}"
    return papers, taxonomy


def _published_in_paper(paper: dict, posts: list) -> list:
    return sorted(
        (p for p in posts if p["paper_id"] == paper["id"] and p["status"] == "published"),
        key=lambda p: (p["question_number"], p["slug"])
    )


def _coverage(paper: dict, n: int) -> str:
    total = paper["total_questions"]
    return f"已公开 {n} / 原卷 {total} 题" if total is not None else f"已公开 {n} 题 · 原卷总题数未登记"


def build_papers_index(papers, posts, base, html_page):
    """Paper-first discovery; never link to unpublished articles."""
    entries = []
    ordered = sorted(papers, key=lambda p: (p["year"] or 0, p["exam_type"], p["title"]), reverse=True)
    for paper in ordered:
        published = _published_in_paper(paper, posts)
        if not published:
            continue
        location = paper.get("school") or paper.get("region") or "专题资料"
        entries.append(
            f'<article class="paper-card"><div class="paper-card-top"><span>{H(str(paper["year"] or "年份未注明"))}</span>'
            f'<span>{H(paper["exam_type"])}</span></div>'
            f'<h2><a href="./{H(paper["id"])}/">{H(paper["title"])}</a></h2>'
            f'<p>{H(location)} · {H(_coverage(paper, len(published)))}</p>'
            f'<a href="./{H(paper["id"])}/">按原卷题号浏览 →</a></article>'
        )
    body = (
        '<div class="container paper-browser"><nav class="breadcrumb" aria-label="面包屑"><a href="../">首页</a> / 按试卷浏览</nav>'
        '<div class="eyebrow muted">PAPER ATLAS / SOURCE-VERIFIED</div>'
        '<h1>按试卷浏览</h1><p class="category-description">按学校、地区、年份与试卷来源找到题目。'
        '汇编中的地区单题标为摘录；本站只提供已核验并正式公开的题解。</p>'
        f'<div class="paper-browser-grid">{"".join(entries)}</div></div>'
    )
    return html_page(title="按试卷浏览 · math-posts", description="数学试卷、学校、地区、年份与原题顺序浏览。",
                     canonical=base.rstrip("/") + "/papers/", body=body, depth=1, active="papers")


def build_paper_detail(paper, posts, taxonomy, base, html_page, article_url):
    published = _published_in_paper(paper, posts)
    all_entries = {p["question_number"]: p for p in posts if p["paper_id"] == paper["id"]}
    count = len(published)
    total = paper.get("total_questions")
    numbers = range(1, total + 1) if total else sorted(all_entries)
    concept_names = {t["id"]: t["title"] for d in taxonomy["dimensions"]
                     if d["id"] == "concept" for t in d["tags"]}
    lines = []
    for number in numbers:
        post = all_entries.get(number)
        if post and post["status"] == "published":
            kinds = TYPE_LABELS.get(post["category"], "题目")
            tags = " · ".join(concept_names[t] for t in post["facets"]["concept"][:3])
            lines.append(
                f'<li class="paper-question"><span class="paper-question-number">第 {number} 题</span>'
                f'<div><span class="paper-question-meta">{H(kinds)} · {H(tags)}</span>'
                f'<h2><a href="../../{H(article_url(post))}">{H(post["title"])}</a></h2>'
                f'<p>{H(post["subtitle"])}</p></div><a href="../../{H(article_url(post))}" aria-label="阅读第 {number} 题">阅读题解 →</a></li>'
            )
        else:
            status = "暂未公开" if post else "尚未收录"
            lines.append(
                f'<li class="paper-question paper-question--unavailable">'
                f'<span class="paper-question-number">第 {number} 题</span>'
                f'<div><span class="paper-question-meta">{status}</span></div></li>'
            )
    kind_note = ("该页面仅代表汇编里的地区第 20 题摘录，不是完整试卷。"
                 if paper["kind"] == "exam-excerpt" else
                 "原卷题数尚未登记，目录仅列已登记题号。"
                 if total is None else "已知原卷总题数；尚未收录或未公开的题目不提供链接。")
    body = (
        '<div class="container paper-browser paper-detail">'
        '<nav class="breadcrumb" aria-label="面包屑"><a href="../../">首页</a> / '
        f'<a href="../">试卷</a> / {H(paper["title"])}</nav>'
        '<div class="eyebrow muted">ORIGINAL ORDER / VERIFIED QUESTIONS</div>'
        f'<h1>{H(paper["title"])}</h1><p class="category-description">{H(_coverage(paper, count))}</p>'
        f'<p class="paper-source-note">来源：{H(paper["source_title"])} · '
        f'{H(paper["source_access"])}。{H(kind_note)}'
        ' 用户上传的 PDF 不提供虚构的公网下载链接。</p>'
        f'<ol class="paper-question-list" aria-label="按原卷题号排列的题目">{"".join(lines)}</ol></div>'
    )
    return html_page(title=paper["title"] + " · math-posts", description=paper["title"] + "的已公开题解与原卷题号。",
                     canonical=base.rstrip("/") + "/papers/" + paper["id"] + "/",
                     body=body, depth=2, active="papers")
