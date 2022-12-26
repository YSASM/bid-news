import time
import requests
from lxml.html import fromstring, tostring
import html as h
import logging
from model.bid_news import News
from news.spider_base import SpiderBase,GET,POST
class Main(SpiderBase):
    def __init__(self, arg):
        super().__init__(arg)
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    }


    def get_detail(self,url):
        response = self.http_wrapper(GET,url=url, headers=self.headers)
        html = fromstring(response.text)
        issue_time = html.xpath('//span[@id="news-time"]/text()')[0]
        content = tostring(html.xpath("//article[@id='mp-editor']")[0]).decode()
        content = h.unescape(content)
        return str(issue_time),str(content)


    def save(self,news):
        self.add(news)


    def run(self):
        spider_list = [
            {
                "data": '{"suv":"221027100411RGAP","pvId":"1672036979168_SL9GsDO","clientType":3,"resourceParam":[{"requestId":"1672036977821_22102710041_DGf","resourceId":"1672036977821428356","page":1,"size":1000,"spm":"smpc.channel_248.block3_308_NDdFbm_1_fd","context":{"pro":"0,1,3,4,5","feedType":"XTOPIC_SYNTHETICAL","mkey":"100235159"},"resProductParam":{"productId":324,"productType":13},"productParam":{"productId":325,"productType":13,"categoryId":47,"mediaId":1},"expParam":{}}]}',
                "name": "建设库",
                "key": "1672036977821428356"
            },
            {
                "data": '{"suv":"221027100411RGAP","pvId":"1672037062290_PhKicTZ","clientType":3,"resourceParam":[{"requestId":"1672037061050_22102710041_kat","resourceId":"1672037061050845219","page":1,"size":1000,"spm":"smpc.channel_248.block3_308_NDdFbm_1_fd","context":{"pro":"0,1,3,4,5","feedType":"XTOPIC_SYNTHETICAL","mkey":"763498"},"resProductParam":{"productId":324,"productType":13},"productParam":{"productId":325,"productType":13,"categoryId":47,"mediaId":1},"expParam":{}}]}',
                "name": "e车网",
                "key": "1672037061050845219"
            },
            {
                "data": '{"suv":"221027100411RGAP","pvId":"1672035686643_g8goHT2","clientType":3,"resourceParam":[{"requestId":"1672035693967_22102710041_zeh","resourceId":"1672035693967825815","page":1,"size":400,"spm":"smpc.channel_248.block3_308_NDdFbm_1_fd","context":{"pro":"0,1,3,4,5","feedType":"XTOPIC_SYNTHETICAL","mkey":"120633305"},"resProductParam":{"productId":324,"productType":13},"productParam":{"productId":325,"productType":13,"categoryId":47,"mediaId":1},"expParam":{}}]}',
                "name": "中政国誉",
                "key": "1672035693967825815"
            },
            {
                "data": '{"suv":"221027100411RGAP","pvId":"1672036903444_8fthHUO","clientType":3,"resourceParam":[{"requestId":"1672036907752_22102710041_d6Y","resourceId":"1672036907752308786","page":1,"size":1000,"spm":"smpc.channel_248.block3_308_NDdFbm_1_fd","context":{"pro":"0,1,3,4,5","feedType":"XTOPIC_SYNTHETICAL","mkey":"120633305"},"resProductParam":{"productId":324,"productType":13},"productParam":{"productId":325,"productType":13,"categoryId":47,"mediaId":1},"expParam":{}}]}',
                "name": "智多星软件",
                "key": "1672036907752308786"
            },

        ]
        for info in spider_list:
            response = requests.post(
                'https://cis.sohu.com/cisv4/feeds', headers=self.headers, data=info.get("data"))
            data = response.json()
            infos = data.get(info.get("key")).get("data")
            for info in infos:
                news = News()
                title = info.get("resourceData").get("contentData").get("title")
                # 标题
                news.origin_title = str(title)
                url = info.get("resourceData").get("contentData").get("url")
                # url
                url = "https://www.sohu.com" + url
                news.origin_url = str(url)
                if self.exist(news):
                    continue
                # 主体
                news.origin_subject = "搜狐"
                news.type_id = 5
                try:
                    news.origin_issue_time,news.origin_content = self.get_detail(url=url)
                except:
                    continue
                self.save(news)
                time.sleep(10)
