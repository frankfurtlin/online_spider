import datetime
import time
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/58.0.3029.110 Safari/537.3'
}


# 获取weibo热点 https://weibo.com
def get_weibo_hot(param='热搜'):
    if param == '':
        param = '热搜'

    weibo_headers = {
        'cookie': 'SCF=ArAW9t5j05RX6Xhf2A-3J3-VMYRZi52Lnvcb4BtTHAWdhreBaaLVFfr9IEdy_Zr3sDf5nrpsjSBldsMnBialzmg.; ALF=1713835383; SUB=_2AkMT6V4cf8NxqwFRmPAQzG3jbIp1ywnEieKlta_HJRMxHRl-yT9kqhMetRB6OGlw85NSIqP_Bln5y57Kahn1rBw9_umZ; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WhyaFr8K4RQsX-x7OW932r9; SINAGLOBAL=681242051596.9175.1710571336873; XSRF-TOKEN=PftPJU8bqZHp-eqFO8KkdK5w; _s_tentry=localhost:3000; UOR=www.kugou.com,service.weibo.com,localhost:3000; Apache=3834341385417.486.1711859043676; ULV=1711859043733:9:3:1:3834341385417.486.1711859043676:1711166018094; WBPSESS=eyDLPcU90tHVPRrsWrtAPoxANF48eX03QnTsSxJLi-Pye7en8H1m5w4l_PITRMlwRUHfxELvqibnqbZ_1iRZMVBbMUJFwa-zNGcl6c7i79hQ6wAC3IpXn6saI18651vRq8eReC2jZkzZSsyCwUGOOYb5vtlSrOqlXjyi0rcTWPA='
    }
    weibo_headers.update(HEADERS)

    result = {
        'tabs': ['热搜', '文娱', '要闻'],
        'site': 'weibo',
    }
    articles = []

    if param == '热搜':
        data = requests.get('https://weibo.com/ajax/side/hotSearch', headers=weibo_headers).json()['data']
        for item in data['hotgovs']:
            article = {
                'title': item['word'],
                'subTitle': '',
                'link': f"https://s.weibo.com/weibo?q={quote(item['word'])}",
                'detail': f'上榜时间: {datetime.datetime.fromtimestamp(item["stime"]).strftime("%m-%d %H:%M")}',
                'img_url': '',
                'hot': ' '
            }
            articles.append(article)

        for item in data['realtime']:
            if 'ad_channel' in item:
                link = f"https://s.weibo.com/weibo?q={quote(item['name'])}"
                detail = f"广告类型: {item['ad_type']}" if 'ad_type' in item else '商业广告'
                hot = ' '
            else:
                link = f"https://s.weibo.com/weibo?q={quote(item['word_scheme'])}"
                detail = f'上榜时间: {datetime.datetime.fromtimestamp(item["onboard_time"]).strftime("%m-%d %H:%M")}'
                hot = item['num']

            article = {
                'title': item['word'],
                'subTitle': '',
                'link': link,
                'detail': detail,
                'img_url': '',
                'hot': hot
            }
            articles.append(article)
    elif param == '文娱':
        response = requests.get('https://weibo.com/ajax/statuses/entertainment', headers=weibo_headers)
        items = response.json()['data']['band_list']
        for item in items:
            article = {
                'title': item['word'],
                'subTitle': ' | '.join(list(item['subject_querys'].keys())),
                'link': f"https://s.weibo.com/weibo?q={quote(item['word'])}",
                'detail': f'上榜时间: {datetime.datetime.fromtimestamp(item["onboard_time"]).strftime("%m-%d %H:%M")}',
                'img_url': '',
                'hot': item['num']
            }
            articles.append(article)
    elif param == '要闻':
        items = requests.get('https://weibo.com/ajax/statuses/news', headers=weibo_headers).json()['data']['band_list']
        for item in items:
            article = {
                'title': item['topic'],
                'subTitle': item['claim'].split('_')[-1],
                'link': f"https://s.weibo.com/weibo?q=%23{quote(item['topic'])}%23",
                'detail': item['summary'],
                'img_url': '',
                'hot': item['read']
            }
            articles.append(article)

    result['articles'] = articles
    return result


