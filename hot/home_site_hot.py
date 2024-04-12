import datetime
import json

import requests
from bs4 import BeautifulSoup


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/58.0.3029.110 Safari/537.3'
}


# 获取baidu热点 https://top.baidu.com/board
def get_baidu_hot(param='热搜'):
    param_to_tab = {
        '热搜': 'realtime',
        '小说': 'novel',
        '电影': 'movie',
        '电视剧': 'teleplay',
        '汽车': 'car',
        '游戏': 'game'
    }
    tab = param_to_tab[param] if param in param_to_tab else param_to_tab['热搜']
    response = requests.get(f'https://top.baidu.com/board?tab={tab}', headers=HEADERS)

    response_json = json.loads(response.text.split('<!--s-data:')[1].split('--> <div class="bg-wrapper">')[0])
    items = response_json['data']['cards'][0]['content']

    result = {
        'tabs': ['热搜', '小说', '电影', '电视剧', '汽车', '游戏'],
        'site': 'baidu'
    }
    articles = []

    for index, item in enumerate(items):
        article = {
            'title': item['word'],
            'subTitle': ' | '.join(item['show']),
            'link': item['rawUrl'],
            'detail': item['desc'],
            'img_url': item['img'],
            'hot': item['hotScore']
        }
        articles.append(article)

    result['articles'] = articles
    return result


# 获取新浪新闻热榜 https://news.sina.com.cn/hotnews/
def get_sina_hot(param='热搜'):
    # 获取今天日期，格式化成20240401格式
    today = datetime.date.today().strftime('%Y%m%d')
    num = 50

    param_to_url = {
        '热搜': 'https://top.news.sina.com.cn/ws/GetTopDataList.php?top_type=day&top_cat=www_www_all_suda_suda&top_time'
                f'={today}&top_show_num={num}&top_order=DESC&js_var=all_1_data01',

        '社会': 'https://top.news.sina.com.cn/ws/GetTopDataList.php?top_type=day&top_cat=news_society_suda&top_time'
                f'={today}&top_show_num={num}&top_order=DESC&js_var=news_',

        '体育': 'https://top.sports.sina.com.cn/ws/GetTopDataList.php?top_type=day&top_cat=sports_suda&top_time'
                f'={today}&top_show_num={num}&top_order=DESC&js_var=channel_',

        '财经': 'https://top.finance.sina.com.cn/ws/GetTopDataList.php?top_type=day&top_cat=finance_0_suda&top_time'
                f'={today}&top_show_num={num}&top_order=DESC&js_var=channel_',

        '娱乐': f'https://top.ent.sina.com.cn/ws/GetTopDataList.php?top_type=day&top_cat=ent_suda&top_time={today}'
                f'&top_show_num={num}&top_order=DESC&js_var=channel_',

        '科技': 'https://top.tech.sina.com.cn/ws/GetTopDataList.php?top_type=day&top_cat=tech_news_suda&top_time'
                f'={today}&top_show_num={num}&top_order=DESC&js_var=channel_',

        '军事': 'https://top.news.sina.com.cn/ws/GetTopDataList.php?top_type=day&top_cat=news_mil_suda&top_time'
                f'={today}&top_show_num={num}&top_order=DESC&js_var=channel_'
    }
    url = param_to_url[param] if param in param_to_url else param_to_url['热搜']
    response = requests.get(url, headers=HEADERS)

    response_json = json.loads(response.text.split('=')[1].strip()[:-1])
    items = response_json['data']

    result = {
        'tabs': ['热搜', '社会', '体育', '财经', '娱乐', '科技', '军事'],
        'site': 'sina'
    }
    articles = []

    for index, item in enumerate(items):
        article = {
            'title': item['title'],
            'subTitle': item['media'],
            'link': item['url'],
            'detail': '',
            'img_url': '',
            'hot': item['top_num']
        }
        articles.append(article)

    result['articles'] = articles
    return result


