import os
import re
import requests
from bs4 import BeautifulSoup

k = re.compile('@.+?。')
today = input('今天日期：')
with open(today + '.md', 'a+', encoding='utf-8') as f:
    f.write("# {}\n".format(today))
    while True:
        text = input("单词 @类型 中文 。@类型 中文 。")
        if text.startswith('end'):
            break
        if not text.endwith("。"):
            text += "。"
        string = '**' + text.split(' ')[0] + '** '
        response = requests.get('https://cn.bing.com/dict/search?q={0}'.format(text.split(' ')[0]))
        us, en = '', ''
        if response.ok:
            r = response.text
            soup = BeautifulSoup(r, 'html.parser')
            us = soup.find(class_='hd_prUS b_primtxt').text
            en = soup.find(class_='hd_pr b_primtxt').text
        mean = []
        for i in re.finditer(k, text):
            print(i.group()[1: -1])
            temp = i.group()[1: -1].split(' ')
            mean.append('*' + temp[0] + '.* ')
            mean.append(temp[1])
        all_mean = ' '.join(mean)
        f.write(string + en + ' ' + us + ' ' + all_mean + '\n')