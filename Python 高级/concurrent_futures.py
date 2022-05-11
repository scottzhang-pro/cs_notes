import logging
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
import time

def thread_function(name):
    """模拟某个函数的执行"""
    logging.info("Thread %s: starting", name)
    time.sleep(2)
    logging.info("Thread %s: finishing", name)


def start_thread_1():
    logging.info("# Start thread with method 1")
    executor = ThreadPoolExecutor(max_workers=2)
    task1 = executor.submit(thread_function, ('A thread'))
    task2 = executor.submit(thread_function, ('B thread'))
    task3 = executor.submit(thread_function, ('C thread'))
    # 查看是否成功，返回结果
    print(f"Task 1 status: {task1.done()}")
    # 取消某个任务(还未执行)
    print(f"Cancel task 3: {task3.cancel()}")


def start_thread_2(names):
    logging.info("# Start thread with method 2")
    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(thread_function, names)


def start_thread_3(names):
    logging.info("# Start thread with method 3")
    executor = ThreadPoolExecutor(max_workers=2)

    all_tasks = [
        executor.submit(thread_function, (x)) for x in names
    ]
    for future in as_completed(all_tasks):
        data = future.result()

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    names = ['A thread', 'B thread', 'C thread']

    start_thread_1()
    start_thread_2(names)
    start_thread_3(names)
