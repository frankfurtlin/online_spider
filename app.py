
from flask import Flask, render_template, request

from hot.site_hot import get_site_hot
from site_news import get_site_news

app = Flask(__name__, template_folder='./templates')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/hot')
def hot():
    return render_template('hot/home.html', data=get_site_hot('baidu'))


@app.route('/hot/technology')
def hot_technology():
    return render_template('hot/technology.html', data=get_site_hot('ithome'))


@app.route('/hot/entertainment')
def hot_entertainment():
    return render_template('hot/entertainment.html', data=get_site_hot('weibo'))


@app.route('/hot/community')
def hot_community():
    return render_template('hot/community.html', data=get_site_hot('tieba'))


@app.route('/hot/finance')
def hot_finance():
    return render_template('hot/finance.html', data=get_site_hot('baidu'))


@app.route('/hot/develop')
def hot_develop():
    return render_template('hot/develop.html', data=get_site_hot('csdn'))


@app.route('/load-hots', methods=['GET'])
def load_hots():
    site = request.args.get('site')
    param = request.args.get('param')
    return render_template('hot/hot-content.html', data=get_site_hot(site, param))


@app.route('/news')
def news():
    site_params = {
        'site': 'xueqiu',
        'xueqiu_max_id': -1
    }
    return render_template('news.html', news=get_site_news(site_params))


@app.route('/load-news', methods=['GET'])
def load_news():
    site_params = {}
    site = request.args.get('site')
    if site == 'xueqiu':
        site_params = {
            'site': site,
            'xueqiu_max_id': int(request.args.get('xueqiu_max_id'))
        }
    elif site == 'dsb':
        site_params = {
            'site': site,
            'dsb_page': int(request.args.get('dsb_page'))
        }
    elif site == 'jinse':
        site_params = {
            'site': site,
            'jinse_bottom_id': int(request.args.get('jinse_bottom_id'))
        }
    elif site == 'tmtpost':
        site_params = {
            'site': site,
            'tmtpost_offset': int(request.args.get('tmtpost_offset'))
        }
    return render_template('news-articles.html', news=get_site_news(site_params))


if __name__ == '__main__':
    app.run(debug=True)
