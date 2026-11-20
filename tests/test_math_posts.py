"""Cross-file coverage and selected independent math invariants."""
import json,math
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
    for n,c in ((4,'fill-in'),(5,'fill-in'),(13,'multiple-choice'),(17,'worked-solutions')):
        src=(ROOT/'posts'/c/f'jianping-2021-q{n:02d}'/'index.html').read_text('utf-8')
        assert '<canvas tabindex="0"' in src
        assert 'class="static-scene"' in src
        assert 'assets/math3d.js' in src
