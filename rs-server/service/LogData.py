from dao import mongo_db
from datetime import datetime


class LogData(object):
    def __init__(self):
        self._mongo = mongo_db.MongoDB(db='test')

    def insert_log(self, user_id, content_id, title, tables):
        collections = self._mongo.db_loginfo[tables]
        info = {}
        info['user_id'] = user_id
        info['content_id'] = content_id
        info['title'] = title
        info['date'] = datetime.utcnow()
        collections.insert_one(info)
        return True


    def get_logs(self, user_id, tables):
        collections = self._mongo.db_loginfo[tables]
        data = collections.find(
            {"user_id": user_id}
        )
        results = []
        for x in data:
            results.append(x)

        return results

    def modify_article_detail(self, key, ops):
        try:
            pass
        except Exception as e:
            return 1
