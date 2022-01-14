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
# 1. int 值相加
def add(a, b):
    a += b
    return a
a = 1
b = 2
c=add(a, b)

print(a, b, c)
>>> 1 2 3

# 2. list 值相加
def add(a, b):
    a += b
    return a
a=[1]
b=[2]
# a，b 两个 list 传入的是引用
# 实际上会将 a 修改掉
c = add(a, b)

print(a,b,c) # a 被改变
>>> [1, 2] [2] [1, 2]

# 3. tuple 值相加
def add(a, b):
    a += b
    return a

a=(1)
b=(2)
c=add(a,b)

print(a,b,c)
>>> 1 2 3
```


# 元类编程

## Property 动态属性

你拿到一个之前写的类 User，其中初始化需要传入 name，birthday，现在对于获取 user 的 age 的方式有了变化，但是很多以前的代码都是通过 `obj.age` 的方式访问 age 的，你希望在不改变大量代码的情况下，能更新 age 的方法。一个办法是通过 python 的属性描述符，即为这个类定义一个 age 方法：

```python
@property
def age(self):
    return datetime.now().year - self.birthday.year

```

在使用方式上，和之前的使用方式是一样的：

```python
user = User('scott', 1995)
user.age
```

不只是取值，设置值也是有相关的方法的：

```pythyon
@age.setter
def age(self, value):
    self.age = value
```

## getattr 和 getattribute

这两个函数的完整名字是 `__getattr__` 和 `__getattribute__`,实际上就是之前介绍的魔法函数。

第一个函数是，在查找不到一个属性的时候调用，就是说当你在访问一个类不存在的属性的时候，就会被调用。
第二个函数是，则会接管所有对对象属性的访问：

```python
class User:
    def __init__(self, name):
        self.name = name

    def __getattribute__(self, item):
        return 'Disabled'

user = User('scott')
user.name
```

## 属性描述符和属性查找过程

假设你想要写一个数据库 ORM 类（将数据库的表结构映射成一个类），在这个类的设计中，你想要控制一些属性的数据类型，比如对于名字只能是 str 类型，对于年龄只能是 int 类型。

```python
import numbers

# 一个 int 类，实现了属性描述符协议，内部的值只能是 int
class IntField:
    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        if not isinstance(value, numbers.Integral):
            raise ValueError("Must be Int value")
        self.value = value

    def __delete__(self, instance):
        pass

# 使用 int 类作为 age 的 user 类
class User:
    age = IntField()

# 测试
user = User()
# all good
user.age = '10'
print(user.age)
# get error
user.age = 10
print(user.age)
```

在 `IntField` 中，它实现了 get 和 set，称为数据描述符；如果只实现了 get，则为非数据属性描述符。他们的属性查找过程是不一样的。

如果user是某个类的实例，使用 `user.age` （等于 `getattr(user,’age’)`），首先会调用`__getattribute__`, 如果在`__getattribute__`找不到属性就会抛出`AttributeError`。

如果类定义了`__getattr__`方法，在抛出`AttributeError`的时候就会调用到`__getattr__`；而对于描述符`__get__`的调用，则是发生在`__getattribute__`内部的。

举例来说 `user = User()`, 那么 user.age 顺序如下：

1. 如果“age”是出现在User或其基类的`__dict__`中，且 age 是 data descriptor，那么调用其`__get__`方法
2. 如果“age”出现在user(对象)的`__dict__`中， 那么直接返回 `obj.__dict__[‘age’]`
3. 如果“age”出现在User(类)或其基类的`__dict__`中
    - 如果age是non-data descriptor，那么调用其`__get__`方法
    - 返回`__dict__[‘age’]`
4. 如果User有`__getattr__`方法，调用`__getattr__`方法，否则
5. 抛出AttributeError

- 类的静态函数、类函数、普通函数、全局变量以及一些内置的属性都是放在类.__dict__里的
- 对象.__dict__中存储了一些self.xxx的一些东西

```python
import numbers

class IntField:
    #数据描述符
    def __get__(self, instance, owner):
        return self.value
    def __set__(self, instance, value):
        if not isinstance(value, numbers.Integral):
            raise ValueError("int value need")
        if value < 0:
            raise ValueError("positive value need")
        self.value = value
    def __delete__(self, instance):
        pass

class User:
    age = IntField()


if __name__ == "__main__":
    user = User()
    # user.age = 30           # 进入数据描述符的__set__
    # setattr(user, 'age',18) # 进入数据描述符的__get__
    # print(user.age)         # 进入数据描述符的__get__
    user.__dict__["age"] = 18
    print(user.__dict__["age"])

    user.__dict__["age"] = 18
    print(user.age)
    >>> 'IntField' object has no attribute 'value'
```

```python
class User:
    age = 1

if __name__ == "__main__":
    user = User()
    user.name = 30         # 保存在user对象的内存中
    print(user.name)       # 从user对象的内存中去取
    user.age = 30          # 保存在user对象的内存中, 不影响类的内存中的值
    print(user.age)       # 进入数据描述符的__get__
    user.__dict__["age"] = 18
    print(user.__dict__["age"])
    print (user.__dict__)
