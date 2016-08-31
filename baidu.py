#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request
import urllib.error
import re

class Bdtb(object):
    def __init__(self, base_url, see_lz):
        self.base_url = base_url
        self.see_lz = '?see_lz'+ str(see_lz)
        self.tool = Tool()

    def get_page(self, page_num):
        try:
            url = self.base_url+ self.see_lz+ '&pn='+ str(page_num)
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            html = response.read().decode('utf-8')
            return html
        except urllib.error.URLError as e:
            if hasattr(e, "reason"):
                print("链接百度贴吧失败", e.reason)
                return None

    def get_title(self, page):
        # page = self.get_page()
        # print(page)
        pattern = re.compile('<h3 class="core_title_txt.*?>(.*?)</h3>',re.S)
        search = re.search(pattern, page)
        if search:
            result = str(search.group(1)).strip()
            # print(result)
            return result
        else:
            return None

    def get_reply_num(self, page):
        # page = self.get_page()
        pattern = re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>', re.S)
        search = re.search(pattern, page)
        if search:
            result = str(search.group(1)).strip()
            # print(result)
            return result
        else:
            return None

    def get_content(self, page):
        # page = self.get_page()
        pattern = re.compile('<div id="post_content_.*?>(.*?)</div>', re.S)
        items = re.findall(pattern, page)
        for item in items:
            # print(item)
            print(self.tool.replace(item))

class Tool(object):
    # 去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    # 删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    # 把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    # 将表格制表<td>替换为\t
    replaceTD = re.compile('<td>')
    # 把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    # 将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    # 将其余标签剔除
    removeExtraTag = re.compile('<.*?>')

    def replace(self, x):
        x = re.sub(self.removeImg, "", x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.replaceLine, "\n", x)
        x = re.sub(self.replaceTD, "\t", x)
        x = re.sub(self.replacePara, "\n    ", x)
        x = re.sub(self.replaceBR, "\n", x)
        x = re.sub(self.removeExtraTag, "", x)
        # strip()将前后多余内容删除
        return x.strip()

if __name__ == '__main__':
    base_url = 'http://tieba.baidu.com/p/3138733512'
    bdtb = Bdtb(base_url,1)
    html = bdtb.get_page(1)
    bdtb.get_title(html)
    bdtb.get_content(html)
    page = int(bdtb.get_reply_num(html))
    # print(page)
    index = 2
    while page - index >= 0:
        html = bdtb.get_page(index)
        bdtb.get_content(html)
        index += 1

