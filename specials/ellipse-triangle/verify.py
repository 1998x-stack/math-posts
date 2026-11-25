from pathlib import Path
from bs4 import BeautifulSoup
from xml.etree import ElementTree as ET
from math import sin,cos,pi,sqrt,isclose
from random import Random
import json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parent; D=R/'qa';D.mkdir(exist_ok=True)
report={'math':{},'articles':{}};rng=Random(20261124);maximum=3*sqrt(3)/4
def det(p,q):return p[0]*q[1]-p[1]*q[0]
def dot(p,q):return sum(x*y for x,y in zip(p,q))
def area(P):return abs(sum(det(p,q) for p,q in zip(P,P[1:]+P[:1])))/2
def close(x,y):assert isclose(x,y,rel_tol=1e-9,abs_tol=1e-9),(x,y)
for i in range(1000):
 a=rng.uniform(1,10);b=rng.uniform(.1,a);theta=rng.uniform(0,2*pi);ang=sorted(rng.uniform(0,2*pi) for _ in range(3));P=[(cos(t),sin(t)) for t in ang];Q=[(a*x,b*y) for x,y in P];s=area(P);close(area(Q),a*b*s);assert s<=maximum+1e-9
 x=(ang[1]-ang[0])/2;y=(ang[2]-ang[1])/2;z=pi-x-y;close(s,2*sin(x)*sin(y)*sin(z));assert sin(x)*sin(y)<=cos(z/2)**2+1e-9
 u=[p[0] for p in P];v=[p[1] for p in P];w=[v[1]-v[2],v[2]-v[0],v[0]-v[1]];X=dot(u,u);Y=dot(v,v);close(X+Y,3);close(dot(w,w),3*Y-sum(v)**2);close(2*s,abs(dot(u,w)));assert 4*s*s<=3*X*Y+1e-9
 t=rng.uniform(.1,2);M=[(*p,t) for p in P];d=M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1])-M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0])+M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0]);close(abs(d),2*t*s);assert s<=(1+t*t)**1.5/(2*t)+1e-9
 k=rng.uniform(-5,5);D0=b*b+a*a*k*k;t=rng.uniform(0,.99);m=t*sqrt(D0);dx=2*a*b*sqrt(D0-m*m)/D0;cen=-a*a*k*m/D0;x1=cen-dx/2;x2=cen+dx/2;A=(x1,k*x1+m);B=(x2,k*x2+m);C=(a*a*k/sqrt(D0),-b*b/sqrt(D0));close(x1+x2,-2*a*a*k*m/D0);close(x1*x2,a*a*(m*m-b*b)/D0);close(area([A,B,C]),a*b*(1+t)*sqrt(1-t*t))
 for p in [A,B,C]:close((p[0]/a)**2+(p[1]/b)**2,1)
 p=(a*cos(theta),b*sin(theta));q=(-a*sin(theta),b*cos(theta));close(det(p,q),a*b);s0=sqrt(1-t*t);A=tuple(t*x+s0*y for x,y in zip(p,q));B=tuple(t*x-s0*y for x,y in zip(p,q));C=tuple(-x for x in p);close(area([A,B,C]),a*b*(1+t)*s0)
 P=[(cos(theta+2*pi*j/3),sin(theta+2*pi*j/3)) for j in range(3)];close(area(P),maximum)
 for j in range(3):
  close(dot(P[j],tuple(x-y for x,y in zip(P[(j+1)%3],P[(j+2)%3]))),0);close(dot((*P[j],sqrt(.5)),(*P[(j+1)%3],sqrt(.5))),0)
 for j in range(2):close(sum(p[j] for p in P),0)
