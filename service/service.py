import time
from base import get_all,async_call
from config.config import Config
from .message import MessageService
from .worker import Worker

@async_call
def start_work(spider):
    worker = Worker()
    worker.run(spider)
class Service(object):
    def __init__(self):
        pass
    def send_alarm(self, title, exp, receiver=None):
        message = []
        message.append("【%s】【%s】" % (title, Config.env()))
        message.append("时间：%s" % time.strftime("%Y-%m-%d %H:%M:%S"))
        message.append(exp)
        MessageService.send_text("\n".join(message), receiver)
    def run(self):
        spiders = get_all()
        for spider in spiders:
            start_work(spider)
    