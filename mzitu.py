#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import lxml.html
import os
import random
from pymongo import MongoClient
import datetime

from downloader import Downloader
from settings import USER_AGENT, get_proxy_ips


class Mzitu:
    def __init__(self, start_url, img_path, downloader=Downloader()):
        self.start_url = start_url
        self.img_path = img_path
        self.D = downloader
        # mongodb存储数据
        client = MongoClient()
        db = client['meinvxiezhenji']
        self.meizitu_collection = db['meizitu']
        self.title = ''
        self.url = ''
        self.img_urls = []

    def all_urls(self):
        link_queue = self.get_all_links(self.start_url)
        for link in link_queue[:11]:
            title, href = self.extract_link(link)
            if self.meizitu_collection.find_one({'主题页面': href}):
                print(u'这个页面已经爬过了')
            else:
                self.title = title
                self.url = href
                self.get_img_and_save(title, href)

    def get_all_links(self, url):
        start_html = self.D(url)
        tree = lxml.html.fromstring(start_html)
        # 找到'<div class="all">'这个节点，可以有多种方式
        # 获取页面中所有的'div'元素，选取属性为@class="all"的即可
        # div_all = tree.xpath('//div[@class="all"]')[0]
        # 从最顶层的标签'body'开始，逐层向下，找到元素所在的层，通过属性获取即可
        div_all_2 = tree.xpath('body/div/div/div[@class="all"]')[0]
        # 获取某个元素下包含的某个标签的所有值，有2种方式
        # link_queue = [t for t in div_all.iterdescendants('a')]
        # 从当前元素开始，获取当前元素下的某个标签的所有值
        link_queue_2 = div_all_2.xpath('.//a')
        return link_queue_2

    def extract_link(self, link):
        return (link.text, link.get('href'))

    def mkdir(self, path):
        print(u'文件夹:' + path)
        isExist = os.path.exists(path)
        if not isExist:
            print(u'创建新的')
            os.makedirs(path)
        else:
            print(u'文件夹已经存在了')

    def get_img_and_save(self, title, href):
        html = self.D(href)
        html_tree = lxml.html.fromstring(html)
        last_page_div = html_tree.xpath('//div[@class="pagenavi"]')[0]
        last_page_a = last_page_div.xpath('.//a')[-2]
        last_page = int(last_page_a.find('span').text)
        if self.img_urls:
            self.img_urls = []
        # 部分标题带？在win下存储会有问题
        img_saved_dir = os.path.join(self.img_path, title.strip().replace('?', '_'))
        # 创建图片的存储目录
        self.mkdir(img_saved_dir)
        for p in range(1, last_page+1):
            img_url = (href + '/' + str(p)) if p > 1 else href
            self.img_urls.append(img_url)
            img_html = self.D(img_url)
            img_tree = lxml.html.fromstring(img_html)
            img_div = img_tree.xpath('//div[@class="main-image"]')[0]
            img_t = img_div.xpath('p/a/img')[0]
            img_src = img_t.get('src')
            img_name = img_src[-9:-4]
            img = self.D(img_src)
            with open(img_saved_dir + '/' + img_name+'.jpg', 'ab') as fd:
                fd.write(img)
            if p == last_page:
                post = {
                    '标题': self.title,
                    '主题页面': self.url,
                    '图片地址': self.img_urls,
                    '获取时间': datetime.datetime.now()
                }
                self.meizitu_collection.insert_one(post)
                print(u'插入数据库成功')

    def clear(self):
        self.meizitu_collection.drop()



if __name__ == "__main__":
    # proxy = get_proxy_ips()
    # downloader = Downloader(user_agent=random.choice(USER_AGENT), proxies=proxy,
    #                        num_retries=2)
    downloader = Downloader(user_agent=random.choice(USER_AGENT), num_retries=2)
    start_url = 'http://www.mzitu.com/all'
    img_path = '/home/teddy/Pictures/mzitu'
    mzitu = Mzitu(start_url, img_path, downloader=downloader)
    mzitu.all_urls()
    # mzitu.clear()