```

## 元类编程

首先来了解 init 和 new 的区别。

new 方法可以用来控制一个类的生成过程，init 则是在对象生成之后，对对象做一些操作。

init 调用是在 new 方法之后，其参数是实例，new 方法的参数是类。

如果 new 方法没有返回对象，则 init 方法不会调用。

然后，我们说的元类编程，什么是元类？元类是创建类的类，我们看下面一个动态创建类的例子：


```python
def create_class_by_class(name):
    """一个按需求定义类的例子
    :param name:
    :return:
    """
    if name == 'user':
        class User:
            def __str__(self):
                return 'user'
        return User

    if name == 'company':
        class Company:
            def __str__(self):
                return 'Company'
        return Company


def create_class_by_type(name):
    """动态的创建类：
    Python type(即元类)，里面可以创建类，关于 python
    type 如何创建类，以及其中的构造方法的用法，可以参考我之前写的文章。
    """
    # type 中第一个是要创建的类的名字，第二个是它的父类，第三个是类的属性
    # 这里没有给它设置父类，也没有属性
    User = type("User", (), {})
    user = User()
    print(user)

    # 加上一个 name 属性
    User = type("User", (), {"name": "user"})
    user = User()
    print(user.name)

    # 加方法
    def say(self):
        return "I am a func will bind to use"
    User = type("User", (), {"name": "user", "say": say})
    user = User()
    user_say = user.say()
    print(user_say)

    # 继承其他类
    class BaseClass:
        def answer(self):
            return "I am BaseClass"
    User = type("User", (BaseClass, ), {"name": "user", "say": say})


if __name__ == '__main__':
    create_class_by_type('')
```






## 元类编程实例 ORM

ORM 即一个数据库中表与 python 中类的一个映射关系，下面的代码实现了一个简单的 ORM 类：


```python
import numbers


class Field:
    """
    一个 IndField 和 CharField 的基类，用来在某些情况下方便
    我们判断传入的对象是 Field 或者它的子类
    """
    pass


class IntField(Field):
    """表示 Int 类型值的类
    """

    def __init__(self, db_column, min_value=None, max_value=None):
        """
        初始化一个 IntField
        :param db_column: pass
        :param min_value: 最小值
        :param max_value: 最大值
        """
        self._value = None
        self.min_value = min_value
        self.max_value = max_value
        self.db_column = db_column
        # 对值的大小与规定做检查
        if min_value is not None:
            if not isinstance(min_value, numbers.Integral):
                raise ValueError('min_value must be int')
            elif min_value < 0:
                raise ValueError('min value must be positive int')

        if max_value is not None:
            if not isinstance(max_value, numbers.Integral):
                raise ValueError('max_value must be int')
            elif max_value < 0:
                raise ValueError('max_value must be positive int')

        if min_value is not None and max_value is not None:
            if min_value > max_value:
                raise ValueError("min value must be smaller then maxvalue")

    def __get__(self, instance, owner):
        return self._value

    def __set___(self, instance, value):
        if not isinstance(value, numbers.Integral):
            raise ValueError('int value need')

        if value < 0:
            raise ValueError("positive value need")

        if value < self.min_value or value > self.max_value:
            raise ValueError("value must between min_value and max_value")

        self._value = value


class CharField(Field):
    """表示字符类型的类
    """

    def __init__(self, db_column, max_length=None):
        self._value = None
        self.db_column = db_column
        if max_length is None:
            raise ValueError("You must specific max_length for CharField")
        self.max_length = max_length

    def __get__(self, instance, owner):
        return self._value

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise ValueError("str value need")

        if len(value) > self.max_length:
            raise ValueError("value len > max_length")
        self._value = value


class ModelMetaClass(type):
    def __new__(cls, name, bases, attrs, **kwargs):
        """New 需要返回一个新的对象，解释下这里的参数：
           本来的参数是这么写的：def __new__(cls, *args, **kwargs):
           但因为我们知道 *args 会是什么参数，所以 *args 可以拆包成：
           name, bases, attrs
        """
        # name 是类的名字，所以这里可以知道是子类还是父类来到了 MetaClass
        # 如果是父类 BaseModel ，因为它没有 name, age 等属性描述符，直接
        # 让 type 去处理
        if name == 'BaseModel':
            return super().__new__(cls, name, bases, attrs, **kwargs)

        # 如果是子类 User，处理进来的参数
        fields = {}
        for key, value in attrs.items():
            if isinstance(value, Field):
                fields[key] = value

        # 比如子类的话应该有 Meta 类
        # 这里从 Meta 类中提取、注入信息
        attrs_meta = attrs.get("Meta", None)
        _meta = {}
        db_table = name.lower()

        if attrs_meta is not None:
            table = getattr(attrs_meta, "db_table", None)
            if table is not None:
                db_table = table
        _meta["db_table"] = db_table

        attrs["_meta"] = _meta
        attrs["fields"] = fields
        del attrs["Meta"]

        return super().__new__(cls, name, bases, attrs, **kwargs)


