import json,logging
def get_status(spider):
    f = open('base/status.json','r',encoding='utf-8').read()
    try:
        spiders = json.loads(f)
        for temp in spiders:
            if temp['spider'] == spider:
                return temp['status']
    except:
        logging.error('status.json error!')
    return None
def get_config(spider):
    f = open('base/status.json','r',encoding='utf-8').read()
    try:
        spiders = json.loads(f)
        for temp in spiders:
            if temp['spider'] == spider:
                return json.loads(temp['config'])
    except:
        logging.error('status.json error!')
    return None
def get_all():
    f = open('base/status.json','r',encoding='utf-8').read()
    try:
        spiders = json.loads(f)
        l = []
        for temp in spiders:
            l.append(temp['spider'])
    except:
        logging.error('status.json error!')
    return l
def get_all_id():
    f = open('base/status.json','r',encoding='utf-8').read()
    try:
        spiders = json.loads(f)
        l = []
        for temp in spiders:
            l.append(temp['id'])
    except:
        logging.error('status.json error!')
    return l
def get_name(spider):
    f = open('base/status.json','r',encoding='utf-8').read()
    try:
        spiders = json.loads(f)
        for temp in spiders:
            if temp['spider'] == spider:
                return temp['name']
    except:
        logging.error('status.json error!')
    return None
def get_owner(spider):
    f = open('base/status.json','r',encoding='utf-8').read()
    try:
        spiders = json.loads(f)
        for temp in spiders:
            if temp['spider'] == spider:
                return temp['owner']
    except:
        logging.error('status.json error!')
    return None
def write(source):
    f = open('base/status.json','r',encoding='utf-8').read()
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
            open('base/status.json','w').write(json.dumps(spiders))
            return True
        except:
            logging.error('update status.json error!')
    return None
