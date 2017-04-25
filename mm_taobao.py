#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import urllib2
import re
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from settings import USER_AGENT

base_url = 'https://mm.taobao.com/json/request_top_list.htm'
driver = webdriver.PhantomJS(executable_path='/home/teddy/code/bin/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')

def download_page(base_url, page=0):
    url = (base_url + '?page=' + str(page)) if page else base_url
    headers = {
        'User-Agent': random.choice(USER_AGENT)
    }
    try:
        req = urllib2.Request(url, headers=headers)
        resp = urllib2.urlopen(req)
    except urllib2.URLError as e:
        if hasattr(e, 'reason'):
            print('下载页面出错了：%s，原因：%s' % (url, e.reason))
            return None
    return resp.read()

# 在MM列表页获取个人页网址、姓名、年龄、总积分、新增积分、好评率、导购照片、签约数
def get_taobao_info(html):
    html = html.decode('gbk')
    # 1头像地址
    s1 = r'<div class="pic s60.*?<img src="(.*?)".*?<a class="lady-name" href='
    # 2个人页面地址、3姓名、4年龄、5居住地
    s2 = '"(.*?)".*?>(.*?)</.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>'
    # 6积分，7新增积分、8好评率，9导购照片，10签约数
    s3 = r'.*?<div class="list-info.*?</span>(.*?)</dd>.*?<strong>(.*?)</'
    s4 = r'.*?<strong>(.*?)</.*?<strong>(.*?)</.*?<strong>(.*?)</.*?'
    # 11描述
    s5 = r'<p class="description.*?>(.*?)</p>'
    pat =re.compile(s1+s2+s3+s4+s5, re.S)
    result = []
    for item in pat.findall(html):
        model_url = 'https:' + item[1]
        icon_url = 'https:' + item[0]
        model_info = [icon_url, item[2], item[3], item[4], item[5], item[6],
                      item[7], item[8], item[9], item[10].strip()]
        result.append((model_url, model_info))
    return result

# 在个人详细页面中获取：生日、所在城市、职业、学校/专业、风格、身高、体重、三围、
# bra、鞋码、个性域名（有个人写真照片要下载）、个人经历
# 个人详细信息通过JS加载，这种方式读不了
def extract_personal_page(url):
    # 加载页面，等待页面加载完成，即出现了个性域名项目
    user_id = url.split('=')[1]
    href = '//mm.taobao.com/' + user_id + '.htm'
    driver.get(url)
    try:
        wait = WebDriverWait(driver, 10)
        locator = driver.find_element
        element = wait.until(
            EC.presence_of_element_located((By.XPATH, '//a[@href="%s"]' % href))
        )
    except TimeoutException as e:
        print('加载页面超时了：%s' % url)
    else:
        if element:
            html = driver.page_source
        else:
            html = ''
    # 获取公历出生日期
    s1 = r'<ul class="mm-p-info-cell.*?<li class="mm-p-cell-left.*?<span>(.*?)</s'
    # 获取职业
    s2 = r'.*?<li class="mm-p-cell-left.*?<span>(.*?)</s.*?'
    # 获取血型
    s3 = r'<li class="mm-p-cell-right.*?<span>(.*?)</s.*?'
    # 学校、专业
    s4 = r'<li>.*?<span>(.*?)</span>.*?'
    # 风格
    s5 = s4
    # 个性域名
    s6 = r'<div class="mm-p-info mm-p-domain-info.*?<li>.*?<span>(.*?)</s'
    s = s1 + s2 + s3 + s4 + s5 + s6
    pat = re.compile(s, re.S)
    if html:
        for item in pat.findall(html):
            print item[0], item[1], item[2], item[3], item[4], item[5]

# 根据年龄和出生日期计算出生年份
def count_birthday(ds, age):
    pat = re.compile(r'\s+(\d+)月(\d+)日')
    month = pat.search(ds).group(1)
    day = pat.search(ds).group(2)
    import datetime
    today = datetime.datetime.today()
    if int(day) < today.day:
        if int(month) <= today.month:
            year = today.year - age + 1
        else:
            year = today.year - age
    return year + month + day

# 下载图片
def download_img(url, fname):
    data = urllib2.urlopen(url).read()
    with open(fname, 'wb') as fd:
        fd.write(data)
        print '保存照片：', name

page_info = get_taobao_info(download_page(base_url, 1))
for per_url, model_info in page_info:
    print per_url
    extract_personal_page(per_url)
    #print model_info
# print download_page(base_url, 1)
# req = urllib2.Request(base_url)
# resp = urllib2.urlopen(req)
# html = resp.read().decode('gbk')
#
# s1 = r'<div class="pic s60.*?<img src="(.*?)" alt=.*?<a class="lady-name" href="(.*?)".*?>(.*?)</.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>'
# s2 = r'.*?<em>(.*?)</em>.*?<strong>(.*?)</strong>'
# pat = re.compile(s1+s2, re.S)
#
# # 匹配在淘宝上的相关数据，积分，好评，导购照片，签约数
# s3 = r'<div class="list-info.*?</span>(.*?)</dd>.*?<strong>(.*?)</'
# s4 = r'.*?<strong>(.*?)</.*?<strong>(.*?)</.*?<strong>(.*?)</.*?'
# s5 = r'<p class="description.*?>(.*?)</p>'
# pat2 = re.compile(s3+s4+s5, re.S)
#
# for item in pat.findall(html):
#     print item[0], item[1]
#     print item[2], item[3]
#     print item[4], item[5], item[6]
#
# for item in pat2.findall(html):
#     print item[0]
#     print item[1]
#     print item[2]
#     print item[3]
#     print item[4]
#     print item[5].strip()
