import datetime

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/58.0.3029.110 Safari/537.3'
}


# 获取CSDN热榜 https://blog.csdn.net/
def get_csdn_hot(param='热榜'):
    if param == '':
        param = '热榜'

    result = {
        'tabs': [
            '热榜', 'C/C++', '云原生', '人工智能', '前沿技术', '软件工程', '后端',
            'Java', 'JavaScript', 'PHP', 'Python', '区块链', '大数据',
            '移动开发', '嵌入式', '开发工具', '结构与算法', '微软技术', '测试', '游戏', '网络', '运维'
        ],
        'site': 'csdn'
    }
    articles = []

    if param == '热榜':
        response1 = requests.get('https://blog.csdn.net/phoenix/web/blog/hot-rank?page=0&pageSize=50&type=',
                                 headers=HEADERS)
        items = response1.json()['data']
        response2 = requests.get('https://blog.csdn.net/phoenix/web/blog/hot-rank?page=1&pageSize=50&type=',
                                 headers=HEADERS)
        items += response2.json()['data']
    else:
        if param == 'C/C++':
            url = 'https://blog.csdn.net/phoenix/web/blog/hot-rank?page=0&pageSize=50&child_channel=c%2Fc%2B%2B&type='
        elif param == '结构与算法':
            url = 'https://blog.csdn.net/phoenix/web/blog/hot-rank?page=0&pageSize=50&child_channel=%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84%E4%B8%8E%E7%AE%97%E6%B3%95&type='
        else:
            url = f'https://blog.csdn.net/phoenix/web/blog/hot-rank?page=0&pageSize=50&child_channel={param.lower()}&type='
        response = requests.get(url, headers=HEADERS)
        items = response.json()['data']

    for item in items:
        article = {
            'title': item['articleTitle'],
            'subTitle': item['nickName'],
            'link': item['articleDetailUrl'],
            'detail': f"{item['viewCount']} 浏览 · {item['commentCount']} 评论 · {item['favorCount']} 收藏",
            'img_url': item['picList'][0] if len(item['picList']) > 0 else '',
            'hot': item['hotRankScore'],
        }
        articles.append(article)

    result['articles'] = articles
    return result


# 获取Github热榜
def get_github_hot(param='总榜'):
    if param == '':
        param = '总榜'

    param_to_url = {
        '总榜': 'https://github.com/trending',
        '中文热榜': 'https://github.com/trending?spoken_language_code=zh',
        'C': 'https://github.com/trending/c',
        'C++': 'https://github.com/trending/c++',
        'Java': 'https://github.com/trending/java',
        'Python': 'https://github.com/trending/python',
        'Go': 'https://github.com/trending/go',
        'HTML': 'https://github.com/trending/html',
        'CSS': 'https://github.com/trending/css',
        'JavaScript': 'https://github.com/trending/js',
        'TypeScript': 'https://github.com/trending/ts',
        'C#': 'https://github.com/trending/c%23',
        'PHP': 'https://github.com/trending/php',
        'Rust': 'https://github.com/trending/rust',
        'Swift': 'https://github.com/trending/swift',
        'Lua': 'https://github.com/trending/lua',
        'Vue': 'https://github.com/trending/vue',
    }

    s = requests.Session()
    s.mount('https://', HTTPAdapter(max_retries=10))

    response = s.get(param_to_url[param], headers=HEADERS, timeout=5)
    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.find_all('article', class_='Box-row')

    result = {
        'tabs': ['总榜', '中文热榜', 'C', 'C++', 'Java', 'Python', 'Go', 'HTML', 'CSS', 'JavaScript', 'TypeScript',
                 'C#', 'PHP', 'Rust', 'Swift', 'Lua', 'Vue'],
        'site': 'github'
    }
    articles = []

    for item in items:
        article = {
            'title': item.find('a', class_='Link').text,
            'subTitle': item.find('span', class_='d-inline-block ml-0 mr-3').findAll('span')[-1].text
                    if item.find('span', class_='d-inline-block ml-0 mr-3') is not None else '',
            'link': f"https://www.github.com{item.find('a', class_='Link')['href']}",
            'detail': item.find('p', class_='col-9 color-fg-muted my-1 pr-4').text
                    if item.find('p', class_='col-9 color-fg-muted my-1 pr-4') is not None else '',
            'img_url': '',
            'hot': f"{item.find('a', class_='Link Link--muted d-inline-block mr-3').text} star"
                   f" | {item.find('a', class_='Link Link--muted d-inline-block mr-3').text} fork" +
                   (' | ' + item.find('span', class_='d-inline-block float-sm-right').text)
                        if item.find('span', class_='d-inline-block float-sm-right') is not None else '',
        }
        articles.append(article)

    result['articles'] = articles
    return result


