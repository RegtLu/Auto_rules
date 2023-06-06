def init():
    # download_GFWlist()
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
    del update


def in_GFW(url):  # True or False
    import re
    for rule in adblock_rules:
        res = re.findall(rule.replace('\n', ''), url)
        if res == [] or len(res) > 1 or res[0] != url:
            continue
        else:
            return True
    return False


def in_direct(url):
    pass


def in_proxy(url):
    pass

def to_direct(url):
    pass


def to_proxy(url):
    pass


def in_whitelist(url):  # True or False
    import re
    for rule in white_rules:
        res = re.findall(rule.replace('\n', ''), url)
        if len(res) == 1:
            return True
        else:
            continue
    return False


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
        to_direct(url)
        return 'Direct'
    else:
        to_proxy(url)
        return 'Proxy'


def detect(url):
    if in_whitelist(url) == True:
        return ('Whitelist', 'Direct')
    if in_GFW(url) == True:
        return ('GFW', 'Proxy')
    if in_direct(url) == True:
        return ('Custom', 'Direct')
    if in_proxy(url) == True:
        return ('Custom', 'Proxy')
    robot_ans = test_robot(url)
    if robot_ans == 'Proxy':
        return ('Robots', 'Proxy')
    elif robot_ans == 'Direct':
        return ('Robots', 'Direct')
    return ('Final', 'Proxy')


init()
print(detect('www.google.com'))
print(detect('www.baidu.com'))
print(detect('cdda.fun'))
