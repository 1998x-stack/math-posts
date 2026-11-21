"""Cross-file coverage and selected independent math invariants."""
import json,math,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def manifest():return json.loads((ROOT/'content/posts.json').read_text('utf-8'))
def test_original_21_problems_and_exam_types():
    posts=manifest()
    # Keep Jianping coverage fixed while allowing independently sourced new exams.
    original=[p for p in posts if p['slug'].startswith('jianping-2021-q')]
    assert len(original)==21
    assert len(posts)>=52
    assert sorted(x['question_number'] for x in original)==list(range(1,22))
    counts={}
    for p in original:counts[p['category']]=counts.get(p['category'],0)+1
    assert counts=={'fill-in':12,'multiple-choice':4,'worked-solutions':5}


def test_2024_geometry_first_five_are_registered_and_evidenced():
    posts=manifest()
    batch=[p for p in posts if p.get('source_exam')=='2024-shanghai-gaosan-second-mock-analytic-geometry']
    batch=[p for p in batch if p['source_pages'][0] <= 6]
    assert len(batch)==5
    assert [p['source_region'] for p in batch]==['浦东新区','嘉定区','长宁区','闵行区','虹口区']
    assert [p['source_pages'] for p in batch]==[[2],[3],[4],[5],[6]]
    for p in batch:
        assert p['question_number']==20 and p['category']=='worked-solutions'
        evidence=json.loads((ROOT/'posts'/p['category']/p['slug']/'evidence.json').read_text('utf-8'))
        assert evidence['source']['region']==p['source_region']
        assert evidence['source']['pages']==p['source_pages']
        assert evidence['answer']['official']=='原卷未提供官方答案或解析。'
        assert evidence['answer']['independent_check']

def test_2024_geometry_second_five_are_registered_and_evidenced():
    posts=manifest()
    batch=[p for p in posts if p.get('source_exam')=='2024-shanghai-gaosan-second-mock-analytic-geometry' and 7 <= p['source_pages'][0] <= 11]
    assert len(batch)==5
    assert [p['source_region'] for p in batch]==['静安区','普陀区','徐汇区','宝山区','松江区']
    assert [p['source_pages'] for p in batch]==[[7],[8],[9],[10],[11]]
    for p in batch:
        assert p['question_number']==20 and p['category']=='worked-solutions'
        article=ROOT/'posts'/p['category']/p['slug']
        html=(article/'index.html').read_text('utf-8')
        assert '<math' in html and '先理解题目在问什么' in html
        evidence=json.loads((article/'evidence.json').read_text('utf-8'))
        assert evidence['source']['region']==p['source_region']
        assert evidence['source']['pages']==p['source_pages']
        assert evidence['answer']['official']=='原卷未提供官方答案或解析。'
        assert evidence['answer']['independent_check']
    jingan=json.loads((ROOT/'posts/worked-solutions/shanghai-2024-geometry-jingan-q20/evidence.json').read_text('utf-8'))
    assert '开放式设计题' in jingan['editorial_note']

def test_original_svg_cover_and_source():
    captions=set()
    for p in manifest():
        article=ROOT/'posts'/p['category']/p['slug']
        assert (article/'index.html').exists()
        assert (article/p['cover']['src']).exists()
        svg=(article/p['cover']['src']).read_text('utf-8')
        assert '<svg' in svg and 'viewBox' in svg and '<title' in svg
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


def test_2024_geometry_final_six_and_source_caveat():
    posts=manifest()
    part=[p for p in posts if p.get('source_exam')=='2024-shanghai-gaosan-second-mock-analytic-geometry' and p['source_pages'][0]>=12]
    assert len(part)==6
    assert [p['source_region'] for p in part]==['青浦区','金山区','崇明区','黄浦区','杨浦区','奉贤区']
    assert [p['source_pages'] for p in part]==[[12],[13],[14],[15],[16],[17]]
    assert [p['status'] for p in part]==['published']*5+['draft']
    for p in part:
        art=ROOT/'posts'/p['category']/p['slug']
        html=(art/'index.html').read_text('utf-8')
        svg=(art/'assets/cover.svg').read_text('utf-8')
        ev=json.loads((art/'evidence.json').read_text('utf-8'))
        assert '先理解题目在问什么' in html and '<math' in html and '<svg' in html
        assert 'viewBox' in svg and '<title>' in svg and '<desc>' in svg
        assert ev['source']['pages']==p['source_pages']
        assert ev['answer']['official']=='原卷未提供官方答案或解析。'
    fx=part[-1]
    evidence=json.loads((ROOT/'posts'/fx['category']/fx['slug']/'evidence.json').read_text('utf-8'))
    assert '竖直' in evidence['editorial_note']
    assert 'draft'==fx['status']

