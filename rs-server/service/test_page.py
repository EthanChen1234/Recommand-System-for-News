#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
from dao import redis_db
import json


class PageSize(object):
    def __init__(self):
        self._redis = redis_db.Redis()

    def get_data_with_page(self, page, page_size):
        #1   1~10
        #2   11~20
        #3   21~30
        start = (page - 1) * page_size
        end = start + page_size
        data = self._redis.redis.zrange("rec_list", start, end)  # end-1 ？，测试下是否一次拿10条
        lst = list()
        for x in data:
            info = self._redis.redis.get("news_detail:" + x)
            lst.append(info)
        return lst


if __name__ == '__main__':
    page_size = PageSize()
    print(page_size.get_data_with_page(1, 20))

