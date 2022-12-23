import time
from model.bid_news import News,NewsDao
from news.spider_base import SpiderBase

class EditorService(SpiderBase):
    def __init__(self,news:News):
        super().__init__({'spider':'other'})
        self.nd = NewsDao()
        self.news = news
    def run(self):
        if self.exist(self.news):
            return {'msg':'已存在！'},400
        try:
            self.add(self.news)
            return {'msg':'插入成功'},200
        except Exception as e:
            return {'msg':str(e)},400