report['math']={'status':'passed','random_trials':1000,'seed':20261124,'scope':'七种证明的面积恒等式、上界、取等条件'}
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 for file in sorted(R.glob('0*.html')):
  soup=BeautifulSoup(file.read_text(),'html.parser');assert len(soup.find_all('h1'))==1 and soup.main and soup.article and soup.nav
  ids=[e['id'] for e in soup.select('[id]')];assert len(ids)==len(set(ids))
  for a in soup.select('a[href]'):
   href=a['href'];assert (href[1:] in ids if href.startswith('#') else (R/href).exists()),href
  for fig in soup.find_all('figure'):assert fig.svg and fig.figcaption and fig.svg.title and fig.svg.desc
  for math in soup.find_all('math'):
   assert math.get('aria-label') and not math.find_parent('svg') and math.find_parent(class_='math-scroll')['tabindex']=='0'
   for tag,n in [('mfrac',2),('msub',2),('msup',2),('msubsup',3),('munder',2),('munderover',3)]:assert all(len(x.find_all(recursive=False))==n for x in math.find_all(tag)),tag
  entry={'static':'passed','figures':len(soup.find_all('figure')),'mathml':len(soup.find_all('math')),'viewports':{},'interaction':{},'svg_standalone':{}};report['articles'][file.name]=entry
  page=browser.new_page();errors=[];network=[];page.on('pageerror',lambda e:errors.append(str(e)));page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None);page.route('http**/*',lambda r:(network.append(r.request.url),r.abort()))
  for w,h in [(1440,900),(768,1024),(390,844),(360,800)]:
   page.set_viewport_size({'width':w,'height':h});page.set_content(file.read_text());page.screenshot(path=str(D/f'{file.stem}-{w}.png'))
   measure=page.evaluate('''()=>({width:document.documentElement.scrollWidth,mathBad:[...document.querySelectorAll('math')].filter(e=>e.namespaceURI!=='http://www.w3.org/1998/Math/MathML'||e.getBoundingClientRect().height<4).length,badFractions:[...document.querySelectorAll('mfrac')].filter(e=>!(e.children[0].getBoundingClientRect().top<e.children[1].getBoundingClientRect().top)).length,blankSVG:[...document.querySelectorAll('svg')].filter(e=>e.getBoundingClientRect().height<1).length,clipped:[...document.querySelectorAll('svg')].flatMap((s,i)=>[...s.querySelectorAll('text')].map(t=>({figure:i+1,text:t.textContent,b:t.getBBox()})).filter(x=>x.b.x<-.5||x.b.y<-.5||x.b.x+x.b.width>520.5||x.b.y+x.b.height>284.5).map(x=>({figure:x.figure,text:x.text})))})''')
   before=page.locator('#demo-status').inner_text();page.locator('#reset').click();after=page.locator('#demo-status').inner_text();ratio=float(page.locator('#ratio').inner_text());assert abs(ratio-maximum)<1e-4,(file,w,ratio);assert before!=after
   old=page.locator('#vval').inner_text();page.locator('#variation').focus();page.keyboard.press('ArrowRight');assert page.locator('#vval').inner_text()!=old
   if w==1440:
    entry['interaction']={'reset_ratio':ratio,'keyboard':'passed'};page.locator('#experiment figure').screenshot(path=str(D/f'{file.stem}-experiment.png'));page.emulate_media(media='print');page.screenshot(path=str(D/f'{file.stem}-print.png'));page.emulate_media(media='screen')
   measure.update(errors=list(errors),network=list(network),pass_=measure['width']<=w+1 and not any(measure[k] for k in ['mathBad','badFractions','blankSVG']) and not errors and not network);entry['viewports'][str(w)]=measure
  for svg in sorted((R/'svg'/file.stem).glob('*.svg')):
   ET.parse(svg);page.set_content(svg.read_text());ok=page.evaluate('''()=>{let s=document.querySelector('svg');return s.localName==='svg'&&s.getBBox().width>0&&s.getBBox().height>0}''');entry['svg_standalone'][svg.name]=ok
  page.close();print(file.name,entry['viewports']['360'],flush=True)
 browser.close()
(R/'qa-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print('ALL',all(v['pass_'] for e in report['articles'].values() for v in e['viewports'].values()))
