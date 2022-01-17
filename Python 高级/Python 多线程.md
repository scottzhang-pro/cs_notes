# 关于线程

线程是操作系统的最小调度单位，属于进程。如果将操作系统比较工厂，那么进程就属于车间，而线程就是具体的工人。

# 使用 Tread 类

Python 中线程的模块是 treading, 我们先看一个简单的例子：

先导入包，定义好我们需要的函数：

```python
import time
import threading

def get_detail_html(url):
    """模拟爬取网页内容的操作"""
    print('get detail started')
    time.sleep(2)
    print('get detail end')


def get_detail_url(url):
    """模拟获取网页地址的操作"""
    print('get url started')
    time.sleep(2)
    print('get url end')
```

进行我们第一个测试：

```python
if __name__ == '__main__':
    # 定义两个线程
    thread1 = threading.Thread(target=get_detail_html, args=("",))
    thread2 = threading.Thread(target=get_detail_url, args=("",))

    start_time = time.time()

    # 线程可以并行，所以线程开始执行后无需等待执行结果即可继续执行打印时间的代码
    thread1.start()
    thread2.start()

    print(time.time() - start_time)
```

查看执行结果:

```python
get detail started
get url started
0.0020024776458740234
get detail end
get url end
```

设置守护线程可以让主线程结束后将子线程都 kill 掉：

```python
if __name__ == '__main__':
    # 定义两个线程
    thread1 = threading.Thread(target=get_detail_html, args=("",))
    thread2 = threading.Thread(target=get_detail_url, args=("",))

    # 设置守护线程
    # 主进程执行完毕后，子线程都 kill 掉，若其中只有某个
    # 子线程设置了守护线程，则等待另外一个
    thread1.setDaemon(True)
    thread2.setDaemon(True)

    start_time = time.time()

    # 线程可以并行，所以线程开始执行后无需等待执行结果即可继续执行打印时间的代码
    thread1.start()
    thread2.start()

    print(time.time() - start_time)
```

主线程执行完毕后，其它子线程也将结束（在 jupyter 中不一样）

```
get detail started
get url started
0.0010001659393310547
```

同时线程还有一个 join 方法，可以造成阻塞并等待前面的线程结束之后才运行后面的代码:

```python
if __name__ == '__main__':
    # 定义两个线程
    thread1 = threading.Thread(target=get_detail_html, args=("",))
    thread2 = threading.Thread(target=get_detail_url, args=("",))

    start_time = time.time()

    # 线程可以并行，所以线程开始执行后无需等待执行结果即可继续执行打印时间的代码
    thread1.start()
    thread2.start()

    # 阻塞，等所有子线程运行完成才继续
    thread1.join()
    thread2.join()

    print(time.time() - start_time)
```

# 继承 Tread 类

我们也可以集成 treading.Tread 类实现多线程：

```python
class GetDetailHtml(threading.Thread):
    def run(self):
        """模拟爬取网页内容的操作"""
        print('get detail started')
        time.sleep(2)
        print('get detail end')


class GetDetailURL(threading.Thread):
    def run(self):
        """模拟获取网页地址的操作"""
        print('get url started')
        time.sleep(2)
        print('get url end')


if __name__ == '__main__':
    thread1 = GetDetailHtml()
    thread2 = GetDetailURL()
    start_time = time.time()

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    print(time.time() - start_time)
```

# 线程间通信

前面提供了两个函数，一个是负责去抓 url，一个是去爬取 url 的内容，那么对于抓到的 url，你需要有一种方式传给爬取内容的函数，这就是线程之间需要通信的例子。

