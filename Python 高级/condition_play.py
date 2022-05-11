from asyncio import as_completed
import threading
from threading import Condition

class A(threading.Thread):
    def __init__(self, cond):
        super().__init__(name='A')
        self.cond = cond
    def run(self):
        # notify 和 wait，必须在 with 语句中
        with self.cond:
            print(f"{self.name}, 1") # A先处理自己的逻辑
            self.cond.notify()       # 通知调用 wait 的方法启动
            self.cond.wait()         # 等待某个变量的通知

            print(f"{self.name}, 3")
            self.cond.notify()
            self.cond.wait()


class B(threading.Thread):
    def __init__(self, cond):
        super().__init__(name='B')
        self.cond = cond

    def run(self):
        # notify 和 wait，必须在 with 语句中
        with self.cond:
            self.cond.wait()        # B顺序在后，所以先等待
            print(f"{self.name} 2") # B再处理自己的逻辑
            self.cond.notify()      # 再通知 A

            self.cond.wait()
            print(f"{self.name} 4")
            self.cond.notify()


if __name__ == '__main__':
    cond = Condition()

    a = A(cond)
    b = B(cond)

    # 启动顺序很重要，在这里如果 a 启动，那么 a 首先处理自己的代码
    # 随后发送 notify，但这个时候会出问题，因为 b 还没有启动起来
    # 所有正确的方式是先让 b 起来等待，再启动 a
    b.start()
    a.start()
