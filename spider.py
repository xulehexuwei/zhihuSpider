# -*- coding: utf-8 -*-
import re
import time
import requests
import random
import json

# 知乎有反爬虫，加入http headers伪装浏览器
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
    "Connection": "keep-alive",
    "Accept": "text/html,application/json,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8"}

# 以 f 开头表示在字符串内支持大括号内的 python 表达式
# url = f'https://www.zhihu.com/api/v4/questions/{question_id}'
url = 'https://www.zhihu.com/topics'
html = requests.get(url, headers=headers)

# <li class="zm-topic-cat-item" data-id="1761"><a href="#生活方式">生活方式</a></li>
topicRegex = r'<li class="zm-topic-cat-item" data-id="(\d+)"><a href="#([\u4e00-\u9fa5]+)">'
pattern = re.compile(topicRegex)

# topic 是一个list（topicID，名字）
topic = pattern.findall(html.text)
cnt = 0
topicSet = set()
for i in topic:
    urlSubtopic = url + '#' + i[1]
    print(urlSubtopic)
    offset = 0
    while 1:
        try:
            data = {
                "method":"next",
                "params": '{"topic_id":' + str(i[0]) + ',"offset":' + str(offset) + ',"hash_id":""}'
            }
            html = requests.Session().post('https://www.zhihu.com/node/TopicsPlazzaListV2', data=data, headers=headers).content

            htmlDict = json.loads(html)
            msg = htmlDict['msg']
            offset += 20

            if msg == []:
                break

            for j in msg:
                subTopicRegex = r'<a target="_blank" href="\/topic\/(\d+)">'
                subTopicPattern = re.compile(subTopicRegex)
                # subTopicID = re.search(subTopicRegex, i).group(0)
                subTopicID = subTopicPattern.findall(j)
                topicSet.add(subTopicID[0])
                cnt += 1
        except Exception as ce:
            break

print(len(topicSet))
print(cnt)
