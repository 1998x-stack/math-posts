"""Structural MathML validation and exact elementary-number-theory assertions."""
from pathlib import Path
from bs4 import BeautifulSoup
import math,random,json
ROOT=Path(__file__).resolve().parents[1]/'specials'/'number-theory'

def test_pages():
 rows=json.loads((ROOT/'evidence.json').read_text(encoding='utf-8'))['chapters']
 assert len(rows)==12
 assert len(list(ROOT.glob('[0-9][0-9]-*.html')))==12
 for row in rows:
  page=ROOT/(row['slug']+'.html')
  soup=BeautifulSoup(page.read_text(encoding='utf-8'),'html.parser')
  assert len(soup.find_all('h1'))==1 and soup.find('main')
  assert len(soup.find_all('math'))==6
  assert len(soup.find_all('svg'))==4
  assert len(soup.select('.proof-step'))==4
  assert len(soup.select('.exercise'))==3
  assert len(soup.select('.stage-grid figure'))==3
  assert len(soup.select('input[type=range]'))==1
  assert (ROOT/'svg'/(row['slug']+'.svg')).exists()
  for m in soup.find_all('math'):
   assert m.get('aria-label') and m.find_parent('svg') is None
   for tag in ('mfrac','msup','msub'):
    for part in m.find_all(tag):
     assert len(part.find_all(recursive=False))==2,(page,tag)
  for svg in soup.find_all('svg'):
   assert svg.find('title') and svg.find('desc') and svg.get('viewbox')

def test_arithmetic():
 rng=random.Random(20261126)
 for _ in range(500):
  a,b=rng.randrange(1,100000),rng.randrange(1,100000)
  assert math.gcd(a,b)==math.gcd(b,a%b)
  r0,r1=a,b;x0,x1=1,0;y0,y1=0,1
  while r1:
   q=r0//r1;r0,r1=r1,r0-q*r1;x0,x1=x1,x0-q*x1;y0,y1=y1,y0-q*y1
  assert r0==math.gcd(a,b)==a*x0+b*y0
 for x in range(3):
  for y in range(5):assert len([n for n in range(15) if n%3==x and n%5==y])==1
 for n in range(2,35):
  u=[k for k in range(1,n+1) if math.gcd(k,n)==1]
  for a in u:assert pow(a,len(u),n)==1
 for p in (5,7,11,13,17,19,23):
  squares={x*x%p for x in range(1,p)}
  assert len(squares)==(p-1)//2
  if p%4==3:assert p-1 not in squares
 assert pow(3,13,17)==12
 assert sum(all(n%d for d in range(2,math.isqrt(n)+1)) for n in range(2,101))==25
