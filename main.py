
from encodings import utf_8


def hash_file(file_path):
    import hashlib
    with open(file_path, "rb") as f:
        hash_object = hashlib.sha256()
        for chunk in iter(lambda: f.read(4096), b""):
            hash_object.update(chunk)
        return hash_object.hexdigest()


def download_GFWlist():
    import wget
    import base64
    import os
    url = r'https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt'
    wget.download(url, './GFW/GFWlist.temp')
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
        content = re.sub(r"/.*", "", content)
        content = re.sub(r"\n\.", "\n", content)
        with open('./GFW/GFWlist.txt', 'w') as f:
            f.write(content)


def in_GFW(url):  # True or False
    return False


def ping_speed(url):  # 'Direct' or 'Proxy' or 'Blocked'
    return 'Blocked'


def test_robot(url):  # 'Direct' or 'Proxy' or 'Not Found'
    proxy = {
        'http': 'http://127.0.0.1:7890',
        'https': 'http://127.0.0.1:7890'
    }
    url = url+'/robots.txt'

    import requests
    import time

    start_time = time.time()
    response = requests.get(url, proxies=proxy)
    end_time = time.time()

    direct_speed = len(response.content) / \
        (end_time - start_time) / 1024 / 1024

    start_time = time.time()
    response = requests.post(url, proxies=proxy)
    end_time = time.time()

    proxy_speed = len(response.content) / \
        (end_time - start_time) / 1024 / 1024

    if direct_speed>=proxy_speed:
        return 'Direct'
    else:
        return 'Proxy' 


def detect(url):
    if in_GFW(url) == True:
        return 'Proxy'

    if ping_speed(url) == 'Proxy':
        return 'Proxy'
    elif ping_speed(url) == 'Direct':
        return 'Direct'

    if test_robot(url) == 'Proxy':
        return 'Proxy'
    elif test_robot(url) == 'Direct':
        return 'Direct'
    return 'Proxy'


print(test_robot('https://www.epicgames.com'))