# 获取抖音热榜 https://douyin.com
def get_douyin_hot(param='热榜'):
    if param == '':
        param = '热榜'

    param_to_url = {
        '热榜': 'https://www.douyin.com/aweme/v1/web/hot/search/list/?device_platform=webapp&aid=6383&channel=channel_pc_web&detail_list=1&source=6&board_type=0&board_sub_type=&pc_client_type=1&version_code=290100&version_name=29.1.0&cookie_enabled=true&screen_width=1536&screen_height=864&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=123.0.0.0&browser_online=true&engine_name=Blink&engine_version=123.0.0.0&os_name=Windows&os_version=10&cpu_core_num=16&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=100&webid=7279439812141352448&msToken=xjM8LvEblV6EJpZ_X10nmI-fGnOuLGKuQYTLZuQzQgIQbj-d1NFrkapP0Ot7iumAhR_iFRBcDidBUzSLho0D1FZicjFv4jKi3oIdasaFVF1XT5nxxTwwAWquUssVlleo&X-Bogus=DFSzswVY%2FW0ANnTJt5kou1VIVi5j&a_bogus=EJW0BQz6DEfNgf6156VLfY3q6RN3YMBF0trEMD2f%2FxVcjy39HMOB9exLXSUvdjYjLT%2FAIeujy4hbT3ohrQVr01wf9W0L%2F25ksDSkKl5Q5xSSs1X9eghgJ04qmkt5SMx2RvB-rOXmqXBHFmLk09oHmhK4bIOwu3GMkj%3D%3D',
        '娱乐榜': 'https://www.douyin.com/aweme/v1/web/hot/search/list/?device_platform=webapp&aid=6383&channel=channel_pc_web&detail_list=1&source=6&board_type=2&board_sub_type=2&pc_client_type=1&version_code=290100&version_name=29.1.0&cookie_enabled=true&screen_width=1536&screen_height=864&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=123.0.0.0&browser_online=true&engine_name=Blink&engine_version=123.0.0.0&os_name=Windows&os_version=10&cpu_core_num=16&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=100&webid=7279439812141352448&msToken=QpiSJvOT_M6j17ke-vzRMxS4JwI9vqfN-Ob0bL4Pg9AjGRE7WL6As9UewwDXiAjkfbYT2HqKpMyHqTc_o6mO05HkO3RJWM2S4mXcEhnOpaIMNrEoBLs3sQa9z1YE1dv8&X-Bogus=DFSzswVuoYkANHFwt5kqUqVIVi2E&a_bogus=mJmMM5LXdDVigDy156VLfY3q61H3YBaK0trEMD2fCnvbag39HMPU9exEXS4vshEjLT%2FAIeujy4hbT3ohrQVr01wf9W0L%2F25ksDSkKl5Q5xSSs1X9eghgJ04qmkt5SMx2RvB-rOXmqXBHFmLk09oHmhK4bIOwu3GMFf%3D%3D',
        '社会榜': 'https://www.douyin.com/aweme/v1/web/hot/search/list/?device_platform=webapp&aid=6383&channel=channel_pc_web&detail_list=1&source=6&board_type=2&board_sub_type=4&pc_client_type=1&version_code=290100&version_name=29.1.0&cookie_enabled=true&screen_width=1536&screen_height=864&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=123.0.0.0&browser_online=true&engine_name=Blink&engine_version=123.0.0.0&os_name=Windows&os_version=10&cpu_core_num=16&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=100&webid=7279439812141352448&msToken=QpiSJvOT_M6j17ke-vzRMxS4JwI9vqfN-Ob0bL4Pg9AjGRE7WL6As9UewwDXiAjkfbYT2HqKpMyHqTc_o6mO05HkO3RJWM2S4mXcEhnOpaIMNrEoBLs3sQa9z1YE1dv8&X-Bogus=DFSzswVuCmhANHFwt5kqvqVIVi2v&a_bogus=xfmMBRwXdkgN6d6d56VLfY3q61P3YBaK0trEMD2ftxvbP639HMYX9exEXS4v44DjLT%2FAIeujy4hbT3ohrQVr01wf9W0L%2F25ksDSkKl5Q5xSSs1X9eghgJ04qmkt5SMx2RvB-rOXmqXBHFmLk09oHmhK4bIOwu3GMzj%3D%3D',
        '挑战榜': 'https://www.douyin.com/aweme/v1/web/hot/search/list/?device_platform=webapp&aid=6383&channel=channel_pc_web&detail_list=1&source=6&board_type=2&board_sub_type=hotspot_challenge&pc_client_type=1&version_code=290100&version_name=29.1.0&cookie_enabled=true&screen_width=1536&screen_height=864&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=123.0.0.0&browser_online=true&engine_name=Blink&engine_version=123.0.0.0&os_name=Windows&os_version=10&cpu_core_num=16&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=100&webid=7279439812141352448&msToken=QpiSJvOT_M6j17ke-vzRMxS4JwI9vqfN-Ob0bL4Pg9AjGRE7WL6As9UewwDXiAjkfbYT2HqKpMyHqTc_o6mO05HkO3RJWM2S4mXcEhnOpaIMNrEoBLs3sQa9z1YE1dv8&X-Bogus=DFSzswVu7IUANHFwt5kqIHVIVi5G&a_bogus=DfRMMD0hmDVBhV6p56VLfY3q65F3YBaK0trEMD2fbxvbU639HMPj9exEXS4vFIyjLT%2FAIeujy4hbT3ohrQVr01wf9W0L%2F25ksDSkKl5Q5xSSs1X9eghgJ04qmkt5SMx2RvB-rOXmqXBHFmLk09oHmhK4bIOwu3GM5E%3D%3D',
    }

    douyin_headers = {
        'Cookie': 'xgplayer_user_id=954223654578; store-region=cn-zj; store-region-src=uid; bd_ticket_guard_client_web_domain=2; live_use_vvc=%22false%22; my_rd=2; dy_swidth=1536; dy_sheight=864; _bd_ticket_crypt_doamin=2; __security_server_data_status=1; xgplayer_device_id=83982547968; __live_version__=%221.1.1.8232%22; passport_assist_user=CkGkSUQN5NDxSLIhcuaMw28PspLnzGs1eZpTWVhCnFVYsganKUpjIrlMXqa6Y3sOANFxDcoL6vRWL2zWbCjxsj6uBRpKCjz8yzs9BIZ3lIKMbJJ9nHQb2Otv314NPFyyxf-FdmDZOB5QxSPKsKL5Q3khhkvq9q2I4T-rcPwdFjBEu4gQ9-HKDRiJr9ZUIAEiAQMflYFG; n_mh=-WIktPPolbYQZ5VqgRsIvFrdvqOW5BELw9ab69tzxGM; sso_uid_tt=07299bda4bcb3574d0c4509c55f4ea9e; sso_uid_tt_ss=07299bda4bcb3574d0c4509c55f4ea9e; toutiao_sso_user=37efeb09b942f67e9466d267bc02571a; toutiao_sso_user_ss=37efeb09b942f67e9466d267bc02571a; sid_ucp_sso_v1=1.0.0-KGJlZjFlNDZjNTQ2ZTMyNTQyNzkyYTY0NzI0ODQ5YjJhMWM2OTAwM2EKHwisu_DimfSaAhDvsYavBhjvMSAMMPyL5-gFOAZA9AcaAmhsIiAzN2VmZWIwOWI5NDJmNjdlOTQ2NmQyNjdiYzAyNTcxYQ; ssid_ucp_sso_v1=1.0.0-KGJlZjFlNDZjNTQ2ZTMyNTQyNzkyYTY0NzI0ODQ5YjJhMWM2OTAwM2EKHwisu_DimfSaAhDvsYavBhjvMSAMMPyL5-gFOAZA9AcaAmhsIiAzN2VmZWIwOWI5NDJmNjdlOTQ2NmQyNjdiYzAyNTcxYQ; passport_auth_status=00217bdddd17ad067d9ce6e7996afb33%2C772378561c0b38d713e9b9c762826c8e; passport_auth_status_ss=00217bdddd17ad067d9ce6e7996afb33%2C772378561c0b38d713e9b9c762826c8e; uid_tt=d14a9689b5a92559ca796d574f33e277; uid_tt_ss=d14a9689b5a92559ca796d574f33e277; sid_tt=e313235c60de9c20e3d1422f9935b5e9; sessionid=e313235c60de9c20e3d1422f9935b5e9; sessionid_ss=e313235c60de9c20e3d1422f9935b5e9; LOGIN_STATUS=1; _bd_ticket_crypt_cookie=0198b972b7052dadc4ebf80181b3a792; sid_guard=e313235c60de9c20e3d1422f9935b5e9%7C1709283572%7C5183998%7CTue%2C+30-Apr-2024+08%3A59%3A30+GMT; sid_ucp_v1=1.0.0-KGEzYzIxN2U1OTc4YjY0MTIzNzY2NGY3YjYxMmU5YzE0MWZkZDgzOTgKGwisu_DimfSaAhD0sYavBhjvMSAMOAZA9AdIBBoCbGYiIGUzMTMyMzVjNjBkZTljMjBlM2QxNDIyZjk5MzViNWU5; ssid_ucp_v1=1.0.0-KGEzYzIxN2U1OTc4YjY0MTIzNzY2NGY3YjYxMmU5YzE0MWZkZDgzOTgKGwisu_DimfSaAhD0sYavBhjvMSAMOAZA9AdIBBoCbGYiIGUzMTMyMzVjNjBkZTljMjBlM2QxNDIyZjk5MzViNWU5; ttwid=1%7CxeVVwlx-OXfhqgW-cINpmwQvtLZO0szAywKTMlB7-PM%7C1709808610%7C3beee4a3d1681b2a55432ed777067f4768bea300db3fcdda93cdbc6a3dc11c6a; pwa2=%220%7C0%7C3%7C0%22; douyin.com; device_web_cpu_core=16; device_web_memory_size=8; architecture=amd64; csrf_session_id=c257f56294bb1274d2723c2a4ef629d3; strategyABtestKey=%221711093312.444%22; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Afalse%2C%22volume%22%3A1%7D; passport_csrf_token=c240148944aa4fccfd8c6d13f59453fc; passport_csrf_token_default=c240148944aa4fccfd8c6d13f59453fc; publish_badge_show_info=%220%2C0%2C0%2C1711093313381%22; xg_device_score=7.78551698226827; __ac_signature=_02B4Z6wo00f01bAssrQAAIDDPgSYHvuWnOmwDLYAAAn3xCxpK3UGoKNebnnu150OoopD7pd6Lu1lblxyoMi4qNReqdJpTw0QFbV421c7DLWbM9U8yuKxLSc3mseKBMbkoa-xpF-S2Zdk.XrM3e; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A1%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A0%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A0%7D%22; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAATAfNoho0J3AlYyR806gu8f1XiYTkhC_PPrhTPcwGMGopnj1QXCwgFEMC-fGlbumQ%2F1711123200000%2F1711094529114%2F0%2F1711098594522%22; download_guide=%222%2F20240322%2F0%22; odin_tt=c7a4601095a0c2a33d9df06ce42fbaf928e2da555e9b4eb667a4dcd83b1a2c5d89643ade1f6648c4eaf701eccef1ecb4ee418bf052e234432df912bdc5f3123e; IsDouyinActive=true; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1536%2C%5C%22screen_height%5C%22%3A864%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A16%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A50%7D%22; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCTG50NGxBUlovTVhJbmUyQU9ydDZIZnJlZWFjVHJrbmhUdFhmeW45eGRKY3ZSU1A0N0VYWGNhOGNLSDhoY3Nid1lJdlJpSXJ3dkhib2J2RTJzWGRrbzg9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoxfQ%3D%3D; passport_fe_beating_status=true; home_can_add_dy_2_desktop=%221%22; msToken=3zkwCAgY-cMAyuWue0CAgC2bE4vuPnqnXHCE8EKLPuf6L-ppcP1mCoGD1alRRBiaptuys7TVXAXYsUzbCmAc01sRRZq2AXA4gHd5VXdFCqCg-kJ1XalSOPmQU1tYyV_K; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAATAfNoho0J3AlYyR806gu8f1XiYTkhC_PPrhTPcwGMGopnj1QXCwgFEMC-fGlbumQ%2F1711123200000%2F0%2F1711110171462%2F0%22; msToken=eDUZmWTUva8XHXKKomq-mxVJuy7ddg3UVeRDkc3_8bPjdBnbRqBNGtSEHawIUyU1HQBkn52nIhQd-gnqf3gecKr_FmCfWLlE1FkQ7AJhi3OAEO_4VHg-GuHtzhTZ8f0n; tt_scid=ugobMuo4CarC2zI9jAZtyphDC4omzCSPxlwSoEqmWPO.FR5e48-Qc34D2okWwLzd6daa',
        'Referer': 'https://www.douyin.com/discover'
    }
    douyin_headers.update(HEADERS)

    response = requests.get(param_to_url[param], headers=douyin_headers)
    items = response.json()['data']['word_list']

    result = {
        'tabs': ['热榜', '娱乐榜', '社会榜', '挑战榜'],
        'site': 'douyin',
    }
    articles = []

    for index, item in enumerate(items):
        if index == 0 and param == '热榜':
            continue
        article = {
            'title': item['word'],
            'subTitle': datetime.datetime.fromtimestamp(item['event_time']).strftime('%m-%d %H:%M'),
            'link': f"https://www.douyin.com/hot/{item['sentence_id']}/{quote(item['word'])}",
            'detail': f"相关视频数: {item['video_count']}, 视频浏览量: {round(item['view_count'] / 10000, 2)} w",
            'img_url': item['word_cover']['url_list'][0],
            'hot': f"{round(item['hot_value'] / 10000, 2)} w",
        }
        articles.append(article)
    result['articles'] = articles
    return result


