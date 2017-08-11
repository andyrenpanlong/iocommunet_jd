# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

class IocommunetJdPipeline(object):
    def process_item(self, item, spider):
        # 建立MongoDB数据库连接
        client = MongoClient('127.0.0.1', 27017)
        # 连接所需数据库,test为数据库名
        db = client.admin
        # 连接所用集合，也就是我们通常所说的表，test为表名
        for i in item['cate']:
            db.category.insert(i)
        for j in item['catelist']:
            db.categorylist.insert(j)
        print "数据写入成功"
        return item

class JdListPipeline(object):
    def process_item(self, item):
        # # Instantiate DB
        client = MongoClient('127.0.0.1', 27017)
        db = client.admin
        pid = item['pid'][0]
        name = item['name'][0]
        comment_num = str(item['comment_num'])
        if item['shop_name']:
            shop_name = item['shop_name']
        else:
            shop_name = ''
        sid = str(item['sid'])
        link = "https:" + item['link'][0]
        img = str(item['img'][0])
        commentVersion = str(item['commentVersion'])
        commentVersion = commentVersion[1:-1]
        score1count = str(item['score1count'])
        score2count = str(item['score2count'])
        score3count = str(item['score3count'])
        score4count = str(item['score4count'])
        score5count = str(item['score5count'])
        price = str(item['price'])
        data = {}
        data['pid'] = pid.encode('utf-8')
        data['name'] = name.encode('utf-8')
        data['comment_num'] = comment_num.encode('utf-8')
        data['shop_name'] = shop_name.replace('\r\n', '').strip(' ').encode('utf-8')
        data['sid'] = sid.encode('utf-8')
        data['link'] = link.encode('utf-8')
        data['img'] = img.encode('utf-8')
        data['commentVersion'] = commentVersion.encode('utf-8')
        data['score1count'] = score1count.encode('utf-8')
        data['score2count'] = score2count.encode('utf-8')
        data['score3count'] = score3count.encode('utf-8')
        data['score4count'] = score4count.encode('utf-8')
        data['score5count'] = score5count.encode('utf-8')
        data['price'] = price.encode('utf-8')
        # print "准备插入数据"
        db.product2.insert(data)
        print "插入数据成功"
        return item

class JdCommentPipeline(object):
    def process_item(self, item):
        # Instantiate DB
        client = MongoClient('127.0.0.1', 27017)
        db = client.admin
        data = {}
        data['user_name'] = item['user_name']
        data['user_ID'] = item['user_ID']
        data['userProvince'] = item['userProvince']
        data['content'] = item['content']
        data['good_ID']= item['good_ID']
        data['good_name'] = item['good_name']
        data['date'] = item['date']
        data['replyCount'] = item['replyCount']
        data['score'] = item['score']
        data['status'] = item['status']
        data['title'] = item['title']
        data['userRegisterTime'] = item['userRegisterTime']
        data['productColor'] = item['productColor']
        data['productSize'] = item['productSize']
        db.comment.insert(data)
        print "yes"

