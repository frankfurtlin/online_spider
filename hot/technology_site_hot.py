import datetime
import json
import time

import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/58.0.3029.110 Safari/537.3'
}


# 获取IT之家热榜 https://www.ithome.com/
def get_ithome_hot(param='资讯'):
    if param == '':
        param = '资讯'

    param_to_url = {
        '资讯': 'https://it.ithome.com/',
        '手机': 'https://mobile.ithome.com/',
        '电脑': 'https://www.ithome.com/pc/',
        '测评': 'https://www.ithome.com/labs/',
        '视频': 'https://www.ithome.com/video/',
        'AI': 'https://next.ithome.com/',
        '苹果': 'https://www.ithome.com/apple/',
        'iPhone': 'https://iphone.ithome.com/',
        '鸿蒙': 'https://hmos.ithome.com/',
        '软件': 'https://soft.ithome.com/',
        '智车': 'https://auto.ithome.com/',
        '数码': 'https://digi.ithome.com/',
        '学院': 'https://www.ithome.com/college/',
        '游戏': 'https://game.ithome.com/',
        '直播': 'https://www.ithome.com/live/',
        '5G': 'https://www.ithome.com/5g/',
        '微软': 'https://www.ithome.com/microsoft/',
        'Win10': 'https://win10.ithome.com/',
        'Win11': 'https://win11.ithome.com/',
        '专题': 'https://www.ithome.com/zt/',
    }
    if param in param_to_url:
        response = requests.get(param_to_url[param], headers=HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find('div', id='list', class_='bb clearfix').find('div', class_='fl').find('ul',
                                                                                                class_='bl').findAll(
            'li')
    else:
        response = requests.get('https://www.ithome.com/block/rank.html?d=it')
        soup = BeautifulSoup(response.text, 'html.parser')
        items = []
        if param == '热榜':
            items = soup.find('ul', id='d-4').findAll('li')
        if param == '日榜':
            items = soup.find('ul', id='d-1').findAll('li')
        elif param == '周榜':
            items = soup.find('ul', id='d-2').findAll('li')
        elif param == '月榜':
            items = soup.find('ul', id='d-3').findAll('li')

    result = {
        'tabs': ['资讯', '热榜', '日榜', '周榜', '月榜', '手机', '电脑', '测评', '视频', 'AI', '苹果', 'iPhone', '鸿蒙',
                 '软件',
                 '智车', '数码', '学院', '游戏', '直播', '5G', '微软', 'Win10', 'Win11', '专题'],
        'site': 'ithome'
    }
    articles = []

    for item in items:
        article = {
            'title': item.find('a').text if param not in param_to_url else item.find('a', class_='title').text,
            'subTitle': item.find('div', class_='tags').find('a').text + ' | ' + item.find('div',
                                                                                           class_='d').text if param in param_to_url else '',
            'link': item.find('a')['href'],
            'detail': item.find('div', class_='m').text if param in param_to_url else ' ',
            'img_url': item.find('img')['data-original'] if param in param_to_url else '',
            'hot': '',
        }
        articles.append(article)
    result['articles'] = articles
    return result


# 获取36kr热榜 https://36kr.com/
def get_36kr_hot(param='热榜'):
    if param == '':
        param = '热榜'

    param_to_url = {
        '资讯': 'https://36kr.com/information/web_news/',
        '创投': 'https://36kr.com/information/contact/',
        '财经': 'https://36kr.com/information/ccs/',
        '汽车': 'https://36kr.com/information/travel/',
        '科技': 'https://36kr.com/information/technology/',
        'AI': 'https://36kr.com/information/AI/',
        '企服': 'https://36kr.com/information/enterpriseservice/',
        '创新': 'https://36kr.com/information/innovate/',
        '专精特新数字化': 'https://36kr.com/motif/2244745907613570',
        '专精特新IPO': 'https://36kr.com/motif/2244718518906500',
        '专精特新新风向': 'https://36kr.com/motif/2244717091155593',
        '生活': 'https://36kr.com/information/happy_life/',
        '城市': 'https://36kr.com/information/real_estate/',
        '职场': 'https://36kr.com/information/web_zhichang/',
        '企业号': 'https://36kr.com/information/qiyehao/',
        '红人': 'https://36kr.com/information/sensation/',
        '其他': 'https://36kr.com/information/other/',
        '专题': 'https://36kr.com/topics/',
    }
    headers_36kr = {
        'cookie': 'aliyungf_tc=76fdd5968e11e4d7680affed482aa2e7a67736af79414119fded8b72805c1f23; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2218e47b368baff1-05e1901bc15e6c-26001b51-1327104-18e47b368bbda1%22%2C%22%24device_id%22%3A%2218e47b368baff1-05e1901bc15e6c-26001b51-1327104-18e47b368bbda1%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; Hm_lvt_713123c60a0e86982326bae1a51083e1=1710599924,1710733468,1711866752; Hm_lvt_1684191ccae0314c6254306a8333d090=1710599924,1710733468,1711866752; acw_sc__v2=66120ea9a64bb5217d72380843ec2c47fea072e5; Hm_lpvt_1684191ccae0314c6254306a8333d090=1712459898; Hm_lpvt_713123c60a0e86982326bae1a51083e1=1712459898; acw_tc=ac11000117124599931272535e776600e6265ffd722ffb09f347e01d09e900; SERVERID=6754aaff36cb16c614a357bbc08228ea|1712460091|1712458172'
    }
    headers_36kr.update(HEADERS)
    if param == '热榜':
        # 获取当前日期，格式为 2024-03-16
        today = datetime.date.today().strftime('%Y-%m-%d')
        response = requests.get(f'https://36kr.com/hot-list/renqi/{today}/1', headers=headers_36kr)
        soup = BeautifulSoup(response.text, 'html.parser')
        script_content = soup.findAll('script')[-3].string.replace('window.initialState=', '').replace(' ', '')
        items = json.loads(script_content)['hotListDetail']['articleList']['itemList']
    elif param.startswith('专精特新'):
        response = requests.get(param_to_url[param], headers=headers_36kr)
        soup = BeautifulSoup(response.text, 'html.parser')
        script_content = soup.findAll('script')[-3].string.replace('window.initialState=', '').replace(' ', '')
        items = [item['templateMaterial'] for item in
                 json.loads(script_content)['motifDetailData']['data']['motifArticleList']['data']['itemList']]
    elif param.startswith('专题'):
        response = requests.get(param_to_url[param], headers=headers_36kr)
        soup = BeautifulSoup(response.text, 'html.parser')
        script_content = soup.findAll('script')[-3].string.replace('window.initialState=', '').replace(' ', '')
        items = [item['templateMaterial'] for item in
                 json.loads(script_content)['specialTopicCatalogData']['data']['specialTopicList']['data']['itemList']]
    else:
        response = requests.get(param_to_url[param], headers=headers_36kr)
        soup = BeautifulSoup(response.text, 'html.parser')
        script_content = soup.findAll('script')[-3].string.replace('window.initialState=', '').replace(' ', '')
        items = [item['templateMaterial'] for item in
                 json.loads(script_content)['information']['informationList']['itemList']]

    result = {
        'tabs': ['热榜', '资讯', '创投', '财经', '汽车', '科技', 'AI', '企服', '创新', '专精特新数字化', '专精特新IPO',
                 '专精特新新风向', '生活', '城市', '职场', '企业号', '红人', '其他', '专题'],
        'site': '36kr'
    }
    articles = []

    for item in items:
        if param == '专题':
            article = {
                'title': item['categoryTitle'],
                'subTitle': '',
                'link': 'https://36kr.com/p/' + str(item['itemId']),
                'detail': item['catagoryIntroduce'],
                'img_url': item['categoryImage'],
                'hot': '',
            }
            articles.append(article)
            continue

        if param.startswith('专精特新'):
            sub_title = item['author']
        elif param == '资讯':
            sub_title = item['authorName'] + ' | ' + item['themeName']
        else:
            sub_title = item['authorName']
        article = {
            'title': item['widgetTitle'],
            'subTitle': sub_title + ' | ' + datetime.datetime.fromtimestamp(item['publishTime'] / 1000).strftime(
                '%m-%d %H:%M'),

            'link': 'https://36kr.com/p/' + str(item['itemId']),
            'detail': item['content'] if param.startswith('专精特新') else item['summary'],
            'img_url': item['widgetImage'],
            'hot': item['statHot'] if param == '热榜' else '',
        }
        articles.append(article)

    result['articles'] = articles
    return result


# 少数派热榜 https://sspai.com
def get_sspai_hot(param='热榜'):
    if param == '':
        param = '热榜'

    if param == '热榜':
        params = {
            'limit': 40,
            'offset': 0,
            'tag': '热门文章',
            'released': False,
        }
        response = requests.get('https://sspai.com/api/v1/article/tag/page/get', headers=HEADERS, params=params)
    elif param == '视频':
        params = {
            'limit': 40,
            'offset': 0,
            'created_at': int(time.time()),
            'post_type': 2,
        }
        response = requests.get('https://sspai.com/api/v1/article/post_type/page/get', headers=HEADERS, params=params)
    elif param == '效率技巧':
        params = {
            'limit': 40,
            'offset': 0,
            'created_at': int(time.time()),
            'tag': '效率技巧',
            'search_type': 1,
        }
        response = requests.get('https://sspai.com/api/v1/article/tag/special/page/get', headers=HEADERS, params=params)
    elif param == 'Matrix精选':
        response = requests.get(
            f'https://sspai.com/api/v1/article/matrix/page/get?offset=0&limit=40&created_at={time.time()}',
            headers=HEADERS)
    elif param == 'Matrix热门':
        response = requests.get(
            f'https://sspai.com/api/v1/article/matrix/hot/page/get?offset=0&limit=40&created_at={time.time()}',
            headers=HEADERS)
    else:
        params = {
            'limit': 40,
            'offset': 0,
            'created_at': int(time.time()),
            'tag': param,
            'search_type': 1,
        }
        response = requests.get('https://sspai.com/api/v1/article/tag/page/get', headers=HEADERS, params=params)

    items = response.json()['data']

    result = {
        'tabs': ['热榜', '应用推荐', '生活方式', '效率技巧', '播客', '视频', 'Matrix精选', 'Matrix热门'],
        'site': 'sspai'
    }
    articles = []

    for item in items:
        article = {
            'title': item['title'],
            'subTitle': item['author']['nickname'] + ' | ' + datetime.datetime.fromtimestamp(
                item['modify_time']).strftime('%m-%d %H:%M'),
            'link': 'https://sspai.com/post/' + str(item['id']),
            'detail': item['summary'],
            'img_url': ('https://cdn.sspai.com/' + item['banner']) if item['banner'] != '' else '',
            'hot': str(item['like_count']) + ' 喜欢',
        }
        articles.append(article)

    result['articles'] = articles
    return result


# 获取极客公园资讯 https://www.geekpark.net/
def get_geekpark_hot(param='资讯'):
    if param == '':
        param = '资讯'

    param_to_url = {
        '资讯': 'https://mainssl.geekpark.net/api/v2?page=1',
        '周榜': 'https://mainssl.geekpark.net/api/v1/posts/hot_in_week?per=7',
        '综合报道': 'https://mainssl.geekpark.net/api/v1/columns/179?page=1',
        'AI新浪潮观察': 'https://mainssl.geekpark.net/api/v1/columns/304?page=1',
        '新造车观察': 'https://mainssl.geekpark.net/api/v1/columns/305?page=1',
        '财报解读': 'https://mainssl.geekpark.net/api/v1/columns/271?page=1',
        '底稿对话CEO': 'https://mainssl.geekpark.net/api/v1/columns/308?page=1',
        'GeekInsight特稿': 'https://mainssl.geekpark.net/api/v1/columns/306?page=1',
        '心科技': 'https://mainssl.geekpark.net/api/v1/columns/307?page=1',
        '行业': 'https://mainssl.geekpark.net/api/v1/columns/2?page=1',
    }
    response = requests.get(param_to_url[param], headers=HEADERS)

    if param == '资讯':
        items = [item['post'] for item in response.json()['homepage_posts']]
    elif param == '7日热榜':
        items = response.json()['posts']
    else:
        items = response.json()['column']['posts']

    result = {
        'tabs': ['资讯', '周榜', '综合报道', 'AI新浪潮观察', '新造车观察', '财报解读', '底稿对话CEO', 'GeekInsight特稿',
                 '心科技', '行业'],
        'site': 'geekpark'
    }
    articles = []

    for item in items:
        article = {
            'title': item['title'],
            'subTitle': ' | '.join(item['tags']) + ' | ' + datetime.datetime.fromtimestamp(
                item['published_timestamp']).strftime('%m-%d %H:%M'),
            'link': f"https://www.geekpark.net/news/{item['id']}",
            'detail': item['abstract'],
            'img_url': item['cover_url'],
            'hot': f"{item['views']} 浏览",
        }
        articles.append(article)
    result['articles'] = articles
    return result


# 获取品玩热榜 https://www.pingwest.com
def get_pinwest_hot(param='资讯'):
    if param == '':
        param = '资讯'

    param_to_url = {
        '资讯': 'https://www.pingwest.com/api/state/list?last_id=',
        '品驾': 'https://www.pingwest.com/api/tag_article_list?id=17530&type=0',
        '品玩Global': 'https://www.pingwest.com/api/tag_article_list?id=20259&type=0',
        '硅星人': 'https://www.pingwest.com/api/tag_article_list?id=13606&type=0',
        '不客观实验室': 'https://www.pingwest.com/api/tag_article_list?id=14715&type=0',
        '大模型焦点对话': 'https://www.pingwest.com/api/newest_tag_article_list?id=20868&page=1&type=5',
        '大模型第一视角': 'https://www.pingwest.com/api/newest_tag_article_list?id=20868&page=1&type=6',
        '大模型新鲜事': 'https://www.pingwest.com/api/newest_tag_article_list?id=20868&page=1&type=4',
        '大模型测评': 'https://www.pingwest.com/api/newest_tag_article_list?id=20868&page=1&type=7',
        '大模型融资追踪': 'https://www.pingwest.com/api/newest_tag_article_list?id=20868&page=1&type=8',
    }

    result = {
        'tabs': ['资讯', '品驾', '品玩Global', '硅星人', '不客观实验室', '大模型焦点对话', '大模型第一视角', '大模型测评', '大模型新鲜事', '大模型融资追踪'],
        'site': 'pinwest'
    }
    articles = []

    response = requests.get(param_to_url[param], headers=HEADERS)
    section = response.json()['data']['list'].replace('\n', '').replace('\\', '')
    soup = BeautifulSoup(section, 'html.parser')

    if param == '资讯':
        items = soup.findAll('section', class_='item w clearboth')

        for index, item in enumerate(items):
            article = {
                'title': item.find('p', class_='title').find('a').text,
                'subTitle': item.find('section', class_='item-tag-list bg clearboth').find('span').text + ' | ' + item.find('section', class_='time').text,
                'link': f"https:{item.find('p', class_='title').find('a')['href']}",
                'detail': item.find('p', class_='description').find('a').text
                if item.find('p', class_='description') is not None else '',

                'img_url': item.find('img')['src'] if item.find('img') is not None else '',
                'hot': '',
            }
            articles.append(article)
    else:
        items = soup.findAll('section', class_='row clearboth')

        for index, item in enumerate(items):
            article = {
                'title': item.find('p', class_='title').find('a').text,
                'subTitle': item.find('section', class_='author').find('a').text + ' | ' + item.find('span', class_='time').text,
                'link': f"https:{item.find('p', class_='title').find('a')['href']}",
                'detail': item.find('p', class_='desc').text if item.find('p', class_='desc') is not None else '',
                'img_url': item.find('img')['src'],
                'hot': '',
            }
            articles.append(article)

    result['articles'] = articles
    return result


# 获取爱范儿资讯 get_ifanr_hot
def get_ifanr_hot(param='资讯'):
    if param == '':
        param = '资讯'

    param_to_url = {
        '资讯': 'https://www.ifanr.com/',
        '每日早报': 'https://sso.ifanr.com/api/v5/wp/article/?post_category=%E6%97%A9%E6%8A%A5&position=ifr_fourth_cards_layout',
        '评测': 'https://sso.ifanr.com/api/v5/wp/article/?post_category=%E8%AF%84%E6%B5%8B&position=ifr_fourth_cards_layout',
        '众测': 'https://sso.ifanr.com/api/v5/wp/article/?post_category=%E7%B3%96%E7%BA%B8%E4%BC%97%E6%B5%8B&post_type=tangzhiapp&position=ifr_fourth_cards_layout',
        '新锐产品': 'https://sso.ifanr.com/api/v5/wp/article/?post_category=%E4%BA%A7%E5%93%81&position=ifr_fourth_cards_layout',
        'AppSo': 'https://sso.ifanr.com/api/v5/wp/article/?post_type=app&position=ifr_fourth_cards_layout',
        '玩物志': 'https://sso.ifanr.com/api/v5/wp/article/?post_type=coolbuy&position=ifr_fourth_cards_layout',
        '行业': 'https://sso.ifanr.com/api/v5/wp/article/?post_category=%E5%85%AC%E5%8F%B8&position=ifr_fourth_cards_layout',
        '生活': 'https://sso.ifanr.com/api/v5/wp/article/?post_category=%E7%94%9F%E6%B4%BB&position=ifr_fourth_cards_layout',
        '董车会': 'https://sso.ifanr.com/api/v5/wp/article/?post_category=%E8%91%A3%E8%BD%A6%E4%BC%9A&position=ifr_fourth_cards_layout',
        '小程序': 'https://sso.ifanr.com/api/v5/wp/article/?post_type=minapp&position=ifr_fourth_cards_layout',
        '视频': 'https://sso.ifanr.com/api/v5/wp/article/?post_type=video&position=ifr_fourth_cards_layout',
        '游戏': 'https://sso.ifanr.com/api/v5/wp/article/?post_category=%E6%B8%B8%E6%88%8F&position=ifr_fourth_cards_layout',
        '人物': 'https://sso.ifanr.com/api/v5/wp/article/?post_category=%E4%BA%BA%E7%89%A9&position=ifr_fourth_cards_layout',
    }

    if param == '资讯':
        response = requests.get(param_to_url[param], headers=HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.findAll('div', class_='article-container')
    else:
        response = requests.get(param_to_url[param], headers=HEADERS)
        items = response.json()['objects']

    result = {
        'tabs': ['资讯', '每日早报', '评测', '众测', '新锐产品', 'AppSo', '玩物志', '行业', '生活', '董车会', '小程序', '视频', '游戏', '人物'],
        'site': 'ifanr'
    }
    articles = []

    if param == '资讯':
        for item in items:
            article = {
                'title': item.find('h3').find('a').text,
                'subTitle': item.find('span', class_='author-name').text.replace(' ', '') + ' | ' + item.find('time').text,
                'link': item.find('h3').find('a')['href'],
                'detail': item.find('div', class_='article-summary').text if item.find('div', class_='article-summary') is not None else '',
                'img_url': item.find('a', class_='article-link cover-block')['style'].split("'")[1],
                'hot': '',
            }
            articles.append(article)
    else:
        for item in items:
            article = {
                'title': item['post_title'],
                'subTitle': item['created_by']['name'].replace(' ', '') + ' | ' + datetime.datetime.fromtimestamp(item['published_at']).strftime('%m-%d %H:%M'),
                'link': item['post_url'],
                'detail': item['post_excerpt'].replace('\r', '').replace('\n', '').strip(),
                'img_url': item['post_cover_image'],
                'hot': '',
            }
            articles.append(article)

    result['articles'] = articles
    return result


# 获取创业邦资讯 https://www.cyzone.cn/
def get_cyzone_hot(param='资讯'):
    if param == '':
        param = '资讯'

    param_to_url = {
        '资讯': f'https://api1.cyzone.cn/v2/content/channel/getArticle?page=1&created_at={time.time()}',
        '热文榜': f"https://api1.cyzone.cn/v2/content/find_page/hotlist?page=1&size=40&created_at={time.time()}"
    }
    response = requests.get(param_to_url[param], headers=HEADERS)
    items = response.json()['data']

    result = {
        'tabs': ['资讯', '热文榜'],
        'site': 'cyzone'
    }
    articles = []

    for item in items:
        article = {
            'title': item['title'],
            'subTitle': (' | '.join(item['tags'].split(',')) + ' | ' if 'tags' in item else '') + item['published_time'],
            'link': f"https:{item['url']}",
            'detail': item['description'],
            'img_url': item['thumb'],
            'hot': item['pv'],
        }
        articles.append(article)
    result['articles'] = articles
    return result