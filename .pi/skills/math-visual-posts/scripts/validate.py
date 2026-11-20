#!/usr/bin/env python3
"""Static article quality gate. Exit nonzero on critical failures; write JSON with --report."""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path
from bs4 import BeautifulSoup

# Production-process labels are disallowed inside an article; they belong in project docs.
BANNED = (
    '原创图解 · 单文件离线 HTML',
    '用直觉 → 图示 → 数学 → 工程实现，理解残差网络 · 参考 Colah 风格，非原文翻译',
)

def validate(path: Path) -> dict:
    html = path.read_text(encoding='utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    failures, warnings = [], []
    h1 = soup.find_all('h1')
    if len(h1) != 1: failures.append(f'Expected exactly one h1, found {len(h1)}')
    if not soup.find('main'): failures.append('Missing semantic main')
    if not soup.find('nav'): warnings.append('No navigable table of contents')
    if not soup.find('meta', attrs={'name': 'viewport'}): failures.append('Missing mobile viewport meta')
    if len(soup.find_all('h2')) < 2: failures.append('Expected at least two instructional sections')
    for phrase in BANNED:
        if phrase in soup.get_text(' ', strip=True) or phrase in html:
            failures.append('Banned production/process copy found: ' + phrase)
    overview = soup.find(id='overview')
    question = soup.find(id='question')
    if overview is None or question is None:
        failures.append('Every post needs a problem-first overview before the formal question')
    elif html.find('id="overview"') > html.find('id="question"'):
        failures.append('Problem overview must appear before the formal question')
    elif len(overview.get_text(' ', strip=True)) < 100:
        failures.append('Problem overview is too short to explain the task')
    elif '解题路线' not in overview.get_text(' ', strip=True):
        failures.append('Problem overview must include a concise solution route')
    if '不要直接套公式' in html:
        failures.append('Generic filler copy is forbidden; explain this problem specifically')
    solution_steps = soup.select('#solution ol li')
    for index, step in enumerate(solution_steps, 1):
        if not step.select_one('.step-note'):
            failures.append(f'Solution step {index} needs a problem-specific why/explanation note')
    anchors = {tag.get('id') for tag in soup.select('[id]')}
    for a in soup.select('a[href^="#"]'):
        target = a['href'][1:]
        if target and target not in anchors: failures.append('Broken local anchor #' + target)
    figures = soup.find_all('figure')
    if not figures: failures.append('No semantic figures')
    for index, figure in enumerate(figures, 1):
        if not figure.find('svg') and not figure.find('img'):
            failures.append(f'Figure {index} has no image or SVG')
        caption = figure.find('figcaption')
        if not caption or not caption.get_text(strip=True):
            failures.append(f'Figure {index} has no nonempty figcaption')
    svgs = soup.find_all('svg')
    if not svgs: failures.append('No SVG illustrations')
    for index, svg in enumerate(svgs, 1):
        if not svg.has_attr('viewbox'): failures.append(f'SVG {index} missing viewBox')
        if not (svg.get('aria-label') or svg.get('aria-labelledby') or svg.find('title')):
            failures.append(f'SVG {index} missing accessible label/title')
    for i, img in enumerate(soup.find_all('img'), 1):
        if not img.get('alt'): warnings.append(f'Image {i} missing alt text')
        src = img.get('src', '')
        if src and not re.match(r'^(?:data:|https?://)', src) and not (path.parent / src).exists():
            failures.append('Missing image: ' + src)
    for script in soup.find_all('script', src=True):
        if script['src'].startswith('http'): warnings.append('External JS dependency: ' + script['src'])
    for link in soup.find_all('link', href=True):
        if link['href'].startswith('http'): warnings.append('External stylesheet dependency: ' + link['href'])
    # MathML is optional for legacy articles; whenever present it must be well formed.
    maths = soup.find_all('math')
    for idx, math in enumerate(maths, 1):
        if math.find_parent('svg'):
            failures.append(f'MathML {idx} nested inside SVG (invalid namespace)')
        if not (math.get('aria-label') or math.get('aria-labelledby')):
            failures.append(f'MathML {idx} missing accessible description')
        if not math.find(['mi', 'mn', 'mo', 'mrow', 'mfrac', 'msup', 'msub', 'munder', 'munderover', 'mtable']):
            failures.append(f'MathML {idx} has no mathematical structure')
        if math.get('display') not in (None, 'inline', 'block'):
            failures.append(f'MathML {idx} invalid display attribute')
        for name, arity in [('mfrac', 2), ('msub', 2), ('msup', 2),
                            ('msubsup', 3), ('munder', 2), ('mover', 2), ('munderover', 3)]:
            for node in math.find_all(name):
                children = [child for child in node.children if getattr(child, 'name', None)]
                if len(children) != arity:
                    failures.append(f'MathML {idx} malformed {name}: expected {arity} children, got {len(children)}')
        if math.get('display') == 'block':
            region = math.find_parent(attrs={'data-math-scroll': True})
            if region is None:
                region = math.find_parent(class_=['math-scroll', 'eq-scroll'])
            if region is None or region.get('tabindex') != '0' or region.get('role') != 'region':
                failures.append(f'MathML {idx} display equation needs a keyboard-focusable scroll region')

    # Visual-first pages are held to a stricter presentation contract than legacy articles.
    body = soup.body
    if body and body.get('data-visual-first') == 'true':
        overview_section = soup.find(id='overview')
        solution_section = soup.find(id='solution')
        answer_section = soup.find(id='answer')
        if overview_section is None or not overview_section.select('figure.problem-visual'):
            failures.append('Visual-first page needs a problem diagram inside #overview')
        if solution_section is None or len(solution_section.select('figure.step-visual')) < 2:
            failures.append('Visual-first page needs at least two step-level SVG diagrams inside #solution')
        if answer_section is None or not answer_section.select('figure.conclusion-visual'):
            failures.append('Visual-first page needs a conclusion diagram inside #answer')
        if len(figures) < 4:
            failures.append(f'Visual-first page needs at least four meaningful figures, found {len(figures)}')
        inline_math = soup.select('math.math-inline')
        if len(inline_math) < 8:
            failures.append(f'Visual-first page needs at least eight inline MathML expressions, found {len(inline_math)}')
        for index, figure in enumerate(soup.select('figure.visual-figure'), 1):
            svg = figure.find('svg')
            if svg is None or svg.find('title') is None or svg.find('desc') is None:
                failures.append(f'Visual-first figure {index} needs an SVG title and description')
            if not figure.find('figcaption'):
                failures.append(f'Visual-first figure {index} needs a teaching caption')
        for section_id in ('overview', 'question', 'solution', 'answer'):
            section = soup.find(id=section_id)
            if section is None:
                continue
            for paragraph in section.find_all('p'):
                fragment = BeautifulSoup(str(paragraph), 'html.parser')
                for tag in fragment.select('math, svg, code'):
                    tag.decompose()
                text = fragment.get_text(' ', strip=True)
                if len(text) > 110:
                    failures.append(f'Visual-first paragraph in #{section_id} is too long ({len(text)} chars); split it or visualize the reasoning')
        visible = BeautifulSoup(str(body), 'html.parser')
        for tag in visible.select('math, svg, script, style, code, pre, noscript'):
            tag.decompose()
        visible_text = visible.get_text(' ', strip=True)
        raw_formula_patterns = (
            re.compile(r'(?<![\w])(?:[A-Za-z][A-Za-z0-9₀-₉]*)(?:\([^()\n]{1,24}\))?\s*(?:=|≤|≥|<|>)\s*[-−]?\s*(?:\d+(?:\.\d+)?|[A-Za-z(])'),
            re.compile(r'(?<![\w])[A-Z]\s*\([^()\n]*,[^()\n]*\)'),
            re.compile(r'(?<![\w])[A-Za-z][A-Za-z0-9₀-₉]*[²³⁴]'),
            re.compile(r'(?<![\w])\d+\s*/\s*\d+(?![\w])'),
            re.compile(r'(?<![\w])[A-Z]{1,3}\s*(?:∥|⊥)\s*(?:[A-Z]{1,3}|平面)'),
            re.compile(r'(?<![\w])[A-Za-z][A-Za-z0-9₀-₉]*\s*(?:·|×)\s*[A-Za-z]')
        )
        for pattern in raw_formula_patterns:
            match = pattern.search(visible_text)
            if match:
                failures.append('Unrendered mathematical expression in visual-first page: ' + match.group(0))
    if not soup.find('a', href=re.compile('source-notes|github.com/1998x-stack/math-posts')):
        warnings.append('No source provenance hyperlink in article')
    return {
        'path': str(path), 'pass': not failures,
        'counts': {'h2': len(soup.find_all('h2')), 'figures': len(figures), 'svg': len(svgs), 'buttons': len(soup.find_all('button')), 'mathml': len(maths)},
        'failures': failures, 'warnings': warnings,
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument('html', type=Path)
    p.add_argument('--report', type=Path)
    args = p.parse_args()
    report = validate(args.html.resolve())
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report['pass'] else 1

if __name__ == '__main__': sys.exit(main())
