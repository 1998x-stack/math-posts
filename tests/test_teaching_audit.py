"""The per-question teaching inventory is an advisory report, not a math proof."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from audit_teaching_quality import create_report, audit_post


def test_teaching_quality_inventory_covers_every_registered_question():
    import json
    posts=json.loads((ROOT / 'content/posts.json').read_text('utf-8'))
    report=create_report(ROOT)
    rows=report['articles']
    assert len(rows)==len(posts) >= 132
    assert report['summary']['registered']==len(rows)
    assert {r['slug'] for r in rows}=={p['slug'] for p in posts}
    assert all(r['review_level']=='mechanical-html-only' for r in rows)
    assert all(r['full_pdf_proof_verified'] is False for r in rows)


def test_teaching_audit_reports_position_and_explanations_without_inventing_proof():
    import json
    posts=json.loads((ROOT / 'content/posts.json').read_text('utf-8'))
    post=next(p for p in posts if p['slug']=='jianping-2021-q02')
    row=audit_post(ROOT,post)
    assert row['structure']['overview'] and row['structure']['question'] and row['structure']['solution']
    assert row['structure']['steps'] > 0
    assert row['structure']['steps']==row['structure']['steps_with_explanations']
    assert row['mathml']['total'] >= row['mathml']['original_question']
    assert isinstance(row['editorial_candidates']['raw_formula_solution'],list)
