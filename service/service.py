import time
import traceback
from base import get_all,async_call,get_owner
from config.config import Config
from .message import MessageService
from .worker import Worker

@async_call
def start_work(spider,owner):
    worker = Worker(spider,owner)
    worker.run()
class Service(object):
    def __init__(self):
        self.owner = ""
    def send_fail(self, exp):
        message = []
        message.append("【资讯框架异常】【%s】" % Config.env())
        message.append("时间：%s" % time.strftime("%Y-%m-%d %H:%M:%S"))
        message.append(exp)
        MessageService.send_text("\n".join(message), self.owner)
    def run(self):
        self.owner = get_owner(spider)
        try:
            spiders = get_all()
            for spider in spiders:
                start_work(spider,self.owner)
        except:
            exp = traceback.format_exc()
            self.send_fail(exp)
    