# 什么是 GIL

Python 全局解释器锁或 GIL(Global Interpreter Lock)，简单来说，是一个互斥体（或锁），它只允许一个线程持有 Python 解释器的控制权。

这意味着，在同一时刻，只有一个线程可以在 CPU 上可以执行字节码，即便是在拥有多核 CPU 的情况下，这也是 Python 被诟病的一个点。

# GIL 解决了什么问题？

既然 GIL 会带来性能利用上的问题，那为什么还要这样设计呢？

在谈这个问题之前，先来说说 Python 中的内存管理，Python 使用引用计数来实现内存管理：

```python
import sys
a = []
b = a
sys.getrefcount(a)
# 3
```

当一个对象的引用计数为0的时候，也就是没有变量指向它的时候，它就会被销毁。

这种引用计数的机制需要一个保护机制，以确保当多个线程同时对同一个对象进行操作时，不会发生错误（比如 A 线程对 X 加一百万次，B 线程对 X 减一百万次），如果放任不管，可能会造成内存泄漏（内存永远无法释放），或者是错误释放了还存在引用的内存。

如果给在不同线程之间共享的数据结构的引用计数加一把锁，这样它们就不会被不一致地修改。 

但是给每一个对象（或者是一组对象）都加锁可能会导致死锁，而且在多把锁的情况下，对于锁的申请与释放又会导致性能下降。

GIL 规定执行任何 Python 字节码都需要先获得解释器锁, 这就避免了死锁和性能大幅下降的情况，坏处是 Python 程序只能以单线程的形式运行。

# 为什么选择 GIL 作为解决方案？

那么，为什么在 Python 中使用了一种看似如此笨拙的方法呢？ Python 的开发人员做出了一个错误的决定吗？毕竟现在动不动给就是 8 核 CPU。

在 [Larry Hastings](https://www.youtube.com/watch?v=KVKufdTphKs&t=731s) 关于 GIL 的演讲中，他说：“选择 GIl 的这个决定正是让 Python 如此流行的原因”

在操作系统出现线程这个概念以前，Python就存在。Python 被设计的易于使用，以使得开发更快。早期的 Python 依赖许多 C 的库，为了避免问题的产生，这些 C 程序需要一个线程安全的内存管理，而 GIL 让这成为了可能。可以说 GIL 是 CPython 开发人员在 Python 早期面临的难题的一个实用的解决方案。

# 什么是 CPython

Cpython 是用 C 写的一个解释器。

PYthon 有很多个解释器，如 CPython, Jython, IronPython 以及 PyPy, 分别使用 C, Java, C# 和 Python 实现。

我们知道 C 并不是一门面向对象的编程语言。你可能听说过在 Python 中一切皆对象（比如 int, str)，这在 CPython 层面的实现也是一样的，在 CPython 中，有一个 struct 叫做 PyObject，CPython 中的每一个对象都使用它。

> Note: A struct, or structure, in C is a custom data type that groups together different data types. To compare to object-oriented languages, it’s like a class with attributes and no methods.

PyObject，也就是所有 Python 对象的爷爷，包含了两个东西:

- `ob_refcnt`, 引用计数，实现垃圾回收机制
- `ob_type`, 指针指向另一个结构体，结构体中保存了实际的对象类型

关于 CPython 的内存管理，可以参考 RealPython 的[这篇](https://realpython.com/python-memory-management/#garbage-collection)文章。


# GIL 的影响

Python 中，如果你使用线程来同时对一个变量进行加减操作，会发现结果是不一样的:

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

# 每次的结果都不一样
# GIL 并不是上面某个函数一直占有，而是在某个函数转化成字节码后
# 执行一段长度的字节码后，会释放 GIL 码，然后给其他线程执行
print(total)

```

GIL 让你在同一时刻只能利用到一个线程，对于 CPU 密集型程序，使用单线程和多线程，其执行效率是一样的:

```python
# single_threaded.py
import time
from threading import Thread

COUNT = 50000000

def countdown(n):
    while n>0:
        n -= 1

start = time.time()
countdown(COUNT)
end = time.time()

print('所需时间(秒) -', end - start)
```

在四核的机器上，它需要的时间是：

```
$ python single_threaded.py
所需时间(秒) - 6.20024037361145
```

现在使用两个线程编写一个一样的程序:

```python
# multi_threaded.py
import time
from threading import Thread

COUNT = 50000000

def countdown(n):
    while n>0:
        n -= 1

t1 = Thread(target=countdown, args=(COUNT//2,))
t2 = Thread(target=countdown, args=(COUNT//2,))

start = time.time()
t1.start()
t2.start()
t1.join()
t2.join()
end = time.time()

print('所需时间(秒) -', end - start)
```

运行查看结果:

```python
$ python multi_threaded.py
所需时间(秒) - 6.924342632293701
```

可以看到使用多线程和不适用多线程花的时间是差不多的。

GIL 对于 CPU 密集型的程序有限制的，对于 IO 密集型的则没有很大影响。

如果你编写了使用线程去处理图象中的每一个部分，那么甚至会让你的运行时间增加，这是因为申请和释放锁还需要额外的开销。

在 Python 3 更新的时候，许多人都希望将 GIL 移除，确实也有很多人做过尝试，但发现这么做除了导致很多的 C 语言库不支持意外，还让单线程下的 Python 相比较 Python2 更慢。

所以 Python 的创始人在谈及 GIL 时说：

> “I’d welcome a set of patches into Py3k only if the performance for a single-threaded program (and for a multi-threaded but I/O-bound program) does not decrease”.

但 Python3 对 GIl 有过一次升级，即将 IO 密集型的线程申请锁的优先级降低。

Python 的 GIL 会饿死 I/O 密集型线程，因为它们不给它们从 CPU 密集型线程获取 GIL 的机会。

这是因为 Python 内置了一种机制，该机制强制线程在固定的连续使用间隔后释放 GIL，如果没有其他人获得 GIL，同一个线程可以继续使用它。

```python
import sys
# The interval is set to 100 instructions:
sys.getcheckinterval()
```

这种机制的问题在于，大多数情况下，CPU 密集型线程会在其他线程获取 GIL 之前重新获取 GIL，在 2009 年的时候，这个 bug 在 Python 3.2 中由 Antoine Pitrou 修复了，他设计了一种机制去查看其他线程申请锁但被拒绝的次数，目的就是防止 CPU 密集型线程长期占用 GIL 锁。

# 如何解决 GIL 带来的问题

如果确定 GIL 是你程序的瓶颈，可以有几个优化的方向：

**使用多进程**：

```python
from multiprocessing import Pool
import time

COUNT = 50000000
def countdown(n):
    while n>0:
        n -= 1

if __name__ == '__main__':
    pool = Pool(processes=2)
    start = time.time()
    r1 = pool.apply_async(countdown, [COUNT//2])
    r2 = pool.apply_async(countdown, [COUNT//2])
    pool.close()
    pool.join()
    end = time.time()
    print('所需时间(秒)', end - start)
```

使用多进程，所需时间只需要 4 秒。在进程中，每个进程都有自己的 GIL 锁用于内部线程的控制，所以互不影响。

> 参考阮一峰关于: [进程与线程的一个简单解释](http://www.ruanyifeng.com/blog/2013/04/processes_and_threads.html)。


**更换解释器**

GIL 的问题，只存在于最开始的 CPython 中。


这篇文章对 Python 的 GIL 做了一个简单的介绍，如果你还想了解 GIL 更底层的东西，可以看一下 David Beazley 关于 GIL 的讲座: [Understanding the Python GIL](https://www.youtube.com/watch?v=Obt-vMVdM8s)