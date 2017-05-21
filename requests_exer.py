#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import requests
import json

url = 'http://httpbin.org/'

playload = {'key1': 'v1', 'key2': 'v2'}
r = requests.get(url+'get', params=playload)

data = {'key1': 'v1', 'key2': 'v2'}
r = requests.post(url+'post', data=data)

# 以json的形式传递参数
r = requests.post(url+'post', data=json.dumps(data))

# 获取cookie
print r.cookies
ck_url = url + 'cookies'
ck = dict(cookies_are='working')
r = requests.get(ck_url, cookies=cookies)
print r.text

# 超时配置，仅与请求有关，如果请求的内容太大，这样设置没用
requests.get(url, timeout=0.001)

# 会话对象

s = requests.Session()
s.get(url + 'cookies/set/sessioncookie/123456789')
r = s.get(url + 'cookies')
print(r.text)

# SSL证书验证，针对https开头的网站
url_12306 = 'https://kyfw.12306.cn/otn'
url_v = 'https://v2ex.com'
r = requests.get(url_12306 verify=True)
r2 = requests.get(url_v, verify=True)
# 会出现证书验证错误的问题
print r.text

# 代理
proxies = {'http': 'http://41.118.132.69:4433'}
r = requests.post('http://httpbin.org/post', proxies=proxies)
print r.text


