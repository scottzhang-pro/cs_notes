from cgitb import html
import socket
from urllib.parse import urlparse

# 需处理系统兼容性问题
# 如 Windows 和 Linux 不一样, 推荐使用 selectors
# import select
from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE


# select + 回调 + 事件循环
# 使用 select，一个线程发出url请求后即可不管，操作系统 select
# 会自动使用可用的 socket 处理，对比多线程中一个线程对应一个 url
# 省去了线程切换的开销，以及其占用的内存
selector = DefaultSelector()
urls = ["www.baidu.com"]
stop = False

class Fetcher:
    def connected(self, key):
        selector.unregister(key.fd)
        # 使用了事件监听，所以无需 try catch
        self.client.send(
            "GET {} HTTP/1.1\r\nHost:{}\r\nConnection:close\r\n\r\n"
            .format(self.path, self.host).encode("utf8")
        )
        selector.register(self.client.fileno(), EVENT_READ, self.readable)


    def readable(self, key):
        d = self.client.recv(1024)
        if d:
            self.data += d
        else:
            selector.unregister(key.fd)
            data = self.data.decode("utf8")
            html_data = data.split("\r\n\r\n")[1]
            print(html_data)
            self.client.close()
            urls.remove(self.spider_url)
            if not urls:
                global stop
                stop = True


    def get_url(self, url):
        self.spider_url = url
        url = urlparse(url)
        self.host = url.netloc
        self.path = url.path
        self.data = b""
        if self.path == "":
            self.path = "/"

        # 建立socket连接
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setblocking(False)

        try:
            self.client.connect((self.host, 80))  # 阻塞不会消耗cpu
        except BlockingIOError as e:
            pass

        # 将 socket 注册到 select 中
        # 参数是 client.fileno, 事件，回调函数，即我们需要执行的函数
        selector.register(
            self.client.fileno(),
            EVENT_WRITE,
            self.connected  
        )


def loop():
    #事件循环，不停的请求socket的状态并调用对应的回调函数
    #1. select本身是不支持register模式
    #2. socket状态变化以后的回调是由程序员完成的
    while not stop:
        ready = selector.select()
        for key, mask in ready:
            call_back = key.data
            call_back(key)


if __name__ == '__main__':
    fetcher = Fetcher()
    fetcher.get_url("www.baidu.com")
    loop()
