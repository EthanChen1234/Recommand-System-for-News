from sqlalchemy import Column, String, create_engine,Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import DATE
from dao.mysql_db import Mysql

Base = declarative_base()
class User(Base):
    __tablename__ = 'User'
    id = Column(Integer(), primary_key=True)
    username = Column(String(20))
    password = Column(String(500))
    nick = Column(String(20))
    gender = Column(String(10))
    age = Column(String(2))
    city = Column(String(10))

    def __init__(self):
        mysql = Mysql()
        engine = mysql.engine
        Base.metadata.create_all(engine)
        print('aaaaaaaa')
