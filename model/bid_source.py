import json
import logging

from sqlalchemy.ext.declarative import declarative_base  # 调用sqlalchemy的基类
from sqlalchemy import Column, Index, distinct, update  # 指定字段属性，索引、唯一、DML
from sqlalchemy.types import *  # 所有字段类型
from . import DBSession
from . import Base


class Source(Base):
    __tablename__ = "bid_source"  # 数据表的名字
    id = Column(Integer, primary_key=True)
    name = Column(String(128), unique=True)
    url = Column(String(128), unique=True)
    city_id = Column(Integer)
    spider = Column(String(128))
    cluster = Column(String(64))
    owner = Column(String(128))
    status = Column(Integer)
    config = Column(String(512))
    last_spider_time = Column(Integer)
    last_spider_nozero_time = Column(Integer)
    last_spider_nozero_count = Column(Integer)
    send_succ_info = Column(Boolean)
    sleep_page = Column(Integer)
    min_spider_span = Column(Integer)
    max_nodata_threshold = Column(Integer)
    error = Column(Text)
    statistics = Column(String(256))
    origin_url_type = Column(String(32))


class SourceDao(object):
    @classmethod
    def query_all_online(cls, cluster=''):
        session = DBSession()
        o = session.query(Source).filter_by(status=1). \
            filter_by(cluster=cluster).filter(Source.spider.__ne__("")).all()

        session.close()
        return o

    @classmethod
    def query_all(cls, cluster=''):
        session = DBSession()
        o = session.query(Source).filter_by(cluster=cluster).filter(Source.spider.__ne__("")).all()
        session.close()
        return o

    @classmethod
    def update(cls, source):
        session = DBSession()
        xm_source = session.query(Source).filter(Source.id == source.id).first()

        xm_source.last_spider_nozero_time = source.last_spider_nozero_time
        xm_source.last_spider_nozero_count = source.last_spider_nozero_count
        xm_source.last_spider_time = source.last_spider_time
        xm_source.error = source.error
        xm_source.cluster = source.cluster
        xm_source.status = source.status

        session.commit()
        session.close()

    @classmethod
    def get_by_id(cls, id):
        session = DBSession()
        ret = session.query(Source).filter_by(id=id).first()
        session.close()
        return ret

    def update_statistics_by_id(self, id, data):
        """
        通过id，更新con
        """
        session = DBSession()
        ret = session.query(Source).filter_by(id=id).first()
        if isinstance(data,dict):
            data = json.dumps(data)
        ret.statistics = data
        session.commit()
        session.close()