# 获取bilibili热榜 https://bilibili.com
def get_bilibili_hot(param='综合热门'):
    if param == '':
        param = '综合热门'

    param_to_url = {
        '综合热门': f'https://api.bilibili.com/x/web-interface/popular?ps=20&pn=1&web_location=333.934&w_rid=4212cdbd9a99b5d1f3c13b15a0d2866f&wts={time.time()}',
        '每周必看': f'https://api.bilibili.com/x/web-interface/popular/series/one?number=263&web_location=333.934&w_rid=5953add9efec41fa6b3b3a2463deaceb&wts={time.time()}',
        '入站必刷': f'https://api.bilibili.com/x/web-interface/popular/precious?page_size=100&page=1&web_location=333.934&w_rid=109d64ee7e135e6df9135c60f5268f1e&wts={time.time()}',
        '热榜': f'https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all&web_location=333.934&w_rid=21116138e3e30c09f59d99353eec2def&wts={time.time()}',
        '番剧': f'https://api.bilibili.com/pgc/web/rank/list?day=3&season_type=1&web_location=333.934&w_rid=017b11648826c2c6c7cc5e1443c89c77&wts={time.time()}',
        '国产动画': f'https://api.bilibili.com/pgc/season/rank/web/list?day=3&season_type=4&web_location=333.934&w_rid=2ef68792e2e0fa132abcba283e3a4aa9&wts={time.time()}',
        '国创相关': f"https://api.bilibili.com/x/web-interface/ranking/v2?rid=168&type=all&web_location=333.934&w_rid=254697d548edbd6c617ee8e7e44ad34a&wts={time.time()}",
        '纪录片': f"https://api.bilibili.com/pgc/season/rank/web/list?day=3&season_type=3&web_location=333.934&w_rid=b339bae5ee3ba273d54bb01ebf478c02&wts={time.time()}",
        '动画': f"https://api.bilibili.com/x/web-interface/ranking/v2?rid=1&type=all&web_location=333.934&w_rid=91cde112ae2e48c21400254557da7dd5&wts={time.time()}",
        '音乐': f"https://api.bilibili.com/x/web-interface/ranking/v2?rid=3&type=all&web_location=333.934&w_rid=05936fd60016fafcacb43fb294e0a4fe&wts={time.time()}",
        '舞蹈': f"https://api.bilibili.com/x/web-interface/ranking/v2?rid=129&type=all&web_location=333.934&w_rid=ffe1c9febe809e005c11e89c194cca97&wts={time.time()}",
        '游戏': f"https://api.bilibili.com/x/web-interface/ranking/v2?rid=4&type=all&web_location=333.934&w_rid=7ec87796fe8d4ce6be90daa83b9f9b66&wts={time.time()}",
        '知识': f"https://api.bilibili.com/x/web-interface/ranking/v2?rid=36&type=all&web_location=333.934&w_rid=980643983e639c7a077d3ef634364322&wts={time.time()}",
        '科技': f"https://api.bilibili.com/x/web-interface/ranking/v2?rid=188&type=all&web_location=333.934&w_rid=e203be3aa45d92e49c9b49745e996152&wts={time.time()}",
        '运动': f"https://api.bilibili.com/x/web-interface/ranking/v2?rid=234&type=all&web_location=333.934&w_rid=0cae54e8e72c39006b5abf387a55dd82&wts={time.time()}",
        '汽车': f"https://api.bilibili.com/x/web-interface/ranking/v2?rid=223&type=all&web_location=333.934&w_rid=ef034d7f88d68ca5c7518bf4ea0fe343&wts={time.time()}",
        '生活': f"https://api.bilibili.com/x/web-interface/ranking/v2?rid=160&type=all&web_location=333.934&w_rid=8c7c0991447fe6061363fc48147320cd&wts={time.time()}",
        '美食': f"https://api.bilibili.com/x/web-interface/ranking/v2?rid=211&type=all&web_location=333.934&w_rid=842b3531c8d8fcd43cbb335063e33adc&wts={time.time()}",
        '动物圈': f"https://api.bilibili.com/x/web-interface/ranking/v2?rid=217&type=all&web_location=333.934&w_rid=f3159562650dfee352118930f623247f&wts={time.time()}",
        '鬼畜': f"https://api.bilibili.com/x/web-interface/ranking/v2?rid=119&type=all&web_location=333.934&w_rid=f3ab91ada64273c91e978fb3fab1973f&wts={time.time()}",
        '时尚': f"https://api.bilibili.com/x/web-interface/ranking/v2?rid=155&type=all&web_location=333.934&w_rid=796297e216b6ba1dc54555abb9a99c6b&wts={time.time()}",
        '娱乐': f"https://api.bilibili.com/x/web-interface/ranking/v2?rid=5&type=all&web_location=333.934&w_rid=e46688e39f4f2f6983e20686693f00de&wts={time.time()}",
        '影视': f"https://api.bilibili.com/x/web-interface/ranking/v2?rid=181&type=all&web_location=333.934&w_rid=f934b1b2f71115aaade478b974234fae&wts={time.time()}",
        '电影': f"https://api.bilibili.com/pgc/season/rank/web/list?day=3&season_type=2&web_location=333.934&w_rid=9d2ebd5095363d72c1be78d79bed380b&wts={time.time()}",
        '电视剧': f"https://api.bilibili.com/pgc/season/rank/web/list?day=3&season_type=5&web_location=333.934&w_rid=c46f04493bf27dfc453a9b8f1d497901&wts={time.time()}",
        '综艺': f"https://api.bilibili.com/pgc/season/rank/web/list?day=3&season_type=7&web_location=333.934&w_rid=bce3ca901053bccafeb3a39ee731b6b4&wts={time.time()}",
        '原创': f"https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=origin&web_location=333.934&w_rid=65f0777c5fa96eb9c60f2553c660dc93&wts={time.time()}",
        '新人': f"https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=rookie&web_location=333.934&w_rid=fefb1acfc4da275bddc9c7865aab0374&wts={time.time()}"
    }

    result = {
        'tabs': ['综合热门', '每周必看', '入站必刷', '全站音乐榜', '精选短剧', '热榜', '番剧', '国产动画', '国创相关',
                 '纪录片', '动画', '音乐', '舞蹈', '游戏', '知识', '科技', '运动', '汽车', '生活', '美食', '动物圈',
                 '鬼畜', '时尚', '娱乐', '影视', '电影', '电视剧', '综艺', '原创', '新人'],
        'site': 'bilibili',
    }
    articles = []

    if param == '全站音乐榜':
        response = requests.get(
            'https://api.bilibili.com/x/copyright-music-publicity/toplist/all_period?list_type=1&web_location=333.934&csrf=cfd561c2cc24f2fa881f7a145bdbbb24',
            headers=HEADERS)
        list_id = response.json()['data']['list'][str(datetime.datetime.now().year)][0]['ID']
        response = requests.get(
            f"https://api.bilibili.com/x/copyright-music-publicity/toplist/music_list?list_id={list_id}&web_location=333.934&csrf=cfd561c2cc24f2fa881f7a145bdbbb24",
            headers=HEADERS)
        items = response.json()['data']['list']
        for item in items:
            article = {
                'title': item['creation_title'],
                'subTitle': item['creation_nickname'],
                'link': f"https://www.bilibili.com/video/{item['creation_bvid']}",
                'detail': f"{round(item['creation_play'] / 10000, 1)}万次播放" + ' | ' + item['creation_reason'],
                'img_url': item['creation_cover'],
                'hot': ''
            }
            articles.append(article)
    elif param == '精选短剧':
        phase_id = requests.post('https://api.bilibili.com/pgc/activity/rank/ugc/playlet/queryList', json={},
                                 headers=HEADERS).json()['data']['editorChoicePhaseId']
        response = requests.post('https://api.bilibili.com/pgc/activity/rank/ugc/playlet/queryInfo',
                                 json={'phaseId': phase_id}, headers=HEADERS)
        items = response.json()['data']['rankInfoList']
        for item in items:
            article = {
                'title': item['title'],
                'subTitle': item['upName'] + ' | ' + f"共{item['epCount']}集",
                'link': item['jumpLink'],
                'detail': item['recommend'],
                'img_url': item['cover'],
                'hot': ''
            }
            articles.append(article)
    elif param == '番剧' or param == '国产动画' or param == '纪录片' or param == '电影' or param == '电视剧' or param == '综艺':
        response = requests.get(param_to_url[param], headers=HEADERS)
        if param == '番剧':
            items = response.json()['result']['list']
        else:
            items = response.json()['data']['list']
        for item in items:
            article = {
                'title': item['title'],
                'subTitle': item['badge'] + ' | ' + item['new_ep']['index_show'] + ' | ' + item['rating'],
                'link': item['url'],
                'detail': '',
                'img_url': item['cover'],
                'hot': f"{item['stat']['view'] if item['stat']['view'] < 10000 else str(round(item['stat']['view'] / 10000, 1)) + '万'},"
                       f","
                       f","
                       f"{item['stat']['follow'] if item['stat']['follow'] < 10000 else str(round(item['stat']['follow'] / 10000, 1)) + '万'},"
                       f""
            }
            articles.append(article)
    else:
        bilibili_headers = {
            'Origin': 'https://www.bilibili.com',
            'Referer': 'https://www.bilibili.com/v/popular/rank/all/',
            'Cookie': "i-wanna-go-back=-1; CURRENT_BLACKGAP=0; buvid_fp_plain=undefined; DedeUserID=234061658; DedeUserID__ckMd5=4ec0199292d00373; LIVE_BUVID=AUTO3216504240021279; buvid4=4AA2C06F-A64F-E7BE-9EEC-CA9F4014F85D83748-022042010-Gr0m3iB%2FfbcfWYuHC6Tc2A%3D%3D; FEED_LIVE_VERSION=V8; buvid3=A2F464B3-892E-FC9A-165E-EA14CDB8518425286infoc; b_nut=1682138625; b_ut=5; _uuid=F92810D18-955D-9A72-3AF3-2F15CE975BC625771infoc; header_theme_version=CLOSE; nostalgia_conf=-1; enable_web_push=DISABLE; CURRENT_QUALITY=80; hit-dyn-v2=1; home_feed_column=5; CURRENT_FNVAL=4048; rpdid=|(J|~)Y~mlYl0J'u~|RkRkuY); SESSDATA=58faf1df%2C1728181281%2Cc0a49%2A42CjCzxBpXP1Lj_6hooq8w2aib-mDqE8OAJUDN_hC7MdnzJT_RHGpcyQnxsCJBjT77e3sSVkJwcGFhVmNaM1VvSWRpYXJaLUdEMWJwU25MMHo5TnVodWZoUUdZckdweEZ3eU5NeTZmTktrRHdmZWlBbGxxbkd2aC04TEotanFqVFAzSjdWb1BSRll3IIEC; bili_jct=cfd561c2cc24f2fa881f7a145bdbbb24; sid=79cvho3u; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTI4ODg0ODYsImlhdCI6MTcxMjYyOTIyNiwicGx0IjotMX0.YDmq1xTQz4oVFJnvbyxGDglOAivoBq0fAcfU9epjLco; bili_ticket_expires=1712888426; browser_resolution=1536-482; PVID=4; bp_video_offset_234061658=918245406400315395; fingerprint=09a7bcba6757d0ef8a235f4397baf749; buvid_fp=09a7bcba6757d0ef8a235f4397baf749; b_lsid=FEF1037108_18EC14DB78B"
        }
        bilibili_headers.update(HEADERS)
        response = requests.get(param_to_url[param], headers=bilibili_headers)
        # print(response.text.encode('gbk', errors='ignore'))
        items = response.json()['data']['list']
        for item in items:
            article = {
                'title': item['title'],
                'subTitle': item['owner']['name'] + ' | ' + datetime.datetime.fromtimestamp(item['pubdate']).strftime(
                    '%m-%d %H:%M'),
                'link': item['short_link_v2'],
                'detail': item['desc'],
                'img_url': item['pic'],
                'hot': f"{item['stat']['view'] if item['stat']['view'] < 10000 else str(round(item['stat']['view'] / 10000, 1)) + '万'},"
                       f"{item['stat']['like'] if item['stat']['like'] < 10000 else str(round(item['stat']['like'] / 10000, 1)) + '万'},"
                       f"{item['stat']['coin'] if item['stat']['coin'] < 10000 else str(round(item['stat']['coin'] / 10000, 1)) + '万'},"
                       f"{item['stat']['favorite'] if item['stat']['favorite'] < 10000 else str(round(item['stat']['favorite'] / 10000, 1)) + '万'},"
                       f"{item['stat']['share'] if item['stat']['share'] < 10000 else str(round(item['stat']['share'] / 10000, 1)) + '万'}"
                # + ' 播放' + ' 点赞 ' + ' 收藏 ' + ' 投币 ' + ' 分享 '
                # str(item['stat']['danmaku']) + ' 弹幕 ' + str(item['stat']['reply']) + ' 回复 ' +
            }
            articles.append(article)

    result['articles'] = articles
    return result