def test_geometry_independent_invariants():
    import math
    assert math.isclose((29+25+6)/2,30)
    assert math.isclose((3*20)/30,2)
    assert math.isclose(1/(2*math.sqrt(2)), math.sqrt(2)/4)
    assert math.isclose((math.sqrt(5)/2)**2,1.25)
    assert math.isclose((16*(1+1/3)/(4+5/3))**(-1) + (16*(1+3)/(4+15))**(-1),9/16)
    assert math.isclose((1+4*(1/4))/(4*(1/4)),2)
    assert math.isclose(10/91,10/91) and (10/91)!=(-10/139)

def test_week12_photographed_first_ten_are_complete_and_evidenced():
    problems=[p for p in manifest() if p.get('source_exam')=='week12-gaosan-classroom-practice' and p['question_number']<=10]
    assert [p['question_number'] for p in problems]==list(range(1,11))
    assert all(p['category']=='fill-in' and p['status']=='published' and p['source_pages']==[1] for p in problems)
    for p in problems:
        article=ROOT/'posts'/p['category']/p['slug']
        html=(article/'index.html').read_text('utf-8')
        svg=(article/'assets/cover.svg').read_text('utf-8')
        evidence=json.loads((article/'evidence.json').read_text('utf-8'))
        assert '<math display="block"' in html and 'data-math-scroll' in html
        assert html.index('id="overview"') < html.index('id="question"')
        assert '<svg' in html and '<title' in svg and '<desc' in svg
        assert evidence['source']['pages']==[1]
        assert '官方答案' in evidence['answer']['official']
    assert 1j*complex(2,-1)==complex(1,2)
    assert math.isclose(abs(complex(2,-1))**2,5,rel_tol=1e-12)
    assert [x for x in (-2,0,1) if 2*x*x+x-1<0]==[0]
    assert math.comb(6,2)*2**2==60
    assert (1+3)**2==1*(1+5*3)


def test_week12_q06_to_q10_math_and_source_traps():
    from collections import Counter
    batch=[p for p in manifest() if p.get('source_exam')=='week12-gaosan-classroom-practice' and 6 <= p['question_number'] <= 10]
    assert [p['question_number'] for p in batch]==[6,7,8,9,10]
    values=['√3π/3','−3','7','(0,4)','117']
    for p,value in zip(batch,values):
        base=ROOT/'posts'/'fill-in'/p['slug']
        html=(base/'index.html').read_text('utf-8')
        svg=(base/'assets/cover.svg').read_text('utf-8')
        ev=json.loads((base/'evidence.json').read_text('utf-8'))
        assert html.count('<math display="block"') >= 4
        assert html.count('data-math-scroll') >= 4
        assert html.count('class="step-note"') >= 4
        assert 'MathJax' not in html and 'katex.min.js' not in html
        assert '<title' in svg and '<desc' in svg and 'viewBox' in svg
        assert ev['answer']['independent_result']==value
        assert ev['transcription']['status']=='checked-against-uploaded-photo'
    assert math.isclose(math.sqrt(3)*math.pi/3,1.8137993642342176)
    assert (2**2-1)==3 and -(2**2-1)==-3
    roots=(3-math.sqrt(5),3+math.sqrt(5))
    assert math.isclose(roots[0]+roots[1],6) and math.isclose(roots[0]*roots[1],4)
    assert math.isclose(roots[1]/roots[0]+roots[0]/roots[1],7)
    xm,ym=16/5,12/5
    assert math.isclose((xm-4)**2+(ym-3)**2,1)
    assert math.isclose(xm*xm+ym*ym,16)
    assert math.isclose(((-4-xm)*(4-xm)+ym*ym),0,abs_tol=1e-12)
    def repeated_even(n):
        digits=Counter(str(n))
        return any(digits[str(v)]>=2 for v in (0,2,4,6,8))
    eligible=[n for n in range(100,1000) if repeated_even(n)]
    assert len(eligible)==117
    assert len([n for n in eligible if str(n).count('0')>=2])==9
    for v in ('2','4','6','8'):
        assert len([n for n in eligible if str(n).count(v)>=2])==27
    assert '相同偶数' in (ROOT/'posts/fill-in/week12-gaosan-q10/index.html').read_text('utf-8')


