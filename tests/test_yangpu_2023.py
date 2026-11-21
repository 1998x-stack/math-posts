"""Source and algebra regression checks for the first five 2023 Yangpu mock questions."""
import cmath
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAM = "2023-shanghai-yangpu-first-mock"

def test_yangpu_first_five_are_registered_and_source_checked():
    posts = json.loads((ROOT / "content/posts.json").read_text("utf-8"))
    batch = [p for p in posts if p.get("source_exam") == EXAM and 1 <= p["question_number"] <= 5]
    assert [p["question_number"] for p in batch] == [1, 2, 3, 4, 5]
    assert all(p["category"] == "fill-in" and p["status"] == "published" for p in batch)
    assert all(p["source_pages"] == [1] for p in batch)
    for p, answer in zip(batch, ["真", "[0,1]", "6", "π/6 或 5π/6", "2"]):
        base = ROOT / "posts" / p["category"] / p["slug"]
        html = (base / "index.html").read_text("utf-8")
        svg = (base / "assets/cover.svg").read_text("utf-8")
        evidence = json.loads((base / "evidence.json").read_text("utf-8"))
        assert html.index('id="overview"') < html.index('id="question"')
        assert html.count('class="step-note"') >= 3
        assert '<math display="block"' in html and 'data-math-scroll' in html
        assert "<svg" in html and "<title" in svg and "<desc" in svg
        assert evidence["source"]["pages"] == [1]
        assert evidence["source"]["answer_pages"] == [8]
        assert evidence["answer"]["official"] == answer
        assert evidence["answer"]["independent_check"]

def test_yangpu_five_math_results():
    for a, b in [(3, 1), (0, -2), (-1, -3), (1.5, -2.5)]:
        assert a > b
        assert (a - b) * (a*a + a*b + b*b) == a**3 - b**3
        assert a**3 > b**3
    assert [x for x in range(-3, 4) if 0 <= x <= 2 and x - 1 <= 0] == [0, 1]
    assert (36 - 4*6 - 5) == 6 + 1 == 7
    assert math.isclose(math.sin(math.pi/6), .5)
    assert math.isclose(math.sin(5*math.pi/6), .5)
    z = 2j * (1 - 1j)
    assert z == 2 + 2j and z.imag == 2

def test_yangpu_second_five_are_registered_and_source_checked():
    posts = json.loads((ROOT / "content/posts.json").read_text("utf-8"))
    batch = [p for p in posts if p.get("source_exam") == EXAM and 6 <= p["question_number"] <= 10]
    assert [p["question_number"] for p in batch] == [6, 7, 8, 9, 10]
    assert all(p["category"] == "fill-in" and p["status"] == "published" for p in batch)
    assert all(p["source_pages"] == [1] for p in batch)
    answers = ["(3,0)", "12", "5/3 或 5/4", "4+2√3", "3⁵（即 243）"]
    for p, answer in zip(batch, answers):
        base = ROOT / "posts" / p["category"] / p["slug"]
        html = (base / "index.html").read_text("utf-8")
        svg = (base / "assets/cover.svg").read_text("utf-8")
        evidence = json.loads((base / "evidence.json").read_text("utf-8"))
        assert html.index('id="overview"') < html.index('id="question"')
        assert html.count('class="step-note"') >= 4
        assert '<math display="block"' in html and 'data-math-scroll' in html
        assert "<svg" in html and "<title" in svg and "<desc" in svg
        assert evidence["source"]["pages"] == [1]
        assert evidence["source"]["answer_pages"] == [8]
        assert evidence["answer"]["official"] == answer
        assert evidence["answer"]["independent_check"]
        assert evidence["qa"]["browser_visual_test"] == "not verified"


def test_yangpu_second_five_math_results():
    # Q06: scalar component 3, projection vector (3,0); residual orthogonal.
    a, b = (3, 4), (1, 0)
    dot = a[0]*b[0] + a[1]*b[1]
    norm_sq = b[0]**2 + b[1]**2
    projection = (dot/norm_sq*b[0], dot/norm_sq*b[1])
    assert projection == (3, 0)
    assert (a[0]-projection[0])*b[0] + (a[1]-projection[1])*b[1] == 0

    # Q07: proportional allocation 48:36 -> 12:9.
    male_sample = 21*48/(48+36)
    assert male_sample == 12 and 21-male_sample == 9

    # Q08: same asymptote slopes, two choices of real axis.
    assert math.isclose(math.hypot(4, 3)/4, 5/4)
    assert math.isclose(math.hypot(3, 4)/3, 5/3)

    # Q09: variable reduction and equality case.
    r = math.sqrt(3)
    x, y = 3+r, 1+r
    assert math.isclose(x+3*y, x*y)
    assert math.isclose(x+y, 4+2*r)
    for t in [0.25, 0.5, 1, 2, 3, 4, 10]:
        assert 4+t+3/t >= 4+2*r-1e-12

    # Q10: n=5 from adjacent binomial coefficients; coefficients sum to 243.
    n = next(k for k in range(3, 40) if math.comb(k, 2) == math.comb(k, 3))
    assert n == 5
    coefficients = [math.comb(n, k)*2**k for k in range(n+1)]
    assert coefficients == [1, 10, 40, 80, 80, 32]
    assert sum(coefficients) == 3**5 == 243
