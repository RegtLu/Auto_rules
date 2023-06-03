from weakref import proxy


def hash_file(file_path):
    import hashlib
    with open(file_path, "rb") as f:
        hash_object = hashlib.sha256()
        for chunk in iter(lambda: f.read(4096), b""):
            hash_object.update(chunk)
        del hashlib
        return hash_object.hexdigest()

def init():
    download_GFWlist()
    from adblockparser import AdblockRules
    with open('./GFW/GFWlist.txt') as f:
            rules = f.read()
    global adblock_rules 
    adblock_rules= AdblockRules(rules)


def download_GFWlist():
    import base64
    import os
    import requests
    url = r'https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt'
    response = requests.get(url)
    with open("./GFW/GFWlist.temp", "wb") as f:
        f.write(response.content)
    new_hash = hash_file('./GFW/GFWlist.temp')
    with open('./GFW/GFWlist.md5') as f:
        old_hash = f.read()
    if new_hash == old_hash:
        os.remove('./GFW/GFWlist.temp')
        return
    else:
        os.remove('./GFW/GFWlist.txt')
        os.rename('./GFW/GFWlist.temp', './GFW/GFWlist.txt')
        with open('./GFW/GFWlist.md5', 'w') as f:
            f.write(new_hash)
        with open('./GFW/GFWlist.txt') as f:
            content = f.read()
        import re
        content = base64.b64decode(content).decode('utf-8')
        content = content.split(
            '\n!##############General List End#################')[0]
        content = content.split(
            '!------------------Numerics---------------------\n')[1]
        content = re.sub(r"!-{20}[A-Z]{2}-{25}", "", content)
        content = re.sub(r"!--", "", content)
        content = re.sub(r"!-", "", content)
        content = re.sub(r"\|", "", content)
        content = re.sub(r"\n\*\.", "", content)
        content = re.sub(r"[\n]{2,5}", "", content)
        content = re.sub(r"http[s]{0,1}://", "", content)
        with open('./GFW/GFWlist.txt', 'w') as f:
            f.write(content)


def in_GFW(url):  # True or False
    return False
    is_blocked = adblock_rules.should_block("url")
    return is_blocked


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
        direct_time=100
    try:
        start_time = time.time()
        response = requests.get(url, proxies=proxy, timeout=3)
        end_time = time.time()
        proxy_time = end_time - start_time
    except:
        proxy_time=99
    del requests
    del time
    print('direct_time:'+str(direct_time)+'s')
    print('proxy_time:'+str(proxy_time)+'s')
    if direct_time < proxy_time:
        return 'Direct'
    else:
        return 'Proxy'


def detect(url):
    if in_GFW(url) == True:
        return 'GFW:    Proxy'

    ping_ans=ping_speed(url)
    if ping_ans == 'Proxy':
        return 'Ping:   Proxy'
    elif ping_ans == 'Direct':
        return 'Ping:   Direct'

    robot_ans=test_robot(url)
    if robot_ans == 'Proxy':
        return 'Robots:  Proxy'
    elif robot_ans == 'Direct':
        return 'Robots:  Direct'
    return 'None:   Proxy'

#init()
while True:
    print(detect(input()))
