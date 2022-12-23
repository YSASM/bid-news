# coding=utf-8
import logging
from flask import Flask,render_template,request,url_for
from base import async_call
from logging import handlers
from service.service import Service
from service.editor_service import EditorService
from model.bid_news import News
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
editor = Flask(__name__)
@editor.route('/',methods=['get','post'])
def Editor():
    if request.method=='POST':
        news = News()
        news.origin_title = request.form['origin_title']
        news.origin_url = request.form['origin_url']
        news.origin_subject = request.form['origin_subject']
        news.origin_issue_time = request.form['origin_issue_time']
        news.type_name = request.form['type_name']
        news.origin_content = request.form['origin_content']
        es = EditorService(news)
        return  es.run()
    else:
        return render_template('editor.html')
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
    editor.run(host='0.0.0.0',port='9260')

    
