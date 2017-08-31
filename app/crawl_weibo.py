import codecs
import os
import jieba.analyse

import re

import jieba
import requests
import urllib3
from scipy.misc import imread
from wordcloud import WordCloud
import matplotlib.pyplot as plt

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_charles_proxy():
    """
    使用charles进行抓包
    """
    proxy = {'all': "http://{}:{}@{}".format('', '', '127.0.0.1:8888')}
    return proxy


def filter_content(raw_content):
    pattern = re.compile(r'<.*?>|转发微博|//@.*|回复@.*?:')

    content = re.sub(pattern, '', raw_content)

    content = content.replace('&quot;', '"')

    return content


def get_weibo_from_api(container_id, uid, page):
    # container_id = '1076033952070245'
    # uid = '3952070245'
    # page = '2'

    headers = {
        'Host': 'm.weibo.cn',
        'Accept': 'application/json, text/plain, */a',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': ('Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) '
                       'AppleWebKit/601.1.46 (KHTML, like Gecko) '
                       'Version/9.0 Mobile/13B143 Safari/601.1'),
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2'
    }

    # params = {
    #     'containerid': container_id,
    #     'uid': uid,
    #     'lfid': '100103type=1&q=范冰冰',
    #     'luicode': '10000011',
    #     'page': page,
    #     'type': 'all'
    # }

    params = {
        'containerid': container_id,
        'type': 'uid',
        'value': uid,
        'page': page
    }
    url = 'https://m.weibo.cn/api/container/getIndex'

    proxies = get_charles_proxy()

    resp = requests.request('get', url, params=params, headers=headers,
                            proxies=proxies, verify=False)
    # resp = requests.get(url, params=params, headers=headers)

    return resp.json()


def fetch_data(uid, container_id):
    page = 0
    # total = 1633
    total = 5497
    blogs = []

    for i in range(0, total // 10):
        resp = get_weibo_from_api(container_id, uid, page)
        cards = resp.get('cards')

        for card in cards:
            if card.get('card_type') == 9:
                my_blog = card.get('mblog')

                content = my_blog.get('text')
                create_at = my_blog.get('created_at')

                # blog = {
                #     'content': content,
                #     'create_a'
                # }
                #

                content = filter_content(content)
                blogs.append(content)

        page += 1

        print('page: {}, already crawl: {}'.format(page, len(blogs)))

        with codecs.open(BASE_DIR + '/data/weibo2.txt', 'w',
                         encoding='utf-8') as f:
            f.write('\n'.join(blogs))


def generate_image():
    data = []

    with codecs.open(BASE_DIR + '/data/weibo2.txt', 'r',
                     encoding='utf-8') as f:
        for text in f.readlines():
            data.extend(jieba.analyse.extract_tags(text, topK=20))
        data = " ".join(data)

        mask_img = imread(BASE_DIR + '/data/WechatIMG199.jpeg', flatten=True)
        # mask_img = imread(BASE_DIR + '/data/df.png', flatten=True)

        wordcloud = WordCloud(
            font_path='/System/Library/Fonts/PingFang.ttc',
            background_color='white',
            mask=mask_img
        ).generate(data)

        plt.imshow(
            wordcloud,
            interpolation="bilinear")

        plt.axis('off')

        plt.savefig('./heart9.jpg', dpi=1600)

    pass


if __name__ == "__main__":
    container_id = '1076033952070245'
    uid = '3952070245'
    fetch_data(uid, container_id)

    generate_image()
