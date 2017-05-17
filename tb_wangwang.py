#!/usr/bin/env python
# _*_ coding: utf-8 _*_

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.common.keys import Keys
import lxml.html
import time


driver = webdriver.Firefox()


def get_search_results(keyword):
    search_url = 'https://www.tmall.com/?spm=a220o.1000855.a2226mz.1.IZFzN0'
    driver.get(search_url)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'mq'))
        )
    except TimeoutException:
        print('加载页面失败')
    try:
        element = driver.find_element_by_css_selector('#mq')
        print('成功找到搜索框')
        keyword = keyword.decode('utf-8', 'ignore')
        print(u'输入关键字：%s' % keyword)
        for word in keyword:
            print(word)
            element.send_keys(word)
        element.send_keys(Keys.ENTER)
    except NoSuchElementException:
        print('没有找到搜索框')
    print('正在查询关键字')
    if is_list_page_load():
        html = driver.page_source
        return html
    else:
        print '没有查询到物品列表'
        driver.quit()


def is_list_page_load():
    try:
        WebDriverWait(driver, 10).until(
            # EC.presence_of_element_located((By.CSS_SELECTOR, '#J_ItemList div.productImg-wrap'))
            EC.presence_of_element_located((By.CSS_SELECTOR, '.ui-page b.ui-page-num'))
        )
    except TimeoutException:
        print('查询失败')
        return False
        driver.quit()
    return True


def extract_urls(doc):
    result = []
    tree = lxml.html.fromstring(doc)
    # 只能加载58个，存在页面没加载完的情况
    item_tags = tree.xpath('//div[@class="productImg-wrap"]/a')
    print(len(item_tags))
    for item in item_tags:
        url = item.get('href')
        if not url.startswith('http'):
            url = 'https://' + url
        result.append(url)
    return result


def is_recommends_appear(driver, max_times=10):
    count = 1
    result = scroll_window(driver, count)
    while not result:
        result = scroll_window(driver, count)
        if count == max_times:
            return False
        count += 1
    return True


def scroll_window(driver, count):
    print('正在尝试第' + str(count) + '次下拉')
    try:
        js = "window.scrollTo(0, document.body.scrollHeight-" + str(count*count*100) + ')'
        driver.execute_script(js)
    except WebDriverException:
        print('下拉寻找推荐宝贝时出错')
    # 等待实践不够长会出现部分数据加载不出来的情况
    time.sleep(8)
    try:
        driver.find_element_by_css_selector('#J_TjWaterfall li')
        driver.find_element_by_css_selector('#official-remind')
    except NoSuchElementException:
        return False
    return True


def scrap_recommends_page(url):
    print('开始寻找推荐宝贝' + url)
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'J_TabBarBox'))
        )
    except TimeoutException:
        print('页面加载失败')
        return False
    if is_recommends_appear(driver, 5):
        print('已经成功加载推荐宝贝信息')
        return driver.page_source
    else:
        return False


def extract_recommends_comment(doc):
    result = []
    tree = lxml.html.fromstring(doc)
    comment_tags = tree.xpath('//ul[@id="J_TjWaterfall"]//li')
    print(len(comment_tags))
    comment_count = 0
    for comment_tag in comment_tags:
        comments = []
        if comment_tag.xpath('./p'):
            # print '标签下面有评论'
            print('-------------------------' * 3)
            a = comment_tag.xpath('./a')[0]
            url = a.get('href')
            if not url.startswith('http'):
                url = 'https:' + url
            print(url)
            comment_count += 1
            for t in comment_tag.xpath('./p'):
                username = t.xpath('./b/text()')[0]
                comment = t.xpath('./text()')[0]
                print username, comment
                # print 'p标签下的内容：', t.xpath('string(.)')
                comment_info = (username, comment)
                comments.append(comment_info)
            result.append({'url': url, 'comments': comments})
    print '带评论数目：', comment_count
    return result

def get_next_page():
    try:
        js = 'window.scrollTo(0, document.body.scrollHeight)'
        driver.execute_script(js)
    except WebDriverException:
        print '页面下拉失败'
    try:
        next_page = driver.find_element_by_css_selector('b.ui-page-num > a.ui-page-next')
    except NoSuchElementException:
        print '没找到翻页按钮'
    else:
        print '找到了翻页按钮，点击！'
        next_page.click()
    driver.implicitly_wait(5)
    if is_list_page_load():
        doc = driver.page_source
        return doc
    else:
        print '翻页未成功'
        return ''

if __name__ == "__main__":
    # html = get_search_results('卧室灯')
    # urls = extract_urls(html)
    # doc = get_next_page()
    # print(extract_urls(doc))
    time.sleep(2)
    url = 'https://detail.tmall.com/item.htm?id=529724838242&skuId=3462171455381&user_id=2190232878&cat_id=50030199&is_b=1&rn=07760efb4e59cd59b1462aba5a7f0150'
    doc = scrap_recommends_page(url)
    extract_recommends_comment(doc)
    # driver.quit()
