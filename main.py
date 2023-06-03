

def in_GFW(url):  # True or False
    pass


def ping_speed(url):  # 'Direct' or 'Proxy' or 'Blocked'
    pass


def test_robot(url):  # 'Direct' or 'Proxy' or 'Not Found'
    url = url+'/robots.txt'
    pass


def test_homepage(url):  # 'Direct' or 'Proxy' or ' Not Found'
    pass


def detect(url):
    if in_GFW(url) == True:
        return 'Proxy'

    if res := ping_speed(url) == 'Proxy':
        return 'Proxy'
    elif res == 'Direct':
        return 'Direct'
    else:
        pass

    if res := test_robot(url) == 'Proxy':
        return 'Proxy'
    elif res == 'Direct':
        return 'Direct'
    else:
        pass

    if res := test_homepage(url) == 'Proxy':
        return 'Proxy'
    elif res == 'Direct':
        return 'Direct'
    else:
        pass

    return 'Proxy'
