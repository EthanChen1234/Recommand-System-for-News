import pymongo
import datetime

# mongodb://[username:password@]host1[:port1][/[database][?options]]
# URL = 'mongodb://localhost:27017'  # win home
URL = 'mongodb://192.168.100.8:2710'  # Linux


class MongoDB(object):
    def __init__(self, db='news', collection='sina'):
        client = pymongo.MongoClient(URL, connectTimeoutMS=12000, connect=False)   # False 避免多次连
        self.db = client[db]
        self.collection = self.db[collection]

    def insert_one(self, data):
        # data = dict()
        # data['name'] = 'ethan'
        # data['dates'] = datetime.datetime.utcnow()
        self.collection.insert_one(data)

    def find_one(self, info):
        # info = {'name': 'ethan'}
        result = self.collection.find_one(info)  # object
        return result

    def find_all(self, info):
        # info = {'name': 'ethan'}
        result = self.collection.find(info)  # object
        return result

    def delete_one(self, info):
        self.collection.delete_one(info)

    def delete_collection(self):
        # 删除当前集合
        self.collection.drop()


if __name__ == '__main__':
    mongo = MongoDB(db='news', collection='sina')
    result = mongo.find_all({'type': 'china'})
    for elem in result:
        print(elem['type'])



#     # 插入
#     data = dict()
#     data['name'] = 'ethan'
#     data['dates'] = datetime.datetime.utcnow()
#     mongo.insert_one(data)
#     #
#     # 查找
#     info = {'name': 'ethan'}
#     results = mongo.find_all(info)
#     for result in results:
#         print(result)
#
#     # 删除
#     info1 = {'name': 'ethan1'}
#     mongo.delete_one(info1)
#     #
#     # mongo.delete_one({'name': 'ethan'})



