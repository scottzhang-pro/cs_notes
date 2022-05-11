from calendar import c
import threading
import time

class HtmlSpider(threading.Thread):
    """HTML 爬取模拟器。

    Args:
        threading (Thread): 继承自线程类，每个 URL 有一个线程处理
    """
    def __init__(self, url, sem):
        super().__init__()
        self.url = url
        self.sem = sem

    def run(self):
        time.sleep(2)
        print(f"{self.url} finished.")
        # 处理完成后，释放该锁
        self.sem.release()


class UrlMaker(threading.Thread):
    def __init__(self, sem):
        super().__init__()
        self.sem = sem

    def run(self):
        # 这里有 100 URL 需要处理，但是同时并发这么多请求会报错
        # 可以通过 semaphore 限制并发的数量来控制
        for i in range(100):
            # 一把 sem 锁，最多进入10个线程
            self.sem.acquire()
            html_sider = HtmlSpider(f"http:/scottzhang.pro/{i}", self.sem)
            html_sider.start()



if __name__ == '__main__':
    sem = threading.Semaphore(10)  # 控制并发数量为 10 个
    url_maker = UrlMaker(sem)
    url_maker.start()