#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import re
import urllib2, urllib
from tools import HtmlTagStrip


class BDTB():

    def __init__(self, base_url, see_lz=1):
        self.base_url = base_url
        self.see_lz = '?see_lz=' + str(see_lz)


    def get_page_content(self, page):
        # params = urllib.urlencode({'see_lz': self.see_lz, 'pn': str(page)})
        url = self.base_url + self.see_lz + '&pn=' + str(page)
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:49.0) Gecko/20100101 Firefox/49.0'
            }
            req = urllib2.Request(url, headers=headers)
            resp = urllib2.urlopen(req)
        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                print '连接百度贴吧失效：', e.reason
                return None
        else:
            return resp.read()

    def get_title(self, html):
        pat = re.compile(r'<h3 class="core_title_txt.*?>(.*?)</h3>', re.S)
        found = pat.search(html)
        if found:
            return found.group(1)
        else:
            return None

    def get_page_num_and_comment_num(self, html):
        comment_pat = re.compile(r'<li class="l_reply_num.*?><span.*?>(.*?)</span>')
        page_pat = re.compile(r'<li class="l_reply_num.*?><span.*?</span>' +
                              r'.*?<span.*?>(.*?)</span>', re.S)
        comment_found = comment_pat.search(html)
        page_found = page_pat.search(html)
        page_num = page_found.group(1).strip() if page_found else None
        comment_num = comment_found.group(1) if comment_found else None
        return (page_num, comment_num)

    def get_tiezi_content(self, html):
        pat = re.compile(r'<div id="post_content_.*?>(.*?)</div>', re.S)
        content = pat.findall(html) if pat.search(html) else []
        tag_clear = HtmlTagStrip()
        content = [tag_clear.clear_tags(v) for v in content]
        # for i, v in enumerate(content):
        #     content[i] = tag_clear.clear_tags(v)
        return content

    def start(self):
        index = 1
        page = 1
        html = self.get_page_content(page)
        title = self.get_title(html)
        page_num, comment_num = self.get_page_num_and_comment_num(html)
        content = self.get_tiezi_content(html)
        with open('tieba_tiezi.txt', 'w') as fd:
            fd.write('帖子：%s，共有页数：%s，评论数：%s\n\n' % (title, page_num, comment_num))
            while page < (int(page_num) + 1):
                print '正在下载第%s页的内容' % page
                fd.write('当前页：%s，帖子内容如下：\n\n' % page)
                for item in content:
                    fd.write('%s楼：%s\n---------------------------------------\n' % (index, item))
                    index += 1
                page += 1
                html = self.get_page_content(page)
                content = self.get_tiezi_content(html)
                # n = raw_input('输入Q结束，Enter查看下一页：')
                # if n == 'Q' or n == 'q':
                #     break
                # else:
                #     html = self.get_page_content(page)
                #     content = self.get_tiezi_content(html)
            print '帖子到此结束'


if __name__ == "__main__":
    url = 'https://tieba.baidu.com/p/3138733512'
    t = BDTB(url)
    t.start()
