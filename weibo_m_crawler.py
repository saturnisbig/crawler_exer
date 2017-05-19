#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import urllib2
from settings import make_headers_by_file, get_ip181_proxy, make_cookie
import random
import cookielib
import json
import requests
import httplib2


start_id = '1713926427'
start_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value={}&containerid={}'
test_url = 'https://m.weibo.cn/u/1713926427'

url = start_url.format(start_id, '100505'+start_id)
headers = make_headers_by_file('json_headers.txt')

ghttp = httplib2.Http()
httplib2.debuglevel=1
resp, page = ghttp.request(url, headers=headers)

print json.loads(page)
# cj = cookielib.CookieJar()
# s_cookie = {'Cookie': '_T_WM=ca55e20d09d40a5132d4b046358f7cc1; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D2302831713926427%26fid%3D1005051713926427%26uicode%3D10000011'}
# cookie = s_cookie['Cookie'].split(';')
# for pair in cookie:
#     name, value = pair.split('=')
#     ck = make_cookie(name, value, domain='.weibo.cn')
#     cj.set_cookie(ck)

# cookie = {'Cookie': '_T_WM=ca55e20d09d40a5132d4b046358f7cc1; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D2302831713926427%26fid%3D1005051713926427%26uicode%3D10000011'}
# print headers
# headers['User-Agent'] = random.choice(USER_AGENT)
# print url
print headers

# req = urllib2.Request(url, headers=headers)
# resp0 = urllib2.urlopen(req)
# print resp0.info()

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

# opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
# l = []
# for k, v in headers.items():
#     l.append((k, v))
# opener.addheaders = l
# # urllib2.install_opener(opener)
# resp = opener.open(url)
# print resp.info()

# req = urllib2.Request(test_url, headers=headers)
# resp = urllib2.urlopen(req, timeout=10.0)
# print resp.getcode()
# for ck in cookie:
#     print ck.name, ck.value
# req2 = urllib2.Request(url, headers=headers)
# resp2 = urllib2.urlopen(req2, timeout=5.0)
# for ck in cookie:
#     print ck.name, ck.value
# print resp2.read()
#print json.loads(resp.read())
# json_obj = json.load(resp)
# doc = resp.read()
# print doc
# print unicode(doc, 'utf-8')

# if __name__ == "__main__":
#     selenium_test(url)
