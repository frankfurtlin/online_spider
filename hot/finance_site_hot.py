from urllib.parse import quote

import requests

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/58.0.3029.110 Safari/537.3'
}


# 获取雪球热门话题 https://www.xueqiu.com/
def get_xueqiu_hot(param='热门话题'):
    if param == '':
        param = '热门话题'

    result = {
        'tabs': ['热门话题'],
        'site': 'xueqiu'
    }
    articles = []

    xueqiu_headers = {
        'cookie': 'acw_tc=276077ac17129918749684661ebfc0416c62c1f6dfc5238c90f463a9e14497; xq_a_token=4b8bc7136c9fd7b4395f9ca0a65c38363243df2b; xqat=4b8bc7136c9fd7b4395f9ca0a65c38363243df2b; xq_r_token=3f230866347670b258c76aecd81456e63e6aa98b; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTcxNDk1NjQ2MiwiY3RtIjoxNzEyOTkxODQyMTQzLCJjaWQiOiJkOWQwbjRBWnVwIn0.AzXGzHJdvTeF8T9ncPBdtKpxle7Df-BFD1-SR-t2AupIfDre5Zg6uQ_svGFQxIPLTVBT2Jdep_6CKwz_xmpkZs7iCFdtmU21-bLIpSNPrQ-ewbhcKLpZqjWDEuXnEuBFEFCmW0TSHZENkrVz-AG4rnreES3RuzrUDOAyBAy2xchDou6Rr5atZu9QFFhkkoxDZgsRlrpEsVyHa6qpt94t_Lkhi5iVMrVYy2bnaQvVVKUI9UwsAETe-Nyzc0_DC7ue1nnsg1Af7Ne6gaccvzIFdwC_ndD7ca0RVymk2FPdFv-jwGYGQ6RmxITFBZNksqP5CssjejbUtTvhIqtI2CG0jQ; cookiesu=811712991885631; u=811712991885631; device_id=cac6134e0d6da3a65692903bb9deb613; smidV2=202404131504489a463ffe89f5b874bf7b2ff125cf37d9007af17bdd15c8ca0; Hm_lvt_1db88642e346389874251b5a1eded6e3=1712991889; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1712991889; .thumbcache_f24b8bbe5a5934237bbc0eda20c1b6e7=rzxgPPefM+bQEJtv2tIR3m+9VXwLxFn/VSOvomzisqDh+YrQAR77TTfCWRXwJFWq2lUt82b6YvtEOhYslCji/Q%3D%3D'
    }
    xueqiu_headers.update(HEADERS)

    response = requests.get('https://xueqiu.com/hot_event/list.json?count=10', headers=xueqiu_headers)
    items = response.json()['list']

    for item in items:
        article = {
            'title': item['tag'][1: -1],
            'subTitle': '',
            'link': f"https://www.xueqiu.com/k?q={quote(item['tag'])}",
            'detail': item['content'],
            'img_url': item['pic'],
            'hot': f"{item['status_count']} 跟帖"
        }
        articles.append(article)

    result['articles'] = articles
    return result
