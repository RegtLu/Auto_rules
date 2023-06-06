import re
import sqlite3
import time


class Router(object):
    def __init__(self):
        self.update_GFWlist()
        self.refresh_custom()
        with open('./gfw.lst') as f:
            rules = f.readlines()
        self.black_rules = rules
        with open('./cn.lst') as f:
            rules = f.readlines()
        self.white_rules = rules
        self.sql = sqlite3.connect('./rules.sqlite')

    def update_GFWlist(self):
        import update
        update.main()
        del update

    def in_GFW(self, url):  # True or False
        for rule in self.black_rules:
            res = re.findall(rule.replace('\n', ''), url)
            if res == [] or len(res) > 1 or res[0] != url:
                continue
            else:
                return True
        return False

    def in_whitelist(self, url):  # True or False
        for rule in self.white_rules:
            res = re.findall(rule.replace('\n', ''), url)
            if len(res) == 1:
                return True
            else:
                continue
        return False

    def custom(self, url):
        cursor = self.sql.cursor()
        cursor.execute('SELECT * FROM RULES WHERE PROXY = TRUE')
        rules = cursor.fetchall()
        for rule in rules:
            res = re.findall(rule, url)
            if res == [] or len(res) > 1 or res[0] != url:
                continue
            else:
                cursor.close()
                return 'Proxy'
        cursor.execute('SELECT * FROM RULES WHERE PROXY = FALSE')
        rules = cursor.fetchall()
        for rule in rules:
            res = re.findall(rule, url)
            if res == [] or len(res) > 1 or res[0] != url:
                continue
            else:
                cursor.close()
                return 'Direct'
        cursor.close()
        return None

    def test(self, url):  # 'Direct' or 'Proxy' or 'Not Found'
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
            self.add(url, 'Direct')
            return False
        else:
            self.add(url, 'Proxy')
            return True

    def add(self, url, route):
        if route == 'Proxy':
            arg = 'TRUE'
        elif route == 'Direct':
            arg = 'FALSE'
        else:
            return
        self.sql.execute("INSERT INTO RULES VALUES('$1',$2,$3)" %
                         (url, int(time.time()), arg))

    def route(self, url):
        if self.in_whitelist(url) == True:
            return ('Direct', 'GFW')
        if self.in_GFW(url) == True:
            return ('Proxy', 'GFW')

        custom_ans = self.custom(url)
        if custom_ans == 'Direct':
            return ('Direct', 'Custom')
        elif custom_ans == 'Proxy':
            return ('Proxy', 'Custom')

        test_ans = self.test(url)
        if test_ans:
            return ('Proxy', 'Test')
        else:
            return ('Direct', 'Test')

    def refresh_custom(self):
        self.sql.execute(
            "DELETE FROM RULES WHERE strftime('%s','now') - TIME > 864000")


router = Router()
print(router.route('www.google.com'))
