"""Rigorous algebra and provenance regression tests for source PDF Q06–Q10."""
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SRC='derivatives-application-classics-2024-2025'

def bisect(fun,lo,hi):
    fl=fun(lo)
    assert fl*fun(hi)<0
    for _ in range(90):
        md=(lo+hi)/2
        if fl*fun(md)<=0:hi=md
        else:lo=md;fl=fun(md)
    return (lo+hi)/2

def test_original_source_pages_and_article_quality():
    posts=json.loads((ROOT/'content/posts.json').read_text('utf-8'))
    part=[p for p in posts if p.get('source_exam')==SRC and p['question_number']>=6]
    assert [p['question_number'] for p in part]==[6,7,8,9,10]
    assert [p['source_pages'] for p in part]==[[7,8,9],[9,10],[10,11],[11,12,13],[13,14]]
    for p in part:
        assert p['status']=='published' and p['category']=='worked-solutions'
        base=ROOT/'posts'/p['category']/p['slug']
        html=(base/'index.html').read_text('utf-8')
        svg=(base/'assets/cover.svg').read_text('utf-8')
        evidence=json.loads((base/'evidence.json').read_text('utf-8'))
        assert html.index('id="overview"')<html.index('id="question"')
        assert html.count('class="step-note"')>=5
        assert html.count('<math')>=4 and html.count('<svg')>=1
        assert '<title>' in svg and '<desc>' in svg and 'viewBox' in svg
        assert evidence['source']['pages']==p['source_pages']
        assert 'PDF' in evidence['answer']['official']
        assert evidence['answer']['independent_check']
    q9=(ROOT/'posts/worked-solutions/derivative-classics-q09/evidence.json').read_text('utf-8')
    assert 'k=1' in q9 and '范围缺口' in q9

def test_q06_derivative_factorization_and_interval_bounds():
    f=lambda a,x:(a*x*x+x-1)/math.exp(x)
    der=lambda a,x:-(a*x+1)*(x-2)/math.exp(x)
    assert f(0,0)==-1 and der(0,0)==2
    for x in [-2,-.7,0,1.3,2.5,4]:
        assert abs(der(-.5,x)-((x-2)**2)/(2*math.exp(x)))<1e-12
    for a in (math.e/2,math.e*math.e/4):
        ys=[f(a,1+i*.002) for i in range(1001)]
        assert min(ys)>=.5-1e-12
        assert max(ys)<=1+math.exp(-2)+1e-12
    assert abs(f(math.e/2,1)-.5)<1e-12
    assert abs(f(math.e**2/4,2)-(1+math.exp(-2)))<1e-12
    assert f(math.e/2-.001,1)<.5 and f(math.e**2/4+.001,2)>1+math.exp(-2)

def test_q07_unique_minimum_bernoulli_and_geometric_series():
    for c in [-.9,-.5,-.05,.2,1,2]:
        d=lambda x:(1+c)**x*math.log(1+c)-c
        root=bisect(d,0,1)
        assert 0<root<1 and d(0)<0<d(1)
        assert (1+c)**root*math.log(1+c)**2>0
        for m in range(1,16):
            assert (1+c)**m+1e-12>=1+c*m
    for n in (6,7,8,12,20):
        r=(n+2)/(n+3)
        assert r**n<.5
        assert all(((n+3-k)/(n+3))**n < .5**k for k in range(1,n+1))
        normalized=sum(((n+3-k)/(n+3))**n for k in range(1,n+1))
        assert normalized<1

def test_q08_strict_exponential_logarithm_bounds():
    f=lambda x:1/x-1/math.expm1(x)
    assert all(0<f(x)<.5 for x in (.01,.1,.5,1,2,5,10))
    for k in range(1,51):
        assert 2/(2*k+1)<math.log1p(1/k)<1/k
    for n in (1,2,5,20,50):
        assert sum(2/(2*k+1) for k in range(1,n+1))<math.log(n+1)
        assert math.log(n+1)<sum(1/k for k in range(1,n+1))

def test_q09_single_positive_root_and_all_k_sine_bounds():
    f=lambda x:2*math.sin(x-1)-x+1/x+1
    r=bisect(f,1+math.pi/2,1+math.pi)
    assert 3.07<r<3.09
    assert f(1)==1
    assert f(1+math.pi/2)>0 and f(1+math.pi)<0
    for k in range(1,100):
        t=1/(k*k)
        # Mathematical Taylor bound is strict, but subtraction is ill-conditioned
        # at very small t in binary64: check its strictness only where resolvable.
        assert math.sin(t)>1/(k*(k+1))
        if k<=12:
            assert math.sin(t)>t-t**3/6>1/(k*(k+1))
    for n in (1,2,5,10,50,100):
        s=sum(math.sin(1/(k*k)) for k in range(1,n+1))
        assert 1-1/(n+1)<s<2

def test_q10_logarithmic_mean_strict_and_midpoint_slope():
    for a in (2,-1,3,-2):
        f=lambda x:x*x-a*x-a*a*math.log(x)
        df=lambda x:2*x-a-a*a/x
        critical=a if a>0 else -a/2
        level=f(critical)+1
        x1=bisect(lambda x:f(x)-level,.00001,critical)
        x2=bisect(lambda x:f(x)-level,critical,critical+5)
        s=x1+x2
        L=(x2-x1)/(math.log(x2)-math.log(x1))
        assert x1<critical<x2 and L<s/2
        assert df(s/2)>0
        assert abs(a*a/(s-a)-L)<1e-10
    for n in (2,3,8,30):
        lhs=sum(1/(2*k-1) for k in range(2,n+1))
        assert lhs<.5*math.log(n)
        for k in range(2,n+1):
            assert 1/(2*k-1)<.5*math.log(k/(k-1))
