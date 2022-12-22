import time
from news.spider_base import SpiderBase
class Main(SpiderBase):
    def __init__(self,arg):
        super().__init__(arg)
    def run(self):
        while True:
            print("t")
            time.sleep(2)