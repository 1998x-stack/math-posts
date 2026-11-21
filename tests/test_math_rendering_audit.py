"""Regression tests for the all-article mathematical rendering audit."""
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from audit_math_rendering import audit_post, create_report, formula_candidates


def _fixture(tmp_path: Path, html: str, *, concepts=None):
    article = tmp_path / "posts" / "worked-solutions" / "demo"
    article.mkdir(parents=True)
    (article / "index.html").write_text(html, encoding="utf-8")
    (article / "evidence.json").write_text(json.dumps({
        "source": {"question": 20, "pages": [1]},
        "transcription": {"status": "checked-against-rendered-pages"},
    }), encoding="utf-8")
    post = {
        "slug": "demo",
        "category": "worked-solutions",
        "paper_id": "demo-paper",
        "question_number": 20,
        "status": "published",
        "facets": {"concept": concepts or [], "method": [], "visual": []},
    }
    return article, post


def test_detects_unrendered_formula_in_original_question_and_each_step(tmp_path):
    html = """
    <section id="question"><p>已知椭圆 x²/4+y²/3=1，点 P=(1,2)。</p></section>
    <section id="solution"><ol>
      <li>代入 x²/4+y²/3=1，得到 y²=...</li>
      <li>因为 <math aria-label="x 等于一"><mi>x</mi><mo>=</mo><mn>1</mn></math>，所以继续。</li>
    </ol></section>
    <section id="visual"><figure><svg><title>椭圆</title><desc>坐标图</desc></svg><figcaption>椭圆示意</figcaption></figure></section>
    """
    _, post = _fixture(tmp_path, html, concepts=["analytic-geometry", "conics"])
    row = audit_post(tmp_path, post)
    assert row["formula_rendering"]["original_question"]["formula_candidates"]
    assert row["formula_rendering"]["solution_steps"][0]["needs_formula_review"]
    assert not row["formula_rendering"]["solution_steps"][1]["needs_formula_review"]
    assert row["visualization"]["inline_svg_count"] == 1
    assert row["priority"] == "P0"


def test_ignores_mathml_svg_code_and_script_when_finding_candidates():
    html = """
    <section id="question">
      <p>公式 <math aria-label="x 平方等于一"><msup><mi>x</mi><mn>2</mn></msup><mo>=</mo><mn>1</mn></math> 已排版。</p>
      <pre>x²=1</pre><code>y=2x</code>
      <svg><text>x²+y²=1</text></svg><script>const x = 2;</script>
    </section>
    """
    soup = __import__("bs4").BeautifulSoup(html, "html.parser")
    candidates = formula_candidates(soup.select_one("#question"))
    assert candidates == []


def test_flags_analytic_geometry_without_an_inline_diagram(tmp_path):
    html = """
    <section id="question"><p>椭圆 x²/4+y²/3=1。</p></section>
    <section id="solution"><ol><li>由方程可得。</li></ol></section>
    <section id="visual"><p>图形待补。</p></section>
    """
    _, post = _fixture(tmp_path, html, concepts=["analytic-geometry", "conics"])
    row = audit_post(tmp_path, post)
    assert row["visualization"]["missing_inline_svg"] is True
    assert "analytic-geometry-missing-inline-svg" in row["issue_codes"]


def test_mathml_integrity_checks_accessibility_and_fraction_arity(tmp_path):
    html = """
    <section id="question"><math><mfrac><mi>a</mi></mfrac></math></section>
    <section id="solution"><ol><li>无公式步骤。</li></ol></section>
    """
    _, post = _fixture(tmp_path, html)
    row = audit_post(tmp_path, post)
    assert row["mathml_integrity"]["missing_accessible_name"] == 1
    assert row["mathml_integrity"]["malformed_structure"][0]["element"] == "mfrac"


def test_full_repository_report_covers_every_registered_question():
    posts = json.loads((ROOT / "content/posts.json").read_text(encoding="utf-8"))
    report = create_report(ROOT)
    assert len(report["articles"]) == len(posts) >= 132
    assert report["summary"]["registered"] == len(posts)
    assert {row["slug"] for row in report["articles"]} == {post["slug"] for post in posts}
    assert all(row["mathematical_truth_verified_by_this_audit"] is False for row in report["articles"])
