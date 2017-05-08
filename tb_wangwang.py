#!/usr/bin/env python
# _*_ coding: utf-8 _*_

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.common.keys import Keys


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
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#J_ItemList div.productImg-wrap'))
        )
    except TimeoutException:
        print('查询失败')
        driver.quit()
    print('查询成功')
    html = driver.page_source
    return html


def scroll_window():
    pass


if __name__ == "__main__":
    html = get_result('卧室灯')
    # driver.quit()
