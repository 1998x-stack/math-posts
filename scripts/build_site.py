#!/usr/bin/env python3
"""Reproducible, zero-dependency static build for math-posts GitHub Pages.

Author in posts/<category>/<slug>/index.html, register in content/posts.json,
and let Actions build a complete _site/ bundle. Never deploy drafts or tooling.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
from email.utils import format_datetime
from html import escape as H
import json
import os
from pathlib import Path
import re
import shutil
from urllib.parse import urlparse
from xml.sax.saxutils import escape as X
from xml.etree import ElementTree as ET

if __package__:
    from .related_posts import enrich_article_related, load_reading_paths
    from .atlas import load_atlas, build_papers_index, build_paper_detail
else:
    from related_posts import enrich_article_related, load_reading_paths
    from atlas import load_atlas, build_papers_index, build_paper_detail

ROOT=Path(__file__).resolve().parents[1]
DEFAULT_URL='https://1998x-stack.github.io/math-posts/'
VALID_SLUG=re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')


def data(root:Path):
    categories=json.loads((root/'content/categories.json').read_text(encoding='utf-8'))
    knowledge_map=json.loads((root/'content/knowledge-map.json').read_text(encoding='utf-8'))
    posts=json.loads((root/'content/posts.json').read_text(encoding='utf-8'))
    assert isinstance(categories,list) and isinstance(posts,list)
    ids=[c['slug'] for c in categories]
    assert len(set(ids))==len(ids) and all(VALID_SLUG.fullmatch(x) for x in ids), 'Bad category slug'
    category_topics={}
    for c in categories:
        assert all(isinstance(c.get(k),str) and c[k].strip() for k in ('title','english','description')),c
        assert isinstance(c.get('topics'),list) and c['topics'],f'Missing topics: {c["slug"]}'
        topic_ids=[]
        for t in c['topics']:
            assert isinstance(t,dict) and VALID_SLUG.fullmatch(t.get('slug','')),t
            assert isinstance(t.get('title'),str) and t['title'].strip(),t
            topic_ids.append(t['slug'])
        assert len(topic_ids)==len(set(topic_ids)),f'Duplicate topic ID in {c["slug"]}'
        category_topics[c['slug']]=set(topic_ids)
        assert (root/'posts'/c['slug']/'README.md').is_file(),f'Category README missing: {c["slug"]}'
    assert len({p['slug'] for p in posts})==len(posts), 'Duplicate post slug'
    for p in posts:
        assert VALID_SLUG.fullmatch(p['slug']), p
        assert p['category'] in ids, p
        assert p.get('topic') in category_topics[p['category']],f'Invalid primary topic for {p["slug"]}: {p.get("topic")}'
        assert p['status'] in {'draft','published'}, p
        assert re.fullmatch(r'\d{4}-\d{2}-\d{2}',p['published']),p
        datetime.fromisoformat(p['published'])
        assert p['title'] and p['summary'] and p['subtitle']
        assert isinstance(p.get('reading_minutes'),int) and p['reading_minutes']>=0,p
        assert isinstance(p.get('tags'),list) and all(isinstance(tag,str) and tag.strip() for tag in p['tags']),p
        if p['status']=='published':
            assert re.fullmatch(r'\d{4}-\d{2}-\d{2}',p.get('updated','')),f'Missing ISO updated date: {p["slug"]}'
            datetime.fromisoformat(p['updated'])
            assert p['updated']>=p['published'],f'Updated before published: {p["slug"]}'
            assert p['reading_minutes']>0,p
            assert isinstance(p.get('paper'),str) and urlparse(p['paper']).scheme=='https',p
            path=root/'posts'/p['category']/p['slug']/'index.html'
            assert path.is_file(),f'Article missing: {path}'
            # Covers are editorial decisions, never a generic visual fallback.
            cover=p.get('cover')
            assert isinstance(cover,dict),f'Missing curated cover for {p["slug"]}'
            assert re.fullmatch(r'assets/[a-zA-Z0-9][a-zA-Z0-9_.-]*\.svg',cover.get('src','')),f'Invalid SVG cover path: {p["slug"]}'
            assert isinstance(cover.get('caption'),str) and 8<=len(cover['caption'])<=80,f'Missing cover explanation: {p["slug"]}'
            assert 'observe' not in cover['caption'].lower() and 'derive' not in cover['caption'].lower(),f'Generic cover: {p["slug"]}'
            assert (path.parent/cover['src']).is_file(),f'Cover SVG missing: {p["slug"]}: {cover["src"]}'
    areas=knowledge_map.get('areas',[])
    assert len(areas)==7,'Knowledge map must contain seven subject domains'
    topic_ids=[t['id'] for a in areas for t in a.get('subtopics',[])]
    assert len(topic_ids)==len(set(topic_ids)),'Duplicate knowledge topic ID'
    topic_by_id={t['id']:t for a in areas for t in a.get('subtopics',[])}
    post_ids={p['slug'] for p in posts if p['status']=='published'}
    mapped=set()
    for topic in topic_by_id.values():
        assert 1 <= topic.get('difficulty',0) <= 5,topic
        assert topic.get('title') and topic.get('outcomes') and topic.get('tags'),topic
        assert all(x in topic_by_id for x in topic.get('prerequisites',[])),topic
        assert all(x in post_ids for x in topic.get('posts',[])),topic
        mapped.update(topic.get('posts',[]))
    assert mapped == post_ids, 'Every published post must map to at least one knowledge node'
    visiting=set();visited=set()
    def visit_topic(node):
        assert node not in visiting,'Knowledge prerequisite cycle: '+node
        if node in visited:return
        visiting.add(node)
        for parent in topic_by_id[node].get('prerequisites',[]):visit_topic(parent)
        visiting.remove(node);visited.add(node)
    for node in topic_ids:visit_topic(node)
    cover_captions=[p['cover']['caption'] for p in posts if p['status']=='published']
    assert len(cover_captions)==len(set(cover_captions)),'Published cover explanations must be unique'
    load_atlas(root,posts,knowledge_map)
    return categories,posts,knowledge_map


def url_join(base:str, path:str)->str:
    return base.rstrip('/')+'/'+path.lstrip('/')


def article_url(p):return f"posts/{p['category']}/{p['slug']}/"


def html_page(*,title,description,canonical,body,depth=0,active='home',lang='zh-CN',root_href=None):
    rel=root_href if root_href is not None else ('../'*depth or './')
    desc=H(description,quote=True)
    return f'''<!doctype html>
<html lang="{lang}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light"><meta name="theme-color" content="#f8f7f2">
<meta name="description" content="{desc}"><meta name="robots" content="index,follow">
<meta property="og:type" content="website"><meta property="og:title" content="{H(title,quote=True)}">
<meta property="og:description" content="{desc}"><meta property="og:url" content="{H(canonical,quote=True)}">
<meta name="twitter:card" content="summary"><link rel="canonical" href="{H(canonical,quote=True)}">
<link rel="alternate" type="application/rss+xml" title="math-posts RSS" href="{rel}feed.xml">
<link rel="icon" href="{rel}assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{rel}assets/site.css"><script src="{rel}assets/site.js" defer></script>
<title>{H(title)}</title></head><body>
<a class="skip-link" href="#main">跳至正文</a>
<header class="site-header"><div class="container header-row"><a class="wordmark" href="{rel}" aria-label="math.posts 首页">math<span>.</span>posts</a>
<button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav" data-menu-toggle><span aria-hidden="true">☰</span><span class="menu-label">菜单</span></button><nav id="site-nav" class="top-nav" aria-label="主导航"><a {'aria-current="page"' if active=='home' else ''} href="{rel}">首页</a><a {'aria-current="page"' if active=='topics' else ''} href="{rel}topics/">知识地图</a><a href="{rel}question-types/">按题型</a><a {'aria-current="page"' if active=='papers' else ''} href="{rel}papers/">按试卷</a><a href="{rel}#reading-paths">学习路径</a><a href="{rel}#discover">文章索引</a><a {'aria-current="page"' if active=='archive' else ''} href="{rel}archive/">归档</a><a href="https://github.com/1998x-stack/math-posts" target="_blank" rel="noopener noreferrer">GitHub ↗</a></nav></div></header>
<main id="main">{body}</main>
<footer class="site-footer"><div class="container footer-main"><div><a class="wordmark" href="{rel}">math<span>.</span>posts</a><p>把问题画出来，把推导讲清楚。</p></div><div><p class="footer-label">EXPLORE</p><a href="{rel}archive/">所有文章</a><a href="{rel}feed.xml">RSS 订阅</a><a href="https://github.com/1998x-stack/math-posts">源代码</a></div></div><div class="container legal"><span>© math-posts · Independent technical notes</span><span>Think visually. Prove carefully.</span></div></footer>
</body></html>'''


def category_pill(c, rel, count, active=False):
    return f'<a class="category-pill {"is-selected" if active else ""}" href="{rel}categories/{H(c["slug"])}/"><span>{H(c["title"])}</span><small>{count:02d}</small></a>'


def cover_art(p,rel,*,compact=False):
    """Article's own curated, existing mechanism SVG; no repeated placeholder."""
    cover=p['cover']
    src=rel+article_url(p)+cover['src']
    caption=H(cover['caption'])
    if compact:
        return f'<img class="article-cover-thumb" src="{H(src,quote=True)}" alt="" loading="lazy" decoding="async">'
    return (
        f'<div class="figure-abstract cover-figure">'
        f'<div class="cover-illustration"><img src="{H(src,quote=True)}" alt="{H(cover["caption"],quote=True)}" loading="lazy" decoding="async"></div>'
        f'<span class="cover-caption">{caption}</span></div>'
    )


