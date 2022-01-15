# Scoket 编程

# 理论介绍

计算机网络基础知识，推荐一本书《TCP/IP 详解》。

HTTP，Socket，TCP 的区别，HTTP 是应用层的协议。Socket可理解为操作系统提供的应用层与传输层打交道的插座。而 TCP 属于传输层。
通过 Socket 编程，我们可以自己与传输层打交道，定义自己的协议进行通信。


Client 端涉及的操作：

![Socket编程](https://s2.loli.net/2022/01/15/sXuIOz8T12n5DfB.png)

服务端：

- socket：socket 是应用层和传输层之间的接口，传输层有 tcp 和 udp；
- bind(协议，地址，端口)：地址可在本机 IP，也可以指定；每一个应用程序只能占用一个端口，网络
来的数据，操作系统会转发给相应的端口。
- listen(监听客户端 socket 请求)
- accept()
- 阻塞等待连续请求（新套接字）
- recv()
- send(), socket 建立了连接后，可以一直发送数据；http 则不行。
- close()

客户端：

- socket
- connect()
- send()
- recv()
- close()

# Socket 实现聊天

来看一个 socket 实现聊天的例子，第一个是服务端的代码：

```python
# server.py

import socket

# A Socket Server
# 先启动 Server，否则 Client 会无法连接
def respond(client):
    """使用传入对象 client 的发送方法，作出“回应”.  """
    response_str = input("New msg:")
    response_str = "From Server, Admin:" + response_str
    client.send(bytes(response_str, 'utf-8'))


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 2401))
server.listen()
sock_client, addr = server.accept()

while True:
    # 这里才是用户拿到的 sock，上面的 server 则是用来监听的
    data = sock_client.recv(1024)
    print(data.decode("utf8"))
    respond(sock_client)
```

然后是客户端的代码：

```python
# client.py
import socket

# Client, 第一次会尝试连接 Server Say Hi
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 2401))
client.send(f"From Client, Scott: Hi!".encode('utf8'))

while True:
    # 客户端，先发信息
    data = client.recv(1024)
    print(data.decode('utf8'))
    client_id = "From Client, Scott:"
    client_new_msg = client_id + input("New msg:")
    client.send(client_new_msg.encode('utf8'))
```

当客户端起来之后，服务端会收到一条消息，来看看他们的对话吧！

```
# 服务端
From Client, Scott: Hi!
New msg:Hi Scott!
From Client, Scott:Are you admin from the server?
New msg:Yes, i am.
From Client, Scott:Nice to meet you!!!
New msg:Me too. How can i help you?
From Client, Scott:Just test the connection, bye~
New msg:Ok, Have a great day!
From Client, Scott:You too!

# 客户端
From Server, Admin:Hi Scott!
New msg:Are you admin from the server?
From Server, Admin:Yes, i am.
New msg:Nice to meet you!!!
From Server, Admin:Me too. How can i help you?
New msg:Just test the connection, bye~
From Server, Admin:Ok, Have a great day!
New msg:You too!
```

# Socket 实现多用户聊天

上面的 server 只支持一个用户，如何支持多个用户呢？可以使用线程来实现，背后的思想是，每当遇到一个新的连接
请求，就让一个线程去处理, 也就是这一段 `sock_client, addr = server.accept()` 交给一个新的线程去处理。

这是一个多线程的 server，客户端的代码是一样的:

```python
import socket
import threading

# A Socket Server
# 先启动 Server，否则 Client 会无法连接
def respond(client):
    """使用传入对象 client 的发送方法，作出“回应”.  """
    response_str = input("New msg:")
    response_str = "From Server, Admin:" + response_str
    client.send(bytes(response_str, 'utf-8'))

def handle_sock(sock_client, addr):
    while True:
        # 这里才是用户拿到的 sock，上面的 server 则是用来监听的
        data = sock_client.recv(1024)
        print(data.decode("utf8"))
        respond(sock_client)

if __name__ == '__main__':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 2401))
    server.listen()
    while True:
        sock_client, addr = server.accept()
        # 用线程处理新来的用户
        client_thread = threading.Thread(
            target=handle_sock,
            args=(sock_client, addr)
        )
        client_thread.start()
```

来看服务端与不同客户端的通信：

```
From Client 1, Scott: Hi!
New msg:Hi Scott!
From Client 2, The Weeknd: Hi!
New msg:Hi The Weeknd!
From Client 1, Scott:I really like the weeknd!
New msg:Me too!
From Client 2, The Weeknd:I just adds three tracks to my new album: Dawn FM.
New msg:Great!
```

# Socket 模拟 http 请求

你应该听说过 Python 中 request 这个包，它其实底层是依赖 urllib 实现的，而 urllib 又是依赖于 socket。

既然是模拟 http 请求，还是需要做 url 解析，我们将会用到 urllib 中的部分函数。

```python
import socket
from urllib.parse import urlparse

def get_url(url):
    # 解析 url
    url = urlparse(url)
    host = url.netloc   # host
    path = url.path     # 子路径

    if path == "":      # 子路径为空
        path = "/"

    # 建立 socket 连接, 一般网站都使用 8000 端口
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, 80))

    # 构造请求内容，并开始发送请求
    # 关于请求的内容，可以通过 Chrome 的调试工具打开目标网站
    # 再查看 Headers，具体某个网站必须构造哪些请求内容，各有不同
    # 比如百度必须有: host, connection,
    client.send(
        "GET {} HTTP/1.1\r\nHost:{}\r\nConnection:close\r\n\r\n".format(
            path, host
    ).encode("utf8"))

    # 返回的数据不一定是 1024， 有可能是 > 1024 的
    # client.recv(1024), 这样写会出问题，特殊处理一下
    data = b""
    while True:
        # 先接受 1024 个数据
        d = client.recv(1024)
        if d:
            data += d
        else:
            break
    data = data.decode('utf-8')
    print(data)
    client.close()

if __name__ == '__main__':
    get_url("http://www.baidu.com")
```