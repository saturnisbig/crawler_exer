#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import urllib
import urllib2
import cookielib
import random
import lxml.html
import requests
import re
import configparser
import base64

from settings import USER_AGENT

mission_url = 'https://www.v2ex.com/mission/daily'
#cookie = cookielib.MozillaCookieJar(filename)


class V2EX():
    def __init__(self, configfile='me_info.conf'):
        self.configfile = configfile
        self.login_url = 'https://www.v2ex.com/signin'
        self.username = ''
        self.passwd = ''

    def load_info(self):
        config = configparser.ConfigParser()
        config.read(self.configfile)
        if config.has_section('V2EX_INFO'):
            self.username = base64.b64decode(config['V2EX_INFO']['username'])
            self.passwd = base64.b64decode(config['V2EX_INFO']['passwd'])
            return True
        else:
            print('配置文件没有正确设置：%s' % self.configfile)
            return False

    def sign(self):
        if not self.load_info():
            return
        headers = {
            'Host':'www.v2ex.com',
            'Origin':'https://www.v2ex.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:49.0) Gecko/20100101 Firefox/49.0'
        }
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        result = {}
        req = urllib2.Request(self.login_url, headers=headers)
        resp = opener.open(req)
        tree = lxml.html.fromstring(resp.read())
        for t in tree.xpath('//input[@class="sl"]'):
            t_type = t.get('type')
            if t_type == 'text':
                result['username'] = t.get('name')
            elif t_type == 'password':
                result['password'] = t.get('name')
            else:
                print('unknown type: ', t_type)
        # 具有name属性为once的input标签
        once_t = tree.xpath('//input[@name="once"]')[0]
        result['once'] = once_t.get('value')
        result['next'] = tree.xpath('//input[@name="next"]')[0].get('value')

        # username = raw_input("请输入用户名：")
        # password = raw_input("请输入密码：")
        postdata = urllib.urlencode({
            result.get('username'): self.username,
            result.get('password'): self.passwd,
            'once': result.get('once'),
            'next': result.get('next')
        })
        # print postdata
        # 登录前添加header元素
        headers['Referer'] = 'https://www.v2ex.com/signin'
        req2 = urllib2.Request(self.login_url, postdata, headers)
        resp2 = opener.open(req2)
        login_html = resp2.read()
        #print login_html
        if '条未读提醒' in login_html:
            print("login success")
            resp3 = opener.open(mission_url)
            sign_tree = lxml.html.fromstring(resp3.read())
            sign_btn = sign_tree.xpath('//input[@type="button"]')[0].get('onclick')
            sign_href = sign_btn.split("'")[1]
            if re.search(r'/balance', sign_href):
                print('可能已经签到过了')
            elif re.search(r'/mission/daily', sign_href):
                sign_resp = opener.open('https://www.v2ex.com' + sign_href)
                print('签到成功')
            else:
                print('获取签到地址有误：', sign_href)
        else:
            print("登录失败")


def request_login(login_url):
    headers = {
        'Host':'www.v2ex.com',
        #'Referer':'https://www.v2ex.com/signin',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:52.0) Gecko/20100101 Firefox/52.0'
    }
    sess = requests.Session()
    sess.headers = headers

    resp = sess.get(login_url)
    tree = lxml.html.fromstring(resp.text)
    username = ''
    password = ''
    for t in tree.xpath('//input[@class="sl"]'):
        t_type = t.get('type')
        if t_type == 'text':
            username = t.get('name')
        elif t_type == 'password':
            password = t.get('name')
        else:
            print('unknown type: ', t_type)
    # 具有name属性为once的input标签
    once_t = tree.xpath('//input[@name="once"]')[0]
    uname = raw_input("请输入用户名：")
    passwd = raw_input("请输入密码：")
    postdata = {
        username: uname,
        password: passwd,
        'once': once_t.get('value'),
        'next': '/'
    }
    print postdata
    sess.headers.update({'Referer':'https://www.v2ex.com/signin'})
    resp = sess.post(login_url, postdata, headers=headers)
    #resp = sess.get(mission_url, headers=headers)
    if u'条未读提醒' in resp.text:
        print 'login success.'
        sign_resp = sess.get(mission_url)
        sign_tree = lxml.html.fromstring(sign_resp.text)
        sign_btn = sign_tree.xpath('//input[@type="button"]')[0].get('onclick')
        sign = sess.get('https://www.v2ex.com' + sign_btn.split("'")[1])
        print sign.ok
    else:
        print 'login false.'

if __name__ == "__main__":
    v2ex = V2EX()
    v2ex.sign()
    #request_login(login_url)
