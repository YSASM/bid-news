import html
from datetime import datetime
from service.message import MessageService
from config.config import Config
import logging
from bs4 import BeautifulSoup
import time
import re
from base.http_wrapper import HttpWrapper

SpiderAjaxHeader = {
    "Content-Type": "application/json",
    "Connection": "close",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36",
}

SpiderHtmlHeader = {
    "Content-Type": "text/html",
    "Connection": "close",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36",
}

GET = 'get'
POST = 'post'
OPTIONS = 'options'
HEAD = 'head'
PUT = 'put'
PATCH = 'patch'
DELETE = 'delete'
TargetType = {
    '.doc': 'word',
    '.docx': 'word',
    '.pdf': 'pdf',
    '.ppt': 'ppt',
    '.xls': 'excel',
    '.xlsx': 'excel',
    '.txt': 'text',
    '.jpg': 'image',
    '.png': 'image',
    '.jpeg': 'image',
}


class SpiderBase(object):
    def __init__(self):
        self.count = 0


    def add(self, info):
        info.src_id = self.source.id
        # &lt;font color='#CC00FF'&gt;[公 开招标]&lt;/font&gt;八五九分公司2022 年粮食管护设施项目三标段中标候选人公 示
        # 需要两遍BeautifulSoup去掉
        info.origin_title = BeautifulSoup(info.origin_title, 'html.parser').text
        info.origin_title = self.replace_warpper(BeautifulSoup(info.origin_title, 'html.parser').text)
        info.origin_content = self.replace_warpper(info.origin_content,list_replace=['\n','\r','\t','\xa0',' '])
        if info.type_id == 0:
            if info.origin_type != "":
                info.type_id = self.match_type(type_=info.origin_type, title=info.origin_title)
            else:
                info.type_id, info.origin_type = self.match_type(title=info.origin_title, back_name=True)
        info = self.match_region(info)
        if info.issue_time == 0:
            info.issue_time = self.format_timestamp(info.origin_issue_time)

        if info.issue_time > int(time.time()):
            info.issue_time = int(time.time())
        info = self.extract_attachment_from_content(info)
        info = self.add_title_md5(info)
        if self.is_exist_same(info):
            return True
        if info.project_amount >= 10000000000:
            info.wash_level = f"{info.src_id}_amount"
        if not info.origin_region and not info.city_id:
            info.wash_level = f"{info.src_id}_region"
        back_match_zbr = self.fun_match_zbr(info)
        if not back_match_zbr:
            info.company_name = ''
        else:
            info = back_match_zbr
        try:
            # 入库前对所有 info 的 content 进行转义处理
            info.origin_content = html.unescape(info.origin_content)
            # 入库前检查 入库的字段的空白字符是否去掉 的格式
            info = self.clear_blank_string(info)
            self._info_dao.add(info)
            self.count += 1
        except Exception as e:
            logging.error('[%s] add info fail %s', self.source.spider, str(e))

    def send_alarm(self, title, msg):
        message = []
        message.append("【%s】【%s】" % (str(title), Config.env()))
        message.append("网站名称：%s" % self.source.name)
        message.append("网站地址：%s" % self.source.url)
        message.append("蜘蛛类别：%s" % self.source.spider)
        message.append("发送时间：%s" % str(time.strftime("%Y-%m-%d %H:%M:%S")))
        message.append(str(msg))
        MessageService.send_text("\n".join(message), self.source.owner)

    # 把时间统一变成%Y-%m-%d %H-%M-%S的格式
    def _tobe_time(self, flage, s: str):
        back_str = ''
        for i in s:
            if i.isdigit():
                back_str += i
                continue
            if flage == 0:
                back_str += '-'
                continue
            back_str += ':'
        return back_str

    def _revamp_time(self, now, s: str):
        l = len(s.split(':'))
        if l == 2:
            return s + (':%d' % now.second)
        return s

    # wash:是否清洗时间默认为False只会返回时间戳，为True会返回两个值(时间，时间戳)
    # 比如传进:
    #   timestr = '发布时间：2022-01-01 12:00 【打印】【退出】'
    # 就能返回格式化后的时间和时间戳
    # only_tim:如果wash为True并且only_time为True时只返回时间不返回时间戳
    # 未匹配到时间或发生错误会返回None
    # 调用方法:
    #   不清洗{
    #       back_time = self.format_timestamp('包含时间的字符串')
    #       if not back_time:
    #           continue
    #       info.issue_time = back_time
    #   }
    #   清洗{
    # only_time=False
    #       back_time = self.format_timestamp('包含时间的字符串', wash=True)
    #       if not back_time:
    #           continue
    #       info.origin_issue_time,info.issue_time = back_time
    # only_time=True
    #       back_time = self.format_timestamp('包含时间的字符串', wash=True, only_time=True)
    #       if not back_time:
    #           continue
    #       info.origin_issue_time = back_time   
    #   }
    def format_timestamp(self, timestr, wash=False, only_time=False):
        try:
            now = datetime.now()
            pattern = re.compile(
                r'[0-9]{1}[0-9]?[0-9]?[0-9]?[-:/\.]{1}[0-9]{1}[0-9]?[-:/\.]?[0-9]{1}[0-9]?')
            match = pattern.findall(timestr)
            if len(match) == 0:
                pattern = re.compile(
                    r'[0-9]{1}[0-9]?[0-9]?[0-9]?[-:/\.]?[0-9]{1}[0-9]?[-:/\.]?[0-9]?[0-9]?')
                match = pattern.findall(timestr)
                if len(match) == 0:
                    match.append("%d-%d-%d" % (now.year, now.month, now.day))
                    match.append("%d:%d:%d" % (now.hour, now.minute, now.second))
            # 如果只有年月日
            if len(match) == 1:
                match.append('%d-%d-%d' % (now.hour, now.minute, now.second))
            # 格式化时间
            # 拿到年月日
            match[0] = self._tobe_time(0, match[0])
            # 拿到时分秒
            match[1] = self._revamp_time(now, self._tobe_time(1, match[1]))
            # 拼接
            if match[0].isdigit() and len(match[0]) == 8:
                if len(match[1]) == 4:
                    match[1] += str(now.second)
            match = '%s %s' % (match[0], match[1])
            strptime_str_list = ["%Y-%m-%d %H:%M:%S", "%Y%m%d %H%M%S", "%Y%m%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y%m%d %H:%M",
                                "%Y%m%d %H%M"]
            match_flage = False
            for strptime_str in strptime_str_list:
                try:
                    match = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(match, strptime_str))
                    match_flage = True
                    break
                except:
                    continue
            if not match_flage:
                match = time.strftime("%Y-%m-%d %H:%M:%S")
            # 统一时间格式
            match = time.strptime(str(match), "%Y-%m-%d %H:%M:%S")
            try:
                issue_time = int(time.mktime(match))
            except Exception as e:
                issue_time = int(time.time())
            match = str(time.strftime("%Y-%m-%d %H:%M:%S", match))
            if not wash:
                # wash为False只返回时间戳
                return issue_time
            # wash为True返回(时间，时间戳)
            if only_time:
                return match
            return (match, issue_time)
        except:
            if only_time:
                return time.strftime("%Y-%m-%d %H:%M:%S")
            return (time.strftime("%Y-%m-%d %H:%M:%S"), int(time.time()))

    def do(self):
        # self._fail_count=20
        self.run()
        return self.count

    # retries:错误重连次数
    # pass_status_code:正确status_code会返回'ok',response
    # remove_status_code:忽略的status_code会返回'pass',None
    # verify:是否使用证书,默认为False
    def http_wrapper(self, method, url, headers=SpiderHtmlHeader, cookies=None, timeout=30, **kwargs):
        cookies = self.config.get('cookies') or cookies
        http_retry_times = self.config.get('http_retry_times') or 1
        proxies = self.config.get('proxy', {})
        if method == GET:
            content = HttpWrapper.get(url=url, headers=headers, cookies=cookies,
                                      timeout=timeout, retries=http_retry_times, proxies=proxies, **kwargs)
        elif method == POST:
            content = HttpWrapper.post(url=url, headers=headers, cookies=cookies,
                                       timeout=timeout, retries=http_retry_times, proxies=proxies, **kwargs)
        back_code, back_content = content
        if back_code == 'pass':
            return None
        elif back_code == 'error':
            logging.warning(f"【{self.source.name}】【{self.source.spider}】【网络超时】 ：url : {url},error:{back_content}")
            return None
        elif back_code == 'bad':
            # self.add_fail('网络错误', back_content)
            logging.warning(f"【{self.source.name}】【{self.source.spider}】【网络错误】 ：url : {url},error:{back_content}")
            return None
        elif back_code == 'ok':
            return back_content

    def replace_warpper(self, string: str, list_replace=['\n', '\r', '\t', ' ']):
        for i in list_replace:
            string = string.replace(i, '')
        return string
