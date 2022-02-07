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

# 使用 ThreadPoolExecutor

```python
import logging
import concurrent.futures
import time

def thread_function(name):
    """模拟某个函数的执行"""
    logging.info("Thread %s: starting", name)
    time.sleep(2)
    logging.info("Thread %s: finishing", name)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(thread_function, ['A thread', 'B thread', 'C thread'])

```

输出如下:

```
14:36:14: Thread A thread: starting
14:36:14: Thread B thread: starting
14:36:14: Thread C thread: starting
14:36:16: Thread C thread: finishing
14:36:16: Thread B thread: finishing
14:36:16: Thread A thread: finishing
```

# 竞态(Race Conditions)

竞态指的是两个或以上的线程访问或者操作同一个对象，会导致其中一个线程在正常的处理过程中，对象被其他线程修改的情况。



# 线程间通信

前面提供了两个函数，一个是负责去抓 url，一个是去爬取 url 的内容，那么对于抓到的 url，你需要有一种方式传给爬取内容的函数，这就是线程之间需要通信的例子。

线程中通信有几种方案：

- 使用全局变量
- 使用 Python 中的队列，即 queue

# 线程同步

在之前关于 GIL 的文章中，有一个多线程加减的例子：

```python
import threading

total = 0

def add():
    global total
    for i in range(1000000):
        total += 1

def desc():
    global total
    for i in range(1000000):
        total -= 1


thread1 = threading.Thread(target=add)
thread2 = threading.Thread(target=desc)

thread1.start()
thread2.start()

thread1.join()
thread2.join()

print(total)
```

当我们查看上面代码的字节码的时候，可以看到大概的步骤如下：


1. 加载 total 到内存
2. 加载 1
3. 进行加法操作
4. 赋值给 total （多线程状态下，赋值会出错）

上述代码，每次的结果都不一样，就是因为在上面4个步骤的任意一个步骤中，GIL 都有可能被释放，然后加载的变量被其他的线程修改了。

这里就引出我们的线程的同步机制，即我们设置一种方法，让某一段代码执行完毕之后，才能切换到别的线程执行，这就保证了在修改数据的时候，不会出错。

同步机制可以使用锁来实现：

```python
from threading import Lock
import threading

total = 0
lock = Lock()

def add():
    global total
    global lock
    for i in range(10000):
        lock.acquire()
        total += 1
        lock.release()

def desc():
    global total
    global lock
    for i in range(10000):
        lock.acquire()
        total -= 1
        lock.release()

thread1 = threading.Thread(target=add)
thread2 = threading.Thread(target=desc)

thread1.start()
thread2.start()

print(f"Total is: {total}")
# Total is: 0，可以看到结果正确了
```

但是使用锁，也优缺点，第一个是性能上的损失，另外是容易引起死锁。

```python
# 1. 没有 release 却重新申请导致死锁
lock.acquire()
lock.acquire()

# 2. 竞争死锁
# A 任务需要 a，b，B 任务需要 b，a
# 那么 A 和 B 互相持有 a，b 容易导致死锁


# 3. 子函数死锁
def do_something(lock):
    lock.acquire()

lock.acquire()
do_something(lock)
```

针对第三种情况，Python 有一种 RLock（可以重复申请的锁）, 可以让你连续申请锁，但是注意，申请和释放的次数要一样。

```python
from threading import RLock

lock.acquire()
lock.acquire()
# pass
lock.release()
lock.release()
```