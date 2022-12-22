import requests
import urllib3
import logging
from urllib3.exceptions import InsecureRequestWarning
# retries:错误重连次数
# pass_status_code:正确status_code会返回'ok',response
# remove_status_code:忽略的status_code会返回'pass',None
# verify:是否使用证书,默认为False

def request(method, url, retries=1, pass_status_code=[200, 201], remove_status_code=[], remove_http_error = False, verify=False, **kwargs):
    if not verify:
        # 禁用安全请求警告
        urllib3.disable_warnings(InsecureRequestWarning)
    while retries!=0:
        retries -= 1
        try:
            response = requests.request(
                method=method, url=url, verify=verify, **kwargs)
            status_code = response.status_code
            if isinstance(remove_status_code, list) and status_code in remove_status_code:
                return 'pass', None
            if isinstance(pass_status_code, list) and response.status_code not in pass_status_code:
                return 'bad', url+'\n'+str(status_code)+'\n'+response.reason
            response.encoding = 'utf-8'
            return 'ok', response
        except requests.exceptions.ReadTimeout as e:
            return 'error', url+'\n'+str(e)
        except requests.exceptions.Timeout as e:
            return 'error', url+'\n'+str(e)
        except Exception as e:
            if retries != 0:
                continue
            if remove_http_error:
                return 'pass', None
            return 'bad', url+'\n'+str(e)


class HttpWrapper:
    def get(url, params=None, **kwargs):
        return request("get", url, params=params, **kwargs)

    def options(url, **kwargs):
        return request("options", url, **kwargs)

    def head(url, **kwargs):
        kwargs.setdefault("allow_redirects", False)
        return request("head", url, **kwargs)

    def post(url, data=None, json=None, **kwargs):
        return request("post", url, data=data, json=json, **kwargs)

    def put(url, data=None, **kwargs):
        return request("put", url, data=data, **kwargs)

    def patch(url, data=None, **kwargs):
        return request("patch", url, data=data, **kwargs)

    def delete(url, **kwargs):
        return request("delete", url, **kwargs)
