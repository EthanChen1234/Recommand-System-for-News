import redis


class Redis(object):
    def __init__(self):
        self.redis = redis.StrictRedis(host='192.168.100.8',  # Linux
                                       port=6310,
                                       db=0,
                                       password='',
                                       decode_responses=True)

        # self.redis = redis.StrictRedis(host='localhost',  # win home
        #                                port=6379,
        #                                db=0,
        #                                password='',
        #                                decode_responses=True)

    def redis_test(self):
        r = self.redis
        r.set('apple', 'a')
        print(r.get('apple'))


# if __name__ == '__main__':
#     redis = Redis()
#     redis.redis_test()


