import json
import logging
import time
from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base  # 调用sqlalchemy的基类
from sqlalchemy import Column, Index, distinct, update  # 指定字段属性，索引、唯一、DML
from sqlalchemy.types import *  # 所有字段类型
from . import DBSession, DBNullPoolSession
from . import Base


class Info(Base):
    __tablename__ = "bid_info"  # 数据表的名字
    id = Column(Integer, primary_key=True)
    src_id = Column(Integer)
    type_id = Column(Integer)
    city_id = Column(Integer)
    content = Column(Text)
    contact_name = Column(String(32))
    contact_phone = Column(String(32))
    issue_time = Column(Integer)
    expire_time = Column(Integer)
    create_time = Column(Integer)
    project_amount = Column(Integer)

    origin_type = Column(String(64))
    origin_title = Column(String(512))
    origin_url = Column(String(512))
    origin_content = Column(Text)
    origin_attachment = Column(String(512))
    origin_subject = Column(String(128))
    origin_region = Column(String(128))
    origin_issue_time = Column(String(64))
    origin_project_code = Column(String(64))
    origin_extra = Column(Text)
    origin_title_md5 = Column(String(32))
    abstract_md5 = Column(String(32))
    wash_level = Column(BIGINT())
    company_id = Column(Integer)
    company_name = Column(String(255))

    #  后加入 12.5
    company_name = Column(String(32))
    company_id = Column(Integer)

    def __init__(self):
        self.src_id = 0
        self.city_id = 0
        self.type_id = 0
        self.content = ""
        self.contact_name = ""
        self.contact_phone = ""
        self.issue_time = 0
        self.expire_time = 0
        self.create_time = int(time.time())

        self.origin_type = ""
        self.origin_title = ""
        self.origin_url = ""
        self.origin_content = ""
        self.origin_attachment = "[]"
        self.origin_subject = ""
        self.origin_region = ""
        self.origin_issue_time = ""
        self.origin_project_code = ""
        self.origin_extra = "{}"
        self.project_amount = 0
        self.origin_title_md5 = ''
        self.abstract_md5 = ''
        self.wash_level = -1
        self.company_id = 0
        self.company_name = ''

        #  后加入 12.5 d
        self.company_name=''
        self.company_id = 0

class InfoDao(object):
    def exist(self, url):
        sesion = DBSession()
        res = sesion.query(Info).filter_by(origin_url=url).all()
        sesion.close()
        return len(res) >= 1

    def add(self, info):
        sesion = DBSession()
        sesion.add(info)
        sesion.commit()
        sesion.close()

    def query_abstractmd5_by_srcid_titlemd5_typeid(self, info):
        """
        通过src_id，title_md5 type_id abstract_md5 查询数据
        """
        sesion = DBSession()
        data = sesion.query(Info.id).filter_by(src_id=info.src_id,
                                               abstract_md5=info.abstract_md5,
                                               origin_title_md5=info.origin_title_md5,
                                               type_id=info.type_id).first()
        sesion.close()
        return data

    def query_titlemd5_by_srcid(self, src_id):
        """
        通过src—id 获取title_md5 和creat——time
        """
        sesion = DBSession()
        abstract_list = sesion.query(Info.id, Info.origin_title_md5, Info.create_time).filter_by(src_id=src_id).all()
        sesion.close()
        return abstract_list

    def query_count_by_title_md5(self, info_id, title_md5):
        """
        通过abstract-md5 查询info中的数量
        """
        sesion = DBSession()
        result = sesion.query(func.count(Info.id)).filter(Info.origin_title_md5 == title_md5, Info.id != info_id).all()
        sesion.close()
        return result[0][0]
