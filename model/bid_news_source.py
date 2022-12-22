from sqlalchemy.ext.declarative import declarative_base  # 调用sqlalchemy的基类
from sqlalchemy import Column, Index, distinct, update  # 指定字段属性，索引、唯一、DML
from sqlalchemy.types import *  # 所有字段类型
from . import DBSession
from . import Base


class NewsSource(Base):
    __tablename__ = "bid_news_source"  # 数据表的名字
    id = Column(Integer, primary_key=True)
    name = Column(String(128), unique=True)
    spider = Column(String(128))
    owner = Column(String(128))
    status = Column(Integer)
    config = Column(String(512))


class NewsSourceDao(object):

    @classmethod
    def query_all(cls):
        session = DBSession()
        o = session.query(NewsSource).all()
        session.close()
        return o
    @classmethod
    def get_by_id(cls, id):
        session = DBSession()
        ret = session.query(NewsSource).filter_by(id=id).first()
        session.close()
        return ret
