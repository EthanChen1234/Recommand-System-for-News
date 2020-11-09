#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Text
Base = declarative_base()  # 创建对象基类

# SQL_URL = "mysql+pymysql://root:chenhao828@localhost:3306/scrapy"  # win home
SQL_URL = "mysql+pymysql://chen:123@192.168.100.8:3010/scrapy"  # linux
# SQL_URL = "mysql+pymysql://chen:123@localhost:3306/scrapy"  # linux


class Mysql(object):
    def __init__(self):
        self.engine = create_engine(SQL_URL, encoding='utf-8')  # 初始化数据库连接
        self._DBSession = sessionmaker(bind=self.engine)  # 创建DBSession类型


# 无法从content_label中引入
# class Content(Base):
#     __tablename__ = 'sina'  # 表名字sina
#     __table_args__ = {"mysql_charset": "utf8mb4"}
#     id = Column(Integer(), primary_key=True)
#     type = Column(String(20))
#     times = Column(DateTime())
#     title = Column(String(200))
#     content = Column(Text())
#
#     def __init__(self):
#         mysql = Mysql()
#         engine = mysql.engine
#         Base.metadata.create_all(engine)

