from cgitb import html
import socket
from urllib.parse import urlparse

# 需处理系统兼容性问题
# 如 Windows 和 Linux 不一样, 推荐使用 selectors
# import select
from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE


# select + 回调 + 事件循环
selector = DefaultSelector()
urls = ["www.baidu.com"]
stop = False

class Fetcher:
    def connected(self, key):
        selector.unregister(key.fd)
        # 使用了事件监听，所以无需 try catch
        self.client.send(
            "GET {} HTTP/1.1\r\nHOST:{}\r\nConnection:close\r\n\r\n".format(
                self.path, self.host
            ).encode("utf8")
        )
        selector.register(self.client.fileno(), EVENT_READ, self.readable)


    def readable(self, key):
        """只要可读，就会调用 readable"""
        # data = b""
        # while True:
        #     d = self.client.recv(1024)
        #     if d:
        #         data += d
        #     else:
        #         break
        d = self.client.recv(1024)
        if d:
            self.data += d
        else:
            selector.unregister(key.fd)

            data = self.data.decode("utf8")
            html_data = data.split('\r\n\r\n')[1]
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
        self.path = url .path
        self.data = b""

        if self.path == "":
            self.path = "/"

        # socket connect
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setblocking(False)

        try:
            self.client.connect((self.host, 80))
        except BlockingIOError as e:
            pass

        # 将 socket 注册到 select 中
        selector.register(
            self.client.fileno(), # socket 的文件描述符
            EVENT_WRITE,         # 事件
            self.connected       # 回调函数，即我们需要执行的函数
        )


    def loop(self):
        # event main loop, 不停的请求 socket 状态，并调用对应的回调函数
        # 注意：
        # select 本身不支持 register 模式
        # socket 状态变化以后的回调由我们自己完成
        # 返回的
        while not stop:
            ready = selector.select()
            while True:
                for key, mask in ready:
                    callback = key.data
                    callback(key)


if __name__ == '__main__':
    fetcher = Fetcher()
    fetcher.get_url("www.baidu.com")
    fetcher.loop()