def post_card(p,rel,ordinal=0,topic_title=None):
    path=rel+article_url(p)
    topic_link=(f'<a class="card-topic" href="{rel}categories/{H(p["category"])}/#topic-{H(p["topic"])}">{H(topic_title)}</a>' if topic_title else '')
    return f'''<article class="post-card" data-post-card data-search="{H((p['title']+' '+p['summary']+' '+' '.join(p['tags'])+' '+p['category']+' '+p['topic']+' '+(topic_title or '')).lower(),quote=True)}" data-category="{H(p['category'])}">
<a class="card-hit" href="{path}" aria-label="阅读 {H(p['title'],quote=True)}">{cover_art(p,rel)}</a>
<div class="card-body"><div class="card-topline"><span>MATH EXPLAINER / {H(p['category']).upper()}</span><span>{H(p['published'])}</span></div>
{topic_link}<h3><a href="{path}">{H(p['title'])}</a></h3><p class="card-subtitle">{H(p['subtitle'])}</p>
<p class="card-summary">{H(p['summary'])}</p><div class="card-bottom"><span>{p['reading_minutes']} 分钟阅读</span><span class="card-actions"><a class="paper-source" href="{H(p.get('paper',''),quote=True)}" target="_blank" rel="noopener noreferrer" aria-label="题源说明：{H(p['title'],quote=True)}">题源说明</a><a href="{path}" aria-label="阅读 {H(p['title'],quote=True)}">阅读全文 <span aria-hidden="true">↗</span></a></span></div></div></article>'''


HOME_PAGE_SIZE = 8
ARCHIVE_PAGE_SIZE = 16


def archive_page_url(page:int)->str:
    return 'archive/' if page == 1 else f'archive/page/{page}/'


