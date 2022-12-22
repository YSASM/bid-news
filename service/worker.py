import logging
from threading import Thread
import time
import traceback
import news
from base import get_status,get_config,get_name,async_call,get_owner,stop_thread
from config.config import Config
from .message import MessageService

class Worker(object):
    def __init__(self,spider,owner):
        self.spider = spider
        self.name = get_name(spider)
        self.owner = owner
        self.th = None

    @async_call
    def watch_stop(self,spider,arg):
        while True:
            status = get_status(spider)
            if status == 2:
                if not self.th:
                    time.sleep(1)
                    continue
                stop_thread(self.th)
                logging.info('%s stop...' % spider)
                self.th = None
            if status == 1:
                if self.th:
                    time.sleep(1)
                    continue
                logging.info('%s start...' % spider)
                self.start_spider(spider,arg)
            time.sleep(1)
    def start_spider(self,spider,arg):
        try:
            spider = getattr(getattr(news,spider),'Main')(arg)
        except:
            logging.error("%s can't find!" % spider)
            return None
        self.th = Thread(target=spider.do)
        self.th.start()
    def send_fail(self, exp):
        message = []
        message.append("【资讯爬虫异常】【%s】" % Config.env())
        message.append("时间：%s" % time.strftime("%Y-%m-%d %H:%M:%S"))
        message.append("名称：%s" % self.name)
        message.append("蜘蛛：%s" % self.spider)
        message.append(exp)
        MessageService.send_text("\n".join(message), self.owner)

    def run(self):
        try:
            logging.info("[%s] start worker ...", self.spider)
            config = get_config(self.spider)
            self.watch_stop(self.spider,{"name":self.name,"spider":self.spider,"config":config})
        except:
            exp = traceback.format_exc()
            self.send_fail(exp)