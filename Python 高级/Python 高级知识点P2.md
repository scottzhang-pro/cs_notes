# 深入理解 set 和 dict

## dict

看 dict 的继承关系:

```
Dict -> MutableMapping -> Mapping -> Collection
```

dict 的拷贝中，有深拷贝和浅拷贝两种，先来看浅拷贝：

```python
d = {
    'name1': {"scott zhang": 1},
    'name2': {"the weeknd": 2}
}

# 浅拷贝, 内部值只是指针; 对 d_copy1 值的修改，会将 d 中的值也修改
d_copy1 = d.copy()
d_copy1['name1']['scott zhang'] = 0
d
# 输出
# {'name1': {'scott zhang': 0}, 'name2': {'the weeknd': 2}}
```

另外深拷贝会将字典内部的所有值都拷贝过去，这需要用到 `copy` 模块来实现：

```python
d_copy2 = copy.deepcopy(d)
d_copy2['name1']['scott zhang'] = 0
d
# 输出
# {'name1': {'scott zhang': 1}, 'name2': {'the weeknd': 2}}
```

dict 常用的方法:

```
- fromkeys
- get
- items
- keys
- update
- setdefault
```

不建议继承 python 自带的 list 或者是 dict，因为对于自带的数据结构有的部分是用 C 实现的，当你继承之后会发现某些操作生效了而某些操作缺没有生效，比如下面这个例子:

```python
class MyDict(dict):
    def __setitem__(self, key, value):
        super().__setitem__(key, value * 10)

# 生效
dt = MyDict()
dt['one'] = 10  # {'one': 100}

# 无法生效
dt = MyDict(one=10)
dt  # {'one': 10}
```

如果你一定要继承，则可以使用 `collections.UserDict`，`collections` 中其实还有很多不错的数据结构，可以都了解一下。

## set, frozenset

set 是一个无序的集合，性能很高，其中的元素不能重复，set 接受的一个可迭代的对象作为参数。

```python
s = {'a', 'b'}
```

frozenset 是一个固定的集合，是一种不可变类型，定义后无法修改。这种特性让它作为 dict 的 key 非常好。

## dict 和 set 的实现原理

dict的key或者set的值都必须是可以hash的，不可变对象都是可hash的, str,fronzenset,tuple
，自己实现的类使用魔法函数__hash__实现哈希。

dict的内存花销大，但是查询速度快，自定义的对象或者python内部的对象都是用dict包装的。

dict的存储顺序和元素添加顺序有关，添加数据有可能改变已有数据的顺序, 最开始会申请内存, 然后随着数据的不断添加, 当剩余空间小于三分之一的时候会申请新的内存然后进行数据迁移, 这个时候存储顺序可能会发生改变.

# 引用、可变性、垃圾回收

在其他编程语言当中 java 中，可以将变量想象成盒子，这个盒子内部的内容大小、数据类型都收固定的。

在 python 中，变量则是指针的形式。

```python
# 不可变类型
a = 1
b = 1
print(id(a))
print(id(b))
# 相等，对一定范围小正数或者是字符串，python 会有一个 intern 机制
# 这个机制会避免去新建某些已经存在的值，而将新的变量直接指向存在的值
# 比如 b 直接指向 1 所在的地址

# 可变类型
a=[1,2,3]
b=[1,2,3]
print(id(a))
print(id(b)) # 不相等
# 首先实例化一个list对象, 然后将a指向该对象, 然后再实例化一个list对象将b指向该对象, a和b指向的是不同的对象

# 可变类型
a=[1,2,3]
b=a
print(id(a))
print(id(b)) # 相等
# 首先实例化一个list对象, 然后将a指向该对象, 然后将a赋值给b, a和b指向的是相同的对象
```

Python 使用的引用计数器，当新的变量对对象有引用时，计数器会+1，比如:

```python
# 引用计数
a = 'scott' # 对象引用 +1
b = a       # 继续 +1
del a       # 对象引用 -1 后等于 1，str 对象值还在，b 还存在，a 不再存在

# 自定义回收逻辑
class A:
    def __del__(self):
        print("开始回收了")

a=A()
b=a
c=b

del a
del b
del c
>>> 开始执行`del c`时打印`开始回收了`
```

关于参数传输错误:

```python
# int 值相加
def add(a,b):
    a+=b
    return a
a=1
b=2
c=add(a,b)

print(a,b,c)
>>> 1 2 3

# list 值相加
def add(a,b):
    a+=b
    return a
a=[1]
b=[2]
c=add(a,b)

print(a,b,c) # a 被改变
>>> [1, 2] [2] [1, 2]

# tuple 值相加
def add(a,b):
    a+=b
    return a
a=(1)
b=(2)
c=add(a,b)

print(a,b,c)
>>> 1 2 3
```