"""Source and algebra regression checks for the first five 2023 Yangpu mock questions."""
import cmath
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAM = "2023-shanghai-yangpu-first-mock"

def test_yangpu_first_five_are_registered_and_source_checked():
    posts = json.loads((ROOT / "content/posts.json").read_text("utf-8"))
    batch = [p for p in posts if p.get("source_exam") == EXAM]
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
