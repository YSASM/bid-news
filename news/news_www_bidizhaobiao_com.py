import time
from bs4 import BeautifulSoup
from model.bid_news import News
from news.spider_base import POST, SpiderBase, GET

class Main(SpiderBase): 
    def __init__(self, source):
        super().__init__(source)
        # 请求页面
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'http://www.bidizhaobiao.com',
        'Connection': 'close',
    }
    type_id_list = {
            '行业新闻':5,
            '招标热点':5,
            '招标知识':5,
            '政策法规':6,
            '招采排行榜':6,
            '公司动态':6
        }
    content_list = ['column_list_content','content']
    def write_db(self, content,type_name):
        l = len(content)
        for item in content:
            try:
                news = News()
                a = item.find('a',class_='top')
                news.origin_url = a.get('href')
                if self.exist(news):
                    continue
                # 获取页面html
                html = self.http_wrapper(GET, news.origin_url)
                if not html:
                    continue
                # 获取原始类容content
                html = BeautifulSoup(html.text, 'html.parser')
                for i in self.content_list:
                    news.origin_content = html.find('div',class_=i)
                    if news.origin_content:
                        break
                if not news.origin_content:
                    continue
                news.origin_content = str(news.origin_content)
                # 获取时间
                news.origin_issue_time = self.format_timestamp(item.find('div',class_='date').text, wash=True, only_time=True)
                # 获取标题
                news.origin_title = a.get('title')
                # 填入原始类型
                news.type_name = type_name
                news.origin_subject = '比地招标网'
                news.type_id = self.type_id_list[type_name]
                self.add(news)
                l-=1
                time.sleep(10)
            except Exception as e:
                self.send_alarm('error',str(item)+str(e))
        if l<=0:
            return False
        return True
    def page_down(self,type_id,type_name):
        flage = False
        page = 0
        while True:
            page+1
            if flage:
                break
            # *limit
            url = 'http://www.bidizhaobiao.com/'+type_id
            if page!=1:
                url += '%d.html'%page
            content = self.http_wrapper(POST, url, headers=self.headers) 
            if not content:
                break
            content = BeautifulSoup(content.text, 'html.parser')
            try:
                content = content.find('div',class_='column_list_content').find_all('div',class_='item')
            except:
                continue
            flage = self.write_db(content,type_name)

    def run(self):
        type_list = {
            '行业新闻':'hynews/',
            '招标热点':'zbhot/',
            '招标知识':'zhishi/',
            '政策法规':'laws/',
            '招采排行榜':'zcphb/',
            '公司动态':'gsdt/'
        }
        for type_name in type_list:
            type_id = type_list[type_name]
            self.page_down(type_id,type_name)
