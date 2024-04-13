from hot.entertainment_site_hot import *
from hot.home_site_hot import *
from hot.technology_site_hot import *
from hot.community_site_hot import *
from hot.develop_site_hot import *

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/58.0.3029.110 Safari/537.3'
}

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


# 获取站点的热榜
def get_site_hot(site: str, param=''):
    if site == 'baidu':
        return get_baidu_hot(param)
    elif site == 'sina':
        return get_sina_hot(param)
    elif site == 'tencent':
        return get_tencent_hot(param)
    elif site == 'wangyi':
        return get_wangyi_hot(param)
    elif site == 'toutiao':
        return get_toutiao_hot(param)
    elif site == 'fenghuang':
        return get_ifeng_hot(param)
    elif site == 'msn':
        return get_msn_hot(param)

    elif site == 'ithome':
        return get_ithome_hot(param)
    elif site == '36kr':
        return get_36kr_hot(param)
    elif site == 'sspai':
        return get_sspai_hot(param)
    elif site == 'geekpark':
        return get_geekpark_hot(param)
    elif site == 'pinwest':
        return get_pinwest_hot(param)
    elif site == 'ifanr':
        return get_ifanr_hot(param)
    elif site == 'cyzone':
        return get_cyzone_hot(param)

    elif site == 'weibo':
        return get_weibo_hot(param)
    elif site == 'douyin':
        return get_douyin_hot(param)
    elif site == 'bilibili':
        return get_bilibili_hot(param)
    elif site == 'xiaohongshu':
        return get_xiaohongshu_hot(param)
    elif site == 'douban':
        return get_douban_hot(param)

    elif site == 'tieba':
        return get_baidu_tieba_hot(param)
    elif site == 'hupu':
        return get_hupu_hot(param)
    elif site == 'zhihu':
        return get_zhihu_hot(param)
    elif site == 'wxread':
        return get_wxread_hot(param)
    elif site == 'aisixiang':
        return get_aisixiang_hot(param)
    elif site == 'lishi':
        return get_lishi(param)
    elif site == 'youxiputao':
        return get_youxiputao_hot(param)
    elif site == 'gcores':
        return get_gcores_hot(param)

    elif site == 'csdn':
        return get_csdn_hot(param)
    elif site == 'github':
        return get_github_hot(param)
    elif site == 'juejin':
        return get_juejin_hot(param)
    elif site == 'infoq':
        return get_infoq_hot(param)
    elif site == 'renrenchanpin':
        return get_woshipm_hot(param)
    elif site == 'appinn':
        return get_appinn_hot(param)

    # 添加其他站点的处理逻辑
    else:
        raise ValueError('Invalid site parameter')