# 获取掘金热榜 https://api.juejin.cn/content_api/v1/content/article_rank?category_id=1&type=hot&aid=2608&
# uuid=7090135583016486404&spider=0
def get_juejin_hot(param='热榜'):
    if param == '':
        param = '热榜'

    param_to_url = {
        '热榜': 'https://api.juejin.cn/content_api/v1/content/article_rank?category_id=1&type=hot&aid=2608&uuid=7090135583016486404&spider=0',
        '收藏榜': 'https://api.juejin.cn/content_api/v1/content/article_rank?category_id=1&type=collect&aid=2608&uuid=7090135583016486404&spider=0',
        '后端': 'https://api.juejin.cn/content_api/v1/content/article_rank?category_id=6809637769959178254&type=hot&aid=2608&uuid=7090135583016486404&spider=0',
        '前端': 'https://api.juejin.cn/content_api/v1/content/article_rank?category_id=6809637767543259144&type=hot&aid=2608&uuid=7090135583016486404&spider=0',
        'Android': 'https://api.juejin.cn/content_api/v1/content/article_rank?category_id=6809635626879549454&type=hot&aid=2608&uuid=7090135583016486404&spider=0',
        'iOS': 'https://api.juejin.cn/content_api/v1/content/article_rank?category_id=6809635626661445640&type=hot&aid=2608&uuid=7090135583016486404&spider=0',
        '人工智能': 'https://api.juejin.cn/content_api/v1/content/article_rank?category_id=6809637773935378440&type=hot&aid=2608&uuid=7090135583016486404&spider=0',
        '开发工具': 'https://api.juejin.cn/content_api/v1/content/article_rank?category_id=6809637771511070734&type=hot&aid=2608&uuid=7090135583016486404&spider=0',
        '代码人生': 'https://api.juejin.cn/content_api/v1/content/article_rank?category_id=6809637776263217160&type=hot&aid=2608&uuid=7090135583016486404&spider=0',
        '阅读': 'https://api.juejin.cn/content_api/v1/content/article_rank?category_id=6809637772874219534&type=hot&aid=2608&uuid=7090135583016486404&spider=0',
        '精选专栏': 'https://api.juejin.cn/content_api/v1/column/selected_rank?aid=2608&uuid=7090135583016486404&spider=0',
        '推荐收藏': 'https://api.juejin.cn/interact_api/v2/collectionset/collection_recommend_rank?aid=2608&uuid=7090135583016486404&spider=0',
    }

    if param == '精选专栏':
        data = {
            'cursor': '',
            'page_size': 30,
            'sort_type': 2
        }
        response = requests.post(param_to_url[param], headers=HEADERS, json=data)
        items = response.json()['data']
    elif param == '推荐收藏':
        data = {
            "limit": 30,
            "module_type": 0,
            "cursor": "",
            "sort_type": 2,
            "filter": {
                "article_info": True
            }
        }
        response = requests.post(param_to_url[param], headers=HEADERS, json=data)
        items = response.json()['data']
    else:
        response = requests.get(param_to_url[param], headers=HEADERS)
        items = response.json()['data']

    result = {
        'tabs': [
            '热榜', '收藏榜', '后端', '前端', 'Android', 'iOS', '人工智能', '开发工具', '代码人生', '阅读', '精选专栏',
            '推荐收藏'
        ],
        'site': 'juejin'
    }
    articles = []

    if param == '精选专栏':
        for item in items:
            article = {
                'title': item['column']['column_version']['title'],
                'subTitle': item['column']['author']['user_name'] + ' | '
                            + str(item['column']['column']['article_cnt']) + ' 篇文章 | '
                            + str(item['column']['column']['follow_cnt']) + ' 订阅',
                'link': f"https://juejin.cn/column/{item['column']['column_version']['column_id']}",
                'detail': item['column']['column_version']['content'],
                'img_url': item['column']['column_version']['cover'],
                'hot': '',
            }
            articles.append(article)
    elif param == '推荐收藏':
        for item in items:
            article = {
                'title': item['collection_set']['collection_name'],
                'subTitle': item['creator']['user_name'] + ' | '
                            + datetime.datetime.fromtimestamp(item['collection_set']['update_time']).strftime(
                    '%Y-%m-%d %H:%M'),
                'link': f"https://juejin.cn/collection/{item['collection_set']['collection_id']}",
                'detail': str(item['collection_set']['post_article_count']) + ' 篇文章 | '
                          + str(item['collection_set']['concern_user_count']) + ' 订阅',
                'img_url': '',
                'hot': '',
            }
            articles.append(article)
    else:
        for item in items:
            article = {
                'title': item['content']['title'],
                'subTitle': item['author']['name'],
                'link': f"https://juejin.cn/post/{item['content']['content_id']}",
                'detail': f"{item['content_counter']['view']} 浏览 · {item['content_counter']['interact_count']} 互动 · "
                          f"{item['content_counter']['collect']} 收藏",
                'img_url': '',
                'hot': round(item['content_counter']['hot_rank']),
            }
            articles.append(article)

    result['articles'] = articles
    return result


