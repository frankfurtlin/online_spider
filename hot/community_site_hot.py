import json
import time

import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/58.0.3029.110 Safari/537.3'
}


# 获取百度贴吧热榜 https://tieba.baidu.com/
def get_baidu_tieba_hot(param='热议榜'):
    if param == '':
        param = '热议榜'

    response = requests.get('https://tieba.baidu.com/hottopic/browse/topicList?res_type=1')
    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.findAll('li', class_='topic-top-item')

    result = {
        'tabs': ['热议榜'],
        'site': 'tieba'
    }
    articles = []

    for item in items:
        article = {
            'title': item.find('a', class_='topic-text').text,
            'subTitle': '',
            'link': item.find('a', class_='topic-text')['href'],
            'detail': item.find('p', class_='topic-top-item-desc').text,
            'img_url': item.find('img')['src'],
            'hot': item.find('span', class_='topic-num').text[:-4],
        }
        articles.append(article)
    result['articles'] = articles
    return result


# 获取虎扑热帖 https://hupu.com/
def get_hupu_hot(param):
    if param == '':
        param = '资讯'

    result = {
        'tabs': ['资讯', '步行街热帖', 'NBA热帖', 'CBA热帖', '游戏电竞热帖', '国际足球热帖', '中国足球热帖'],
        'site': 'hupu'
    }
    articles = []

    if param == '资讯':
        response = requests.get('https://www.hupu.com/home/v1/news?pageNo=1&pageSize=50')
        items = response.json()['data']
        for item in items:
            article = {
                'title': item['title'],
                'subTitle': '',
                'link': f"https://bbs.hupu.com/{item['tid']}.html",
                'detail': item['content'],
                'img_url': item['img'],
                'hot': f"{item['replies']} 评论",
            }
            articles.append(article)
    else:
        response = requests.get('https://bbs.hupu.com/')
        soup = BeautifulSoup(response.text, 'html.parser')
        # print(soup.findAll('script')[-5].string.encode('gbk', errors='ignore'))
        items = json.loads(soup.findAll('script')[-5].string.replace('window.$$data=', ''))['pageData']['threads']
        index = result['tabs'].index(param)
        for item in items[index * 10 - 10:index * 10]:
            article = {
                'title': item['title'],
                'subTitle': '',
                'link': f"https://bbs.hupu.com{item['url']}",
                'detail': item['desc'],
                'img_url': item['cover'],
                'hot': f"{item['replies']} 评论",
            }
            articles.append(article)

    result['articles'] = articles
    return result


# 获取zhihu热榜 https://www.zhihu.com/
def get_zhihu_hot(param='热榜'):
    if param == '':
        param = '热榜'

    response = requests.get('https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50&desktop=true',
                            headers=HEADERS)
    data = response.json()['data']

    result = {
        'tabs': ['热榜'],
        'site': 'zhihu'
    }
    articles = []

    for item in data:
        article = {
            'title': item['target']['title'],
            'subTitle': '',
            'link': 'https://zhihu.com/question/' + str(item['target']['id']),
            'detail': item['target']['excerpt'],
            'img_url': item['children'][0]['thumbnail'],
            'hot': str(item['target']['answer_count']) + ' 回答 | ' + str(item['target']['follower_count']) + ' 关注 | ' +
                   item['detail_text'].split(' ')[0] + 'w',
        }
        articles.append(article)

    result['articles'] = articles
    return result