def archive_page_count(posts)->int:
    total = sum(p['status'] == 'published' for p in posts)
    return max(1, (total + ARCHIVE_PAGE_SIZE - 1) // ARCHIVE_PAGE_SIZE)


def archive_pagination(page:int,pages:int,rel:str)->str:
    if pages <= 1:
        return ''
    numbers = sorted(n for n in {1, 2, page-1, page, page+1, pages-1, pages} if 1 <= n <= pages)
    links = []
    if page > 1:
        links.append(f'<a class="page-control" rel="prev" href="{rel}{archive_page_url(page-1)}">← 上一页</a>')
    else:
        links.append('<span class="page-control is-disabled" aria-disabled="true">← 上一页</span>')
    prior = 0
    for n in numbers:
        if prior and n > prior + 1:
            links.append('<span class="page-ellipsis" aria-hidden="true">…</span>')
        if n == page:
            links.append(f'<span class="page-number is-current" aria-current="page">{n}</span>')
        else:
            links.append(f'<a class="page-number" href="{rel}{archive_page_url(n)}" aria-label="第 {n} 页">{n}</a>')
        prior = n
    if page < pages:
        links.append(f'<a class="page-control" rel="next" href="{rel}{archive_page_url(page+1)}">下一页 →</a>')
    else:
        links.append('<span class="page-control is-disabled" aria-disabled="true">下一页 →</span>')
    return f'<nav class="pagination" aria-label="文章归档分页">{"".join(links)}</nav>'


def build_home(categories,posts,base,papers=None,taxonomy=None,knowledge_map=None):
    """Editorial home: fast routes into the corpus, full local search, no draft links."""
    published=[p for p in posts if p['status']=='published']
    published.sort(key=lambda p:(p['published'],p['slug']),reverse=True)
    by_slug={p['slug']:p for p in published}
    labels=topic_labels(categories)
    papers=papers or []
    taxonomy=taxonomy or {"dimensions":[]}
    counts={c['slug']:sum(p['category']==c['slug'] for p in published) for c in categories}
    active=[c for c in categories if counts[c['slug']]]
    planned=[c for c in categories if not counts[c['slug']]]
    count=len(published)

    # Editorial starting points are real, already-published essays; the manifest
    # remains the only source of URLs and metadata. No placeholders are linked.
    feature=by_slug.get('jianping-2021-q17') or by_slug.get('jianping-2021-q20') or (published[0] if published else None)
    if feature:
        feature_markup=f'''<aside class="hero-feature" aria-label="推荐阅读">
            <div class="feature-top"><span>EDITOR'S STARTING POINT</span><span>01 / GUIDE</span></div>
            <div class="feature-art feature-art--cover"><img src="{article_url(feature)+feature['cover']['src']}" alt="{H(feature['cover']['caption'],quote=True)}" loading="eager" decoding="async"></div>
            <div class="feature-copy"><span class="feature-kicker">本期精选 · {H(labels[(feature['category'],feature['topic'])])}</span>
                <h2><a href="{article_url(feature)}">{H(feature['title'])} <span aria-hidden="true">↗</span></a></h2>
                <p>{H(feature['subtitle'])}</p>
                <div class="feature-foot"><span>{feature['reading_minutes']} 分钟深度阅读</span><a href="{article_url(feature)}">进入这篇数学题解 →</a></div>
            </div></aside>'''
    else:
        feature_markup=''

    subject_cards=''.join(
        f'''<a class="research-card" href="./categories/{H(c['slug'])}/">
            <span class="research-card-top"><span class="research-num">{i:02d} / FIELD</span><span class="research-count">{counts[c['slug']]:02d} 篇</span></span>
            <strong>{H(c['title'])}</strong><span class="research-english">{H(c['english'])}</span>
            <span class="research-description">{H(c['description'])}</span>
            <span class="research-enter">进入题型 <span aria-hidden="true">↗</span></span>
        </a>''' for i,c in enumerate(sorted(active,key=lambda c:-counts[c['slug']]),1)
    )
    if knowledge_map:
        published_slugs={p['slug'] for p in published}
        subject_cards=''.join(
            f'<a class="research-card" href="topics/#area-{H(area["slug"])}">'
            f'<span class="research-card-top"><span class="research-num">{i:02d} / DOMAIN</span>'
            f'<span class="research-count">{len({slug for t in area["subtopics"] for slug in t["posts"] if slug in published_slugs}):02d} 道题</span></span>'
            f'<strong>{H(area["title"])}</strong><span class="research-english">{H(area["english"])}</span>'
            f'<span class="research-description">{H(area["description"])}</span>'
            f'<span class="research-enter">进入知识领域 <span aria-hidden="true">↗</span></span></a>'
            for i,area in enumerate(knowledge_map['areas'],1)
        )
    planned_links=''.join(
        f'<a href="categories/{H(c["slug"])}/">{H(c["title"])} <span>规划中 ↗</span></a>'
        for c in planned
    )

    # The editorial routes are now sourced from the same curated manifest as
    # the related-reading cards, rather than hard-coded ML paper slugs.
    learning_paths=[
        (route['title'], '围绕这一数学主题，从较直观的题目逐步过渡到综合应用。', route['posts'])
        for route in json.loads((ROOT/'content/reading_paths.json').read_text(encoding='utf-8'))
    ]
    route_cards=[]
    for number,(name,description,slugs) in enumerate(learning_paths,1):
        available=[by_slug[slug] for slug in slugs if slug in by_slug]
        if not available:continue
        steps=''.join(f'<li><a href="{article_url(p)}">{H(p["title"])}</a></li>' for p in available[:3])
        extra=f'<span class="route-extra">另有 {len(available)-3} 篇已收录</span>' if len(available)>3 else ''
        route_cards.append(
            f'<article class="route-card learning-card"><div class="route-top"><span>ROUTE {number:02d}</span><span>{len(available)} 篇已收录</span></div>'
            f'<h3>{H(name)}</h3><p>{H(description)}</p><ol>{steps}</ol>{extra}'
            f'<a class="route-start" href="{article_url(available[0])}">从第一篇开始 <span aria-hidden="true">↗</span></a></article>'
        )

    spotlight=[]
    for slug,eyebrow in [('jianping-2021-q04','正方体与空间向量'),('jianping-2021-q13','空间轨迹与双曲线'),('jianping-2021-q17','三棱锥与二面角')]:
        if slug not in by_slug:continue
        p=by_slug[slug]
        spotlight.append(
            f'''<article class="spotlight-card"><a class="spotlight-cover-link" href="{article_url(p)}" aria-label="阅读 {H(p['title'],quote=True)}">{cover_art(p,'./',compact=True)}</a><div class="spotlight-top"><span>{H(eyebrow)}</span><span>{p['reading_minutes']} MIN READ</span></div>
                <h3><a href="{article_url(p)}">{H(p['title'])}</a></h3>
                <p>{H(p['subtitle'])}</p>
                <a class="spotlight-link" href="{article_url(p)}">阅读全文 <span aria-hidden="true">↗</span></a>
            </article>'''
        )

    search_cards=[]
    for i,p in enumerate(published[:HOME_PAGE_SIZE]):
        topic=labels[(p['category'],p['topic'])]
        category=next(c['title'] for c in categories if c['slug']==p['category'])
        tokens=' '.join([p['title'],p['subtitle'],p['summary'],p['category'],category,topic,
                         p['topic'],*p['tags']]).lower()
        search_cards.append(
            f'''<article class="index-card post-card" data-post-card data-category="{H(p['category'],quote=True)}" data-search="{H(tokens,quote=True)}">
            <span class="index-order">{i+1:02d}</span><a class="index-image-link" href="{article_url(p)}" aria-label="阅读 {H(p['title'],quote=True)}">{cover_art(p,'./',compact=True)}</a>
            <div class="index-main"><div class="index-kicker">{H(category)} <span>/</span> {H(topic)}</div>
                <h3><a href="{article_url(p)}">{H(p['title'])}</a></h3><p>{H(p['subtitle'])}</p>
                <div class="index-tags"><span>{p['reading_minutes']} 分钟</span><span>{H(p['published'])}</span><a class="paper-source" href="{H(p['paper'],quote=True)}" target="_blank" rel="noopener noreferrer" aria-label="题源说明：{H(p['title'],quote=True)}">题源说明 ↗</a></div>
            </div><a class="index-arrow" href="{article_url(p)}" aria-label="阅读 {H(p['title'],quote=True)}">↗</a>
            </article>'''
        )
    options=''.join(
        f'<option value="{H(c["slug"])}">{H(c["title"])} · {counts[c["slug"]]}</option>' for c in active
    )

    paper_options=''.join(
        f'<option value="{H(paper["id"],quote=True)}">{H(paper["title"])} · {sum(p["paper_id"]==paper["id"] for p in published)} 题</option>'
        for paper in sorted(papers,key=lambda p:(p["year"] or 0,p["title"]),reverse=True)
        if any(p["paper_id"]==paper["id"] for p in published)
    )
    facet_options={}
    for dim in taxonomy["dimensions"]:
        options_for_dim=[]
        for tag in dim["tags"]:
            count_tag=sum(tag["id"] in p["facets"][dim["id"]] for p in published)
            if count_tag:
                options_for_dim.append(f'<option value="{H(tag["id"])}">{H(tag["title"])} · {count_tag}</option>')
        facet_options[dim["id"]]=''.join(options_for_dim)
    selected_papers=[paper for paper in sorted(papers,key=lambda p:(p["year"] or 0,p["title"]),reverse=True)
                     if any(p["paper_id"]==paper["id"] for p in published)][:4]
    paper_cards=''.join(
        f'<a class="paper-highlight" href="papers/{H(paper["id"])}/"><strong>{H(paper["title"])}</strong>'
        f'<span>{sum(p["paper_id"]==paper["id"] for p in published)} 道已公开题解 →</span></a>'
        for paper in selected_papers
    )

    body=f'''<section class="hero container" aria-labelledby="home-title">
      <div class="hero-left">
        <div class="eyebrow"><span class="eyebrow-dot"></span> MATH / VISUAL PROBLEM ATLAS</div>
        <h1 id="home-title">让抽象的数学题，<br>变成<span class="marker">看得见</span>的推导。</h1>
        <p class="hero-text">从 PDF 原题出发，先看关键观察，再一步步推导；遇到空间几何，通过可旋转的三维场景建立直觉。</p>
        <div class="hero-actions"><a class="primary-link" href="#reading-paths">选择一条学习路径 <span aria-hidden="true">↗</span></a><a class="secondary-link" href="#discover">搜索数学题目 ↗</a></div>
        <div class="hero-stats" aria-label="知识库概览"><div><strong>{count}</strong><span>篇数学题解</span></div><div><strong>{len(knowledge_map["areas"]) if knowledge_map else len(active)}</strong><span>大知识领域</span></div><div><strong>{len(route_cards)}</strong><span>条学习路径</span></div></div>
      </div>{feature_markup}
    </section>
    <nav class="entry-strip" aria-label="探索方式"><div class="container entry-grid">
      <a href="#categories"><span class="entry-index">01 / SUBJECTS</span><strong>按知识点探索</strong><span>深入七大数学领域与先修知识 ↗</span></a>
      <a href="papers/"><span class="entry-index">02 / PAPERS</span><strong>按试卷与题号浏览</strong><span>学校 · 地区 · 一模 / 二模 ↗</span></a>
       <a href="#reading-paths"><span class="entry-index">03 / PATHS</span><strong>按学习顺序阅读</strong><span>沿题目知识点逐步进阶 ↗</span></a>
      <a href="#discover"><span class="entry-index">04 / INDEX</span><strong>直接查找一篇文章</strong><span>按关键词与主题筛选 ↗</span></a>
    </div></nav>
    <section class="container spotlight-section" aria-labelledby="spotlight-title">
      <div class="section-header"><div><div class="eyebrow muted">SELECTED STARTING POINTS</div><h2 id="spotlight-title">三道值得先读的题</h2></div><p>从短题入手，再进入几何和综合证明；一题一图，不重复通用封面。</p></div>
      <div class="spotlight-grid">{''.join(spotlight)}</div>
    </section>
    <section id="categories" class="category-band" aria-labelledby="subjects-title"><div class="container">
      <div class="section-header"><div><div class="eyebrow muted">FIELDS OF STUDY</div><h2 id="subjects-title">从知识领域进入数学知识网络</h2></div><p>有内容的领域优先展示；尚在筹备的方向清晰标注。<a href="topics/">完整知识地图 ↗</a></p></div>
      <div class="research-grid">{subject_cards}</div>
      {f'<div class="planned-fields"><span>持续建设中的方向</span>{planned_links}</div>' if planned else ''}
    </div></section>
    <section id="paper-entry" class="container paper-entry-section" aria-labelledby="paper-entry-title">
      <div class="section-header"><div><div class="eyebrow muted">EXAM PAPER ATLAS</div><h2 id="paper-entry-title">按一张试卷的原始题号学习</h2></div>
      <p>区分学校整卷、地区单题摘录与专题练习。<a href="papers/">全部试卷与题集 ↗</a></p></div>
      <div class="paper-highlight-grid">{paper_cards}</div>
    </section>
    <section id="reading-paths" class="container learning-paths" aria-labelledby="paths-title">
      <div class="section-header"><div><div class="eyebrow muted">GUIDED READING / LEARNING ROUTES</div><h2 id="paths-title">以知识点串起题目，而非孤立刷题</h2></div><p>学习路线只连接已发布的内容；每一步都可以独立阅读。</p></div>
      <div class="route-grid">{''.join(route_cards)}</div>
    </section>
    <section id="discover" class="container latest" aria-labelledby="index-title"><span id="latest" class="anchor-alias" aria-hidden="true"></span>
      <div class="section-header"><div><div class="eyebrow muted">COMPLETE ARTICLE INDEX</div><h2 id="index-title">查找你的下一篇数学题解 <span class="count">{count:02d}</span></h2></div><p>全库搜索与筛选；每页只加载 8 篇文章及对应缩略图。</p></div>
      <div class="browse-controls">
        <label class="search-field" for="search-posts"><span aria-hidden="true">⌕</span><input id="search-posts" type="search" placeholder="搜索题号、题型、函数、几何或知识点" autocomplete="off" data-search-input></label>
        <label class="filter-field" for="category-filter"><span>答题形式</span><select id="category-filter" data-category-filter><option value="">全部题型</option>{options}</select></label>
        <label class="filter-field" for="concept-filter"><span>知识点</span><select id="concept-filter" data-facet-filter="concept"><option value="">全部知识点</option>{facet_options.get("concept","")}</select></label>
        <label class="filter-field" for="paper-filter"><span>来源试卷</span><select id="paper-filter" data-facet-filter="paper"><option value="">全部试卷</option>{paper_options}</select></label>
        <label class="filter-field" for="method-filter"><span>解题方法</span><select id="method-filter" data-facet-filter="method"><option value="">全部方法</option>{facet_options.get("method","")}</select></label>
        <label class="filter-field" for="visual-filter"><span>可视化方式</span><select id="visual-filter" data-facet-filter="visual"><option value="">全部图解</option>{facet_options.get("visual","")}</select></label>
        <button type="button" class="facet-reset" data-filter-reset>清除筛选</button>
        <span class="visible-count" aria-live="polite" data-visible-count>共 {count} 篇文章</span>
      </div>
      <div class="index-list" data-post-grid data-page-size="{HOME_PAGE_SIZE}">{''.join(search_cards)}</div>
      <p class="empty-result" hidden data-no-results>没有找到匹配的文章。试试更简短的关键词，或清除筛选条件。</p>
      <div class="index-footer"><nav class="pagination" data-home-pagination aria-label="文章索引分页" hidden></nav><a href="archive/">查看完整时间归档 ↗</a></div>
    </section>
    <section class="closing"><div class="container"><div class="eyebrow">OPEN MATHEMATICS / SOURCE-VERIFIED</div>
      <h2>从原题到答案，每一步都可以核对。</h2>
      <p>每篇题解连接 PDF 来源页码、数学推导与图形实验。想按知识体系检索？前往知识地图；想了解内容生产方式？阅读仓库规范。</p>
      <div class="closing-actions"><a href="topics/">探索知识地图 ↗</a><a href="https://github.com/1998x-stack/math-posts">查看数学题库仓库 ↗</a></div>
    </div></section>'''
    return html_page(title='math-posts · 数学题目与知识图谱',description='按知识点、学校试卷、原卷题号、解题方法与可视化浏览数学题；每题具有可核对的数学推导。',canonical=base,body=body)

def topic_labels(categories):
    return {(c['slug'],t['slug']):t['title'] for c in categories for t in c['topics']}


def build_question_types(categories,posts,base):
    published=[p for p in posts if p['status']=='published']
    summary=''.join(
        f'<a href="#category-{H(c["slug"])}">{H(c["title"])} <small>{sum(p["category"]==c["slug"] for p in published):02d}</small></a>'
        for c in categories
    )
    groups=[]
    for c in categories:
        related=[p for p in published if p['category']==c['slug']]
        links=''.join(
            f'<li><a href="../categories/{H(c["slug"])}/#topic-{H(t["slug"])}"><span>{H(t["title"])}</span>'
            f'<small>{"%02d 篇" % sum(p["topic"]==t["slug"] for p in related) if any(p["topic"]==t["slug"] for p in related) else "规划中"}</small></a></li>'
            for t in c['topics']
        )
        groups.append(
            f'<section class="taxonomy-group" id="category-{H(c["slug"])}" aria-labelledby="taxonomy-{H(c["slug"])}">'
            f'<div class="taxonomy-group-title"><h2 id="taxonomy-{H(c["slug"])}"><a href="../categories/{H(c["slug"])}/">{H(c["title"])}'
            f' <span class="faded-en">/ {H(c["english"])}</span></a></h2><span>{len(related)} 篇 · {len(c["topics"])} 个二级主题</span></div>'
            f'<p>{H(c["description"])}</p><ul class="taxonomy-links">{links}</ul></section>'
        )
    body=(
        '<div class="container taxonomy-page"><div class="breadcrumb"><a href="../">首页</a> <span>/</span> 题型索引</div>'
        '<div class="eyebrow muted">QUESTION TYPES / ANSWER FORM</div><h1>按题型浏览</h1>'
        f'<p class="category-description">覆盖 {len(categories)} 个一级数学题型、{sum(len(c["topics"]) for c in categories)} 个二级主题、'
        f'{len(published)} 篇正式发布文章。每篇文章归属一个主主题；交叉学科通过标签和学习路径相互连接。'
        '“规划中”代表尚无文章，不代表已有解读。</p>'
        f'<nav class="taxonomy-overview" aria-label="跳转至一级分类">{summary}</nav>'
        +''.join(groups)+'</div>'
    )
    return html_page(title='按题型浏览 · math-posts',description='按填空、选择和解答题浏览数学题目，知识分类另见知识地图。',canonical=url_join(base,'question-types/'),body=body,depth=1,active='question-types')



def build_topics(categories, posts, base, knowledge_map):
    """Render the subject-first high-school mathematics knowledge map."""
    published = {p['slug']: p for p in posts if p['status'] == 'published'}
    names = {t['id']: t['title'] for a in knowledge_map['areas'] for t in a['subtopics']}
    area_html = []
    for area in knowledge_map['areas']:
        topic_html = []
        for topic in area['subtopics']:
            related = [published[x] for x in topic['posts'] if x in published]
            dots = ''.join('<i class="difficulty-dot' + (' is-filled' if n <= topic['difficulty'] else '') + '"></i>' for n in range(1, 6))
            prereqs = ''.join('<a href="#topic-' + H(x) + '">' + H(names[x]) + '</a>' for x in topic['prerequisites'])
            outcomes = ''.join('<li>' + H(x) + '</li>' for x in topic['outcomes'])
            tags = ''.join('<span>' + H(x) + '</span>' for x in topic['tags'])
            if related:
                links = ''.join('<li><a href="../' + article_url(p) + '">' + H(p['title']) + '</a><small>Q' + str(p['question_number']).zfill(2) + '</small></li>' for p in related)
            else:
                links = '<li class="knowledge-empty">暂无已发布例题，作为后续内容建设方向</li>'
            prerequisite_text = prereqs or '<span class="knowledge-root">无前置要求</span>'
            topic_html.append(
                '<article class="knowledge-topic" id="topic-' + H(topic['id']) + '">'
                '<div class="knowledge-topic-head"><span class="knowledge-topic-id">' + H(topic['id']) + '</span>'
                '<span class="knowledge-difficulty" aria-label="难度 ' + str(topic['difficulty']) + ' / 5">' + dots +
                '<small>' + H(knowledge_map['difficulty_scale'][str(topic['difficulty'])]) + '</small></span></div>'
                '<h3>' + H(topic['title']) + '</h3><div class="knowledge-tags">' + tags + '</div>'
                '<div class="knowledge-detail"><div><strong>学完能够</strong><ul>' + outcomes + '</ul></div>'
                '<div><strong>建议先修</strong><p>' + prerequisite_text + '</p></div></div>'
                '<div class="knowledge-related"><strong>关联例题 · ' + str(len(related)) + '</strong><ul>' + links + '</ul></div></article>'
            )
        area_count = sum(1 for t in area['subtopics'] for x in t['posts'] if x in published)
        area_html.append(
            '<section class="knowledge-area" id="area-' + H(area['slug']) + '">'
            '<div class="knowledge-area-heading"><div><span class="knowledge-area-kicker">KNOWLEDGE DOMAIN / ' + H(area['english'].upper()) + '</span>'
            '<h2>' + H(area['title']) + '</h2><p>' + H(area['description']) + '</p></div>'
            '<span class="knowledge-area-count">' + str(len(area['subtopics'])) + ' 个知识节点<br>' + str(area_count) + ' 个关联例题位次</span></div>'
            '<div class="knowledge-grid">' + ''.join(topic_html) + '</div></section>'
        )
    nav = ''.join('<a href="#area-' + H(a['slug']) + '">' + H(a['title']) + '<small>' + str(len(a['subtopics'])) + ' 个节点</small></a>' for a in knowledge_map['areas'])
    mapped = {x for a in knowledge_map['areas'] for t in a['subtopics'] for x in t['posts'] if x in published}
    body = (
        '<div class="container knowledge-page"><div class="breadcrumb"><a href="../">首页</a> <span>/</span> 知识地图</div>'
        '<div class="eyebrow muted">HIGH SCHOOL MATHEMATICS / KNOWLEDGE GRAPH</div>'
        '<h1>' + H(knowledge_map['title']) + '</h1><p class="category-description">' + H(knowledge_map['description']) + '</p>'
        '<div class="knowledge-summary"><strong>' + str(len(knowledge_map['areas'])) + ' 大领域</strong>'
        '<strong>' + str(sum(len(a['subtopics']) for a in knowledge_map['areas'])) + ' 个知识节点</strong>'
        '<strong>' + str(len(mapped)) + ' 篇文章已关联</strong><a href="../question-types/">切换到答题形式索引 ↗</a></div>'
        '<nav class="knowledge-overview" aria-label="七大知识领域">' + nav + '</nav>'
        + ''.join(area_html)
        + '<p class="knowledge-note">难度为本站面向高中学习路径的编辑分级，不等同于官方考试难度。先修关系表示推荐学习顺序，不代表唯一依赖。</p></div>'
    )
    return html_page(title='高中数学知识地图 · math-posts', description=knowledge_map['description'],
                     canonical=url_join(base, 'topics/'), body=body, depth=1, active='topics')



def build_category(c,posts,categories,base):
    listing=sorted([p for p in posts if p['status']=='published' and p['category']==c['slug']],key=lambda p:(p['published'],p['slug']),reverse=True)
    rel='../../'
    pills=''.join(category_pill(x,rel,sum(p['status']=='published' and p['category']==x['slug'] for p in posts),x['slug']==c['slug']) for x in categories)
    jumps=''.join(
        f'<a href="#topic-{H(t["slug"])}"><span>{H(t["title"])}</span><small>{sum(p["topic"]==t["slug"] for p in listing):02d} 篇</small></a>'
        for t in c['topics']
    )
    sections=[]
    for t in c['topics']:
        group=[p for p in listing if p['topic']==t['slug']]
        content=(
            '<div class="post-grid">'+''.join(post_card(p,rel,i+1,t['title']) for i,p in enumerate(group))+'</div>'
            if group else '<p class="topic-empty">该研究方向正在规划中，尚无正式发布的文章。</p>'
        )
        sections.append(
            f'<section class="topic-section" id="topic-{H(t["slug"])}" aria-labelledby="heading-{H(t["slug"])}">'
            f'<div class="topic-section-heading"><h2 id="heading-{H(t["slug"])}">{H(t["title"])}</h2>'
            f'<span>{"%02d 篇文章" % len(group) if group else "规划中"}</span></div>{content}</section>'
        )
    body=f'''<div class="container category-page"><div class="breadcrumb"><a href="{rel}">首页</a> <span>/</span> <a href="{rel}topics/">知识地图</a> <span>/</span> {H(c['title'])}</div>
<div class="eyebrow muted">TOPIC COLLECTION · {H(c['english']).upper()}</div><h1>{H(c['title'])}<span class="faded-en"> / {H(c['english'])}</span></h1><p class="category-description">{H(c['description'])}</p>
<p class="taxonomy-hint">{len(listing)} 篇文章 · {len(c['topics'])} 个二级主题 · <a href="{rel}question-types/#category-{H(c['slug'])}">查看完整知识地图 ↗</a></p>
<nav class="topic-jumps" aria-label="本分类二级主题导航">{jumps}</nav>
{''.join(sections)}
<div class="category-nav"><div class="eyebrow muted">MORE TOPICS</div>{pills}</div></div>'''
    return html_page(title=f"{c['title']} · math-posts",description=c['description'],canonical=url_join(base,f'categories/{c["slug"]}/'),body=body,depth=2)


def build_archive(posts,categories,base,page=1):
    """A separate crawlable HTML page per chunk; only current thumbnails enter DOM."""
    published=sorted([p for p in posts if p['status']=='published'],key=lambda p:(p['published'],p['title']),reverse=True)
    labels=topic_labels(categories)
    pages=archive_page_count(posts)
    if not 1 <= page <= pages:
        raise ValueError(f'archive page {page} is outside 1..{pages}')
    rel='../' if page == 1 else '../../../'
    current=published[(page-1)*ARCHIVE_PAGE_SIZE:page*ARCHIVE_PAGE_SIZE]
    cards=''.join(
        f'''<li class="archive-entry">
        <time class="timeline-date" datetime="{H(p['published'])}">{H(p['published'])}</time>
        <a class="archive-cover" href="{rel}{article_url(p)}" aria-label="阅读 {H(p['title'],quote=True)}" title="{H(p['cover']['caption'],quote=True)}">{cover_art(p,rel,compact=True)}</a>
        <div class="archive-entry-copy"><h2><a href="{rel}{article_url(p)}">{H(p['title'])}</a></h2>
        <p>{H(p['subtitle'])}</p>
        <a class="archive-topic" href="{rel}categories/{H(p['category'])}/#topic-{H(p['topic'])}">{H(labels[(p['category'],p['topic'])])}</a></div>
        <span class="timeline-time">{p['reading_minutes']} min <span aria-hidden="true">↗</span></span></li>'''
        for p in current
    )
    first=(page-1)*ARCHIVE_PAGE_SIZE+1 if current else 0
    last=first+len(current)-1 if current else 0
    pager=archive_pagination(page,pages,rel)
    body=f'''<div class="container archive-page"><div class="breadcrumb"><a href="{rel}">首页</a> <span>/</span> <a href="{rel}archive/">文章归档</a>{f' <span>/</span> 第 {page} 页' if page>1 else ''}</div><div class="eyebrow muted">ALL EXPLAINERS · CHRONOLOGICAL</div><h1>数学题解归档<span class="count">{len(published):02d}</span></h1><p class="category-description">按发布时间浏览本试卷已转写并发布的数学题解。每页仅显示 {ARCHIVE_PAGE_SIZE} 篇，保留每题专属的 SVG 图解封面。</p><p class="archive-range">第 {page} / {pages} 页 · 显示 {first}–{last} / {len(published)} 篇</p><ol class="timeline">{cards}</ol>{pager}</div>'''
    return html_page(title=f'文章归档{" · 第 "+str(page)+" 页" if page>1 else ""} · math-posts',description='按时间与题型浏览 math-posts 的原创数学题解文章。',canonical=url_join(base,archive_page_url(page)),body=body,depth=1 if page==1 else 3,active='archive')


def write(out:Path,path:str,content:str):
    dest=out/path;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(content,encoding='utf-8')


def enrich_article_head(html:str,p:dict,base:str)->str:
    """Add missing social/canonical tags to deployed articles, never duplicate existing ones."""
    canonical=url_join(base,article_url(p))
    head=html.split('</head>',1)[0] if '</head>' in html else html.split('</HEAD>',1)[0]
    specs=[
        (r'<link\b[^>]*rel=[^ >]+canonical[^ >]*',
         '<link rel="canonical" href="'+H(canonical,quote=True)+'">'),
        (r'<meta\b[^>]*property=[^ >]+og:url[^ >]*',
         '<meta property="og:url" content="'+H(canonical,quote=True)+'">'),
        (r'<meta\b[^>]*property=[^ >]+og:type[^ >]*',
         '<meta property="og:type" content="article">'),
        (r'<meta\b[^>]*property=[^ >]+og:title[^ >]*',
         '<meta property="og:title" content="'+H(p['title'],quote=True)+'">'),
        (r'<meta\b[^>]*property=[^ >]+og:description[^ >]*',
         '<meta property="og:description" content="'+H(p['summary'],quote=True)+'">'),
        (r'<meta\b[^>]*name=[^ >]+twitter:card[^ >]*',
         '<meta name="twitter:card" content="summary">'),
    ]
    additions=[value for regex,value in specs if not re.search(regex,head,re.I)]
    # Individual paper pages also advertise the same canonical site-wide RSS feed.
    if not re.search(r'<link\b[^>]*application/rss\+xml',head,re.I):
        additions.append('<link rel="alternate" type="application/rss+xml" title="math-posts RSS" href="'+H(url_join(base,'feed.xml'),quote=True)+'">')
    if not additions:return html
    return re.sub(r'</head>',lambda m:'\n'.join(additions)+'\n'+m.group(0),html,count=1,flags=re.I)


def build_feed(categories:list,posts:list,base:str)->str:
    """Deterministic RSS 2.0 from published manifest entries only.

    Manifest dates are calendar dates, not event timestamps. RSS requires a
    datetime for pubDate, so encode midnight UTC consistently; do not present
    this as the actual publication time. Modified dates retain day precision.
    """
    atom_ns='http://www.w3.org/2005/Atom'
    dcterms_ns='http://purl.org/dc/terms/'
    ET.register_namespace('atom',atom_ns)
    ET.register_namespace('dcterms',dcterms_ns)
    rss=ET.Element('rss',{'version':'2.0'})
    channel=ET.SubElement(rss,'channel')
    ET.SubElement(channel,'title').text='math-posts'
    ET.SubElement(channel,'link').text=base
    ET.SubElement(channel,'description').text='从原卷题目出发，用 SVG 图解、数学推导与 Three.js 交互理解数学。'
    ET.SubElement(channel,'language').text='zh-cn'
    ET.SubElement(channel,f'{{{atom_ns}}}link',{
        'href':url_join(base,'feed.xml'),
        'rel':'self',
        'type':'application/rss+xml',
    })

    category_titles={c['slug']:c['title'] for c in categories}
    topic_titles=topic_labels(categories)
    published=(p for p in posts if p['status']=='published')
    for p in sorted(published,key=lambda p:(p.get('updated') or p['published'],p['published'],p['slug']),reverse=True):
        url=url_join(base,article_url(p))
        item=ET.SubElement(channel,'item')
        ET.SubElement(item,'title').text=p['title']
        ET.SubElement(item,'link').text=url
        ET.SubElement(item,'guid',{'isPermaLink':'true'}).text=url
        ET.SubElement(item,'description').text=p['summary']
        day=datetime.fromisoformat(p['published']).replace(tzinfo=timezone.utc)
        ET.SubElement(item,'pubDate').text=format_datetime(day,usegmt=True)
        ET.SubElement(item,f'{{{dcterms_ns}}}modified').text=p.get('updated') or p['published']
        ET.SubElement(item,'category',{
            'domain':url_join(base,f'categories/{p["category"]}/'),
        }).text=category_titles[p['category']]
        ET.SubElement(item,'category',{
            'domain':url_join(base,f'categories/{p["category"]}/#topic-{p["topic"]}'),
        }).text=topic_titles[(p['category'],p['topic'])]

    ET.indent(rss,space='  ')
    return ET.tostring(rss,encoding='utf-8',xml_declaration=True).decode('utf-8')+'\n'


def build(root:Path,out:Path,base:str):
    base=base.rstrip('/')+'/'
    assert base.startswith('https://') or base.startswith('http://localhost:'), 'Provide valid HTTPS base URL'
    if out.exists():shutil.rmtree(out)
    out.mkdir(parents=True)
    categories,posts,knowledge_map=data(root)
    papers,taxonomy=load_atlas(root,posts,knowledge_map)
    write(out,'index.html',build_home(categories,posts,base,papers,taxonomy,knowledge_map))
    write(out,'papers/index.html',build_papers_index(papers,posts,base,html_page))
    public_papers=[paper for paper in papers if any(p["paper_id"]==paper["id"] and p["status"]=="published" for p in posts)]
    for paper in public_papers:
        write(out,f'papers/{paper["id"]}/index.html',build_paper_detail(paper,posts,taxonomy,base,html_page,article_url))
    for archive_page in range(1,archive_page_count(posts)+1):
        write(out,archive_page_url(archive_page)+'index.html',build_archive(posts,categories,base,archive_page))
    write(out,'topics/index.html',build_topics(categories,posts,base,knowledge_map))
    write(out,'question-types/index.html',build_question_types(categories,posts,base))
    for c in categories:write(out,f'categories/{c["slug"]}/index.html',build_category(c,posts,categories,base))
    published=[p for p in posts if p['status']=='published']
    reading_paths=load_reading_paths(root,published)
    for p in published:
        src=root/'posts'/p['category']/p['slug'];dst=out/'posts'/p['category']/p['slug']
        shutil.copytree(src,dst,ignore=shutil.ignore_patterns('README.md','*.pyc','__pycache__','*.py','evidence.json'))
        published_html=dst/'index.html'
        page=enrich_article_head(published_html.read_text(encoding='utf-8'),p,base)
        page=enrich_article_related(page,p,published,reading_paths)
        published_html.write_text(page,encoding='utf-8')
    shutil.copytree(root/'site/assets',out/'assets')
    write(out,'.nojekyll','')
    write(out,'404.html',html_page(title='页面未找到 · math-posts',description='你访问的页面不存在。',canonical=url_join(base,'404.html'),body='<div class="container category-empty not-found"><h1>这条路径尚未被写下。</h1><p>页面可能移动了，或文章尚未正式发布。</p><a href="'+H(base,quote=True)+'">回到首页 ↗</a></div>',root_href=base))
    labels=topic_labels(categories)
    category_names={c['slug']:c['title'] for c in categories}
    ordered=sorted(published,key=lambda p:(p['published'],p['slug']),reverse=True)
    paper_names={paper['id']:paper['title'] for paper in papers}
    facet_tokens={tag['id']:' '.join([tag['title'],*tag.get('aliases',[])]) for dim in taxonomy['dimensions'] for tag in dim['tags']}
    search=[{k:p[k] for k in ['title','slug','subtitle','summary','category','topic','tags','published','reading_minutes']}
            |{'url':article_url(p),'paper':p.get('paper',''),'cover_src':article_url(p)+p['cover']['src'],
              'category_title':category_names[p['category']],'topic_title':labels[(p['category'],p['topic'])],
              'paper_id':p['paper_id'],'paper_title':paper_names[p['paper_id']],
              'question_number':p['question_number'],'facets':p['facets'],
              'facet_terms':' '.join(facet_tokens[tag] for values in p['facets'].values() for tag in values)}
            for p in ordered]
    write(out,'posts.json',json.dumps(search,ensure_ascii=False,indent=2)+'\n')
    urls=[base]+[url_join(base,archive_page_url(i)) for i in range(1,archive_page_count(posts)+1)]+[url_join(base,'topics/'),url_join(base,'question-types/'),url_join(base,'papers/')]+[url_join(base,f'papers/{paper["id"]}/') for paper in public_papers]+[url_join(base,f'categories/{c["slug"]}/') for c in categories]+[url_join(base,article_url(p)) for p in published]
    sitemap=''.join(f'<url><loc>{X(u)}</loc></url>' for u in urls)
    write(out,'sitemap.xml','<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+sitemap+'</urlset>')
    write(out,'robots.txt',f'User-agent: *\nAllow: /\nSitemap: {url_join(base,"sitemap.xml")}\n')
    write(out,'feed.xml',build_feed(categories,posts,base))
    print(json.dumps({'build':str(out),'base':base,'categories':len(categories),'published':len(published),'files':len(list(out.rglob('*')))},ensure_ascii=False))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'_site')
    parser.add_argument('--base-url',default=os.getenv('SITE_URL',DEFAULT_URL))
    args=parser.parse_args();build(ROOT,args.output,args.base_url)
