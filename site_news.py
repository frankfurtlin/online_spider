import datetime

import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/58.0.3029.110 Safari/537.3',
}


# 获取站点的时事资讯
def get_site_news(site_params):
    if site_params['site'] == 'xueqiu':
        return get_xueqiu_news(site_params['xueqiu_max_id'])
    elif site_params['site'] == 'dsb':
        return get_dsb_news(site_params['dsb_page'])
    elif site_params['site'] == 'jinse':
        return get_jinse_news(site_params['jinse_bottom_id'])
    elif site_params['site'] == 'tmtpost':
        return get_tmtpost_news(site_params['tmtpost_offset'])
    # 添加其他站点的处理逻辑
    else:
        raise ValueError('Invalid site parameter')


# 获取雪球的7X24资讯 https://xueqiu.com/statuses/livenews/list.json?since_id=-1&max_id=-1&count=10
def get_xueqiu_news(max_id=-1):
    url = 'https://xueqiu.com/statuses/livenews/list.json'
    params = {
        'since_id': -1,
        'max_id': max_id,
        'count': 20
    }
    xueqiu_headers = {
        'Cookie': 'cookiesu=121710548469745; device_id=11d60e42df500cac3ca92a6a67693365; '
                  'xq_a_token=378f5ce0709f986c272b56ef12b2ad8968c64fc5; '
                  'xqat=378f5ce0709f986c272b56ef12b2ad8968c64fc5; '
                  'xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9'
                  '.eyJ1aWQiOjM4MTc0MDMyODksImlzcyI6InVjIiwiZXhwIjoxNzEzMTQwNTA3LCJjdG0iOj'
                  'E3MTA1NDg1MDczOTYsImNpZCI6ImQ5ZDBuNEFadXAifQ.b6RALIz3DCd9_ZrmEEuNIHBQ8q9G0lcir30mA7'
                  '-aGweO0OvAJGvO014Cb549HYDxI7qeu__K3xn9vGxrhNvaHwd7rB6C_6ucZ8LFQ4KudXHdy0CFig15UtmGt'
                  'VfHiuXQfaq8OOx0qRU29Po2qZl2kvaX919yKpk6JstfFnj7z1Zs11Rsvs0rk05609GLtBDAkBbus_8bPJWXOMop'
                  '-xnto2DEhPOKsoMyfwcmDwXK_nNEZOoL7_G0pjA5Mzk9iqQ2SN4v9e4CeZkU_j_nD4Gy-V1Dy2igQpnWm0wCelzh1'
                  '-LreNSMsI6zCQJUaDm6VYt_7ebF51tc4bWjMIXgwXfgrA; '
                  'xq_r_token=0e34d5f5e9fb81d0a965979e3a93ebee58d32478; xq_is_login=1; u=3817403289; s=ax1alcpcmu; '
                  'bid=318e91d50f0e513d6f46b64bc95ae560_lttfjosj; __utmz=1.1710553769.1.1.utmcsr=(direct)|utmccn=('
                  'direct)|utmcmd=(none); Hm_lvt_1db88642e346389874251b5a1eded6e3=1710548476,1710854548; '
                  '__utma=1.1897728280.1710553769.1710645513.1710854548.3; __utmc=1; snbim_minify=true; '
                  'acw_tc=2760779517110036875495847e5bc530e1c4b2e970d1804d9fbcdeb3243105; '
                  'acw_sc__v2=65fbd873d623b7e3a8f8fe67f9a252a6638d3679; '
                  'Hm_lpvt_1db88642e346389874251b5a1eded6e3=1711003779'
    }
    xueqiu_headers.update(HEADERS)
    response = requests.get(url, headers=xueqiu_headers, params=params)

    result = {}
    articles = []

    if response.status_code == 200:
        result['xueqiu_max_id'] = response.json()['next_max_id']
        items = response.json()['items']
        for item in items:
            article = {
                # hh:mm
                'time': get_timeline_format_time(item['created_at'] / 1000),
                'title': item['text'].split('】')[0][1:] if '【' in item['text'] else item['text'].split('：')[0],
                'url': item['target'],
                'detail': item['text'].split('】')[1] if '【' in item['text'] else item['text'],
                'desc': str(item['reply_count']) + ' 回复 ' + str(item['share_count']) + ' 转发',
                'mark': item['mark']
            }
            articles.append(article)
        result['articles'] = articles
    return result