# 获取微信阅读热榜 https://weread.qq.com/web/category/hot_search
def get_wxread_hot(param='热搜榜'):
    if param == '':
        param = '热搜榜'

    param_to_url = {
        '热搜榜': 'https://weread.qq.com/web/category/hot_search',
        '总榜': 'https://weread.qq.com/web/category/all',
        '神作榜': 'https://weread.qq.com/web/category/newrating_publish',
        '潜力榜': 'https://weread.qq.com/web/category/newrating_potential_publish',
        '飙升榜': 'https://weread.qq.com/web/category/rising',
        '新书榜': 'https://weread.qq.com/web/category/newbook',
        '小说榜': 'https://weread.qq.com/web/category/general_novel_rising',
    }

    result = {
        'tabs': ['热搜榜', '总榜', '神作榜', '潜力榜', '飙升榜', '新书榜', '小说榜'],
        'site': 'wxread'
    }
    articles = []

    response = requests.get(param_to_url[param], headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.findAll('li', class_='wr_bookList_item')
    for item in items:
        article = {
            'title': item.find('p', class_='wr_bookList_item_title').text,
            'subTitle': item.find('p', class_='wr_bookList_item_author').text,
            'link': f"https://weread.qq.com{item.find('a', class_='wr_bookList_item_link')['href']}",
            'detail': item.find('p', class_='wr_bookList_item_desc').text,
            'img_url': item.find('img', class_='wr_bookCover_img')['src'],
            'hot': f"{item.find('span', class_='wr_bookList_item_reading_number').text} 人今日阅读" +
                   (f" | 推荐值 {item.find('span', class_='wr_bookList_item_reading_percent').text}" if item.find('span', class_='wr_bookList_item_reading_percent') else ''),
        }
        articles.append(article)
    result['articles'] = articles
    return result


# 获取爱思想点击量周榜排行 https://www.aisixiang.com/toplist/?period=7
def get_aisixiang_hot(param='周点击榜'):
    if param == '':
        param = '周点击榜'

    response = requests.get('https://www.aisixiang.com/toplist/?period=7', headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.findAll('div', class_='tops_list')

    result = {
        'tabs': ['周点击榜'],
        'site': 'aisixiang'
    }
    articles = []

    for item in items:
        article = {
            'title': item.find('div', class_='tips').find('a').text,
            'subTitle': '',
            'link': f"https://www.aisixiang.com{item.find('div', class_='tips').find('a')['href']}",
            'detail': item.find('div', class_='ablum_list').find('a').text,
            'img_url': '',
            'hot': item.find('div', class_='click').text,
        }
        articles.append(article)

    result['articles'] = articles
    return result


# 获取历史上的今天 http://www.lishi365.cn/lishi.html
def get_lishi(param):
    if param == '':
        param = '历史上的今天'

    response = requests.get('http://www.lishi365.cn/lishi.html', headers=HEADERS)
    # 解决乱码问题 UnicodeEncodeError: 'gbk' codec can't encode character '\xe5' in position 41
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text.encode('utf-8', 'ignore'), 'html.parser')
    items = soup.find_all('tr', attrs={'height': '32'})

    result = {
        'tabs': ['历史上的今天'],
        'site': 'lishi'
    }
    articles = []

    for item in items:
        article = {
            'title': item.findAll('td')[-1].find('a').get('title'),
            'subTitle': '',
            'link': 'http://www.lishi365.cn/' + item.findAll('td')[-1].find('a')['href'],
            'detail': ' ',
            'img_url': '',
            'hot': '',
        }
        articles.append(article)

    result['articles'] = articles
    return result


# 获取游戏葡萄资讯 https://youxiputao.com/api/article/index.html?page=1
def get_youxiputao_hot(param='资讯'):
    if param == '':
        param = '资讯'

    param_to_url = {
        '资讯': 'https://youxiputao.com/api/article/category/id/14.html',
        '深度': 'https://youxiputao.com/api/article/category/id/13.html',
        '海外': 'https://youxiputao.com/api/article/category/id/17.html',
        '专访': 'https://youxiputao.com/api/article/category/id/15.html',
    }

    result = {
        'tabs': ['资讯', '深度', '海外', '专访'],
        'site': 'youxiputao'
    }
    articles = []

    for i in range(2):
        response = requests.get(param_to_url[param], params={'page': i + 1}, headers=HEADERS)
        items = response.json()['data']['data']
        for item in items:
            article = {
                'title': item['title'],
                'subTitle': ' | '.join([author[0] for author in item['authors']]) + ' | ' + item['publishtime'],
                'link': f"https://youxiputao.com/article/{item['id']}",
                'detail': item['summary'],
                'img_url': f"https://cdn.youxiputao.com/small{item['image']}",
                'hot': item['publishtime'],
            }
            articles.append(article)
    result['articles'] = articles
    return result


# 获取机核资讯 https://www.gcores.com/gapi/v1/originals
def get_gcores_hot(param='资讯'):
    if param == '':
        param = '资讯'

    url = "https://www.gcores.com/gapi/v1/originals"
    params = {
        "page[limit]": "36",
        "page[offset]": "0",
        "sort": "-published-at",
        "include": "category,user",
        "filter[is-news]": "1",
        "filter[list-all]": "0",
        "fields[articles]": "title,desc,excerpt,is-published,thumb,app-cover,cover,comments-count,likes-count,"
                            "bookmarks-count,is-verified,published-at,option-is-official,option-is-focus-showcase,"
                            "duration,draft,audit-draft,user,comments,category,tags,entries,entities,similarities,"
                            "latest-collection,collections,operational-events,portfolios,catalog-tags",
        "fields[videos]": "title,desc,excerpt,is-published,thumb,app-cover,cover,comments-count,likes-count,"
                          "bookmarks-count,is-verified,published-at,option-is-official,option-is-focus-showcase,"
                          "duration,draft,audit-draft,user,comments,category,tags,entries,entities,similarities,"
                          "latest-collection,collections,operational-events,portfolios,catalog-tags,media,djs,albums,"
                          "published-albums",
        "fields[radios]": "title,desc,excerpt,is-published,thumb,app-cover,cover,comments-count,likes-count,"
                          "bookmarks-count,is-verified,published-at,option-is-official,option-is-focus-showcase,"
                          "duration,draft,audit-draft,user,comments,category,tags,entries,entities,similarities,"
                          "latest-collection,collections,operational-events,portfolios,catalog-tags,media,djs,"
                          "latest-album,albums,is-free,is-require-privilege",
        "meta[categories]": ",",
        "meta[users]": ","
    }

    result = {
        'tabs': ['资讯'],
        'site': 'gcores'
    }
    articles = []

    response = requests.get(url, params=params, headers=HEADERS)

    items = response.json()['data']
    for item in items:
        article = {
            'title': item['attributes']['title'],
            'subTitle': item['attributes']['published-at'].replace('T', ' ').split('.')[0],
            'link': f"https://www.gcores.com/articles/{item['id']}",
            'detail': item['attributes']['excerpt'],
            'img_url': f"https://image.gcores.com/{item['attributes']['thumb']}",
            'hot': str(item['attributes']['likes-count']) + ' 喜欢 | ' + str(
                item['attributes']['comments-count']) + ' 评论',
        }
        articles.append(article)
    result['articles'] = articles
    return result
