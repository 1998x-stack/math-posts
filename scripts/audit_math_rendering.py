#!/usr/bin/env python3
"""Audit formula rendering in every original question, solution step and geometry figure.

This is a non-destructive review queue. It finds visible formula candidates outside
MathML and checks DOM structure; it does not prove transcription or mathematics.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
import os
from pathlib import Path
import re
from bs4 import BeautifulSoup, NavigableString, Comment, Tag

ROOT = Path(__file__).resolve().parents[1]
PROTECTED = {"math", "svg", "script", "style", "pre", "code", "noscript", "template"}

PATTERNS = {
    "latex_source": re.compile(r"(?:\\\(|\\\[|\$\$?).+?(?:\\\)|\\\]|\$\$?)"),
    "absolute_value": re.compile(r"\|[A-Za-zΑ-Ωα-ω0-9_₀-₉⁰-⁹²³+\-−·×/(), ]{1,36}\|"),
    "absolute_value_relation": re.compile(
        r"\|[A-Za-zΑ-Ωα-ω0-9_₀-₉⁰-⁹²³+\-−·×/(), ]{1,36}\|\s*(?:=|≤|≥|<|>|≠|≈)\s*"
        r"\|[A-Za-zΑ-Ωα-ω0-9_₀-₉⁰-⁹²³+\-−·×/(), ]{1,36}\|"
    ),
    "coordinate": re.compile(r"\b[A-Z][A-Za-z0-9₀-₉]*\s*=\s*\([^()\n]{1,48}\)"),
    "relation": re.compile(
        r"(?<![A-Za-z0-9])[A-Za-zΓΔΣΩΑ-Ωα-ω][A-Za-z0-9_₀-₉⁰-⁹²³⁴⁵⁶⁷⁸⁹′′]*"
        r"[A-Za-z0-9_₀-₉⁰-⁹²³⁴⁵⁶⁷⁸⁹ΓΔΣΩΑ-Ωα-ω+\-−×·*/^(){}\[\],.:| ]{0,60}?"
        r"(?:=|≤|≥|<|>|≠|≈|∈|∉|∥|⊥|→|↔|⇔|⇒)\s*"
        r"[A-Za-z0-9ΓΔΣΩΑ-Ωα-ω_₀-₉⁰-⁹²³⁴⁵⁶⁷⁸⁹π√∞+\-−×·*/^(){}\[\],.:|]+"
    ),
    "superscript": re.compile(r"(?<![A-Za-z0-9])[A-Za-zΓΔΣΩΑ-Ωα-ω][A-Za-z0-9]*[⁰¹²³⁴⁵⁶⁷⁸⁹]"),
    "subscript": re.compile(r"(?<![A-Za-z0-9])[A-Za-zΓΔΣΩΑ-Ωα-ω][A-Za-z0-9]*[₀₁₂₃₄₅₆₇₈₉]"),
    "ratio_with_root": re.compile(r"\b\d+\s*:\s*\d+\s*√\s*\d+"),
    "vector_arrow": re.compile(r"[A-Za-zΑ-Ωα-ω]\s*[⃗→]"),
    "trig_or_log": re.compile(r"\b(?:sin|cos|tan|arctan|ln|log)\s*[A-Za-zΑ-Ωα-ω]\w*"),
}

GEOMETRY_CONCEPTS = {"analytic-geometry", "conics"}
SUBQUESTION = re.compile(r"(?:（\s*[1-9]\d*\s*）|\(\s*[1-9]\d*\s*\)|[①②③④⑤⑥⑦⑧⑨])")


def _is_protected_text(node: NavigableString) -> bool:
    parent = node.parent
    if parent is None or isinstance(node, Comment) or parent.name in PROTECTED:
        return True
    return parent.find_parent(list(PROTECTED)) is not None


def visible_text(node: Tag | None) -> str:
    if node is None:
        return ""
    parts = []
    for item in node.find_all(string=True):
        if not _is_protected_text(item):
            value = re.sub(r"\s+", " ", str(item)).strip()
            if value:
                parts.append(value)
    return " ".join(parts)


def formula_candidates(node: Tag | None, limit: int = 30) -> list[dict]:
    """Find visible formula-like text outside MathML/SVG/code for editorial review."""
    if node is None:
        return []
    found: list[dict] = []
    seen: set[tuple[str, str]] = set()
    for item in node.find_all(string=True):
        if _is_protected_text(item):
            continue
        raw = re.sub(r"\s+", " ", str(item)).strip()
        if not raw:
            continue
        for kind, pattern in PATTERNS.items():
            for match in pattern.finditer(raw):
                value = re.sub(r"\s+", " ", match.group(0)).strip()
                if len(value) < 2 or (kind, value) in seen:
                    continue
                seen.add((kind, value))
                start, end = match.span()
                found.append({
                    "kind": kind,
                    "text": value,
                    "context": raw[max(0, start - 38):min(len(raw), end + 38)],
                })
                if len(found) >= limit:
                    return found
    return found


def mathml_integrity(soup: BeautifulSoup) -> dict:
    math_nodes = soup.find_all("math")
    missing_name = 0
    empty = 0
    malformed = []
    inside_svg = len(soup.select("svg math"))
    arities = {"mfrac": 2, "msub": 2, "msup": 2, "msubsup": 3, "munder": 2, "munderover": 3}
    for index, math in enumerate(math_nodes, start=1):
        if not (math.get("aria-label") or math.get("aria-labelledby")):
            missing_name += 1
        if not math.find(True):
            empty += 1
        for tag_name, expected in arities.items():
            for node in math.find_all(tag_name):
                children = [child for child in node.find_all(recursive=False) if isinstance(child, Tag)]
                if len(children) != expected:
                    malformed.append({
                        "math_index": index,
                        "element": tag_name,
                        "expected_element_children": expected,
                        "actual_element_children": len(children),
                    })
    return {
        "total": len(math_nodes),
        "missing_accessible_name": missing_name,
        "empty": empty,
        "inside_svg": inside_svg,
        "malformed_structure": malformed,
    }


def _load_evidence(article_path: Path) -> dict:
    path = article_path.parent / "evidence.json"
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"_read_error": True}


def _section_audit(node: Tag | None) -> dict:
    return {
        "present": node is not None,
        "mathml_count": len(node.select("math")) if node else 0,
        "formula_candidates": formula_candidates(node),
        "visible_text_length": len(visible_text(node)),
    }


def audit_post(root: Path, post: dict) -> dict:
    relative = Path("posts") / post["category"] / post["slug"] / "index.html"
    article_path = root / relative
    if not article_path.is_file():
        raise FileNotFoundError(f"Missing question HTML: {relative}")

    soup = BeautifulSoup(article_path.read_text(encoding="utf-8"), "html.parser")
    question = soup.select_one("#question")
    solution = soup.select_one("#solution")
    overview = soup.select_one("#overview")
    visual = soup.select_one("#visual")
    steps = solution.select("ol li") if solution else []
    evidence = _load_evidence(article_path)
    source = evidence.get("source", {}) if isinstance(evidence, dict) else {}
    transcription = evidence.get("transcription", {}) if isinstance(evidence, dict) else {}

    question_audit = _section_audit(question)
    solution_audit = _section_audit(solution)
    overview_audit = _section_audit(overview)
    step_rows = []
    for index, step in enumerate(steps, start=1):
        candidates = formula_candidates(step)
        math_count = len(step.select("math"))
        step_rows.append({
            "step": index,
            "mathml_count": math_count,
            "formula_candidate_count": len(candidates),
            "formula_candidates": candidates,
            "has_step_note": bool(step.select_one(".step-note")),
            "needs_formula_review": bool(candidates and math_count == 0),
            "mixed_rendering_review": bool(candidates and math_count > 0),
        })

    concepts = (post.get("facets") or {}).get("concept", [])
    is_geometry = bool(GEOMETRY_CONCEPTS.intersection(concepts))
    visual_figures = visual.select("figure") if visual else []
    visual_svgs = visual.select("svg") if visual else []
    visual_captions = visual.select("figcaption") if visual else []
    accessible_svgs = sum(bool(svg.find("title") and svg.find("desc")) for svg in visual_svgs)
    has_assertions = bool(
        evidence.get("visual_assertions")
        or (evidence.get("qa") or {}).get("visual_assertions")
    ) if isinstance(evidence, dict) else False

    integrity = mathml_integrity(soup)
    question_text = visible_text(question)
    source_pages = source.get("pages", []) if isinstance(source, dict) else []
    issues = []

    if not question:
        issues.append("missing-original-question-section")
    elif question_audit["formula_candidates"] and question_audit["mathml_count"] == 0:
        issues.append("original-question-formulas-not-rendered")
    elif question_audit["formula_candidates"]:
        issues.append("original-question-mixed-rendering-review")

    unrendered_steps = [row for row in step_rows if row["needs_formula_review"]]
    mixed_steps = [row for row in step_rows if row["mixed_rendering_review"]]
    if unrendered_steps:
        issues.append("solution-step-formulas-not-rendered")
    if mixed_steps:
        issues.append("solution-step-mixed-rendering-review")
    if not solution:
        issues.append("missing-solution-section")
    if integrity["missing_accessible_name"] or integrity["empty"] or integrity["inside_svg"] or integrity["malformed_structure"]:
        issues.append("mathml-structure-or-accessibility-review")
    if is_geometry and not visual_svgs:
        issues.append("analytic-geometry-missing-inline-svg")
    if is_geometry and visual_svgs and not visual_captions:
        issues.append("analytic-geometry-missing-figure-caption")
    if is_geometry and visual_svgs and accessible_svgs != len(visual_svgs):
        issues.append("analytic-geometry-svg-accessibility-review")

    if any(code in issues for code in (
        "original-question-formulas-not-rendered",
        "solution-step-formulas-not-rendered",
        "missing-original-question-section",
        "missing-solution-section",
    )):
        priority = "P0"
    elif any(code.startswith("analytic-geometry") for code in issues):
        priority = "P1"
    elif issues:
        priority = "P2"
    else:
        priority = "none"

    latex_candidates = [
        candidate
        for section in (question, solution, overview)
        for candidate in formula_candidates(section)
        if candidate["kind"] == "latex_source"
    ]

    return {
        "slug": post["slug"],
        "paper_id": post.get("paper_id"),
        "question_number": post.get("question_number"),
        "status": post.get("status"),
        "article_path": relative.as_posix(),
        "priority": priority,
        "issue_codes": issues,
        "source_completeness": {
            "question_section_present": question is not None,
            "question_text_length": len(question_text),
            "source_question_number": source.get("question") if isinstance(source, dict) else None,
            "source_pages": source_pages,
            "transcription_status": transcription.get("status") if isinstance(transcription, dict) else None,
            "subquestion_markers_in_question": len(SUBQUESTION.findall(question_text)),
        },
        "formula_rendering": {
            "overview": overview_audit,
            "original_question": question_audit,
            "solution": solution_audit,
            "solution_steps": step_rows,
            "steps_with_formula_candidates_but_no_mathml": len(unrendered_steps),
            "steps_with_mixed_mathml_and_raw_candidates": len(mixed_steps),
            "latex_source_candidates": latex_candidates,
        },
        "visualization": {
            "is_analytic_geometry": is_geometry,
            "figure_count_in_visual_section": len(visual_figures),
            "inline_svg_count": len(visual_svgs),
            "figure_caption_count": len(visual_captions),
            "accessible_svg_count": accessible_svgs,
            "visual_assertions_recorded": has_assertions,
            "visual_assertions_recommended": is_geometry and not has_assertions,
            "missing_inline_svg": is_geometry and not visual_svgs,
        },
        "mathml_integrity": integrity,
        "review_level": "mechanical-visible-text-and-dom-only",
        "source_pdf_visually_verified_by_this_audit": False,
        "mathematical_truth_verified_by_this_audit": False,
    }


def create_report(root: Path = ROOT) -> dict:
    posts = json.loads((root / "content/posts.json").read_text(encoding="utf-8"))
    rows = [audit_post(root, post) for post in posts]
    totals = Counter()
    priority_order = {"P0": 0, "P1": 1, "P2": 2, "none": 3}

    for row in rows:
        totals[row["status"]] += 1
        formulas = row["formula_rendering"]
        question_candidates = formulas["original_question"]["formula_candidates"]
        totals["question_formula_candidate_count"] += len(question_candidates)
        if question_candidates:
            totals["articles_with_question_formula_candidates"] += 1
            if formulas["original_question"]["mathml_count"] == 0:
                totals["articles_with_question_formulas_and_no_mathml"] += 1
        totals["solution_formula_candidate_count"] += len(formulas["solution"]["formula_candidates"])
        for step in formulas["solution_steps"]:
            if step["formula_candidate_count"]:
                totals["steps_with_formula_candidates"] += 1
            if step["needs_formula_review"]:
                totals["steps_with_formula_candidates_but_no_mathml"] += 1
            if step["mixed_rendering_review"]:
                totals["steps_with_mixed_mathml_and_raw_candidates"] += 1
        if formulas["steps_with_formula_candidates_but_no_mathml"]:
            totals["articles_with_unrendered_formula_steps"] += 1
        if row["visualization"]["is_analytic_geometry"]:
            totals["analytic_geometry_articles"] += 1
            if row["visualization"]["missing_inline_svg"]:
                totals["analytic_geometry_articles_missing_inline_svg"] += 1
            if row["visualization"]["visual_assertions_recommended"]:
                totals["analytic_geometry_articles_without_recorded_visual_assertions"] += 1
        totals["mathml_missing_accessible_name"] += row["mathml_integrity"]["missing_accessible_name"]
        totals["mathml_malformed_structures"] += len(row["mathml_integrity"]["malformed_structure"])
        totals["mathml_inside_svg"] += row["mathml_integrity"]["inside_svg"]
        if formulas["latex_source_candidates"]:
            totals["articles_with_visible_latex_source_candidates"] += 1
        if row["priority"] != "none":
            totals["articles_needing_review"] += 1

    totals["registered"] = len(rows)
    priority_queue = sorted(
        [{
            "slug": row["slug"],
            "status": row["status"],
            "article_path": row["article_path"],
            "priority": row["priority"],
            "issue_codes": row["issue_codes"],
            "question_candidates": row["formula_rendering"]["original_question"]["formula_candidates"][:8],
            "unrendered_step_numbers": [
                step["step"] for step in row["formula_rendering"]["solution_steps"]
                if step["needs_formula_review"]
            ],
        } for row in rows if row["priority"] != "none"],
        key=lambda item: (priority_order[item["priority"]], item["slug"]),
    )
    return {
        "schema_version": 1,
        "generated_by": "scripts/audit_math_rendering.py",
        "report_scope": (
            "All registered article source HTML; visible formula-candidate extraction, per-step MathML "
            "placement, MathML DOM structure and analytic-geometry SVG inventory. This is not a PDF "
            "transcription review, browser rendering test or mathematical proof."
        ),
        "summary": dict(totals),
        "priority_queue": priority_queue,
        "articles": rows,
    }


def write_github_summary(report: dict) -> None:
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_path:
        return
    summary = report["summary"]
    lines = [
        "## Math rendering and geometry audit",
        "",
        "| Metric | Count |",
        "|---|---:|",
        f"| Registered articles | {summary.get('registered', 0)} |",
        f"| Original questions with formula candidates but no MathML | {summary.get('articles_with_question_formulas_and_no_mathml', 0)} |",
        f"| Solution steps with formula candidates but no MathML | {summary.get('steps_with_formula_candidates_but_no_mathml', 0)} |",
        f"| Steps with mixed MathML and raw formula candidates | {summary.get('steps_with_mixed_mathml_and_raw_candidates', 0)} |",
        f"| Analytic-geometry articles | {summary.get('analytic_geometry_articles', 0)} |",
        f"| Analytic-geometry articles missing inline SVG | {summary.get('analytic_geometry_articles_missing_inline_svg', 0)} |",
        f"| MathML nodes missing accessible names | {summary.get('mathml_missing_accessible_name', 0)} |",
        f"| Malformed MathML structures | {summary.get('mathml_malformed_structures', 0)} |",
        "",
        "Candidates are review leads, not proven errors. This audit does not inspect original PDF pixels or prove mathematical correctness.",
        "",
    ]
    top = report.get("priority_queue", [])[:12]
    if top:
        lines.extend(["### Highest-priority review queue", "", "| Priority | Article | Issues |", "|---|---|---|"])
        for row in top:
            lines.append(f"| {row['priority']} | {row['slug']} | {', '.join(row['issue_codes'])} |")
        lines.append("")
    with open(summary_path, "a", encoding="utf-8") as handle:
        handle.write("\n".join(lines))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path, default=ROOT / "_audit" / "math-rendering.json")
    args = parser.parse_args()
    report = create_report(args.root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "summary": report["summary"]}, ensure_ascii=False))
    write_github_summary(report)
    print("Review candidates require source-page and mathematical review; no automatic content edits were made.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
