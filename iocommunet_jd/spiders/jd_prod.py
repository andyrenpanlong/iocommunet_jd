# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from iocommunet_jd.items import goodsItem
from scrapy.selector import Selector
import scrapy
import re
import json
import os

class jd_prod(Spider):
    name = "jd_prod"
    start_urls = []
    if len(start_urls) <= 0:
        print "链接数目为0，爬虫暂未开启..."
        os._exit(0)

    def parse_price(self, response):
        item1 = response.meta['item']
        temp1 = response.body.split('jQuery([')
        s = temp1[1][:-4]  # 获取到需要的json内容
        js = json.loads(str(s))  # js是一个list
        if js.has_key('pcp'):
            item1['price'] = js['pcp']
        else:
            item1['price'] = js['p']
        num = item1['pid']  # 获得商品ID
        s1 = str(num)
        url = "https://chat1.jd.com/api/checkChat?my=list&pidList=" + str(item1['pid'][0])
        print "get:", url
        yield scrapy.Request(url, meta={'item': item1}, callback=self.parse_shopMessage)


    def parse_shopMessage(self, response):
        item1 = response.meta['item']
        temp = response.body.split("null(")
        s = temp[1][:-2]  # 获取到需要的json内容
        js = json.loads(str(s))[0]  # js是一个list
        if js.has_key('seller'):
            item1['shop_name'] = js['seller']
        else:
            item1['shop_name'] = ''
        if js.has_key('shopId'):
            item1['sid'] = js['shopId']
        else:
            item1['sid'] = ''
        return item1

    def parse_getCommentnum(self, response):
        item1 = response.meta['item']
        # response.body是一个json格式的
        js = json.loads(str(response.body))
        item1['score1count'] = js['CommentsCount'][0]['Score1Count']
        item1['score2count'] = js['CommentsCount'][0]['Score2Count']
        item1['score3count'] = js['CommentsCount'][0]['Score3Count']
        item1['score4count'] = js['CommentsCount'][0]['Score4Count']
        item1['score5count'] = js['CommentsCount'][0]['Score5Count']
        item1['comment_num'] = js['CommentsCount'][0]['CommentCount']
        num = item1['pid']  # 获得商品ID
        s1 = str(num)
        url = "http://pm.3.cn/prices/pcpmgets?callback=jQuery&skuids=" + s1[3:-2] + "&origin=2"
        yield scrapy.Request(url, meta={'item': item1}, callback=self.parse_price)


    def parse_detail(self, response):
        item1 = response.meta['item']
        temp = response.body.split('commentVersion:')
        pattern = re.compile("[\'](\d+)[\']")
        if len(temp) < 2:
            item1['commentVersion'] = -1
        else:
            match = pattern.match(temp[1][:10])
            item1['commentVersion'] = match.group()

        url = "http://club.jd.com/clubservice.aspx?method=GetCommentsCount&referenceIds=" + str(item1['pid'][0])
        yield scrapy.Request(url, meta={'item': item1}, callback=self.parse_getCommentnum)

    def parse(self, response):  # 解析搜索页
        sel = Selector(response)  # Xpath选择器
        goods = sel.xpath('//li[@class="gl-item"]')
        for good in goods:
            item1 = goodsItem()
            item1['pid'] = good.xpath('./div/@data-sku').extract()
            if not item1['pid']:
                item1['pid'] = good.xpath('./div/@data-sku').extract()
            item1['name'] = good.xpath('./div/div[@class="p-name"]/a/em/text()').extract()
            # item1['shop_name'] = good.xpath('./div/div[@class="p-shop"]/a/@title').extract()
            # if not item1['shop_name']:
            #     item1['shop_name'] = good.xpath('./div/div[@class="p-shop"]/@data-shop_name').extract()
            item1['link'] = good.xpath('./div/div[@class="p-img"]/a/@href').extract()
            item1['img'] = good.xpath('./div/div[@class="p-img"]/a/img/@src').extract()
            if not item1['img']:
                item1['img'] = good.xpath('./div/div[@class="p-img"]/a/img/@data-lazy-img').extract()
            if not item1['link']:
                continue
            url = "http:" + item1['link'][0] + "#comments-list"
            yield scrapy.Request(url, meta={'item': item1}, callback=self.parse_detail)
