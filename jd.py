#!/usr/bin/env python
# _*_ coding: utf-8 _*_

from downloader import Downloader
import lxml.html


def extract_price(html):
    tree = lxml.html.fromstring(html)
    price_tag = tree.cssselect('span#jdPrice-copy')[0]
    price = price_tag.text_content().strip()
    title_tag = tree.cssselect('div.prod-title > a > span.title-text')[0]
    title = title_tag.text.strip()
    return price, title


def extract_title(html):
    pass


def extract_gome_price(html):
    tree = lxml.html.fromstring(html)
    price_tag = tree.cssselect('span#prdPrice')[0]
    price = price_tag.text_content()
    title_tag = tree.cssselect('div.hgroup > h1')[0]
    title = title_tag.text
    # print(title, price)
    return price, title


if __name__ == "__main__":
    url = 'http://item.m.jd.com/product/1084399013.html'
    url2 = 'http://item.m.jd.com/product/1121452.html'
    D = Downloader()
    # html = D(url)
    # html = html.decode('utf-8', 'ignore')
    # price, title = extract_price(html)
    # print(price, title)
    # g_url = 'http://item.m.gome.com.cn/product-9134088881-1123050867.html'
    g_url = 'http://item.gome.com.cn/A0005786258-pop8008596485.html?intcmp=jiadian-1000060225-4'
    price, title = extract_gome_price(D.phatomjs_download(g_url))
    print(title, price)
