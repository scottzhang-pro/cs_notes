# Python 中的对象

## 一切皆对象

在其他的静态语言中，有对象和类，对象是类的一个实例，但是在 Python 中，这两者都是对象。  

在 Python 中，函数、类其实也是对象，属于 Python 的一等公民，这意味着它可以：

- 被赋值给一个变量
- 可以添加到集合对象中
- 可以作为参数传递给函数
- 可以当作函数的返回值

对象的三个特征：身份(内存中的地址)、类型（1 是 int 类型）、值（a=1 中的1）。

## Python 中的内置类型

None: 全局只有一个.

数值类型：int, float, complex 复数类型, bool.

迭代类型：迭代器、生成器，可以用 for 循环遍历。

序列类型：list, (bytes, bytearray, memoryview), range, tuple, str, array.

映射：字典，有 key 和 value

集合：set，frozenset（不可修改的 set），set 和 dict 的实现原理差不多，性能很高。

上下文管理器：with 语句。

其他：模块类型、class 和实例类型、函数类型、方法类型、代码类型、object对象、type类型、ellipsis 类型（省略号）, notimplemented类型。

## type, object 和 class 的关系

 type 有两种用法：一个是生成一个类；另外一个是查看某个对象的类型。

```python
type(1)   # class int
type(int) # class type

# type -> int ->1
# type -> class -> obj
```

object 是所有类的基类，object 的基类是空， object 是 type 生成的。

但 type 本身也是一个类，同时 type 也是一个对象，type 的基类又是 object。

为了理解其中的关系，可以参考下图：

![image.png](https://s2.loli.net/2022/01/09/NrGE3UmuzJpbdIk.png)

- 虚线是实例，实现是继承关系
- type 创建了所有的对象；type 继承自 object，而 object 又是 type 的一个实例；type 还是自己的实例（连自己都不放过, 通过指针实现）；
- list 继承自 object，"abc" 继承自 str, str 继承自 object
- list类 继承自 object 类，同时 list 也是 type 的一个实例对象，所以其实 list 既是类也是实例，即 python 中一切皆对象的一个理解。
- 为什么 list 是一个 class的同时，也要是一个对象，因为如果它变成一个对象，就可以动态的修改。而在静态语言中，类一旦创建放到内存中，修改起来就很麻烦了。而 python 中将其变成对象，就很简单了。

# 魔法函数

## 魔法函数

魔法函数是为了增强某个类的特性，它有约定俗成的名字，你只需要实现这个函数即可。

```python
class Company(object):
    def __init__(self, employee_list):
        self.employee = employee_list

	# 让此类的实例，支持被 for 循环访问内部 employee
    def __getitem__(self, item):
        return self.employee[item]

company = Company(["Apple", "MicroSoft"])

# 支持 for 循环
for company_name in company:
    print(company_name)

# 支持切片
company[:2]
```

## 有哪些魔法函数

首先可以分为非数学运算与数学相关。

非数学运算中又有：

```
- 字符串表示，__repr__, __str__
- 集合序列相关，__len__, __get/set/delitem__, __contains__
- 迭代相关, __iter__, __next__
- 可调用, __call__
- with 上下文管理器, __enter__, __exit__
- 数值转换，__abs__, __int/float/bool/...__, __hash__
- 元类相关, __new__, __init__
- 属性相关，__get/setattr__, __get/setattribute__. __dir__
- 属性描述符, __get__, __set__, __delete__
- 协程, __await__, __aiter__, __anext__, __aenter__, __aexit__
```

数学运算则有一元、二元运算符，算数运算符，位运算符等等，暂时不做过多介绍。

在 Python 中，len 方法有其特殊性。当 len 作用在内置类型如 set, list, dict 上的时候，因为这些结构都是用 C 语言实现的，性能非常高，当 len 计算这些数据结构的长度的时候，会直接读取这个数据结构的长度值（C 会维护一个长度值），而不会遍历该树结构。





# 类和对象

## 鸭子类型和多态

当你看见一只鸟走起来像鸭子、游泳像鸭子、叫起来也像鸭子，那么这只鸟就是鸭子。



```python
class Dog(object):
    def say(self):
        print('I am a dog')


class Duck(object):
    def say(self):
        print('I am a Duck')

for obj in [Dog, Duck]:
    obj().say()

```



## 抽象基类

抽象基类，其他类可以继承此类，并必须要实现其规定的方法，抽象基类本身无法实例化出任何对象。

在 Python 中，检查某个类是否有某个方法，可以通过 hasattr 方法检查，比如:

```python
class Company(object):
    def __init__(self, employee_list):
        self.employee = employee_list

    def __len__(self, item):
        return len(self.employee)

com = Company(['Apple', 'Google'])

# 通过 hasattr 检查类是否有某个方法
hasattr(com, "__len__")
```

其结果与下面代码一致：

```python
from collections.abc import Sized
# 问题：com 没有继承自 Sized，为何可以使用 isinstance 判断？
# Sized 内部有一个 __subclasshot 方法，其中会直接判断 com 有没有 len 方法
isinstance(com, Sized)
```

其中 Sized 是一个抽象基类。背后的逻辑是，com 实现了 `__len__` 方法，所以它继承了 Sized 抽象基类，所以判断为真。

另外一种抽象基类的应用是限制子类必须实现某些方法:



```python
# 抽象基类：限制子类必须实现某个方法
class CacheBase():
    def get(self, key):
        raise NotImplementedError

    def set(self, key, value):
        raise NotImplementedError

# 一个 RedisCache 类，继承自 CacheBase
class RedisCache(CacheBase):
    pass

# 初始化 RedisCache
# 下面这步不会报错
redis_cache = RedisCache()
# 调用 get 或者 set 的时候才会报错
redis_cache.get('test')

```

如果你希望在 RedisCache 初始化的时候就报错，则需要使用 abc 抽象基类模块。

```python
import abc
class CacheBaseABC(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get(self):
        pass

    @abc.abstractmethod
    def set(self):
        pass

# 此处会报错
redis_cache_abc = CacheBaseABC()
```

> Python 中，abc 模块，有系统全局的abc，也有 collections.abc

在平时的编码实践中，注意不要过度依赖 abc 模块，容易导致过度设计, 可以考虑使用 mixin 的方式。



## isinstance 和 type

  

```python
class A:
    pass


class B(A):
    pass

b = B()


# 打印两个都是 true
print(isinstance(b, B))
print(isinstance(b, A))

print(type(b) is B)
# 也是 True
# 注意 is 和 == 的区别
# is 的意思是，判断两个对象是不是同一个对象，即 id() 返回的值是不是一样
# == 的意思是，判断值是否相等
```