# 获取InfoQ热榜 https://www.infoq.cn/hotlist?tag=day
def get_infoq_hot(param='周榜'):
    if param == '':
        param = '周榜'

    result = {
        'tabs': ['周榜', '月榜', '半年榜'],
        'site': 'infoq'
    }
    articles = []

    url = 'https://www.infoq.cn/public/v1/article/getHotList'
    data = {
        "score": None,
        "type": result['tabs'].index(param) + 1,
        "size": 50
    }

    infoq_headers = {
        'Origin': 'https://www.infoq.cn',
        'Referer': 'https://www.infoq.cn/hotlist?tag=month'
    }
    infoq_headers.update(HEADERS)

    response = requests.post(url, headers=infoq_headers, json=data)
    items = response.json()['data']

    for item in items:
        article = {
            'title': item['article_title'],
            'subTitle': f"{' | '.join(topic['name'] for topic in item['topic'])} "
                        f"| {datetime.datetime.fromtimestamp(item['publish_time'] / 1000).strftime('%m-%d %H:%M')}",
            'link': f"https://www.infoq.cn/article/{item['uuid']}",
            'detail': item['article_summary'],
            'img_url': item['article_cover'],
            'hot': f"{item['views']} 浏览"
        }
        articles.append(article)

    result['articles'] = articles
    return result


# 获取人人都是产品经理日榜 https://www.woshipm.com/
def get_woshipm_hot(param='日榜'):
    if param == '':
        param = '日榜'

    response = requests.get('https://www.woshipm.com/api2/app/article/popular/daily', headers=HEADERS)
    # 解析json
    result_list = response.json()['RESULT']

    result = {
        'tabs': ['日榜'],
        'site': 'renrenchanpin'
    }
    articles = []

    for item in result_list:
        article = {
            'title': item['data']['articleTitle'],
            'subTitle': ' | '.join(item['data']['tag'].split(' ')),
            'link': f"https://www.woshipm.com/?p={item['data']['id']}",
            'detail': item['data']['articleSummary'],
            'img_url': item['data']['imageUrl'],
            'hot': item['scores']
        }
        articles.append(article)

    result['articles'] = articles
    return result


# 获取小众软件 https://www.appinn.com/
def get_appinn_hot(param='精选'):
    if param == '':
        param = '精选'

    param_to_url = {
        '精选': 'https://www.appinn.com/category/featured/',
        'Windows': 'https://www.appinn.com/category/windows/',
        'macOS': 'https://www.appinn.com/category/mac/',
        'Chrome': 'https://www.appinn.com/category/chrome/',
        'Web': 'https://www.appinn.com/category/online-tools/',
        'Android': 'https://www.appinn.com/category/featured/',
        'iPhone': 'https://www.appinn.com/category/ios/iphone/',
        'iPad': 'https://www.appinn.com/category/ios/ipad/',
    }

    result = {
        'tabs': ['精选', 'Windows', 'macOS', 'Chrome', 'Web', 'Android', 'iPhone', 'iPad'],
        'site': 'appinn'
    }
    articles = []

    response = requests.get(param_to_url[param], headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.findAll('article')

    for item in items:
        article = {
            'title': item.find('h2').text,
            'subTitle': ' | '.join([tag.text for tag in item.find('span', class_='thecategory').findAll('a')])
                        + ' | ' + item.find('span', class_='thetime updated').find('span').text,
            'link': item.find('a')['href'],
            'detail': item.find('div', class_='post-excerpt').text,
            'img_url': item.find('img')['src'],
            'hot': ''
        }
        articles.append(article)

    result['articles'] = articles
    return result
