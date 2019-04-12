
from os import path
from PIL import Image
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import os
import random

from wordcloud import WordCloud, STOPWORDS

d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

#text = open(path.join(d, 'assets/词云名单.txt')).read()
text = open(path.join(d, 'assets/词云名单2.txt')).read()

alice_mask = np.array(Image.open(path.join(d, "assets/kaola_mask_2.png")))

stopwords = set(STOPWORDS)
stopwords.add("said")
stopwords.add("无敌")


def color_func(*args, **kwargs):
    """
    限定输出字体的颜色
    """
    return random.choice(
        [
            '#2b748e',
            '#46c06f',
            '#3a548c',
            '#481a6c',
            '#000000',
            '#ffffff',
            '#3f4889',
            '#900d2f',
            '#0f101a',
            '#086e3f',
            '#df601b',
            '#b32aae',
            '#086e3f',
            '#b32aae',
            '#481a6c',
        ])

#  def red_color_func(*args,**kwargs):
#      return "hsl(10, 100%%, %d%%)" % random.randint(40, 100)

wc = WordCloud(
         background_color="rgba(255, 255, 255, 0)", mode="RGBA", # 设置背景透明
         max_words=2000, mask=alice_mask,
         font_path='/System/Library/Fonts/PingFang.ttc', # 避免中文乱码
         stopwords=stopwords,
         color_func=color_func
         )

wc.generate(text)

wc.to_file(path.join(d, f'output/words_{datetime.now().timestamp()}.png'))