def test_2023_chongming_first_five_are_registered_and_mathematically_checked():
    posts=manifest()
    batch=[p for p in posts if p.get('source_exam')=='2023-shanghai-chongming-first-mock' and p['question_number']<=5]
    assert [p['question_number'] for p in batch]==[1,2,3,4,5]
    assert all(p['category']=='fill-in' and p['status']=='published' and p['source_pages']==[1] for p in batch)
    expected=['{2,3,4}','(−1/2,2)','6','2','−8']
    for p,answer in zip(batch,expected):
        path=ROOT/'posts'/p['category']/p['slug']
        html=(path/'index.html').read_text('utf-8')
        cover=(path/'assets/cover.svg').read_text('utf-8')
        evidence=json.loads((path/'evidence.json').read_text('utf-8'))
        assert evidence['source']['pages']==[1]
        assert evidence['source']['answer_pages']==[7]
        assert evidence['answer']['official']==answer
        assert evidence['answer']['independent_check']
        assert html.index('id="overview"')<html.index('id="question"')
        assert '<math display="block"' in html and 'data-math-scroll' in html
        assert '<svg' in html and '<title' in cover and '<desc' in cover
        assert html.count('class="step-note"')>=4
    assert (2+6j)*(3+1j)==20j
    assert [x for x in (-1,0,2,3) if x!=2 and (2*x+1)/(x-2)<0]==[0]
    first,ratio=1,-2
    assert first*(1+ratio)==-1
    assert first*(1-ratio**2)==-3
    assert first*ratio**3==-8

def test_songjiang_2023_first_ten_sequential_with_glyph_caveats():
    seq=[p for p in manifest() if p.get("source_exam")=="songjiang-2023-first-mock" and p["question_number"]<=10]
    assert [p["question_number"] for p in seq]==list(range(1,11))
    assert len(seq)==10
    assert [p["status"] for p in seq]==["published"]*7+["draft","draft","published"]
    for q,p in enumerate(seq,1):
        assert p["category"]=="fill-in" and p["source_pages"]==[1]
        assert p["reference_answer_pages"]==[7]
        article=ROOT/"posts"/p["category"]/p["slug"]
        html=(article/"index.html").read_text("utf-8")
        svg=(article/"assets/cover.svg").read_text("utf-8")
        ledger=json.loads((article/"evidence.json").read_text("utf-8"))
        assert html.index('id="overview"')<html.index('id="question"')
        assert '先理解题目在问什么' in html and 'data-math-scroll' in html
        assert '<math display="block"' in html
        assert '<svg' in html and '<title>' in svg and '<desc>' in svg
        assert ledger["source"]["question"]==q and ledger["source"]["answers_pages"]==[7]
        assert ledger["answer"]["official"]
        if q in (8,9):
            assert "operator-missing" in ledger["transcription"]["status"]
            assert "≥" in ledger["editorial_note"]
            assert not ledger["qa"]["source_checked"]
        else:
            assert ledger["qa"]["source_checked"]
    assert [p["question_number"] for p in seq if p["status"]=="draft"]==[8,9]

def test_songjiang_2023_math_invariants():
    import cmath
    assert [n for n in range(-3,3) if -2<n<=1]==[-1,0,1]
    assert all(abs(math.sin(t)*math.cos(t)-0.5*math.sin(2*t))<1e-12 for t in [-2,-0.2,0,1,2])
    assert (2+1j)**2==3+4j
    assert 2*(3*1+3*2)-3*(2*1+2)==6
    fun=lambda x:(2**x-1)/(2**x+1)
    assert all(math.isclose(fun(-x),-fun(x)) for x in (-3,-1,0,1,3))
    assert math.isclose(math.pi*4*5,20*math.pi)
    assert math.isclose((math.pi*4*4*3/3),16*math.pi)
    a,b=(5,3),(-1,2)
    assert a[0]*b[0]+a[1]*b[1]==1 and b[0]**2+b[1]**2==5
    assert math.isclose((a[0]+.2)*b[0]+(a[1]-.4)*b[1],0)
    assert math.isclose(abs(2-2)+abs(2-3),1)
    assert 2*(.5)**2+.5==1 and 2*(-1)**2-1==1
    assert 4<4.5<=5
    assert 3**2==1**2+8
    assert math.isclose(2*math.sqrt(2),math.sqrt(8))


