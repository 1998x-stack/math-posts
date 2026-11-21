from scripts.related_posts import choose_related


def test_related_posts_use_registered_concepts_across_exam_formats():
    current={
        'slug':'vector-fill-in','category':'fill-in','topic':'functions',
        'tags':[],'facets':{'concept':['vector']},
    }
    target={
        'slug':'vector-worked-solution','category':'worked-solutions','topic':'analytic-geometry',
        'tags':[],'facets':{'concept':['vector']},
    }
    cards=choose_related(current,[current,target],[],limit=4)
    assert cards and cards[0]['post']['slug']==target['slug']
    assert cards[0]['kind']=='知识点衔接'
    assert '向量' in cards[0]['explanation']


def test_related_posts_never_recommend_unpublished_drafts():
    current={'slug':'current','category':'fill-in','topic':'functions','tags':[],'facets':{'concept':['vector']}}
    published={'slug':'published','category':'worked-solutions','topic':'geometry','tags':[],'facets':{'concept':['vector']}}
    draft={'slug':'draft','category':'worked-solutions','topic':'geometry','tags':[],'facets':{'concept':['vector']}}
    cards=choose_related(current,[current,published],[],limit=4)
    assert all(card['post']['slug']!='draft' for card in cards)
