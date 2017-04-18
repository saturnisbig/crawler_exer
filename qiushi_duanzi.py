#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import urllib2
import re
import random

from settings import USER_AGENT


class QSBK:

    def __init__(self):
        self.current_page = 1
        self.start_url = 'http://www.qiushibaike.com/hot/page/'
        self.page_stories = []
        self.current_index = 0

    def get_page_stories(self, page=1):
        url = self.start_url + str(page)
        try:
            headers = {'User-Agent': random.choice(USER_AGENT)}
            req = urllib2.Request(url, headers=headers)
            resp = urllib2.urlopen(req)
        except urllib2.URLError as e:
            print(e.reason)
        except urllib2.HTTPError as e:
            print(e.code, e.message)
        else:
            pat = re.compile(r'<div.*?class="author.*?<a.*?href="/users.*?<h2>' +
                             '(.*?)</h2>.*?<div.*?class="content.*?<span>(.*?)' +
                             '</span>(.*?)<div\s+class="stats.*?<i.*?number.*?>(.*?)</i>',
                             re.S)
            html = resp.read()
            self.page_stories = pat.findall(html)

    def load_page(self):
        self.current_page += 1
        self.get_page_stories(self.get_page_stories)
        self.current_index = 0

    def get_one_story(self):
        count = len(self.page_stories)
        while self.current_index < count:
            command = raw_input('请输入Q结束，Enter阅读下一条：')
            if command == 'Q':
                return
            item = self.page_stories[self.current_index]
            if not re.search('img', item[2]):
                print '当前页{0}，用户名：{1}，\n内容:{2}，点赞:{3}'.format(
                    self.current_page, item[0], item[1], item[3])
            else:
                print '当前页：%s, 内容包含图片请上网查看' % self.current_page
            print('\n')
            self.current_index += 1
            if self.current_index == len(self.page_stories):
                self.load_page()

    def read_duanzi(self):
        self.get_page_stories()
        self.get_one_story()



def get_duanzi_item_re():
    page = 1
    start_url = 'http://www.qiushibaike.com/hot/page/' + str(page)
    try:
        headers = {'User-Agent': random.choice(USER_AGENT)}
        req = urllib2.Request(start_url, headers=headers)
        resp = urllib2.urlopen(req)
    except urllib2.URLError as e:
        print(e.reason)
    except urllib2.HTTPError as e:
        print(e.code, e.message)
    else:
        pat = re.compile(r'<div.*?class="author.*?<a.*?href="/users.*?<h2>' +
                         '(.*?)</h2>.*?<div.*?class="content.*?<span>(.*?)' +
                         '</span>(.*?)<div\s+class="stats.*?<i.*?number.*?>(.*?)</i>',
                         re.S)
        html = resp.read()
        # print pat.findall(html)
        return pat.findall(html)
        # for item in pat.findall(html):
        #     if not re.search('img', item[2]):
        #         print item[0], item[1], item[3]

def get_duanzi_item_lxml():
    pass

if __name__ == "__main__":
    #get_page()
    duanzi_reader = QSBK()
    duanzi_reader.read_duanzi()
