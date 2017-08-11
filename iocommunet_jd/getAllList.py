# -*- coding: utf-8 -*-
from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
import time

def search_all_page_url(url):
    r = requests.get(url)
    all_pages = ''
    if r.status_code == 200:
        time.sleep(2)
        bs = BeautifulSoup(r.text, 'html5lib')
        #这里加判断的原因是类似这种链接"https://list.jd.com/list.html?cat=737,13297,1706"，浏览器会自动跳转
        #跳转后的链接为：https://www.jd.com/?static=13，导致没有分页，这种链接不应该加入我们的队列中去
        if(bs.select('#J_topPage i') and bs.select('#J_topPage i')[0].text):
            all_pages = int(bs.select('#J_topPage i')[0].text)
        else:
            all_pages = 0
        print "共计页数为：", all_pages, url
    else:
        print "页面信息获取失败"
    return all_pages

def creatAllUrl():
    client = MongoClient('127.0.0.1', 27017)
    db = client.admin
    collection = db.categorylist
    # 查找集合中所有数据
    for item in collection.find():
        url = item["url"]
        page = search_all_page_url(url)
        for i in range(1, page + 1, 1):
            start_urls.append(url + '&page=' + str(i))
            print "拼接的url:", url + '&page=' + str(i)

start_urls = []
creatAllUrl()
print len(start_urls)