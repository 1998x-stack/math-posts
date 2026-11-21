"""Exact analytic checks for Jianping Q21 tent-map roots and minimal period 2."""
from fractions import Fraction as Q
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def tent(a,x):
    return a*(1-abs(x-1))

def twice(a,x):
    return tent(a,tent(a,x))

def roots_at_a2(m):
    if m<0:
        return (m/4,Q(2)-m/4)
    if m==0:
        return (Q(0),Q(1),Q(2))
    if m<2:
        return (m/4,Q(1)-m/4,Q(1)+m/4,Q(2)-m/4)
    if m==2:
        return (Q(1,2),Q(3,2))
    return ()

def test_exact_root_count_and_coordinates():
    samples=[(Q(-3,2),2),(Q(-1,4),2),(Q(0),3),(Q(1,4),4),(Q(1),4),(Q(7,4),4),(Q(2),2),(Q(9,4),0),(Q(3),0)]
    for m,n in samples:
        xs=roots_at_a2(m)
        assert len(xs)==n and len(set(xs))==n
        assert all(twice(Q(2),x)==m for x in xs)
    assert max(twice(Q(2),Q(i,8)) for i in range(-200,201))==2

def test_true_period_two_not_fixed_points():
    for a in [Q(101,100),Q(11,10),Q(3,2),Q(2),Q(5),Q(20)]:
        u=2*a/(a*a+1)
        v=2*a*a/(a*a+1)
        assert u < 1 < v and u != v
        assert tent(a,u)==v and tent(a,v)==u
        assert twice(a,u)==u and twice(a,v)==v
        w=2*a/(a+1)
        assert tent(a,w)==w and tent(a,Q(0))==0
        assert u!=w and v!=w

def test_q21_explanation_and_interaction_have_source_evidence():
    p=ROOT/'posts/worked-solutions/jianping-2021-q21'
    html=(p/'index.html').read_text('utf-8')
    assert html.count('<math')>=6
    assert html.count('class="step-note"')>=10
    assert html.count('<svg')>=2
    assert 'q21-level-slider' in html and 'q21-root-markers' in html
    assert 'aria-live="polite"' in html
    assert 'm&gt;2' in html or 'm>2' in html
    evidence=json.loads((p/'evidence.json').read_text('utf-8'))
    assert evidence['source']['question']==21
    assert '没有重新取得原始PDF' in evidence['editorial_note']
    manifest=json.loads((ROOT/'content/posts.json').read_text('utf-8'))
    entry=next(x for x in manifest if x['slug']=='jianping-2021-q21')
    assert entry['status']=='published'
    q20=next(x for x in manifest if x['slug']=='jianping-2021-q20')
    assert q20['status']=='draft'


def test_q20_midpoint_discriminant_correction():
    from fractions import Fraction as Q
    for k in [Q(-1,2),Q(-1,4),Q(0),Q(1,5),Q(1,2)]:
        a=5+4*k*k
        b=-32*k*k
        c=64*k*k-20
        delta=b*b-4*a*c
        assert delta==400-960*k*k
        if delta>0:
            u=16*k*k/(5+4*k*k)
            assert 0<=u<1
    limit=Q(5,12)
    assert Q(16)*limit/(5+4*limit)==1
    text=(ROOT/'posts/worked-solutions/jianping-2021-q20'/'index.html').read_text('utf-8')
    assert '400−960k²' in text
    assert '严格范围是 0≤u&lt;1' in text
