#!/usr/bin/env python3
"""Synchronize four agent Skill mirrors with canonical math-visual-posts."""
from pathlib import Path
import argparse, shutil
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'skills/math-visual-posts'
MIRRORS=[ROOT/d/'skills/math-visual-posts' for d in ('.claude','.pi','.agent','.opencode')]
def content_map(p):
    return {str(f.relative_to(p)):f.read_bytes() for f in p.rglob('*') if f.is_file() and '__pycache__' not in f.parts}
def run(check=False):
    src=content_map(SOURCE)
    assert 'SKILL.md' in src and len(src)>=12
    for target in MIRRORS:
        if check:
            assert target.is_dir() and content_map(target)==src,f'Skill mirror out of sync: {target}'
            print('OK',target.relative_to(ROOT),len(src))
        else:
            if target.exists():shutil.rmtree(target)
            shutil.copytree(SOURCE,target)
            print('SYNC',target.relative_to(ROOT))
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--check',action='store_true')
    run(a.parse_args().check)
