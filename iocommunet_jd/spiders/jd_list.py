# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from iocommunet_jd.items import IocommunetJdItem
from bs4 import BeautifulSoup

class jd_spider(Spider):
    name = "jd_list"
    start_urls = ["https://www.jd.com/allSort.aspx"]

    def parse(self, response):  # 解析jd全部页面
        bs = BeautifulSoup(response.text, 'html5lib')
        lists = bs.select('.category-items .category-item')
        categoryList = []
        dataObj = []
        lens = 0
        for i in range(1, len(lists), 1): #一级分类
            data = {
                "id": 1,
                "name": "",
                "stype": 1
            }
            id1 = ''
            data['name'] = lists[i].select('.item-title span')[0].text.encode("utf-8")
            cate2 = lists[i].select('.items .clearfix')
            cca2 = []
            for c2 in cate2: #二级分类
                cc2 = {}
                cc2['name'] = c2.select('dt a')[0].text.encode("utf-8")
                cate3 = c2.select('dd a')
                cca3 = []
                id2 = ''
                for c3 in cate3: #三级分类
                    if(c3.get("href").find("list.jd.com/") >= 0):
                        id1 = c3.get('href').split('=')[1].split(',')[0]
                        id2 = c3.get('href').split('=')[1].split(',')[1]
                        cc3 = {}
                        cc3['id'] = c3.get('href').split('=')[1].split(',')[2]
                        cc3['name'] = c3.text.encode("utf-8")
                        cc3['stype'] = 3
                        cc3['url'] = 'https:' + c3.get('href')
                        cca3.append(cc3)
                        lens += 1
                        c5 = {}
                        c5['name'] = cc3['name']
                        c5['url'] = 'https:' + c3.get('href')
                        categoryList.append(c5)
                cc2['children'] = cca3
                cc2['stype'] = 2
                cc2['id'] = id2
                cca2.append(cc2)
            data['children'] = cca2
            data['id'] = id1
            dataObj.append(data)
        items = IocommunetJdItem()
        items['cate'] = dataObj
        items['catelist'] = categoryList
        return items


