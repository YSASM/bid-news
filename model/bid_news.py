from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base  # 调用sqlalchemy的基类
from sqlalchemy import Column, Index, distinct, update  # 指定字段属性，索引、唯一、DML
from sqlalchemy.types import *  # 所有字段类型
from . import DBSession, DBNullPoolSession
from . import Base


class News(Base):
    __tablename__ = "bid_news"  # 数据表的名字
    id = Column(Integer, primary_key=True)
    type_id = Column(Integer)
    src_id = Column(Integer)
    issue_time = Column(Integer)
    create_time = Column(Integer)
    origin_title = Column(String(512))
    origin_url = Column(String(512))
    origin_content = Column(Text)
    origin_subject = Column(String(128))
    origin_issue_time = Column(String(64))
    origin_title_md5 = Column(String(32))
    type_name = Column(String(32))

    def __init__(self):
        self.id = 0
        self.type_id = 0
        self.src_id = 0
        self.issue_time = 0
        self.create_time = 0
        self.origin_title = ""
        self.origin_url = ""
        self.origin_content = ""
        self.origin_subject = ""
        self.origin_issue_time = ""
        self.origin_title_md5 = ""
        self.type_name = ""

class NewsDao(object):
    def exist(self, url):
        sesion = DBSession()
        res = sesion.query(News).filter_by(origin_url=url).all()
        sesion.close()
        return len(res) >= 1

    def add(self, news):
        sesion = DBSession()
        sesion.add(news)
        sesion.commit()
        sesion.close()
