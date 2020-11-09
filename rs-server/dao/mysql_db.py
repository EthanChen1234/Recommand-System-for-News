from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists

class Mysql(object):
    def __init__(self):
        self.engine = create_engine('mysql+pymysql://root:123456@47.104.154.74:3306/sina')
        self._DBSession = sessionmaker(bind=self.engine)