# 小红书热榜 https://edith.xiaohongshu.com/api/sns/web/v1/search/hotlist?source=search_box
def get_xiaohongshu_hot(param='热搜'):
    if param == '':
        param = '热搜'

    xiaohongshu_headers = {
        'refer': 'https://www.xiaohongshu.com/',
        'Cookie': 'gid.sign=0WSH8CTskNt7qAlABxbgQUrShf0=; abRequestId=b558dfed25fbfea5a34a39136f81b00b; '
                  'webBuild=4.7.0; a1=18e64e2cabdeuj2gnuayrl39snx9t5avgcs1j361c50000923958; '
                  'webId=ad7b36ee0a928384f2268c388e6bd0fa; '
                  'acw_tc=046f80fc2f9daa241f19f2693473454210b1017ebe90ccfca624f3cc6ea61efb; '
                  'gid=yYdK4dJSfykyyYdK4dJS0SqKDfd7VJkI70vFMyS1qjMICy28j920hV888jJqj2Y8YqfYK820; '
                  'web_session=040069b156e443560d27de6fc8374b3c1c545c; unread={'
                  '%22ub%22:%2265dda42f0000000007024012%22%2C%22ue%22:%2265f973f5000000001203d790%22%2C%22uc%22:40}; '
                  'websectiga=984412fef754c018e472127b8effd174be8a5d51061c991aadd200c69a2801d6; '
                  'sec_poison_id=06525301-3999-49d2-aaab-fb3c72a05a1d; xsecappid=ugc',
        'X-S': 'XYW_eyJzaWduU3ZuIjoiNTEiLCJzaWduVHlwZSI6IngxIiwiYXBwSWQiOiJ4aHMtcGMtd2ViIiwic2lnblZlcnNpb24i'
               'OiIxIiwicGF5bG9hZCI6Ijc4M2ZhZDg5NTQ4Zjc5N2JlYThkOTM1OTM2YmQ4ZDdmYjk5YjdiZDExNmI2ZWZjNDZjYTU0'
               'MGU2YjkzZTU5ZmUzNDAwM2MyMmY3OTQ4NzQxNTcyNTdlNTEwNGE0Njc2MmM5ZTNiZmRhMWZhYTFlYjkwZDc0YWEzMWI1'
               'NGM3MmNkMGQ3NGFhMzFiNTRjNzJjZGFjNDg5YjlkYThjZTVlNDhmNGFmYjlhY2ZjM2VhMjZmZTBiMjY2YTZiNGNjM2Ni'
               'NTAyZjEwOGMzOTViMmE5MTE3NGU1NDY2ODRhODM2YTdkZTQ1YmFkOGE4NjJiZWUzMjcwYzY5NzYwMTUxNWVhYjU2OTU1'
               'ZjdmNDIxMzNlZTgyNzJlMjM1Y2Y5NTk5NTgxNzk0ZTE3MzIyNzhkYjNiNzM3YTE5ZDk4MWUxYzhkMGZhZGZhMjNmYzM5'
               'NjgzMTRmNjEyNDg5ODMyMmI5NTI2ZjlmMmJiNDBiOGIxNTIxMGM0MmQzYWU3NzkwMGY1NGQ3ZiJ9',
    }
    xiaohongshu_headers.update(HEADERS)
    response = requests.get('https://edith.xiaohongshu.com/api/sns/web/v1/search/hotlist?source=search_box',
                            headers=xiaohongshu_headers)
    items = response.json()['data']['items']

    result = {
        'tabs': ['热搜'],
        'site': 'xiaohongshu',
    }
    articles = []

    for item in items:
        article = {
            'title': item['title'],
            'subTitle': '',
            'link': f"https://www.xiaohongshu.com/search_result?keyword={quote(item['title'])}",
            'detail': '',
            'img_url': '',
            'hot': item['score'],
        }
        articles.append(article)

    result['articles'] = articles
    return result


