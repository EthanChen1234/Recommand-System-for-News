import sys
import os
import datetime
sys.path.append(os.path.dirname(__file__).split('scheduler')[0])

from dao import redis_db
from dao.mongo_db import MongoDB


class SimpleRecList(object):
    def __init__(self):
        self._redis = redis_db.Redis().redis
        self.mongo = MongoDB()
        self.collection = self.mongo.collection

    def get_news_order_by_time(self, flag):
        # 冷启动，时间近（分数高），时间远（分数低）
        info = {}
        if flag == 1:  # 增量
            date_min = datetime.datetime.now() - datetime.timedelta(days=1)  # 定时任务时间间隔需对应
            info['news_date'] = {'$gt': date_min}
        data = self.collection.find(info).sort([("news_date", -1)])
        count = 10000  # 分数

        for news in data:
            self._redis.zadd("rec_list", {str(news['_id']): count})
            count -= 1
            # if count % 10 == 0:
            #     print(count)


if __name__ == '__main__':
    simple = SimpleRecList()
    simple.get_news_order_by_time(flag=0)   # 0 全量， 1 增量