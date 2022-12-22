import json
def get_status(spider):
    f = open('base/status.json','r',encoding='utf-8').read()
    spiders = json.loads(f)
    for temp in spiders:
        if temp['spider'] == spider:
            return temp['status']
    return None
def get_config(spider):
    f = open('base/status.json','r',encoding='utf-8').read()
    spiders = json.loads(f)
    for temp in spiders:
        if temp['spider'] == spider:
            return json.loads(temp['config'])
    return None
def get_all():
    f = open('base/status.json','r',encoding='utf-8').read()
    spiders = json.loads(f)
    l = []
    for temp in spiders:
        l.append(temp['spider'])
    return l
def get_name(spider):
    f = open('base/status.json','r',encoding='utf-8').read()
    spiders = json.loads(f)
    for temp in spiders:
        if temp['spider'] == spider:
            return temp['name']
    return None
def get_owner(spider):
    f = open('base/status.json','r',encoding='utf-8').read()
    spiders = json.loads(f)
    for temp in spiders:
        if temp['spider'] == spider:
            return temp['owner']
    return None

