import socket
import urllib.parse


def in_GFW(url):#True or False
    pass
def ping_speed(url):# 'Direct' or 'Proxy' or 'Blocked'
    pass
def test_robot(url):# 'Direct' or 'Proxy' or 'Not Found'
    url=url+'/robots.txt'
    pass
def test_homepage(url):# 'Direct' or 'Proxy' or ' Not Found'
    pass








class Connection(object):
    def __init__(self) -> None:
        self.receive_socket=socket.socket()
        self.receive_socket.bind(('127.0.0.1', '4778'))
        self.receive_socket.listen(20)
        self.proxy_socket=socket.socket()
        self.proxy_socket.connect(('127.0.0.1', '7890'))
        
    def receive(self):
        self.request=self.receive_loop().__str__

    def receive_loop(self):
        while True:
            request = self.receive_socket.recv(102400)
            yield request

    def proxy_send(url):
        pass
    def direct_send(url):
        pass

    def detect_protocol(self):
        request = self.request
        url = urllib.parse.urlparse(request.decode("utf-8"))
        scheme = url.scheme
        if scheme == "http":
            return "http"
        elif scheme == "https":
            return "https"
        else:
            raise ValueError("Unsupported protocol: " + url.scheme)

    def send(self):
        request = self.request
        url = urllib.parse.urlparse(request.decode("utf-8"))
        netloc = url.netloc
        if in_GFW(netloc)==True:
            self.proxy_send()
            return

        if res:=ping_speed(netloc)=='Proxy':
            self.proxy_send()
            return
        elif res=='Direct':
            self.direct_send()
            return
        else:
            pass

        if res:=test_robot(netloc)=='Proxy':
            self.proxy_send()
            return
        elif res=='Direct':
            self.direct_send()
            return
        else:
            pass

        if res:=test_homepage(netloc)=='Proxy':
            self.proxy_send()
            return
        elif res=='Direct':
            self.direct_send()
            return
        else:
            pass

        self.proxy_send()
        return