def test_week12_q11_to_q15_faithful_categorization_and_math_invariants():
    import math
    all_posts=manifest()
    batch=[p for p in all_posts if p.get('source_exam')=='week12-gaosan-classroom-practice' and 11<=p['question_number']<=15]
    assert [p['question_number'] for p in batch]==[11,12,13,14,15]
    assert [p['category'] for p in batch]==['fill-in','fill-in','multiple-choice','multiple-choice','multiple-choice']
    assert [p['source_pages'] for p in batch]==[[1],[1],[1],[1],[2]]
    expected=['−1/2','[0,π/3]','D (y=−2)','D ((1/4)a)','B (0,∛2]']
    for item,answer in zip(batch,expected):
        article=ROOT/'posts'/item['category']/item['slug']
        html=(article/'index.html').read_text('utf-8')
        svg=(article/'assets/cover.svg').read_text('utf-8')
        ev=json.loads((article/'evidence.json').read_text('utf-8'))
        assert html.index('id="overview"') < html.index('id="question"')
        assert html.count('<math display="block"')>=5
        assert html.count('data-math-scroll')>=5
        assert html.count('class="step-note"')>=5
        assert '<svg' in html and 'viewBox' in svg and '<title' in svg and '<desc' in svg
        assert ev['source']['pages']==item['source_pages']
        assert ev['answer']['independent_result']==answer
        assert ev['transcription']['status']=='checked-against-uploaded-photo'
    b=(1.,0.);c=(-0.5,math.sqrt(3)/2)
    assert math.isclose(b[0]*c[0]+b[1]*c[1],-.5)
    av=(c[0]-b[0],c[1]-b[1])
    assert math.isclose(av[0]**2+av[1]**2,3)
    assert math.isclose(av[0]+2*b[0],b[0]+c[0])
    assert math.isclose(av[1]+2*b[1],b[1]+c[1])
    def first_is_max(phi):
        samples=[math.sin(k*math.pi/3+phi) for k in range(1,7)]
        return math.isclose(samples[0],max(samples),rel_tol=0,abs_tol=1e-10)
    for phi in [0,math.pi/12,math.pi/6,math.pi/3]:
        assert first_is_max(phi)
    for phi in [math.pi/2,math.pi,2*math.pi-0.1]:
        assert not first_is_max(phi)
    assert 4**2==8*2
    assert math.dist((4,2),(0,2))==abs(2-(-2))==4
    aa=(2.,0.);bb=(.5,math.sqrt(3)/2)
    dot=aa[0]*bb[0]+aa[1]*bb[1]
    projection=(dot/(aa[0]**2+aa[1]**2)*aa[0],dot/(aa[0]**2+aa[1]**2)*aa[1])
    assert math.isclose(dot,1) and math.isclose(projection[0],.5) and math.isclose(projection[1],0)
    threshold=2**(1/3)
    assert math.isclose(threshold**2,math.sqrt(2*threshold))
    assert 1 < math.sqrt(2)
    assert 1.5**2 > math.sqrt(3)
    assert (ROOT/'posts/multiple-choice/week12-gaosan-q15/index.html').exists()


def test_chongming_2023_next_five_visual_mathml_and_source_pages():
    batch=[p for p in manifest() if p.get('source_exam')=='2023-shanghai-chongming-first-mock' and 6<=p['question_number']<=10]
    assert [p['question_number'] for p in batch]==[6,7,8,9,10]
    assert all(p['category']=='fill-in' and p['status']=='published' for p in batch)
    expected=['−4','1/2','√3','y=2x−1','2']
    for item,official in zip(batch,expected):
        directory=ROOT/'posts'/item['category']/item['slug']
        html=(directory/'index.html').read_text('utf-8')
        svg=(directory/'assets/cover.svg').read_text('utf-8')
        record=json.loads((directory/'evidence.json').read_text('utf-8'))
        assert item['source_pages']==([1,2] if item['question_number']==10 else [1])
        assert record['source']['pages']==item['source_pages']
        assert record['source']['answer_pages']==[7]
        assert record['answer']['official']==official
        assert record['answer']['independent_check']
        assert html.index('id="overview"')<html.index('id="question"')
        assert '<math display="block"' in html and 'data-math-scroll' in html
        assert '<svg' in html and '<title' in svg and '<desc' in svg
        assert html.count('class="step-note"')>=4
    assert 16-(-4)**2==0
    assert (2*(-4)) != 8
    assert math.isclose(math.sin(math.pi/2 + math.pi/3),math.cos(math.pi/3))
    assert math.isclose((math.sqrt(3))**2+1,4)
    assert 1**2==(2*1-1)
    assert math.isclose(math.sin(2*math.pi/3-math.pi/6),1)
    assert min(2+6*n for n in range(-20,21) if 2+6*n>0)==2

