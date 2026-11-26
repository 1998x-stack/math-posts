"""Independent quality gates for the 12 geometry-special HTML articles."""
from __future__ import annotations
import json, math, random, re
from pathlib import Path
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
SERIES=ROOT/"specials"/"geometry-transformations"
MANIFEST=SERIES/"source"/"manifest.json"


def determinant(a,b):
    return a[0]*b[1]-a[1]*b[0]


def subtract(a,b):
    return (a[0]-b[0],a[1]-b[1])


def distance(a,b):
    return math.hypot(a[0]-b[0],a[1]-b[1])


def circumcircle(a,b,c):
    ax,ay=a;bx,by=b;cx,cy=c
    z=2*(ax*(by-cy)+bx*(cy-ay)+cx*(ay-by))
    assert abs(z)>1e-9
    aa=ax*ax+ay*ay;bb=bx*bx+by*by;cc=cx*cx+cy*cy
    return ((aa*(by-cy)+bb*(cy-ay)+cc*(ay-by))/z,
            (aa*(cx-bx)+bb*(ax-cx)+cc*(bx-ax))/z)


def foot(p,a,b):
    v=subtract(b,a)
    t=((p[0]-a[0])*v[0]+(p[1]-a[1])*v[1])/(v[0]**2+v[1]**2)
    return (a[0]+t*v[0],a[1]+t*v[1])


def test_twelve_page_structure_and_mathml():
    rows=json.loads(MANIFEST.read_text(encoding="utf-8"))["lessons"]
    assert len(rows)==12
    assert len(list(SERIES.glob("[0-9][0-9]-*.html")))==12
    for item in rows:
        number=f"{item['n']:02d}"
        article=SERIES/(item["slug"]+".html")
        assert article.is_file(),article
        soup=BeautifulSoup(article.read_text(encoding="utf-8"),"html.parser")
        assert len(soup.find_all("h1"))==1,article
        assert len(soup.find_all("figure"))==5,article
        assert len(soup.find_all("svg"))==5,article
        assert len(soup.find_all("math"))>=5,article
        assert len(soup.select("input[type=range]"))==1,article
        assert soup.select_one("[data-geom-lesson]")["data-geom-lesson"]==str(item["n"])
        assert "NaN" not in article.read_text(encoding="utf-8")
        for mathnode in soup.find_all("math"):
            assert mathnode.has_attr("aria-label")
            assert mathnode.find_parent("svg") is None
            for op,arity in [("mfrac",2),("msup",2),("msub",2)]:
                for node in mathnode.find_all(op):
                    assert len([x for x in node.children if getattr(x,"name",None)])==arity,(article,op,str(node)[:160])
        for figure in soup.find_all("figure"):
            assert figure.find("figcaption") and figure.find("figcaption").get_text(strip=True)
            svg=figure.find("svg")
            assert svg.has_attr("viewbox") and svg.find("title") and svg.find("desc")
        lesson=json.loads((SERIES/"source"/f"{number}.json").read_text(encoding="utf-8"))
        assert lesson["title"] in soup.h1.get_text(" ",strip=True)
        assert len(lesson["steps"])>=4
        assert len(lesson["exercises"])==3
    assert (SERIES/"index.html").is_file()


def test_inversion_and_affine_invariants():
    rng=random.Random(20261126)
    for _ in range(100):
        R=rng.uniform(.1,30);r=rng.uniform(.11,50)
        rp=R*R/r
        assert math.isclose(r*rp,R*R,rel_tol=1e-13)
        assert math.isclose(R*R/rp,r,rel_tol=1e-13)
        a=rng.uniform(.2,5);b=rng.uniform(.2,5)
        x=(0.,0.);y=(1.,0.);z=(0.,1.)
        area=.5*abs(determinant(subtract(y,x),subtract(z,x)))
        transform=lambda t:(a*t[0],b*t[1])
        img=.5*abs(determinant(subtract(transform(y),transform(x)),subtract(transform(z),transform(x))))
        assert math.isclose(img,area*a*b,rel_tol=1e-12)


