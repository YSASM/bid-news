# encoding=UTF-8
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import NullPool

from config.config import Config

cfg = Config.get()
Base = declarative_base()
# 初始化数据库连接:
engine = create_engine(
    cfg.get("db"),
    echo=False,
    pool_size=100,  # 连接个数
    pool_recycle=60 * 30,  # 不使用时断开
)

# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建不使用连接池的session
nullpoolengine = create_engine(
    cfg.get("db"),
    echo=False,
    poolclass=NullPool
)
DBNullPoolSession = sessionmaker(bind=nullpoolengine)
