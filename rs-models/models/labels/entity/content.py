from dao.mysql_db import Mysql
from sqlalchemy import Column, Integer, DateTime, Text, String
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class Content(Base):
    __tablename__ = 'sina'  # 表名字sina
    __table_args__ = {"mysql_charset": "utf8mb4"}
    id = Column(Integer(), primary_key=True)
    type = Column(String(20))
    times = Column(DateTime())
    title = Column(String(200))
    content = Column(Text())

    def __init__(self):
        mysql = Mysql()
        engine = mysql.engine
        Base.metadata.create_all(engine)