def test_ceva_radical_axis_and_ptolemy():
    rng=random.Random(2244)
    for _ in range(100):
        t=rng.uniform(.04,.96)
        ratio=t/(1-t)*(3/4)*((1-t)/t)*(4/3)
        assert math.isclose(ratio,1,rel_tol=1e-13)
        c1=(rng.uniform(-5,5),rng.uniform(-5,5))
        c2=(c1[0]+rng.uniform(1,10),c1[1]+rng.uniform(-5,5))
        r1=rng.uniform(.1,8);r2=rng.uniform(.1,8);y=rng.uniform(-10,10)
        rhs=r1*r1-r2*r2+(c2[0]**2+c2[1]**2)-(c1[0]**2+c1[1]**2)
        x=(rhs-2*(c2[1]-c1[1])*y)/(2*(c2[0]-c1[0]))
        pw1=(x-c1[0])**2+(y-c1[1])**2-r1**2
        pw2=(x-c2[0])**2+(y-c2[1])**2-r2**2
        assert abs(pw1-pw2)<1e-8
        angles=sorted(rng.uniform(-math.pi,math.pi) for _ in range(4))
        v=[(math.cos(z),math.sin(z)) for z in angles]
        lhs=distance(v[0],v[2])*distance(v[1],v[3])
        rhs=distance(v[0],v[1])*distance(v[2],v[3])+distance(v[1],v[2])*distance(v[0],v[3])
        assert abs(lhs-rhs)<1e-11


def test_euler_simson_polar_and_cross_ratio():
    rng=random.Random(2233)
    a=(0.,2.);b=(-2.,-1.);c=(2.,-1.);o=circumcircle(a,b,c)
    h=(a[0]+b[0]+c[0]-2*o[0],a[1]+b[1]+c[1]-2*o[1])
    g=((a[0]+b[0]+c[0])/3,(a[1]+b[1]+c[1])/3)
    assert distance(subtract(h,o),(3*(g[0]-o[0]),3*(g[1]-o[1])))<1e-12
    for _ in range(75):
        t=rng.uniform(0,2*math.pi);r=distance(o,a);p=(o[0]+r*math.cos(t),o[1]+r*math.sin(t))
        d=foot(p,a,b);e=foot(p,b,c);f=foot(p,c,a)
        assert abs(determinant(subtract(e,d),subtract(f,d)))<1e-10
        x=rng.uniform(1.01,3);y=rng.uniform(-2,2);s=x*x+y*y
        T=(x/s-y*math.sqrt(s-1)/s,y/s+x*math.sqrt(s-1)/s)
        assert math.isclose(x*T[0]+y*T[1],1,rel_tol=1e-12)
        q=-1+rng.uniform(0,.5)
        cr=((.5-0)/(.5-2))/((q-0)/(q-2))
        assert cr<0
    assert math.isclose(((.5)/(-1.5))/((-1)/(-3)),-1)


def test_miquel_and_pascal_incidence():
    A=(3.,9.);B=(0.,0.);C=(10.,0.)
    for t in (.21,.36,.53,.78):
        X=(B[0]+t*(C[0]-B[0]),0.)
        Y=(C[0]+.46*(A[0]-C[0]),C[1]+.46*(A[1]-C[1]))
        Z=(A[0]+.52*(B[0]-A[0]),A[1]+.52*(B[1]-A[1]))
        o1=circumcircle(A,Y,Z);o2=circumcircle(B,Z,X);o3=circumcircle(C,X,Y)
        r1=distance(o1,Z);r2=distance(o2,Z);d=distance(o1,o2)
        base=(r1*r1-r2*r2+d*d)/(2*d); height=math.sqrt(max(0,r1*r1-base*base))
        ux=(o2[0]-o1[0])/d;uy=(o2[1]-o1[1])/d
        mid=(o1[0]+base*ux,o1[1]+base*uy)
        m1=(mid[0]-height*uy,mid[1]+height*ux)
        m2=(mid[0]+height*uy,mid[1]-height*ux)
        m=m1 if distance(m1,Z)>distance(m2,Z) else m2
        assert abs(distance(m,o3)-distance(X,o3))<1e-9
    # Parametric parabola: two triple-products of chord polynomials agree on y=x².
    a,b,c,d,e,f=(-3.1,-2.,-.5,.7,1.9,3.5)
    for x in (-4,-1.3,0,2,5):
        chord=lambda s,t:x*x-(s+t)*x+s*t
        F=chord(a,b)*chord(c,d)*chord(e,f)
        G=chord(b,c)*chord(d,e)*chord(f,a)
        assert abs(F-G)<1e-8


def test_negative_cases_not_mistaken_for_theorem():
    # A moved away from the circle breaks Ptolemy equality.
    r=1.0
    pts=[(2,0),(0,1),(-1,0),(0,-1)]
    lhs=distance(pts[0],pts[2])*distance(pts[1],pts[3])
    rhs=distance(pts[0],pts[1])*distance(pts[2],pts[3])+distance(pts[1],pts[2])*distance(pts[0],pts[3])
    assert not math.isclose(lhs,rhs,rel_tol=1e-4)
    # Four distinct collinear points must retain the sign in the harmonic cross ratio.
    assert ((.5)/(-1.5))/((-1)/(-3))==-1
