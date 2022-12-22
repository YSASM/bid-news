import logging
from threading import Thread
import time
import traceback
import news
from base import get_status,get_config,get_name,async_call,get_owner
from config.config import Config
from .message import MessageService
import inspect
import ctypes
def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")
def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)

class Worker(object):
    def __init__(self):
        self.name = ''
        self.spider = ''
        self.owner = ''
        self.th = None

    @async_call
    def watch_stop(self,spider,config):
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
                self.start_spider(spider,config)
                logging.info('%s start...' % spider)
            time.sleep(1)
    def start_spider(self,spider,config):
        spider = getattr(getattr(news,spider),'Main')(config)
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

    def run(self,spider):
        try:
            self.spider = spider
            self.name = get_name(spider)
            self.owner = get_owner(spider)
            logging.info("[%s] start worker ...", self.spider)
            config = get_config(spider)
            self.watch_stop(spider,config)
        except:
            exp = traceback.format_exc()
            self.send_fail(exp)