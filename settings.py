#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import urllib2
import re
import random
import lxml.html
import json
import cookielib

USER_AGENT = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]


def get_ip181_proxy(url='http://www.ip181.com/'):
    result = []
    headers = make_headers_by_file('ip181_headers.txt')
    req = urllib2.Request(url, headers=headers)
    resp = urllib2.urlopen(req)
    html = resp.read()
    tree = lxml.html.fromstring(html)
    trs = tree.xpath('//tbody/tr[@class!="active"]')
    for tr in trs:
        tds = tr.xpath('./td/text()')
        ip = tds[0].strip()
        port = tds[1].strip()
        anonymity = tds[2].strip()
        https = tds[3].strip().lower().split(',')
        if len(https) > 1:
            scheme = https[1]
        else:
            scheme = https[0]
        country = tds[5].strip()
        proxy = (ip, port, anonymity, scheme, country)
        result.append(proxy)
    return result


def make_headers_by_file(fname='headers.txt'):
    headers = {}
    with open(fname, 'r') as fd:
        for line in fd:
            index = line.find(':')
            if index != -1:
                k = line[0:index]
                v = line[index+1:]
                headers[k] = v.strip()
    with open('dic_'+fname, 'w') as wfd:
        json_obj = json.dumps(headers)
        wfd.write(json_obj)
    return headers

def make_cookie(name, value, domain):
    return cookielib.Cookie(
        version=0,
        name=name,
        value=value,
        port=None,
        port_specified=False,
        domain=domain,
        domain_specified=True,
        domain_initial_dot=False,
        path="/",
        path_specified=True,
        secure=False,
        expires=None,
        discard=False,
        comment=None,
        comment_url=None,
        rest=None
    )

if __name__ == "__main__":
    # url = 'http://haoip.cc/tiqu.htm'
    # get_proxy_ips(url)
    # headers = make_headers_by_file()
    # for k, v in headers.items():
    #     print k, v
    print(get_ip181_proxy())
