"""Independent mathematical and source-provenance regression tests for derivative PDF Q11–Q15."""
import json
import math
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
SRC="derivatives-application-classics-2024-2025"

def bisect(fun,lo,hi):
    flo=fun(lo)
    assert flo*fun(hi)<0
    for _ in range(90):
        mid=(lo+hi)/2
        fm=fun(mid)
        if flo*fm<=0:
            hi=mid
        else:
            lo=mid
            flo=fm
    return (lo+hi)/2

def test_q11_q15_source_pages_mathml_svg_and_evidence():
    posts=json.loads((ROOT/"content/posts.json").read_text("utf-8"))
    batch=[p for p in posts if p.get("source_exam")==SRC and 11<=p["question_number"]<=15]
    assert [p["question_number"] for p in batch]==[11,12,13,14,15]
    assert [p["source_pages"] for p in batch]==[[15],[15,16,17,18],[18,19],[19,20],[21,22]]
    for p in batch:
        base=ROOT/"posts"/p["category"]/p["slug"]
        html=(base/"index.html").read_text("utf-8")
        svg=(base/"assets/cover.svg").read_text("utf-8")
        ev=json.loads((base/"evidence.json").read_text("utf-8"))
        assert html.index('id="overview"')<html.index('id="question"')<html.index('id="solution"')
        assert html.count('class="step-note"')>=5
        assert html.count("<math")>=4
        assert 'aria-label="' in html and "<svg" in html
        root=ET.fromstring(svg)
        assert root.tag.endswith("svg") and root.attrib.get("viewBox")
        assert root.find("{http://www.w3.org/2000/svg}title") is not None
        assert root.find("{http://www.w3.org/2000/svg}desc") is not None
        assert ev["source"]["pages"]==p["source_pages"]
        assert ev["qa"]["source_checked"] is True
        assert ev["answer"]["independent_check"]

def test_source_pdf_registry_is_verified_without_public_url():
    docs=json.loads((ROOT/"content/source_documents.json").read_text("utf-8"))["documents"]
    source=next(d for d in docs if d["id"]=="derivative-classics-collection-source")
    assert source["page_count"]==62
    assert source["checksum_sha256"]=="375c40bcb5f176576841cad38f1d520350ab17bf6d831e4508d480fdab188e9c"
    assert source["access"]=="user-uploaded" and source["public_url"] is None

def test_q11_unique_peak_and_parameter():
    a=-2/math.e
    xstar=-1/(2*a)
    f=lambda x:math.sqrt(x)*math.exp(a*x)
    assert abs(xstar-math.e/4)<1e-12
    assert abs(f(xstar)-.5)<1e-12
    assert all((1+2*a*x)>0 for x in (.05,.2,.5))
    assert all((1+2*a*x)<0 for x in (1,2,5))

def test_q12_no_extremum_threshold_and_second_parameter_bound():
    e=math.e
    g=lambda a,x:math.exp(x)+2*a*x
    assert abs(g(-e/2,1))<1e-12
    assert all(g(-e/2,-4+i*.01)>=-1e-10 for i in range(801))
    assert g(1,-.5)<0<g(1,0)
    assert g(-2,0)>0 and g(-2,1)<0 and g(-2,3)>0
    astar=(7-e*e)/4
    phi=lambda a,x:math.exp(-x)*(.5*x**3-a*x*x+x+1)-1
    assert abs(phi(astar,2))<1e-12
    assert phi(astar-.001,2)>0
    for a in (astar,0,.5,1,3):
        assert max(phi(a,i*.02) for i in range(2501))<=1e-10

def test_q13_log_base_split_and_unique_parameter():
    f=lambda a,x:math.log(x)/(math.log(a)*x**a)
    assert abs(f(1/math.e,math.exp(math.e))+1)<1e-12
    assert f(.5,math.exp(2))<-1
    assert f(2,1e-8)<-1

def test_q14_endpoint_vs_interior_global_minimum():
    h=lambda x:(x*math.log(x)-x*x+x)/math.exp(x)
    phi=lambda x:math.log(x)-x+2
    x0=bisect(phi,3,4)
    assert abs(x0-3.1461932206205826)<1e-10
    assert abs(h(x0)+1/math.e**2)<1e-12
    assert h(1/math.e)>h(x0)
    assert (-1/math.e**2+.001)>h(x0)

def test_q15_even_minimum_and_cosine_sum_telescoping_bound():
    f=lambda x:x*x/math.pi+math.cos(x)-1
    assert abs(f(math.pi/2)-(math.pi/4-1))<1e-12
    assert abs(f(-math.pi/2)-f(math.pi/2))<1e-12
    for a in (.5,.75,1,2):
        assert min(a*x*x+math.cos(x)-1 for x in [i*.05 for i in range(-400,401)])>=-1e-10
    for n in (2,3,5,10,30,80):
        assert sum(math.cos(1/k) for k in range(2,n+1))>n-4/3
        for k in range(2,n+1):
            bound=1/(2*k-1)-1/(2*k+1)
            assert 1-math.cos(1/k)<bound
