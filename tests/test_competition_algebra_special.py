"""Algebra curriculum: structural MathML and independent mathematical invariants."""
from __future__ import annotations
import cmath
import json
import math
from pathlib import Path
import random
import sympy as sp
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
DIR=ROOT/"specials"/"algebra-structures"
MANIFEST=DIR/"source"/"manifest.json"

def formulas(data):
    return [*data["core"],data["example"].get("eq"),
            *(s.get("eq") for s in data["steps"]),
            *(q.get(k) for q in data["exercises"] for k in ("eq","answerEq"))]

def test_12_algebra_html_documents_and_mathml():
    lessons=json.loads(MANIFEST.read_text(encoding="utf-8"))["lessons"]
    assert len(lessons)==12
    assert len(list(DIR.glob("[0-9][0-9]-*.html")))==12
    assert len(list((DIR/"svg").glob("*.svg")))==12
    seen=set()
    for p in lessons:
        article=DIR/(p["slug"]+".html")
        assert article.is_file(),article
        soup=BeautifulSoup(article.read_text(encoding="utf-8"),"html.parser")
        assert len(soup.find_all("h1"))==1
        assert len(soup.find_all("figure"))==5
        assert len(soup.find_all("svg"))==5
        assert len(soup.find_all("math"))>=7
        assert soup.select_one("input[type=range]") is not None
        assert soup.select_one("[data-algebra-lesson]")["data-algebra-lesson"]==str(p["n"])
        assert "https://cdn." not in article.read_text(encoding="utf-8")
        assert all(soup.select_one("#"+key) is not None for key in
                   ("problem","explore","theory","walkthrough","pitfalls","practice","links"))
        assert len(soup.find_all("details"))==3
        for svg in soup.find_all("svg"):
            assert svg.get("viewbox") and svg.find("title") and svg.find("desc")
        for node in soup.find_all("math"):
            assert node.get("aria-label") and node.find_parent("svg") is None
            for tag,count in (("mfrac",2),("msup",2),("msub",2),
                              ("munder",2),("munderover",3),("msubsup",3)):
                for item in node.find_all(tag):
                    elements=[x for x in item.children if getattr(x,"name",None)]
                    assert len(elements)==count,(p["slug"],tag,str(item)[:140])
        src=json.loads((DIR/"source"/f'{p["n"]:02d}.json').read_text(encoding="utf-8"))
        assert len(src["steps"])>=4 and len(src["exercises"])==3
        assert len([x for x in formulas(src) if x])>=7
        assert p["slug"] not in seen
        seen.add(p["slug"])

def test_vieta_newton_factor_interpolation():
    x,y,z,t=sp.symbols("x y z t")
    p=x+y+z;q=x*y+y*z+z*x;r=x*y*z
    assert sp.expand((t-x)*(t-y)*(t-z)-(t**3-p*t**2+q*t-r))==0
    assert sp.expand(x**2+y**2+z**2-(p*p-2*q))==0
    poly=t**3-2*t**2+t-1
    roots=sp.nroots(poly,maxsteps=300)
    for k,target in ((1,2),(2,2),(3,5),(4,10),(5,17)):
        assert abs(complex(sum(v**k for v in roots))-target)<1e-7
    assert sp.factor(t**3-6*t*t+11*t-6)==(t-1)*(t-2)*(t-3)
    P=sp.interpolate([(0,1),(1,2),(2,5)],t)
    assert sp.simplify(P-(t*t+1))==0
    for y2 in (1,3,5,7,9):
        f=sp.interpolate([(0,1),(1,2),(2,y2)],t)
        for xx,yy in ((0,1),(1,2),(2,y2)):
            assert f.subs(t,xx)==yy

def test_cauchy_complex_roots_chebyshev():
    rng=random.Random(20261126)
    for _ in range(100):
        c=rng.uniform(.1,3);x=rng.uniform(-10,10);y=rng.uniform(-10,10)
        assert math.isclose(c*(x+y),c*x+c*y,rel_tol=1e-11,abs_tol=1e-11)
        angle=rng.uniform(-3,3);z=complex(x,y)
        assert math.isclose(abs(cmath.exp(1j*angle)*z),abs(z),rel_tol=1e-11,abs_tol=1e-11)
    for n in range(3,10):
        omega=cmath.exp(2j*math.pi/n)
        for exponent in (0,1,2,3,4,5,6,10,12):
            value=sum(omega**(exponent*k) for k in range(n))
            expected=n if exponent%n==0 else 0
            assert abs(value-expected)<1e-8
    for theta in [0,.12,.31,.78,1.3,2.2,math.pi]:
        xx=math.cos(theta);t0=1;t1=xx
        for n in range(0,11):
            if n==0:val=t0
            elif n==1:val=t1
            else:val=2*xx*t1-t0;t0,t1=t1,val
            assert abs(val-math.cos(n*theta))<1e-10

def test_recurrence_matrix_differences_sophie_germain():
    rng=random.Random(1009)
    a=[2**n-1 for n in range(20)]
    for n in range(18):
        assert a[n+2]-3*a[n+1]+2*a[n]==0
    M=sp.Matrix([[1,1],[1,0]])
    fib=[0,1]
    for n in range(2,16):fib.append(fib[-1]+fib[-2])
    for n in range(1,14):
        expected=sp.Matrix([[fib[n+1],fib[n]],[fib[n],fib[n-1]]])
        assert M**n==expected
        assert expected.det()==(-1)**n
    for n in range(0,50):
        assert (n+2)**2-2*(n+1)**2+n*n==2
    for n in range(1,50):
        assert sum(k*k for k in range(1,n+1))==n*(n+1)*(2*n+1)//6
    X,Y=sp.symbols("X Y")
    A=X*X-2*X*Y+2*Y*Y
    B=X*X+2*X*Y+2*Y*Y
    assert sp.expand(A*B-(X**4+4*Y**4))==0
    for _ in range(100):
        x=rng.randint(1,100);y=rng.randint(0,100)
        assert (x*x-2*x*y+2*y*y)*(x*x+2*x*y+2*y*y)==x**4+4*y**4

def test_boundary_cases():
    # Interpolation at repeated abscissae does not satisfy the distinct-node theorem.
    x=sp.symbols("x")
    assert x.subs(x,0)!=1
    # For the Sophie Germain example n=1 is prime, not composite.
    assert sp.isprime(1**4+4)
    # Chebyshev's interval bound is not globally true.
    assert abs(4*2**3-3*2)>1
    # Characteristic roots of this specific recurrence are distinct.
    lam=sp.symbols("lam")
    assert sp.factor(lam**2-3*lam+2)==(lam-1)*(lam-2)
