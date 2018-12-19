import codecs
import re

import jieba
import jieba.analyse
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import requests
import urllib3
from scipy.misc import imread
from wordcloud import WordCloud

from app import BASE_DIR
from app.utils import get_charles_proxy

import pandas as pd

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def filter_content(raw_content):
    pattern = re.compile(r'<.*?>|转发微博|//@.*|回复@.*?:')

    content = re.sub(pattern, '', raw_content)

    content = content.replace('&quot;', '"')

    return content


def get_weibo_from_api(container_id, uid, page):
    """
    捉别人
    """
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

    return resp.json()


def get_weibo_from_personal(container_id, page):
    """
    捉个人
    """
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
    params = {
        'containerid': container_id,
        'page_type': '03',
        'page': page
    }
    url = 'https://m.weibo.cn/api/container/getIndex'

    proxies = get_charles_proxy()

    resp = requests.request('get', url, params=params, headers=headers,
                            proxies=proxies, verify=False)

    return resp.json()


def fetch_data(uid, container_id, total):
    """
    :param uid: 
    :param container_id: 
    :param total: 总页数
    :return: 
    """
    page = 0
    blogs = []

    create_date = []
    sources = []

    for i in range(0, total // 10):
        resp = get_weibo_from_api(container_id, uid, page)
        cards = resp.get('cards')

        for card in cards:
            if card.get('card_type') == 9:
                my_blog = card.get('mblog')

                content = my_blog.get('text')
                create_at = my_blog.get('created_at')
                source = my_blog.get('source')

                content = filter_content(content)
                blogs.append(content)
                create_date.append(create_at)
                sources.append(source)

        page += 1

        print('page: {}, already crawl: {}'.format(page, len(blogs)))

        with codecs.open(BASE_DIR + '/data/weibo6.txt', 'w',
                         encoding='utf-8') as f:
            f.write('\n'.join(blogs))

    df = pd.DataFrame({
        '内容': blogs,
        '时间': create_date,
        '来自': sources
    })

    writer = pd.ExcelWriter(BASE_DIR + '/data/weibo_record_me.xlsx',
                            engine='xlsxwriter')

    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()


def fetch_myself_data(container_id, total):
    page = 0
    blogs = []

    create_date = []
    sources = []

    for i in range(0, total // 10):
        resp = get_weibo_from_personal(container_id, page)
        cards = resp.get('cards')

        for card in cards:
            if card.get('card_type') == 9:
                my_blog = card.get('mblog')

                content = my_blog.get('text')
                create_at = my_blog.get('created_at')
                source = my_blog.get('source')

                content = filter_content(content)
                blogs.append(content)
                create_date.append(create_at)
                sources.append(source)

        page += 1

        print('page: {}, already crawl: {}'.format(page, len(blogs)))

        with codecs.open(BASE_DIR + '/data/weibo6.txt', 'w',
                         encoding='utf-8') as f:
            f.write('\n'.join(blogs))

    df = pd.DataFrame({
        '内容': blogs,
        '时间': create_date,
        '来自': sources
    })

    writer = pd.ExcelWriter(BASE_DIR + '/data/weibo_record_me.xlsx',
                            engine='xlsxwriter')

    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()


def generate_image():
    data = []

    with codecs.open(BASE_DIR + '/example/wc的词库.txt', 'r',
                     encoding='utf-8') as f:
        for text in f.readlines():
            data.extend(jieba.analyse.extract_tags(text, topK=20))
        data = " ".join(data)

        # mask_img = imread(BASE_DIR + '/data/WechatIMG110.jpeg', flatten=True)

        wordcloud = WordCloud(
            font_path='/System/Library/Fonts/PingFang.ttc',
            background_color='white',
         #   mask=mask_img
        ).generate(data)

        plt.imshow(
            wordcloud,
            interpolation="bilinear")

        plt.axis('off')

        plt.savefig(BASE_DIR + '/example/wc.jpg', dpi=1600)