# 获取腾讯新闻 https://www.qq.com/
def get_tencent_hot(param='要闻'):
    if param == '':
        param = '要闻'

    if param == '要闻':
        url = 'https://i.news.qq.com/web_feed/getHotModuleList'
    elif param == '问答':
        url = 'https://i.news.qq.com/web_backend/getHotQuestionList'
    elif param == '教育':
        url = 'https://i.news.qq.com/trpc.qqnews_web.kv_srv.kv_srv_http_proxy/list?sub_srv_id=edu&srv_id=pc&offset=0&limit=20&strategy=1&ext={%22pool%22:[%22top%22,%22hot%22],%22is_filter%22:10,%22check_type%22:true}'
    else:
        url = 'https://r.inews.qq.com/web_feed/getPCList'

    param_to_channel_id = {
        '要闻': 'news_news_top',
        '眼界': 'news_news_nchupin',
        '娱乐': 'news_news_ent',
        '体育': 'news_news_sports',
        '财经': 'news_news_finance',
        'NBA': 'news_news_nba',
        '科技': 'news_news_tech',
        '游戏': 'news_news_game',
        '汽车': 'news_news_auto',
        '健康': 'news_news_antip',
        '军事': 'news_news_mil',
        '国际': 'news_news_world',
        '电竞': 'news_news_esport',
        '房产': 'news_news_house',
        '科学': 'news_news_kepu',
    }
    if param == '要闻':
        data = {
            "qimei36": "1_250091009",
            "base_req": {"from": "pc"},
            "flush_num": 1,
            "channel_id": param_to_channel_id['要闻'],
            "device_id": "1_250091009",
            "item_count": 20,
            "forward": "2"
        }
    elif param == '问答' or param == '教育':
        data = {}
    else:
        data = {
            "qimei36": "1_1610053260",
            "forward": "2",
            "base_req": {"from": "pc"},
            "flush_num": 0,
            "channel_id": param_to_channel_id[param],
            "device_id": "1_1610053260",
            "is_local_chlid": ""
        }

    if param == '问答':
        response = requests.get(url, headers=HEADERS)
        items = response.json()['data']['hot_questions']
    elif param == '教育':
        response = requests.get(url, headers=HEADERS)
        items = response.json()['data']['list']
    else:
        response = requests.post(url, json=data, headers=HEADERS)
        items = response.json()['data']

    result = {
        'tabs': ['要闻', '眼界', '问答', '娱乐', '体育', '财经', '教育', 'NBA', '科技', '游戏', '汽车', '健康', '军事',
                 '国际',
                 '电竞', '房产', '科学'],
        'site': 'tencent'
    }
    articles = []

    for index, item in enumerate(items):
        if param == '问答':
            article = {
                'title': item['title'],
                'subTitle': '',
                'link': item['url'],
                'detail': item['main_points'],
                'img_url': item['image'],
                'hot': str(item['read_num']) + ' 阅读'
            }
            articles.append(article)
            continue
        elif param == '教育':
            article = {
                'title': item['title'],
                'subTitle': " | ".join(tag['tag_word'] for tag in item['tags']),
                'link': item['url'],
                'detail': '',
                'img_url': item['thumb_nail_2x'],
                'hot': ''
            }
            articles.append(article)
            continue
        elif item['articletype'] == '525':
            continue
        else:
            article = {
                'title': item['qa_info']['question_title'] if item['articletype'] == '233' else
                (item['short_title'] if 'short_title' in item else item['title']),

                'subTitle': (item['category']['cate1_name'] + ' | ' + item['category']['cate2_name'])
                if item['category'] is not None else '',

                'link': item['link_info']['url'],
                'detail': item['desc'] if 'desc' in item else '',
                'img_url': item['pic_info']['small_img'][0],
                'hot': (str(item['interation_info']['read_num']) + ' 阅读') if 'read_num' in item[
                    'interation_info'] else ''
            }
            articles.append(article)

    result['articles'] = articles
    return result


