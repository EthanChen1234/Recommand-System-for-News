#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import datetime
import sys
import os
sys.path.append(os.path.dirname(__file__).split('models')[0])

# from dao.mongo_db import MongoDB
from dao.mysql_db import Mysql
# from dao.mysql_db import Content
from models.labels.entity.content import Content
from models.keywords.tfidf import Segment
from sqlalchemy import distinct

# mongodb连接问题
import pymongo
# URL = 'mongodb://localhost:27017'  # win home
URL = 'mongodb://192.168.100.8:2710'  # Linux
client = pymongo.MongoClient(URL, connectTimeoutMS=12000, connect=False)   # False 避免多次连


class ContentLabel(object):
    def __init__(self):
        self.seg = Segment(stopword_files=['baidu_stopwords.txt'], userdict_files=[])
        self.engine = Mysql()
        self.session = self.engine._DBSession()
        # self.mongo = MongoDB(db='news')
        # self.mongo_db = self.mongo.db
        self.collection = client['news']['sina']

    def get_data_from_mysql(self, flag):
        types = self.session.query(distinct(Content.type))
        for i in types:
            # print(i[0])  # film, ...
            if flag == 1:  # 增量
                date_min = datetime.datetime.now() - datetime.timedelta(days=1)  # 定时任务时间间隔需对应
                res = self.session.query(Content).filter(Content.type == i[0], Content.times >= date_min)  # 表Content
            else:
                res = self.session.query(Content).filter(Content.type == i[0])  # 表Content
            if res.count() > 0:
                for x in res.all():
                    # x.title没有利用起来
                    keywords = self.get_keywords(x.content, 10)
                    word_nums = self.get_words_nums(x.content)
                    create_time = datetime.datetime.utcnow()
                    content_collection = dict()
                    content_collection['describe'] = x.content
                    content_collection['type'] = x.type
                    content_collection['keywords'] = keywords
                    content_collection['word_num'] = word_nums
                    content_collection['news_date'] = x.times
                    content_collection['hot_heat'] = 10000  # 初始值热度值(可以为0)
                    content_collection['likes'] = 0        # 点赞
                    content_collection['reads'] = 0        # 阅读
                    content_collection['collections'] = 0  # 收藏
                    content_collection['create_time'] = create_time
                    self.collection.insert_one(content_collection)  # 放到 mongodb中去, 可以用insert_many优化
                # 存入MongoDB后，同时删除MySQL中对应数据
                self.session.query(Content).filter(Content.type == i[0]).delete()  # 好像没有删除？？

    def get_keywords(self, contents, nums=10):
        keywords = self.seg.extract_keyword(contents)[:nums]
        return keywords

    def get_words_nums(self, contents):
        ch = re.findall('([\u4e00-\u9fa5])', contents)
        nums = len(ch)
        return nums


if __name__ == '__main__':
    content_label = ContentLabel()
    content_label.get_data_from_mysql(flag=0)  # 0 全量， 1 增量

