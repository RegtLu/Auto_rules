def hash_file(file_path):
    import hashlib
    with open(file_path, "rb") as f:
        hash_object = hashlib.sha256()
        for chunk in iter(lambda: f.read(4096), b""):
            hash_object.update(chunk)
        del hashlib
        return hash_object.hexdigest()


def init():
    #download_GFWlist()
    with open('./gfw.lst') as f:
        rules = f.readlines()
    global adblock_rules
    adblock_rules = rules
    with open('./cn.lst') as f:
        rules = f.readlines()
    global white_rules
    white_rules = rules


def download_GFWlist():
    import update
    update.main()


def in_GFW(url):  # True or False
    import re
    for rule in adblock_rules:
        res=re.findall(rule.replace('\n',''), url)
        if  res == []:
            continue
        elif len(res) >1:
            continue
        else:
            return True
    return False

def in_whitelist(url):  # True or False
    import re
    for rule in white_rules:
        res=re.findall(rule.replace('\n',''), url)
        if  len(res) == 1:
            return True
        else:
            continue
    return False

def ping_speed(url):  # 'Direct' or 'Proxy' or 'Blocked'
    return 'Blocked'


def test_robot(url):  # 'Direct' or 'Proxy' or 'Not Found'
    proxy = {
        'http': 'http://127.0.0.1:7890',
        'https': 'http://127.0.0.1:7890'
    }
    url = r'https://'+url+'/robots.txt'
    import requests
    import time
    try:
        start_time = time.time()
        response = requests.get(url, timeout=3)
        end_time = time.time()
        direct_time = end_time - start_time
    except:
        direct_time = 100
    try:
        start_time = time.time()
        response = requests.get(url, proxies=proxy, timeout=3)
        end_time = time.time()
        proxy_time = end_time - start_time
    except:
        proxy_time = 99
    del requests
    del time
    if direct_time < proxy_time:
        return 'Direct'
    else:
        return 'Proxy'


def detect(url):
    if in_whitelist(url) == True:
        return 'Whitelist:  Direct'
    if in_GFW(url) == True:
        return 'GFW:    Proxy'
    ping_ans = ping_speed(url)
    if ping_ans == 'Proxy':
        return 'Ping:   Proxy'
    elif ping_ans == 'Direct':
        return 'Ping:   Direct'
    robot_ans = test_robot(url)
    if robot_ans == 'Proxy':
        return 'Robots:  Proxy'
    elif robot_ans == 'Direct':
        return 'Robots:  Direct'
    return 'None:   Proxy'


init()
print(detect('www.google.com'))
print(detect('www.baidu.com'))