class BaseModel(metaclass=ModelMetaClass):
    """定义的一个 User 的父类，实现让使用者可以自定义初始化
       以及实现了子类通用的 save 方法
    """
    def __init__(self, *args, **kwargs):
        # 绑定属性到对象上，让使用者可以自定义初始化，如：
        # 子类 User 可以这样用，User(name='scott')
        for key, value in kwargs.items():
            setattr(self, key, value)
        return super().__init__()

    def save(self):
        """保存数据到数据库的方法
        """
        fields = []
        values = []
        for key, value in self.fields.items():
            db_column = value.db_column
            if db_column is None:
                db_column = key.lower()
            fields.append(db_column)
            value = getattr(self, key)
            values.append(str(value))

        sql = "insert {db_table}({fields}) value({values})".format(db_table=self._meta["db_table"],
                                                                   fields=",".join(fields), values=",".join(values))
        return sql


class User(BaseModel):
    # name，age 分别是利用属性描述符实现的字段，内部会对该属性做类型、范围检查
    name = CharField(db_column="name", max_length=10)
    age = IntField(db_column="age", min_value=0, max_value=100)

    # 单独的内部的类，定义关于表的信息
    class Meta:
        db_table = "user"


if __name__ == "__main__":
    user = User()
    # 如果属性的类型不对，报错
    user.name = "scott"
    user.age = 26
    print(user.save())
```

# 迭代器与迭代协议

将一个list转成迭代器：

```python
iter_rator = iter(a)
```

如果给一个类增加了 `__getitem__` 方法，则你可以对它使用 for 循环，这背后其实是使用了 `__iter__`，python 会自动创建一个 `__iter__` 实现它。

> getitem 的作用是切片，不要混淆。

你也可以自定义 `__iter__` 函数，但必须返一个 iteratle.

也可以通过继承 Iterator 来支持可迭代，这时候可以通过 `__next__` 来定制取值。

来看一个实现迭代器协议的例子：

```python
from collections.abc import Iterator

class Company(object):
    def __init__(self, employee_list):
        self.employee = employee_list

    # 可迭代对象中的__iter__返回迭代器
    def __iter__(self):
        return MyIterator(self.employee)

class MyIterator(Iterator):
    def __init__(self, employee_list):
        self.iter_list = employee_list
        self.index = 0 # 需要在内部维护一个取值位置

    # 继承了Iterator可以不写该方法, 如果重写那么return self
    # def __iter__(self):
    #     return self

    def __next__(self):
        #真正返回迭代值的逻辑
        try:
            word = self.iter_list[self.index]
        except IndexError:
            raise StopIteration # 抛出的异常应该是StopIteration
        self.index += 1
        return word
```

# 生成器函数

生成器可以返回*多次*值：

```python
# 函数
def func():
    return 1

# 生成器
def gen():
    yield 1
    yield 2
    yield 3
```

如果你研究过斐波拉契数列的实现，有一种办法是使用滑动数组：

```python
def list_fib(index):
    re_list = []
    n, cur_val, next_val = 0, 0, 1
    while n < index:
        re_list.append(next_val)
        cur_val, next_val = next_val, cur_val + next_val
        n += 1
    return re_list

list_fib(10)
```

这种办法可以改造成生成器实现：

```python
def gen_fib(index):
    n, cur_val, next_val = 0, 0, 1
    while n < index:
        # 为什么在这里 yield
        yield next_val
        pre_val, cur_val = cur_val, next_val
        next_val = pre_val + cur_val

for x in gen_fib(10):
    print(x)
```

理解生成器的原理非常重要，在理解生成器原理之前，先看看 python 中函数的工作原理，假设定义了以下函数：

```python
# forbar.py

def bar():
    pass

def foo():
    bar()
```

当你用 `python.exe` 调用 `forbar.py` 的时候， python 会用一个叫 `PyEval_EvalFramEx` 的 C 语言函数去执行。

在执行之前，会先创建一个栈帧（stackframe），实际上是一个上下文，也是一个对象。

然后，将所有已变成字节码对象的代码，放入栈帧。

> 可使用 dis 包查看字节码。

当上面 foo 调用 bar 的时候，又会创建一个新的栈帧。

所有栈帧都是分配在堆内存上，这就决定了栈帧可以独立于调用者存在。

详细的过程可以看下面的图：

![image.png](https://s2.loli.net/2022/01/14/31jKD8RZPWyOxvd.png)

那么生成器到底是怎么来的呢？它其实就是想 Python 的 frame 做了一个包装。
其中 `f_lasti` 会指向最近执行的代码，也就是执行到 yield 语句时，程序停下来的地方。

![image.png](https://s2.loli.net/2022/01/14/wxmMjKIOFLk627a.png)


