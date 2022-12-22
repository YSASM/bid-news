import time
from model.bid_news_source import NewsSourceDao
from base import get_all_id,write
class Watcher(object):
    def __init__(self):
        self.nsd = NewsSourceDao()
    def run(self):
        while True:
            ids = get_all_id()
            for id in ids:
                source = self.nsd.get_by_id(id)
                if not source:
                    continue
                write(source)
            time.sleep(10)
