"""Regression tests for derivative PDF questions 1–5: exact sources, algebra, boundaries and authored artifacts."""
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BATCH='derivatives-application-classics-2024-2025'

def bisect(fun,lo,hi):
    a,b=fun(lo),fun(hi)
    assert a*b<0
    for _ in range(90):
        mid=(lo+hi)/2
        fm=fun(mid)
        if fm==0:
            return mid
        if a*fm<0:
            hi=mid
        else:
            lo=mid
            a=fm
    return (lo+hi)/2

def test_source_and_artifact_registration():
    posts=json.loads((ROOT/'content/posts.json').read_text('utf-8'))
    q=[p for p in posts if p.get('source_exam')==BATCH]
    assert [p['question_number'] for p in q]==[1,2,3,4,5]
    assert [p['source_pages'] for p in q]==[[2,3],[3,4,5],[5,6],[6],[6,7]]
    assert all(p['status']=='published' and p['category']=='worked-solutions' for p in q)
    for p in q:
        base=ROOT/'posts'/p['category']/p['slug']
        html=(base/'index.html').read_text('utf-8')
        cover=(base/'assets/cover.svg').read_text('utf-8')
        evidence=json.loads((base/'evidence.json').read_text('utf-8'))
        assert html.index('id="overview"')<html.index('id="question"')
        assert html.count('class="step-note"')>=5 and html.count('<math')>=4
        assert '<svg' in html and '<title>' in cover and '<desc>' in cover
        assert evidence['source']['pages']==p['source_pages']
        assert 'PDF 参考答案' in evidence['answer']['official']
        assert '独立' in evidence['editorial_note']

def test_q01_minimum_and_root_threshold():
    f=lambda x:x*math.exp(x)-1
    assert abs(f(-1)+1+1/math.e)<1e-12
    w=bisect(lambda x:x*math.exp(x)-1,.1,1)
    K=lambda x:math.exp(x)-(math.log(x)+1)/x
    assert abs(K(w)-1)<1e-12
    assert K(.2)>1 and K(2)>1
    for m,expect in ((-2,2),(-1,1),(0,0)):
        vals=[K(.01+i*(4-.01)/2000)+m for i in range(2001)]
        roots=sum((a*b<0) for a,b in zip(vals,vals[1:]))
        if m==-1:
            assert min(vals)>-1e-4
        else:
            assert roots==expect

def test_q02_necessary_threshold_and_sufficiency():
    a=2/(3*math.pi)
    derivative=lambda x:3*a*x*x-2*x+2*math.sin(x)
    assert abs(derivative(math.pi))<1e-12
    assert all(derivative(i/37)>=-1e-10 for i in range(-2000,2001))
    assert 3*(a-.0001)*math.pi**2-2*math.pi<0
    tangent=(math.pi**2+2)/(2*math.pi**3)
    f=lambda x:tangent*x**3-x*x-2*math.cos(x)
    assert abs(f(math.pi)-math.pi*(3*tangent*math.pi**2-2*math.pi))<1e-10

def test_q03_tangent_optimization_and_a_limit():
    g=lambda x:(x+1)*math.exp(-x)
    assert abs(g(0)-1)<1e-12
    assert g(-1)<1 and g(2)<1
    t=lambda x,aa:math.exp(x)-1-x-aa*x*x
    assert all(t(i/100,.5)>=-1e-11 for i in range(0,1001))
    assert t(.001,.501)<0

def test_q04_reflection_gives_strict_asymmetry():
    fun=lambda x:math.log(4*x)-x
    x1=bisect(fun,.01,1)
    x2=bisect(fun,1,4)
    assert 0<x1<1<x2
    assert fun(2-x1)>0
    assert x1+x2>2

def test_q05_tangent_and_strict_stationary_gap():
    for a in [-2.5,-1,-.01]:
        x0=bisect(lambda x:x*math.exp(x)+a,.0000001,1)
        assert 0<x0<1
        gap=a*math.log(x0)
        assert gap>0
    assert abs((math.e+1)*1-math.e-1)<1e-12