# 获取网易新闻热榜 https://news.163.com/
def get_wangyi_hot(param='热搜'):
    if param == '':
        param = '热搜'
    param_to_order = {
        '热搜': 'https://news.163.com/',
        '要闻': 'https://news.163.com/special/cm_yaowen20200213/?callback=data_callback',
        '国内': 'https://news.163.com/special/cm_guonei/?callback=data_callback',
        '国际': 'https://news.163.com/special/cm_guoji/?callback=data_callback',
        '独家': 'https://news.163.com/special/cm_dujia/?callback=data_callback',
        '军事': 'https://news.163.com/special/cm_war/?callback=data_callback',
        '财经': 'https://news.163.com/special/cm_money/?callback=data_callback',
        '科技': 'https://news.163.com/special/cm_tech/?callback=data_callback',
        '体育': 'https://news.163.com/special/cm_sports/?callback=data_callback',
        '娱乐': 'https://news.163.com/special/cm_ent/?callback=data_callback',
        '时尚': 'https://news.163.com/special/cm_lady/?callback=data_callback',
        '汽车': 'https://news.163.com/special/cm_auto/?callback=data_callback',
        '航空': 'https://news.163.com/special/cm_hangkong/?callback=data_callback',
        '房产': 'https://news.163.com/special/cm_houseshanghai/?callback=data_callback',
        '健康': 'https://news.163.com/special/cm_jiankang/?callback=data_callback',
    }
    response = requests.get(param_to_order[param], headers=HEADERS)

    if param == '热搜':
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find('div', class_='mt35 mod_hot_rank clearfix').findAll('li')
    else:
        items = json.loads(response.text.replace('data_callback(', '')[:-1])

    result = {
        'tabs': ['热搜', '要闻', '国内', '国际', '独家', '军事', '财经', '科技', '体育', '娱乐', '时尚', '汽车', '航空',
                 '房产', '健康'],
        'site': 'wangyi'
    }
    articles = []

    for item in items:
        if param == '热搜':
            article = {
                'title': item.find('a')['title'],
                'subTitle': '',
                'link': item.find('a')['href'],
                'detail': '',
                'img_url': '',
                'hot': item.find('span').text
            }
            articles.append(article)
        elif param != '要闻' or item['time'] != '':
            article = {
                'title': item['title'],
                'subTitle': '来自：' + item['source'],
                'link': item['docurl'],
                'detail': " | ".join(keyword["keyname"] for keyword in item['keywords']),
                'img_url': item['imgurl'],
                'hot': str(item['tienum']) + ' 跟帖'
            }
            articles.append(article)

    result['articles'] = articles
    return result


# 获取头条热点 https://www.toutiao.com/hot-event/hot-board/
def get_toutiao_hot(param='热榜'):
    url = "https://www.toutiao.com/hot-event/hot-board/"
    params = {
        "origin": "toutiao_pc",
        "_signature": "_02B4Z6wo00d01QWLvJQAAIDDi6OWPW2K620Fr7gAACdn62Aom7bB9BucUc"
                      ".JMGMS9LmVq7b1bIFoXSG4QiQo55SACPOfirYukcOcv.qVCRDKE0-oAsO-rOI0.S2YN4-z-McJvKdW0A-0LmZGe1"
    }
    response = requests.get(url, headers=HEADERS, params=params)
    items = response.json()['data']

    result = {
        'tabs': ['热榜'],
        'site': 'toutiao'
    }
    articles = []

    for item in items:
        article = {
            'title': item['Title'],
            'link': item['Url'],
            'detail': '',
            'img_url': item['Image']['url'],
            'hot': item['HotValue']
        }
        articles.append(article)

    result['articles'] = articles
    return result