# 获取豆瓣的热榜 https://douban.com/
def get_douban_hot(param='电影榜'):
    if param == '':
        param = '电影榜'

    result = {
        'tabs': ['电影榜', '图书榜', '书评榜', '精选讨论', '精选话题'],
        'site': 'douban'
    }
    articles = []

    if param == '电影榜':
        response = requests.get('https://movie.douban.com/chart', headers=HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.findAll('tr', class_='item')
        for item in items:
            article = {
                'title': item.find('div', class_='pl2').find('a').text,
                'subTitle': '',
                'link': item.find('div', class_='pl2').find('a')['href'],
                'detail': item.find('div', class_='pl2').find('p', class_='pl').text,
                'img_url': 'https://images.weserv.nl/?url=' + item.find('a', class_='nbg').find('img')['src'],
                'hot': item.find('div', class_='star clearfix').findAll('span')[-2].text + ' 分 ' +
                       item.find('div', class_='star clearfix').findAll('span')[-1].text,
            }
            articles.append(article)
    elif param == '图书榜':
        response = requests.get('https://book.douban.com/chart?subcat=all&icn=index-topchart-popular', headers=HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.findAll('li', class_='media clearfix')
        for item in items:
            article = {
                'title': item.find('h2', class_='clearfix').find('a').text,
                'subTitle': item.find('p', class_='subject-abstract color-gray').text,
                'link': item.find('h2', class_='clearfix').find('a')['href'],
                'detail': item.find('span', class_='buy-info').text,
                'img_url': item.find('img', class_='subject-cover')['src'],
                'hot': item.find('span', class_='font-small color-red fleft').text + ' 分 ' +
                       item.find('span', class_='fleft ml8 color-gray').text,
            }
            articles.append(article)
    elif param == '书评榜':
        response = requests.get('https://book.douban.com/review/best/', headers=HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.findAll('div', class_='main review-item')
        for item in items:
            article = {
                'title': item.find('h2').find('a').text,
                'subTitle': item.find('a', class_='name').text + ' | ' + item.find('span', class_='main-meta').text,
                'link': item.find('h2').find('a')['href'],
                'detail': item.find('div', class_='short-content').text,
                'img_url': item.find('img')['src'],
                'hot': item.find('a', class_='action-btn up').text + ' 赞同'
            }
            articles.append(article)
    elif param == '精选讨论':
        response = requests.get('https://www.douban.com/group/explore', headers=HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.findAll('div', class_='channel-item')
        for item in items:
            article = {
                'title': item.find('h3').find('a').text,
                'subTitle': item.find('span', class_='from').find('a').text + ' | ' + item.find('span',
                                                                                                class_='pubtime').text,
                'link': item.find('h3').find('a')['href'],
                'detail': item.find('div', class_='block').find('p').text if item.find('div', class_='block').find(
                    'p') is not None else '',
                'img_url': item.find('img')['src'] if item.find('img') is not None else '',
                'hot': item.find('div', class_='likes').text
            }
            articles.append(article)
    elif param == '精选话题':
        douban_headers = {
            'Origin': 'https://www.douban.com',
            'Referer': 'https://www.douban.com/gallery'
        }
        douban_headers.update(HEADERS)
        response = requests.get('https://m.douban.com/rexxar/api/v2/gallery/hot_items?ck=&start=0&count=40',
                                headers=douban_headers)
        items = response.json()['items']
        for item in items:
            article = {
                'title': item['target']['title'],
                'subTitle': item['target']['author']['name'] + ' | ' + item['target'][
                    'create_time'] + ' | ' + f"来自话题: {item['topic']['name']}",
                'link': item['target']['url'],
                'detail': item['target']['abstract'],
                'img_url': item['target']['cover_url'],
                'hot': f"{item['target']['likers_count']} 喜欢"
            }
            articles.append(article)

    result['articles'] = articles
    return result
