# 什么是对象？

一般来说，对象指的是拥有数据（或属性）和操作数据的方法的一个实体。

不同的编程语言对它的定义不一样，有的编程语言规定对象必须有属性和方法，有的编程语言则规定对象必须是subclassable 的（暂时没想到中文），Python 的定义则比较宽松，因为 Python 中不要求对象一定要有数据或方法，也不要求对象是 subclassable 的。


# 一切皆对象

在其他的静态语言中，有对象和类，对象是类的一个实例，但是在 Python 中，这两者都是对象。

“Python 中一切皆对象”这句话，它的意思暗示了在 Python 中，所有元素都是对象，string, list, 函数、类甚至是模块都是对象，属于 Python 的一等公民，这意味着它可以：

- 被赋值给一个变量
- 可以添加到集合对象中
- 可以作为参数传递给函数
- 可以当作函数的返回值

这就提供了一种动态性，你可以在运行的时候修改它。

对象的三个特征：身份(内存中的地址)、类型（1 是 int 类型）、值（a=1 中的1）。

# 以 list 为例

对象有数据和方法：

```python
# x 是一个对象
x = 1

# type 可以告诉我们变量属于什么对象
# output: int
type(x)

# 查看 x 对象的一个属性
# 对于 Int 类型，它有 Real and imaginary part of the value
# if viewed as a complex number
print(x.real)
print(x.imag)

# 查看 x 对象的一个方法
print(x.is_integer())

# 我们说一切皆对象，真的就是所有都是对象
# 比如 x.is_interger 这个方法本身，也是对象
# output: builtin_function_or_method
type(x.is_interger)

```

# 参考

- [How everything in Python is an Object?](https://www.codingninjas.com/blog/2020/08/27/how-everything-in-python-is-an-object/)