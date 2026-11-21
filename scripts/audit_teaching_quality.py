#!/usr/bin/env python3
"""Non-destructive, per-question teaching-quality inventory.

Reports review CANDIDATES, not mathematical errors. Source-PDF transcription,
mathematical proofs, and SVG geometry invariants still need human verification.
The review artifact does not alter public website content or release drafts.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
MATH = re.compile(r'<math(?:\s|>)', re.I)
RELATION = re.compile(
    r'(?<![A-Za-z])(?:[A-Za-zα-ωΑ-Ω][A-Za-z0-9_₀-₉′]*\s*'
    r'(?:=|≤|≥|∈|≠|→)\s*[A-Za-z0-9_+\-−π√∞]+)',
    re.UNICODE
)


def raw_math_candidates(node):
    """Heuristic for editorial follow-up, not an assertion of a math error."""
    if node is None:
        return []
    fragment = BeautifulSoup(str(node), 'html.parser')
    for protected in fragment.select('math,svg,script,style,pre,code'):
        protected.decompose()
    plain = fragment.get_text(' ', strip=True)
    return list(dict.fromkeys(RELATION.findall(plain)))[:12]


def audit_post(root: Path, post: dict):
    relative = Path('posts') / post['category'] / post['slug'] / 'index.html'
    html_path = root / relative
    if not html_path.is_file():
        raise FileNotFoundError(f"Missing question HTML: {relative}")
    markup = html_path.read_text(encoding='utf-8')
    soup = BeautifulSoup(markup, 'html.parser')
    question = soup.select_one('#question')
    solution = soup.select_one('#solution')
    overview = soup.select_one('#overview')
    steps = solution.select('ol li') if solution else []
    notes = sum(bool(s.select_one('.step-note')) for s in steps)
    source_svg = soup.select('figure svg')
    figure_captions = soup.select('figure figcaption')
    problem_math = len(question.select('math')) if question else 0
    solution_math = len(solution.select('math')) if solution else 0
    step_math = sum(len(step.select('math')) for step in steps)
    page_math = len(soup.select('math'))
    raw_question = raw_math_candidates(question)
    raw_solution = raw_math_candidates(solution)
    raw_overview = raw_math_candidates(overview)
    no_semantic_step = sum(not step.select('math') for step in steps)
    svg_with_desc = sum(bool(svg.find('title') and svg.find('desc')) for svg in source_svg)
    return {
        'slug': post['slug'],
        'paper_id': post['paper_id'],
        'question_number': post['question_number'],
        'status': post['status'],
        'article_path': relative.as_posix(),
        'structure': {
            'overview': overview is not None,
            'question': question is not None,
            'solution': solution is not None,
            'steps': len(steps),
            'steps_with_explanations': notes,
            'steps_without_inline_mathml': no_semantic_step,
            'figures': len(soup.select('figure')),
            'figure_captions': len(figure_captions),
            'svg': len(source_svg),
            'svg_with_title_and_desc': svg_with_desc,
        },
        'mathml': {
            'total': page_math,
            'original_question': problem_math,
            'solution_section': solution_math,
            'inside_solution_steps': step_math,
        },
        'editorial_candidates': {
            'raw_formula_question': raw_question,
            'raw_formula_solution': raw_solution,
            'raw_formula_overview': raw_overview,
        },
        'review_level': 'mechanical-html-only',
        'full_pdf_proof_verified': False,
    }


def create_report(root: Path):
    posts = json.loads((root / 'content/posts.json').read_text(encoding='utf-8'))
    rows = [audit_post(root, post) for post in posts]
    totals = Counter()
    for row in rows:
        totals[row['status']] += 1
        if row['mathml']['original_question'] == 0:
            totals['no_mathml_in_original_question'] += 1
        if row['mathml']['inside_solution_steps'] == 0:
            totals['no_mathml_inside_steps'] += 1
        if row['editorial_candidates']['raw_formula_question']:
            totals['raw_formula_question_candidates'] += 1
        if row['editorial_candidates']['raw_formula_solution']:
            totals['raw_formula_solution_candidates'] += 1
        if row['structure']['steps'] != row['structure']['steps_with_explanations']:
            totals['some_steps_missing_notes'] += 1
        if row['structure']['svg'] != row['structure']['svg_with_title_and_desc']:
            totals['some_svg_without_title_or_desc'] += 1
    totals['registered'] = len(rows)
    return {
        'schema_version': 1,
        'report_scope': 'Source HTML semantic/formula/step inventory, not PDF or mathematical truth verification',
        'summary': dict(totals),
        'articles': rows,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / '_audit' / 'teaching-quality.json')
    args = parser.parse_args()
    report = create_report(ROOT)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'output': str(args.output), 'summary': report['summary']}, ensure_ascii=False))
    print('CANDIDATES are not mathematical errors; every item requires editorial and original-PDF review.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