# 获取电商报的7X24h快讯 https://www.dsb.cn/news?pure=true&page=2&_pjax=body
def get_dsb_news(page=1):
    url = 'https://www.dsb.cn/news'
    params = {
        'pure': 'true',
        'page': page,
        '_pjax': 'body'
    }
    response = requests.get(url, headers=HEADERS, params=params)

    result = {}
    articles = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all('div', class_='news-list-item')
        result['dsb_page'] = page + 1
        for item in items:
            article = {
                'time': item.find('div', class_='news-timeago').text,
                'title': item.find('a', class_='news-title rm-tdu').text.strip(),
                'url': item.find('a', class_='news-title rm-tdu')['href'],
                'detail': item.find('div', class_='news-content').text,
                'desc': '',
                'mark': 0
            }
            articles.append(article)
        result['articles'] = articles
    return result


# 获取金色财经的7X24h快讯 https://api.jinse.cn/noah/v2/lives?limit=20&reading=false&source=web&flag=down&id=0&category=0
def get_jinse_news(bottom_id=0):
    url = 'https://api.jinse.cn/noah/v2/lives'
    params = {
        'limit': 20,
        'reading': 'false',
        'source': 'web',
        'flag': 'down',
        'id': bottom_id,
        'category': 0
    }
    response = requests.get(url, headers=HEADERS, params=params)

    result = {}
    articles = []

    if response.status_code == 200:
        data = response.json()
        result['jinse_bottom_id'] = data['bottom_id']
        for items in data['list']:
            for item in items['lives']:
                format_time = datetime.datetime.fromtimestamp(item['created_at'])
                now_format_day = f"{datetime.datetime.now().month:02d}-{datetime.datetime.now().day:02d}"

                article = {
                    'time': f"{format_time.hour:02d}:{format_time.minute:02d}"
                    if item['created_at_zh'][-5:] == now_format_day else
                    f"{item['created_at_zh'][-5:]} {format_time.hour:02d}:{format_time.minute:02d}",

                    'title': item['content_prefix'],
                    'url': f"https://jinse.cn/lives/{item['id']}",
                    'detail': item['content'],
                    'desc': f"{item['up_counts']} 利好 · {item['down_counts']} 利空",
                    'mark': 1 if item['attribute'] == '精选' or item['grade'] == 5 else 0
                }
                articles.append(article)
        result['articles'] = articles
    else:
        print(response.raise_for_status())
    return result


# 获取钛媒体快报
def get_tmtpost_news(offset):
    url = "https://api.tmtpost.com/v1/word/list"
    params = {
        "limit": "20",
        "offset": offset,
        "if_keyword_highlight": "true",
        "platform": "pc",
        "fields": "number_of_bookmarks;number_of_comments;number_of_upvotes;if_current_user_bookmarked"
                  ";if_current_user_voted;share_link;share_link;share_description;share_image;word_comments"
                  ";stock_list;is_important;audio;duration;word_classify;stock",
        "word_fields": "number_of_bookmarks;number_of_comments;number_of_upvotes;if_current_user_bookmarked"
                       ";if_current_user_voted;share_link;share_link;share_description;share_image;word_comments"
                       ";stock_list;is_important;word_classify;stock"
    }
    tmtpost_headers = {
        'App-Version': 'web1.0'
    }
    tmtpost_headers.update(HEADERS)
    response = requests.get(url, params=params, headers=tmtpost_headers)

    result = {}
    articles = []

    if response.status_code == 200:
        items = response.json()['data']
        result['tmtpost_offset'] = offset + 20
        for item in items:
            article = {
                'time': get_timeline_format_time(item['time_published']),
                'title': item['title'],
                'url': item['share_link'],
                'detail': item['detail'],
                'desc': f"{item['number_of_bookmarks']} 收藏 {item['number_of_upvotes']} 点赞",
                'mark': 1 if item['is_important'] else 0,
            }
            articles.append(article)
        result['articles'] = articles
    return result


# 获取时间线的标准时间
def get_timeline_format_time(timestamp):
    time_format = datetime.datetime.fromtimestamp(int(timestamp))
    format_day = f"{time_format.month:02d}-{time_format.day:02d}"
    format_time = f"{time_format.hour:02d}:{time_format.minute:02d}"

    now_format_day = f"{datetime.datetime.now().month:02d}-{datetime.datetime.now().day:02d}"

    result = format_time if format_day == now_format_day else f"{format_day} {format_time}"
    return result
