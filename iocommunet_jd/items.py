# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field

class IocommunetJdItem(Item):
    # define the fields for your item here like:
    name = Field()
    cate = Field()
    catelist = Field()
    pass

class goodsItem(scrapy.Item):
    link = Field()  # 商品链接
    pid = Field()  # 商品ID
    img = Field()   #商品图片
    name = Field()  # 商品名字
    comment_num = Field()  # 评论人数
    shop_name = Field()  # 店家名字
    sid = Field() #店铺id
    price = Field()  # 价钱
    commentVersion = Field()  # 为了得到评论的地址需要该字段
    score1count = Field()  # 评分为1星的人数
    score2count = Field()  # 评分为2星的人数
    score3count = Field()  # 评分为3星的人数
    score4count = Field()  # 评分为4星的人数
    score5count = Field()  # 评分为5星的人数

