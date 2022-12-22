import json
import logging
from config.config import Config
path = Config.load_status(Config.env())

def get(fn):
    def _get(spider):
        f = open(path, 'r', encoding='utf-8').read()
        try:
            spiders = json.loads(f)
            for temp in spiders:
                if temp['spider'] == spider:
                    return fn(temp)
        except:
            logging.error('status.json error!')
    return _get


@get
def get_status(spider):
    '''
    获取开关状态
    '''
    return spider['status']


@get
def get_config(spider):
    '''
    获取配置信息
    '''
    return json.loads(spider['config'])


@get
def get_id(spider):
    '''
    获取id
    '''
    return spider['id']


def get_all():
    '''
    获取所有spider
    '''
    f = open(path, 'r', encoding='utf-8').read()
    try:
        spiders = json.loads(f)
        l = []
        for temp in spiders:
            l.append(temp['spider'])
    except:
        logging.error('status.json error!')
    return l


def get_all_id():
    '''
    获取所有id
    '''
    f = open(path, 'r', encoding='utf-8').read()
    try:
        spiders = json.loads(f)
        l = []
        for temp in spiders:
            l.append(temp['id'])
    except:
        logging.error('status.json error!')
    return l


@get
def get_name(spider):
    '''
    获取名字
    '''
    return spider['name']


@get
def get_owner(spider):
    '''
    获取负责人
    '''
    return spider['owner']


def write(source):
    '''
    从数据库更新信息
    '''
    f = open(path, 'r', encoding='utf-8').read()
    try:
        spiders = json.loads(f)
        flage = False
        for temp in spiders:
            if temp['id'] == source.id:
                w = spiders.index(temp)
                if spiders[w]['name'] != source.name:
                    spiders[w]['name'] = source.name
                    flage = True
                if spiders[w]['status'] != source.status:
                    spiders[w]['status'] = source.status
                    flage = True
                if spiders[w]['spider'] != source.spider:
                    spiders[w]['spider'] = source.spider
                    flage = True
                if spiders[w]['config'] != source.config:
                    spiders[w]['config'] = source.config
                    flage = True
                if spiders[w]['owner'] != source.owner:
                    spiders[w]['owner'] = source.owner
                    flage = True
                break
    except:
        logging.error('status.json error!')
    if flage:
        try:
            open(path, 'w').write(json.dumps(spiders))
            return True
        except:
            logging.error('update status.json error!')
    return None
