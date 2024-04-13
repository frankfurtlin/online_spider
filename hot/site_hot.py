import config
from hot.entertainment_site_hot import *
from hot.finance_site_hot import *
from hot.home_site_hot import *
from hot.technology_site_hot import *
from hot.community_site_hot import *
from hot.develop_site_hot import *

# ----------------------------------------------------------------------------------------------------------------------
# 输出样例
# {
#     'tabs': ['热搜', '小说', '电影', '电视剧', '汽车', '游戏'],
#     'site': 'baidu',
#     'articles': [
#         {
#              'title': '万相之王',
#              ‘subTitle': '作者: 天蚕土豆, 类型: 玄幻',
#              'link': 'https://www.baidu.com/s?wd=%E4%B8%87%E7%9B%B8%E4%B9%8B%E7%8E%8B+%E5%B0%8F%E8%AF%B4',
#              'detail': '天地间，有万相。而我李洛，终将成为这万相之王。继《斗破苍穹》《武动乾坤》《大主宰》《元尊》之后，天蚕土豆又一部玄幻力作。',
#              'img_url': 'https://fyb-2.cdn.bcebos.com/hotboard_image/448112da61a64bed8e6996bc44d9d798',
#              'hot': '299829'
#         }
#     ]
# }
# ----------------------------------------------------------------------------------------------------------------------

data = {}


# 获取站点的热榜
def get_site_hot(site: str, param=''):
    if config.CACHE_ENABLED:
        now_timestamp = int(time.time())
        if (site in data and param in data[site] and
                now_timestamp - data[site][param]['timestamp'] < config.CACHE_EXPIRATION):
            # print(f"读取网站 {site} 的 {param} 内容命中了缓存")
            return data[site][param]['result']

    if site == 'baidu':
        result = get_baidu_hot(param)
    elif site == 'sina':
        result = get_sina_hot(param)
    elif site == 'tencent':
        result = get_tencent_hot(param)
    elif site == 'wangyi':
        result = get_wangyi_hot(param)
    elif site == 'toutiao':
        result = get_toutiao_hot(param)
    elif site == 'fenghuang':
        result = get_ifeng_hot(param)
    elif site == 'msn':
        result = get_msn_hot(param)

    elif site == 'ithome':
        result = get_ithome_hot(param)
    elif site == '36kr':
        result = get_36kr_hot(param)
    elif site == 'sspai':
        result = get_sspai_hot(param)
    elif site == 'geekpark':
        result = get_geekpark_hot(param)
    elif site == 'pinwest':
        result = get_pinwest_hot(param)
    elif site == 'ifanr':
        result = get_ifanr_hot(param)
    elif site == 'cyzone':
        result = get_cyzone_hot(param)

    elif site == 'weibo':
        result = get_weibo_hot(param)
    elif site == 'douyin':
        result = get_douyin_hot(param)
    elif site == 'bilibili':
        result = get_bilibili_hot(param)
    elif site == 'xiaohongshu':
        result = get_xiaohongshu_hot(param)
    elif site == 'douban':
        result = get_douban_hot(param)

    elif site == 'xueqiu':
        result = get_xueqiu_hot(param)

    elif site == 'tieba':
        result = get_baidu_tieba_hot(param)
    elif site == 'hupu':
        result = get_hupu_hot(param)
    elif site == 'zhihu':
        result = get_zhihu_hot(param)
    elif site == 'wxread':
        result = get_wxread_hot(param)
    elif site == 'aisixiang':
        result = get_aisixiang_hot(param)
    elif site == 'lishi':
        result = get_lishi(param)
    elif site == 'youxiputao':
        result = get_youxiputao_hot(param)
    elif site == 'gcores':
        result = get_gcores_hot(param)

    elif site == 'csdn':
        result = get_csdn_hot(param)
    elif site == 'github':
        result = get_github_hot(param)
    elif site == 'juejin':
        result = get_juejin_hot(param)
    elif site == 'infoq':
        result = get_infoq_hot(param)
    elif site == 'renrenchanpin':
        result = get_woshipm_hot(param)
    elif site == 'appinn':
        result = get_appinn_hot(param)

    # 添加其他站点的处理逻辑
    else:
        raise ValueError('Invalid site parameter')

    if config.CACHE_ENABLED:
        # 更新缓存
        param_ = {
            'result': result,
            'timestamp': int(time.time())
        }
        if site in data:
            data[site][param] = param_
        else:
            data[site] = {param: param_}

    return result
