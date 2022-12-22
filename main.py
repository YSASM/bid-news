# coding=utf-8
import logging
from base import async_call
from logging import handlers
from service.service import Service
from service.watcher import Watcher
from config.config import Config
import news
@async_call
def start_service():
    service = Service()
    service.run()
@async_call
def start_watcher():
    watcher = Watcher()
    watcher.run()
if __name__ == "__main__":

    print(Config.get())
    logger = logging.getLogger()
    for h in logger.handlers:
        logger.removeHandler(h)
    fmt = "[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s"
    file_handler = handlers.TimedRotatingFileHandler(
        filename="log/news.log", when="D", interval=1, backupCount=14
    )
    file_handler.setFormatter(logging.Formatter(fmt))
    file_handler.setLevel(logging.DEBUG)

    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    if Config.env() == "test" or Config.env() == "dev":
        console_handler.setLevel(logging.DEBUG)
    else:
        console_handler.setLevel(logging.ERROR)

    console_handler.setFormatter(logging.Formatter(fmt))
    logger.addHandler(console_handler)

    logging.info("start bid-news ....")
    start_service()
    start_watcher()

    