# 获取凤凰网新闻 https://www.ifeng.com/
def get_ifeng_hot(param='要闻'):
    if param == '':
        param = '要闻'

    param_to_url = {
        '要闻': 'https://news.ifeng.com/',
        '财经': 'https://finance.ifeng.com/',
        '军事': 'https://mil.ifeng.com/',
        '科技': 'https://shankapi.ifeng.com/season/tech/selectedPoolData/20002/203/getSelectedPoolDataCb20002?callback=getSelectedPoolDataCb20002',
        '数码': 'https://tech.ifeng.com/digi/',
        '旅游': 'https://travel.ifeng.com/',
        '汽车': 'https://auto.ifeng.com/',
        '体育': 'https://sports.ifeng.com/',
        '娱乐': 'https://ent.ifeng.com/',
        '酒业': 'https://jiu.ifeng.com/',
        '评测': 'https://pingce.ifeng.com/',
        '房产': 'https://fengcx.com/',
        '读书': 'https://culture.ifeng.com/',
        '健康': 'https://health.ifeng.com/',
        '国学': 'https://guoxue.ifeng.com/',
        '佛教': 'https://fo.ifeng.com/',
        '教育': 'https://edu.ifeng.com/',
        '家居': 'https://home.ifeng.com/',
    }
    response = requests.get(param_to_url[param], headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')

    if param == '财经':
        items = json.loads(
                soup.findAll('script')[6].text.split('var adKeys')[0].strip().replace('var allData = ', '')[:-1])[
                'newsData']
    elif param == '军事':
        json_data = json.loads(
            soup.findAll('script')[2].text.split('var adKeys')[0].strip().replace('var allData = ', '')[:-1])
        items = json_data['newsStream0'] + json_data['newsStream1'] + json_data['newsStream2'] + json_data[
            'newsStream3']
    elif param == '科技':
        items = json.loads(response.text.replace('getSelectedPoolDataCb20002(', '')[:-1])['data']
    elif param == '旅游':
        json_data = json.loads(
            soup.findAll('script')[3].text.split('var adKeys')[0].strip().replace('var allData = ', '')[:-1])
        items = (json_data['news1'] + json_data['jzContent'] + json_data['globalGoContent'] + json_data[
            'globalNewsContent']
                 + json_data['globalGoAndChinaGlGContent'] + json_data['globalGoAndChinaChContent'] + json_data[
                     'addictedConent']
                 + json_data['appreciationTabConent'] + json_data['travelWayOnWay'] + json_data['travelWaySelfDrive']
                 + json_data['travelWayLiner'] + json_data['travelWayFly'] + json_data['swimsConent'])
    elif param == '汽车':
        json_data = json.loads(
            soup.findAll('script')[4].text.split('var adData')[0].strip().replace('var allData = ', '')[:-1])
        items = json_data['newsstream0'] + json_data['newsstream1']
    elif param == '娱乐':
        json_data = json.loads(
            soup.findAll('script')[3].text.split('var adKeys')[0].strip().replace('var allData = ', '')[:-1])
        items = (json_data['slider'] + json_data['sliderEditor'] + json_data['topNews'] + json_data['topNewsEditor']
                 + json_data['topNewsEditorEnd'] + json_data['specialSlider'] + json_data['entVideo'] + json_data[
                     'mingXingTop']
                 + json_data['mingXingContent'] + json_data['movieTop'] + json_data['movieContent'] + json_data[
                     'tvShowTop']
                 + json_data['tvShowContent'] + json_data['musicTop'] + json_data['musicContent'] + json_data['idolife']
                 + json_data['alternative'] + json_data['publicShow'] + json_data['entertainment'] + json_data[
                     'movieBang']
                 + json_data['showRecom'])
    elif param == '房产':
        items = soup.find('ul', class_='news-list-pc').findAll('div', class_='newslist')
    elif param == '读书' or param == '健康' or param == '国学' or param == '佛教' or param == '教育':
        json_data = json.loads(
            soup.findAll('script')[2].text.split('var adKeys')[0].strip().replace('var allData = ', '')[:-1])
        items = []
        for data in json_data['mainData']:
            if data['chip'] and type(data['data']) is not str:
                items.extend(data['data'])
        items.extend(json_data['newsstream'])
        for data in json_data['asideData']:
            if data['chip'] and type(data['data']) is not str:
                items.extend(data['data'])
    elif param == '家居':
        json_data = json.loads(
            soup.findAll('script')[2].text.split('var adKeys')[0].strip().replace('var allData = ', '')[:-1])
        items = json_data['topslide'] + json_data['homenews'] + json_data['hotnewsauto'] + json_data['branddy']
        for data in (json_data['todyhot'] + json_data['dongjianhot'] + json_data['lifehot']
                     + json_data['qxjhot'] + json_data['sjxwchot'] + json_data['hwtjhot'] + json_data['hwtjhot']):
            if len(data) > 0:
                items.extend(data)
    else:
        items = json.loads(
                soup.findAll('script')[2].text.split('var adKeys')[0].strip().replace('var allData = ', '')[:-1])[
                'newsstream']

    result = {
        'tabs': ['要闻', '财经', '军事', '科技', '数码', '旅游', '汽车', '体育', '娱乐', '酒业', '评测', '房产', '读书',
                 '健康', '国学', '佛教', '教育', '家居'],
        'site': 'fenghuang'
    }
    articles = []

    for index, item in enumerate(items):
        if param == '房产':
            article = {
                'title': item.find('div', class_='title').text,
                'subTitle': ' | '.join(
                    span.text for span in item.find('span', class_='tagWrap').findAll('span')) if item.find('span',
                                                                                                            class_='tagWrap') is not None else '',
                'link': item.find('a')['href'],
                'detail': item.find('div', class_='desc').text if item.find('div', class_='desc') is not None else '',
                'img_url': item.find('img')['src'],
                'hot': ''
            }
            articles.append(article)
            continue

        if param == '财经':
            img_url = item['thumbnail'] if 'thumbnail' in item else ''
        elif param == '旅游':
            img_url = item['thumbnails'] if 'thumbnails' in item else ''
        elif param == '娱乐' or param == '读书' or param == '健康' or param == '国学' or param == '佛教' or param == '教育' or param == '家居':
            img_url = item['thumbnail'] if 'thumbnail' in item else (
                item['thumbnails']['image'][0]['url'] if len(item['thumbnails']['image']) > 0 else '')
        else:
            img_url = item['thumbnails']['image'][0]['url'] if len(item['thumbnails']['image']) > 0 else ''

        article = {
            'title': item['title'],
            'subTitle': item['summary'] if 'summary' in item else '',
            'link': item['url'],
            'detail': item['newsTime'] if 'newsTime' in item else '',
            'img_url': img_url,
            'hot': ''
        }
        articles.append(article)

    result['articles'] = articles
    return result


# 获取MSN微软中国新闻 https://www.msn.cn/zh-cn/
def get_msn_hot(param='要闻'):
    if param == '':
        param = '要闻'
    param_to_url = {
        '要闻': 'https://assets.msn.cn/service/news/feed/pages/channelfeed?InterestIds=Y_77f04c37-b63e-46b4-a990-e926f7d129ff&activityId=ED044C58-761A-438C-8FB9-2184E65F9826&apikey=0QfOX3Vn51YCzitbLaRkTTBadtWpgTN8NZLW0C1SEM&cm=zh-cn&it=web&memory=8&scn=ANON&timeOut=2000&user=m-295E8B528B7763E01A2F9ADE8A1C62B7',
        '娱乐': 'https://assets.msn.cn/service/news/feed/pages/channelfeed?InterestIds=Y_ffca5126-f1eb-4232-a09d-0cc253506007&activityId=D4F8C325-5C91-4844-950F-EBF1956536C4&apikey=0QfOX3Vn51YCzitbLaRkTTBadtWpgTN8NZLW0C1SEM&cm=zh-cn&it=web&memory=8&scn=ANON&timeOut=2000&user=m-295E8B528B7763E01A2F9ADE8A1C62B7',
        '生活': 'https://assets.msn.cn/service/news/feed/pages/channelfeed?InterestIds=Y_21b7d513-d3fa-45e0-91c8-c9a2ea25272f&activityId=AADF99E1-72B4-4C94-B1E7-2DFEFCE22C40&apikey=0QfOX3Vn51YCzitbLaRkTTBadtWpgTN8NZLW0C1SEM&cm=zh-cn&it=web&memory=8&scn=ANON&timeOut=2000&user=m-295E8B528B7763E01A2F9ADE8A1C62B7',
        '教育': 'https://assets.msn.cn/service/news/feed/pages/channelfeed?InterestIds=Y_0319d67d-6e91-4b00-8ed8-0f3d5f957680&activityId=BB52B21E-E0ED-45EE-B18C-5ECD798961F2&apikey=0QfOX3Vn51YCzitbLaRkTTBadtWpgTN8NZLW0C1SEM&cm=zh-cn&it=web&memory=8&scn=ANON&timeOut=2000&user=m-295E8B528B7763E01A2F9ADE8A1C62B7',
        '科技': 'https://assets.msn.cn/service/news/feed/pages/channelfeed?InterestIds=Y_49e75779-668d-4379-952f-8f366d0a1acf&activityId=55A8AF82-496B-46D3-905F-BFCF444109BE&apikey=0QfOX3Vn51YCzitbLaRkTTBadtWpgTN8NZLW0C1SEM&cm=zh-cn&it=web&memory=8&scn=ANON&timeOut=2000&user=m-295E8B528B7763E01A2F9ADE8A1C62B7',
        '悦读天下': 'https://assets.msn.cn/service/news/feed/pages/channelfeed?InterestIds=Y_b2251eaa-d926-441a-97de-ce74046fc6a8&activityId=D046C3C4-AA71-4729-AD54-73E12D07B7FD&apikey=0QfOX3Vn51YCzitbLaRkTTBadtWpgTN8NZLW0C1SEM&cm=zh-cn&it=web&memory=8&scn=ANON&timeOut=2000&user=m-295E8B528B7763E01A2F9ADE8A1C62B7',
        '健康': 'https://assets.msn.cn/service/MSN/Feed?$skip=16&$top=30&DisableTypeSerialization=true&activityId=8ECC7B5D-0C44-498E-8743-EA95E6A5BA7B&apikey=FywQv6H345wNCU4yKWraF2esI9qiMQFx90v53mMHrm&cipenabled=false&cm=zh-cn&contentType=article,video,slideshow,webcontent&ids=Y_1e23f79e-6b1a-4983-b97c-8834d8ce3388&infopaneCount=10&it=web&location=30.2766|120.1188&ocid=health-verthp-feeds&queryType=myfeed&responseSchema=cardview&scn=ANON&timeOut=1000&user=m-295E8B528B7763E01A2F9ADE8A1C62B7&wrapodata=false',
        '美食': 'https://assets.msn.cn/service/MSN/Feed?$top=10&DisableTypeSerialization=true&activityId=B03DC41C-617B-4FE6-8D74-7CA319B81BF3&apikey=0QfOX3Vn51YCzitbLaRkTTBadtWpgTN8NZLW0C1SEM&cm=zh-cn&contentType=article,video,slideshow,link,content360&delta=true&ids=Y_82678d1b-b69e-4790-b964-8f2f7b0b3827&it=web&location=30.2766|120.1188&ocid=hponeservicefeed&queryType=myfeed&responseSchema=cardview&scn=ANON&timeOut=1000&user=m-295E8B528B7763E01A2F9ADE8A1C62B7&wrapodata=false',
        '旅游': 'https://assets.msn.cn/service/MSN/Feed?$top=30&DisableTypeSerialization=true&activityId=77CCEE8C-160A-4839-8F85-912B758206DF&apikey=8RwD77wJgNQmmVBdGmZsK6vvPCrG58iRCQRoPsE4JJ&cipenabled=false&cm=zh-cn&contentType=article,video,slideshow,webcontent&ids=Y_c62c26e0-d1da-4ae9-b96e-2328e72ba8ac&infopaneCount=10&it=web&location=30.2766|120.1188&ocid=travel-verthp-feeds&queryType=myfeed&responseSchema=cardview&scn=ANON&timeOut=1000&user=m-295E8B528B7763E01A2F9ADE8A1C62B7&wrapodata=false',
        '萌宠': 'https://assets.msn.cn/service/news/feed/pages/channelfeed?InterestIds=Y_bbdcb2fa-e4e3-4188-8982-0034230d4101&activityId=B2B591A2-342B-4D7F-ACA0-94349A322586&apikey=0QfOX3Vn51YCzitbLaRkTTBadtWpgTN8NZLW0C1SEM&cm=zh-cn&it=web&memory=8&scn=ANON&timeOut=2000&user=m-295E8B528B7763E01A2F9ADE8A1C62B7',
        '星座': 'https://assets.msn.cn/service/news/feed/pages/channelfeed?InterestIds=Y_5b4dd9be-cd6c-44ca-b8c7-c17f26a2acac&activityId=2A591FCF-4143-4C82-BCE6-26DE7E6543D5&apikey=0QfOX3Vn51YCzitbLaRkTTBadtWpgTN8NZLW0C1SEM&cm=zh-cn&it=web&memory=8&scn=ANON&timeOut=2000&user=m-295E8B528B7763E01A2F9ADE8A1C62B7',
    }
    if param == '财经':
        items = requests.get('https://assets.msn.cn/service/MSN/Feed/me?$top=30&DisableTypeSerialization=true&activityId=CA107B23-0182-4394-8840-08C88F21328A&apikey=0QfOX3Vn51YCzitbLaRkTTBadtWpgTN8NZLW0C1SEM&cm=zh-cn&contentType=article,video,slideshow&it=web&location=30.2766|120.1188&ocid=finance-verthp-feeds&query=ef_finance_trending_growth&queryType=entityfeed&responseSchema=cardview&scn=ANON&timeOut=2000&user=m-295E8B528B7763E01A2F9ADE8A1C62B7&wrapodata=false', headers=HEADERS).json()['subCards']
        sub_cards = requests.get('https://assets.msn.cn/service/MSN/Feed/me?$top=30&DisableTypeSerialization=true&activityId=CA107B23-0182-4394-8840-08C88F21328A&apikey=0QfOX3Vn51YCzitbLaRkTTBadtWpgTN8NZLW0C1SEM&cm=zh-cn&contentType=article,video,slideshow&infopaneCount=5&it=web&location=30.2766|120.1188&ocid=finance-verthp-feeds&query=finance_news&queryType=myfeed&responseSchema=cardview&scn=ANON&timeOut=3000&user=m-295E8B528B7763E01A2F9ADE8A1C62B7&wrapodata=false', headers=HEADERS).json()['subCards']
        for index, card in enumerate(sub_cards):
            if index == 0:
                items.extend(card['subCards'])
            else:
                items.append(card)
    elif param == '体育':
        items = requests.get('https://assets.msn.com/service/news/feed?activityId=42219EAB-F9EF-454D-BC36-D794D7FE9C45&apikey=kO1dI4ptCTTylLkPL1ZTHYP8JhLKb8mRDoA5yotmNJ&cm=zh-cn&contentType=article%2Cvideo&ids=Y_da8de783-28cd-4248-9b12-ca42f01520ff&infopaneCount=0&it=web&market=zh-cn&ocid=sports-vertical-landing&queryType=myFeed&scn=ANON&skip=0&timeOut=3000&top=8&user=m-295E8B528B7763E01A2F9ADE8A1C62B7', headers=HEADERS).json()['value'][0]['subCards']
        sub_sections = requests.get('https://assets.msn.cn/service/news/feed/pages/ntpxfeed?InterestIds=Y_da8de783-28cd-4248-9b12-ca42f01520ff&User=m-295E8B528B7763E01A2F9ADE8A1C62B7&activityId=42219EAB-F9EF-454D-BC36-D794D7FE9C45&apikey=kO1dI4ptCTTylLkPL1ZTHYP8JhLKb8mRDoA5yotmNJ&audienceMode=adult&cm=zh-cn&contentType=article,video,slideshow,webcontent&it=web&memory=8&newsSkip=8&newsTop=48&ocid=sports-league-landing&private=1&rid=42219eabf9ef454dbc36d794d7fe9c45&scn=ANON&timeOut=1500&vpSize=1536x242&wposchema=byregion', headers=HEADERS).json()['sections'][0]['subSections']
        for section in sub_sections:
            for card in section['cards']:
                if 'title' in card:
                    items.append(card)
    elif param == '汽车':
        sub_sections = requests.get('https://assets.msn.cn/service/news/feed/pages/ntpxfeed?InterestIds=Y_a66938e0-1d0f-4e74-9a37-a8a2513a59f0&User=m-295E8B528B7763E01A2F9ADE8A1C62B7&apikey=0QfOX3Vn51YCzitbLaRkTTBadtWpgTN8NZLW0C1SEM&audienceMode=adult&cm=zh-cn&contentType=article,video,slideshow,webcontent&duotone=true&it=web&memory=8&newsSkip=0&newsTop=48&ocid=anaheim-ntp-feeds&private=1&rid=f8944135b1cd46c48a33473b24ffc993&scn=ANON&timeOut=1000&vpSize=1536x439&wposchema=byregion', headers=HEADERS).json()['sections'][0]['subSections']
        items = []
        for card in sub_sections[0]['cards'][0]['subCards']:
            if 'title' in card:
                items.append(card)
        for section in sub_sections:
            for card in section['cards']:
                if 'title' in card:
                    items.append(card)
    elif param == '旅游':
        response = requests.get(param_to_url[param], headers=HEADERS)
        next_page_url = response.json()['nextPageUrl']
        sub_cards = response.json()['subCards']
        items = sub_cards[0]['subCards'] + sub_cards[1:]
        response = requests.get(next_page_url, headers=HEADERS)
        items.extend(response.json()['subCards'])
    elif param == '游戏':
        sub_sections = requests.get('https://assets.msn.cn/service/news/feed/pages/gamingfeed?InterestIds=Y_45de0d85-5a67-4f14-a85f-b9a750271d50&User=m-295E8B528B7763E01A2F9ADE8A1C62B7&activityId=C0F7633C-F404-4D82-A486-1A12C2311DD9&apikey=0QfOX3Vn51YCzitbLaRkTTBadtWpgTN8NZLW0C1SEM&audienceMode=adult&cm=zh-cn&contentType=article,video,slideshow,webcontent,esports&duotone=true&infopaneCount=17&it=web&memory=8&newsSkip=0&newsTop=48&ocid=anaheim-ntp-feeds&private=1&scn=ANON&timeOut=1500&vpSize=1536x170&wposchema=byregion', headers=HEADERS).json()['sections'][0]['subSections']
        items = []
        for card in sub_sections[0]['cards'][0]['subCards']:
            if 'title' in card:
                items.append(card)
        for section in sub_sections:
            for card in section['cards']:
                if 'title' in card:
                    items.append(card)
    else:
        response = requests.get(param_to_url[param], headers=HEADERS)
        next_page_url = response.json()['nextPageUrl']
        items = response.json()['sections'][0]['cards'] if param != '健康' and param != '美食' else response.json()['subCards']
        response = requests.get(next_page_url, headers=HEADERS)
        items.extend(response.json()['sections'][0]['cards'] if param != '健康' and param != '美食' else response.json()['subCards'])

    result = {
        'tabs': ['要闻', '娱乐', '生活', '财经', '教育', '科技', '体育', '悦读天下', '健康', '美食', '旅游', '汽车', '游戏', '萌宠', '星座'],
        'site': 'msn'
    }
    articles = []

    for item in items:
        article = {
            'title': item['title'],
            'subTitle': item['provider']['name'] + ' | ' + item['publishedDateTime'].replace('T', ' ').replace('Z', ''),
            'link': item['url'],
            'detail': item['abstract'],
            'img_url': item['images'][0]['url'] if 'images' in item else '',
            'hot': ''
        }
        articles.append(article)

    result['articles'] = articles
    return result
