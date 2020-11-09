# coding: utf-8

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import re

from sqlalchemy import Text, String, Integer, DateTime, Column, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# SQL_URI = "mysql+pymysql://root:chenhao828@localhost:3306/scrapy"  # win home
SQL_URI = "mysql+pymysql://chen:123@192.168.100.8:3010/scrapy"  # linux
# SQL_URI = "mysql+pymysql://chen:123@localhost:3306/scrapy"  # linux


class Data(Base):
    __tablename__ = 'sina'  # 表名字sina
    __table_args__ = {"mysql_charset": "utf8mb4"}
    id = Column(Integer(), primary_key=True)
    type = Column(String(20))
    times = Column(DateTime())
    title = Column(String(200))
    content = Column(Text())


class SinaPipeline:
    # # case1, save to csv
    # def process_item(self, item, spider):
    #     # desc = ''
    #     # for line in item['desc']:
    #     #     line = re.sub(r'\s', '', line)
    #     #     desc += line
    #     strs = item['type'] + ',' + item['title'] + ',' + str(item['times']) + ',' + item['desc'] + '\n'
    #     self.file.write(strs)
    #
    # def open_spider(self, spider):
    #     self.file = open('./sina1.csv', 'a', encoding='utf-8-sig')
    #     self.file.write('type' + ',' + 'title' + ',' + 'times' + ',' + 'desc' + '\n')
    #
    # def close_spider(self, spider):
    #     self.file.close()

    # case2, save to MySQL
    def open_spider(self, spider):
        self.engine = create_engine(SQL_URI, encoding='utf-8')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)  # 实例化sessionmaker, 绑定engine
        self.sess = Session()  # 实例化会话

    def process_item(self, item, spider):
        new = Data()
        new.title = item['title']
        new.type = item['type']
        new.times = item['times']
        new.content = item['desc']
        self.sess.add(new)
        self.sess.commit()
        return item

    def close_spider(self, spider):
        self.sess.close()