def test_songjiang_second_ten_source_and_semantic_mathml():
    from bs4 import BeautifulSoup
    docs=sorted([p for p in manifest() if p.get("source_exam")=="songjiang-2023-first-mock" and p["question_number"]>=11],key=lambda p:p["question_number"])
    assert [p["question_number"] for p in docs]==list(range(11,21))
    assert [p["status"] for p in docs]==["published"]*5+["draft"]+["published"]*3+["draft"]
    assert [p["category"] for p in docs]==["fill-in"]*2+["multiple-choice"]*4+["worked-solutions"]*4
    assert [p["source_pages"] for p in docs]==[[2],[2],[2],[2],[2,3],[3],[3],[4],[4],[5]]
    for p in docs:
        root=ROOT/"posts"/p["category"]/p["slug"]
        html=(root/"index.html").read_text(encoding="utf-8")
        cover=(root/"assets/cover.svg").read_text(encoding="utf-8")
        evidence=json.loads((root/"evidence.json").read_text(encoding="utf-8"))
        assert html.index('id="overview"')<html.index('id="question"')
        assert '先理解题目在问什么' in html and html.count('class="step-note"')>=3
        assert '<math display="block"' in html and 'data-math-scroll' in html
        assert '<svg' in html and '<title' in cover and '<desc' in cover
        assert evidence["source"]["question"]==p["question_number"]
        assert evidence["source"]["answers_pages"]==[7]
        assert evidence["answer"]["official_source"]
        soup=BeautifulSoup(html,"html.parser")
        for frac in soup.select("math mfrac"):
            elements=[child for child in frac.children if getattr(child,"name",None)]
            assert len(elements)==2, f"Invalid MathML mfrac in {p['slug']}"
        assert '<mo>frac</mo>' not in html and '<mo>mathrm</mo>' not in html
        assert '<mo>text</mo>' not in html and '<mo>cdots</mo>' not in html
    source19=json.loads((ROOT/"posts/worked-solutions/songjiang-2023-mock-q19/evidence.json").read_text("utf-8"))
    assert "120" in source19["answer"]["official"] and "160" in source19["answer"]["independent_result"]
    q20=docs[-1]
    assert q20["status"]=="draft" and "未定义" in q20["subtitle"]
    issue=json.loads((ROOT/"posts/worked-solutions/songjiang-2023-mock-q20/evidence.json").read_text("utf-8"))
    assert "k" in issue["transcription"]["uncertainty"]

def test_songjiang_second_ten_independent_invariants():
    import math
    R=2*math.sqrt(3)/3
    r=math.sqrt(3)/3
    assert math.isclose(3*R*math.pi/6 + 3*r*math.pi/2,5*math.sqrt(3)*math.pi/6)
    a=[2/3]
    for n in range(1,12):a.append((1+math.sqrt(1+4*a[-1]))/2)
    assert all(a[j+1]>a[j] and a[j+1]<2 for j in range(11))
    for even in (2,4,6,10):
        total=sum((-1)**(n-1)/(a[n-1]-1) for n in range(1,even+1))
        assert math.isclose(total,-4.5-1/a[even-1],abs_tol=1e-12)
        assert -6<total<-5
    assert (-2)**3<1**3 and not((-2)**2<1**2)
    f=lambda x:(x*x-1)*math.exp(x)
    assert f(-1)==0 and f(1)==0 and f(0)==-1
    assert math.isclose(((-1.45)-(-26.7))*2/5,10.1)
    h=lambda x,k: abs(x+2)-k*x-1 if x<0 else x*x-(4+k)*x+1
    assert h(-2,-1)<0<h(-0.1,-1) and h(1,-1)<0<h(3,-1)
    assert math.isclose(math.sqrt(5)/3,math.cos(math.acos(math.sqrt(5)/3)))
    aa=2/math.sqrt(3);bb=2;cc=2*aa
    assert math.isclose(.5*aa*cc*math.sin(math.pi/3),2*math.sqrt(3)/3)
    assert math.isclose(aa+bb+cc,2*math.sqrt(3)+2)
    H=-40**3/800+6*40
    assert H==160 and math.sqrt(H*40)==80 and math.sqrt(H*40)+40==120
    CD=160-(80-20)**2/40
    EF=160+20**3/800-6*20
    assert CD==70 and EF==50 and 1.5*CD+EF==155
    assert math.isclose(10*(-7/4)+.5+17,0)
