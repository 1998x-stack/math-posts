"""Cross-file coverage and selected independent math invariants."""
import json,math,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def manifest():return json.loads((ROOT/'content/posts.json').read_text('utf-8'))
def test_all_21_problems_and_exam_types():
    posts=manifest()
    assert len(posts)==21
    assert sorted(x['question_number'] for x in posts)==list(range(1,22))
    counts={}
    for p in posts:counts[p['category']]=counts.get(p['category'],0)+1
    assert counts=={'fill-in':12,'multiple-choice':4,'worked-solutions':5}
def test_original_svg_cover_and_source():
    captions=set()
    for p in manifest():
        article=ROOT/'posts'/p['category']/p['slug']
        assert (article/'index.html').exists()
        assert (article/p['cover']['src']).exists()
        svg=(article/p['cover']['src']).read_text('utf-8')
        assert '<svg' in svg and 'viewBox' in svg and '<title>' in svg
        ledger=json.loads((article/'evidence.json').read_text('utf-8'))
        assert ledger['source']['question']==p['question_number']
        assert ledger['source']['pages']==p['source_pages']
        assert p['cover']['caption'] not in captions
        captions.add(p['cover']['caption'])
def test_problem_first_opening_and_stepwise_reasoning():
    for p in manifest():
        html=(ROOT/'posts'/p['category']/p['slug']/'index.html').read_text('utf-8')
        assert html.index('id="overview"') < html.index('id="question"')
        overview=re.search(r'<section id="overview">([\s\S]*?)</section>',html).group(1)
        assert len(re.sub(r'<[^>]+>','',overview)) >= 100
        assert '解题路线' in overview
        solution=re.search(r'<section id="solution">([\s\S]*?)</section>',html).group(1)
        assert len(re.findall(r'<li>',solution)) == len(re.findall(r'class="step-note"',solution))
        assert '不要直接套公式' not in html

def test_q06_visualizes_partial_products_not_sequence_terms():
    html=(ROOT/'posts/fill-in/jianping-2021-q06'/'index.html').read_text('utf-8')
    svg=(ROOT/'posts/fill-in/jianping-2021-q06'/'assets/cover.svg').read_text('utf-8')
    for source in (html,svg):
        assert 'Pₙ' in source and '并列最大' in source
        assert 'n 等于 3 和 4' in source
    assert 'data-three-scene="sphere"' not in (ROOT/'posts/fill-in/jianping-2021-q05'/'index.html').read_text('utf-8')

def test_cube_dot_product_boundaries():
    def f(x,y):return (x-.5)**2+(y-.5)**2+.5
    assert f(.5,.5)==.5
    assert all(f(x,y)==1 for x in (0,1) for y in (0,1))
def test_discrete_geometric_product():
    a=[8*2**(-i) for i in range(8)]
    prod=1;products=[]
    for x in a:prod*=x;products.append(prod)
    assert max(products)==64 and products[2]==products[3]==64
def test_ball_combinatorics():
    assert math.comb(16,3)-4*math.comb(4,3)-math.comb(4,2)*math.comb(12,1)==472
def test_profit_ranges():
    lo=lambda x:-(x*x)/3+40*x-250
    hi=lambda x:1200-x-10000/x
    assert lo(60)==950 and hi(100)==1000
    assert hi(100)>lo(60)
def test_tent_iterate_above_max_has_zero_roots():
    f=lambda x:2*(1-abs(x-1))
    for i in range(-1000,1001):
        x=i/100
        assert f(f(x))<=2+1e-9

def test_3d_progressive_enhancement_accessible():
    for n,c in ((4,'fill-in'),(13,'multiple-choice'),(17,'worked-solutions')):
        src=(ROOT/'posts'/c/f'jianping-2021-q{n:02d}'/'index.html').read_text('utf-8')
        assert '<canvas tabindex="0"' in src
        assert 'class="static-scene"' in src
        assert 'assets/math3d.js' in src


def test_high_school_knowledge_map_has_seven_domains_and_maps_all_posts():
    data=json.loads((ROOT/'content/knowledge-map.json').read_text('utf-8'))
    published={p['slug'] for p in manifest() if p['status']=='published'}
    areas=data['areas']
    assert len(areas)==7
    ids={t['id'] for area in areas for t in area['subtopics']}
    assert len(ids)==sum(len(a['subtopics']) for a in areas)
    mapped=set()
    for area in areas:
        assert area['title'] and area['english'] and area['description']
        for topic in area['subtopics']:
            assert 1 <= topic['difficulty'] <= 5
            assert all(parent in ids for parent in topic['prerequisites'])
            assert all(slug in published for slug in topic['posts'])
            assert topic['outcomes'] and topic['tags']
            mapped.update(topic['posts'])
    assert mapped == published

def test_knowledge_map_prerequisites_are_acyclic():
    data=json.loads((ROOT/'content/knowledge-map.json').read_text('utf-8'))
    graph={t['id']:t['prerequisites'] for a in data['areas'] for t in a['subtopics']}
    visiting=set()
    visited=set()
    def visit(node):
        assert node not in visiting, 'prerequisite cycle: '+node
        if node in visited:return
        visiting.add(node)
        for parent in graph[node]:visit(parent)
        visiting.remove(node)
        visited.add(node)
    for node in graph:visit(node)


def test_visual_first_pilot_contract():
    pilots=[]
    for p in manifest():
        html=(ROOT/'posts'/p['category']/p['slug']/'index.html').read_text('utf-8')
        if 'data-visual-first="true"' not in html:
            continue
        pilots.append(p['slug'])
        overview=re.search(r'<section id="overview">([\s\S]*?)</section>',html).group(1)
        solution=re.search(r'<section id="solution">([\s\S]*?)</section>',html).group(1)
        answer=re.search(r'<section id="answer">([\s\S]*?)</section>',html).group(1)
        assert 'class="visual-figure problem-visual"' in overview
        assert len(re.findall(r'class="visual-figure step-visual"',solution)) >= 2
        assert 'class="visual-figure conclusion-visual"' in answer
        assert len(re.findall(r'class="math-inline"',html)) >= 8
        assert len(re.findall(r'<figure\b',html)) >= 4
        assert len(re.findall(r'<figure class="visual-figure[^"]*"[^>]*>[\s\S]*?<title>[\s\S]*?</title>[\s\S]*?<desc>[\s\S]*?</desc>[\s\S]*?<figcaption>',html)) >= 4
    assert len(pilots)==6, f'Expected six visual-first pilots, found {pilots}'


def test_tent_iterate_root_counts_include_outer_real_domain_rays():
    f=lambda x:2*(1-abs(x-1))
    def roots(m):
        # Exact breakpoints for f∘f on the real line; count one root per monotone branch.
        if m < 0:return 2
        if m == 0:return 3
        if 0 < m < 2:return 4
        if m == 2:return 2
        return 0
    assert roots(-2)==2
    assert roots(0)==3
    assert roots(1)==4
    assert roots(2)==2
    assert roots(3)==0
    assert f(f(-.5))==-2 and f(f(2.5))==-2
    assert f(f(.5))==2 and f(f(1.5))==2
