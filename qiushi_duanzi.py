#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import urllib2
import re
import random

from settings import USER_AGENT

page = 1
start_url = 'http://www.qiushibaike.com/hot/page/' + str(page)

try:
    headers = {'User-Agent': random.choice(USER_AGENT)}
    req = urllib2.Request(start_url, headers=headers)
    resp = urllib2.urlopen(req)
except urllib2.URLError as e:
    print e.reason
except urllib2.HTTPError as e:
    print e.code, e.message
else:
    pat = re.compile(r'<div.*?>.*?<a.*?>')
    print resp.read()

