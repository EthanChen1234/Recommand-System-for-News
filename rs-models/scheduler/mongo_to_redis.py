import sys
import os
import datetime
sys.path.append(os.path.dirname(__file__).split('scheduler')[0])

from dao import redis_db

# from dao.mongo_db import MongoDB
import pymongo
# URL = 'mongodb://localhost:27017'  # win home
URL = 'mongodb://192.168.100.8:2710'  # Linux
client = pymongo.MongoClient(URL, connectTimeoutMS=12000, connect=False)   # False 避免多次连


class WriteToRedis(object):
    def __init__(self):
        self._redis = redis_db.Redis().redis
        # self.mongo = MongoDB('news')
        self.collection = client['news']['sina']

    def get_from_mongoDB(self, flag):
        pipelines = [{
            '$group': {
                '_id': "$type"
            }
        }]

        types = self.collection.aggregate(pipelines)  # [{'_id': 'zongyi'}...]
        count = 0
        for type in types:
            info = {"type": type['_id']}
            if flag == 1:
                date_min = datetime.datetime.now() - datetime.timedelta(days=1)  # 定时任务时间间隔需对应
                info['news_date'] = {'$gt': date_min}
            datas = self.collection.find(info)
            for data in datas:
                result = dict()
                result['describe'] = data['describe']  # 原文
                result['type'] = data['type']  # 类型
                result['news_date'] = data['news_date']  # 消息发布时间
                result['content_id'] = str(data['_id'])
                result['likes'] = data['likes']
                result['reads'] = data['reads']
                result['collections'] = data['collections']
                result['hot_heat'] = data['hot_heat']
                self._redis.set("news_detail:"+str(data['_id']), str(result))
                # if count % 100 == 0:
                #     print(count)
                # count += 1


if __name__ == '__main__':
    write_to_redis = WriteToRedis()
    write_to_redis.get_from_mongoDB(flag=0)  # 0 全量， 1 增量
