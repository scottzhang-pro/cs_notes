# 多进程

在 Python 中，对于IO密集型操作，可以考虑多线程。而 CPU 密集型操作则应考虑多进程。

在 Linux 中, `os.fork()` 子进程会将父进程中所有数据拷贝过来。

```python
import os

print("Hi, This is Scott!")
pid = os.fork()

if pid == 0:
    print(f"位于子进程: {os.getpid()}")
    print(f"父进程为: {os.getppid()}")
else:
    print(f"位于父进程: {pid}")
```

这里的运行结果为：

```
Hi, This is Scott!
位于父进程: 3021
Hi, This is Scott!
位于子进程: 3021
父进程为: 3020
```

# Multiprocessing

```python
import time
import multiprocessing

def do_something(n):
    time.sleep(n)
    print("do something in sub_progress")
    return n

if __name__ == '__main__':
    progress = multiprocessing.Process(
        target=do_something,
        args=(2,)
    )
    print(f"progress pid: {progress.pid}")
    progress.start()
    print(f"progress pid: {progress.pid}")
    progress.join()

    print(f"main progress finished")
```

输出如下：

```
progress pid: None
progress pid: 3391
do something in sub_progress
main progress finished
```

当然也可以使用继承的方式，重写内部的 run 方法，这部分和多线程中的代码类似。

# 进程池

```python
import time
import multiprocessing

def do_something(n):
    time.sleep(n)
    print("do something in sub_progress")
    return n


if __name__ == '__main__':
    # using a pool to manage process
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    result = pool.apply_async(do_something, args=(3,))

    # waiting all tasks finished
    # must close a pool before join it, for new task added to pool
    pool.close()
    pool.join()
    print(result.get())
```

输出如下：

```
❯ python multiprocessing_test.py
do something in sub_progress
3
```

pool 中还有 `imap` 方法，类似线程中 `excuter.map` 方法，result 为每个函数的返回值:

```python
# 进入顺序
for result in pool.imap(do_something, [1, 3, 5]):
    print(f"do something in {result}s")

# 完成顺序
for result in pool.imap_unordered(do_something, [1, 3, 5]):
    print(f"do something in {result}s")
```

输出如下:

```
❯ python multiprocessing_test.py
do something in sub_progress
do something in 1s
do something in sub_progress
do something in 3s
do something in sub_progress
do something in 5s
```

# 进程间通信

多进程中，使用全局变量是无法共享数据的，因为进程间的数据是互相隔离的。

## 使用 Queue

```python
import time
from multiprocessing import Process, Queue
# 下面的 queue 在多进程中无法使用
# from queue import Queue

def producer(queue):
    queue.put("a")
    time.sleep(2)

def consumer(queue):
    time.sleep(2)
    data = queue.get()
    print(data)

if __name__ == '__main__':
    queue = Queue(10)

    my_producer = Process(target=producer, args=(queue,))
    my_consumer = Process(target=consumer, args=(queue,))

    my_producer.start()
    my_consumer.start()

    my_producer.join()
    my_consumer.join()

```

## 使用进程池

Pool 中的进程间通信，需要使用 manager 中的 queue.

```python
import time
from multiprocessing import Pool, Manager

def producer(queue):
    queue.put("a")
    time.sleep(2)

def consumer(queue):
    time.sleep(2)
    data = queue.get()
    print(data)

if __name__ == '__main__':
    # pool 中的 queue 需要使用 manager 中的
    queue = Manager().Queue(10)
    pool = Pool(2)

    pool.apply_async(producer, args=(queue,))
    pool.apply_async(consumer, args=(queue,))

    pool.close()
    pool.join()
```

至此我们这里出现了三个 queue，注意区分。

```python
from queue import Queue
from multiprocessing import Queue
from multiprocessing import Manager
queue = Manager().Queue
```

## 使用管道

```python
from multiprocessing import Pipe, Process

def producer(pipe):
    pipe.send('scott')

def consumer(pipe):
    data = pipe.recv()
    print(data)

if __name__ == '__main__':
    # pipe 只能适用于两个进程, 但更高效，相比 queue 它没那么多锁
    recevie_pipe, send_pipe = Pipe()

    my_producer = Process(target=producer, args=(send_pipe,))
    my_consumer = Process(target=consumer, args=(recevie_pipe,))

    my_producer.start()
    my_consumer.start()
    my_producer.join()
    my_consumer.join()

```

## 使用共享内存


Manager 中有一些支持共享内存的数据结构。


```python
from multiprocessing import Manager

def producer(pipe):
    pipe.send('scott')

def consumer(pipe):
    data = pipe.recv()
    print(data)

if __name__ == '__main__':
    share_var = Manager().dict
    share_var = Manager().Array
    share_var = Manager().list
    # and more
```