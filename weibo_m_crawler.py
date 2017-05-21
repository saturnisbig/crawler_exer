#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import urllib2
from settings import make_headers_by_file, get_ip181_proxy
import random
import cookielib
import json
import requests
import httplib2


class WeiboCrawler():

    def __init__(self, user_id, id_prefix='100505'):
        self.user_id = user_id
        self.user_url = 'https://m.weibo.cn/u/' + user_id
        self.base_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value={}&containerid={}'
        self.req_containerid = id_prefix + self.user_id
        self.start_url = self.base_url.format(self.user_id, self.req_containerid)
        self.headers = {
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0",
            "Host": "m.weibo.cn",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": self.user_url
        }

    def get_wb_containerid(self):
        resp = requests.get(self.start_url, headers=self.headers)
        j_data = resp.json()
        # print j_data
        containerid = j_data.get('tabsInfo').get('tabs')[1].get('containerid')
        if containerid:
            # print containerid
            self.wb_containerid = containerid
        else:
            print u'获取wb_containerid失败', self.headers, self.start_url

    def get_wb_list(self, page=1):
        self.get_wb_containerid()
        self.wb_url = self.base_url.format(self.user_id, self.wb_containerid) + '&page=%s' % str(page)
        resp = requests.get(self.wb_url, headers=self.headers)
        j_data = resp.json()
        # print j_data
        cards = j_data.get('cards')
        for card in cards:
            print card.get('mblog').get('text')

# url = start_url.format(start_id, '100505'+start_id)
# headers = make_headers_by_file('json_headers.txt')

# ghttp = httplib2.Http()
# httplib2.debuglevel=1
# resp, page = ghttp.request(url, headers=headers)
# cookie = {'Cookie': '_T_WM=ca55e20d09d40a5132d4b046358f7cc1; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D2302831713926427%26fid%3D1005051713926427%26uicode%3D10000011'}

# resp = requests.get(url, headers=headers)
# for k, v in resp.headers.items():
#     print k, v
# jsondata = resp.json()
# print jsondata

# 添加代理
# proxy = random.choice(get_ip181_proxy())
# proxies = {proxy[3]: proxy[3]+':'+proxy[0]+':'+proxy[1]}
# print proxies
# proxy_hd = urllib2.ProxyHandler(proxies)

if __name__ == "__main__":
    wb = WeiboCrawler('1713926427')
    # wb.get_wb_containerid()
    wb.get_wb_list()
