#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import urllib.request
import urllib.error
import re


DATABASE_NAME = 'spider.db'

#糗事百科爬虫类
class Qsbk(object):

    #初始化
    def __init__(self):
        #页码
        self.page_index = 1

        self.user_agent = 'AppleWebKit/537.36 (KHTML, like Gecko)'
        self.headers = {'User-Agent':self.user_agent}

        #存放是否继续运行的变量
        self.enable = False

        self.creat_database()


    # 创建数据库
    def creat_database(self):
        try:
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()
            cursor.execute('create table if not exists qsbk (id INTEGER PRIMARY KEY NOT NULL , name text, content text)')
        finally:
            cursor.close()
            conn.commit()
            conn.close()

    # 保存数据到数据库
    def save_to_datebase(self, item):
        try:
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()
            cursor.execute('insert into qsbk(name, content) VALUES (?, ?)',(item[0], str(item[1]).strip()))
        except sqlite3.OperationalError as e:
            print(e)
        finally:
            cursor.close()
            conn.commit()
            conn.close()


    def parser_page_content(self, page_index):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(page_index)

            request = urllib.request.Request(url, headers=self.headers)

            response = urllib.request.urlopen(request)

            content = response.read().decode('utf-8')

            return content
        except urllib.error.URLError as e:
            self.enable = False
            if hasattr(e, "reason"):
                print('链接糗事百科失败,错误原因:', e)
                return None


    def get_page_content(self, page_index):
        html = self.parser_page_content(page_index)
        if not html:
            print('页面加载失败')
            return None

        pattern = re.compile(
            '<div class="author clearfix">.*?href.*?<img src.*?title=.*?<h2>(.*?)</h2>.*?<div class="content">(.*?)</div>.*?<i class="number">.*?</i>',
            re.S)
        items = re.findall(pattern, html)
        for item in items:
            print('item[0] is ', item[0])
            print('item[1] is ', item[1])
            self.save_to_datebase(item)

    def start(self):
        self.enable = True
        while self.enable:
            if self.page_index < 100:
                self.get_page_content(self.page_index)
                self.page_index += 1
            else:
                break

if __name__ == '__main__':
    spider = Qsbk()
    spider.start()
