import asyncio
import threading
import time
from datetime import datetime

from pebble import ProcessPool, ThreadPool


def hello(*args):
    print("hello")
    time.sleep(6)
    print('slppy')

    print(*args)
def wait_future_running(wait, future):
    now = datetime.now().timestamp()
    while datetime.now().timestamp() - now < wait:
        if future.running():
            future
            return True
    return False
def run():
    with ThreadPool() as pool:
        future = pool.schedule(hello, args=[1])

        # if running, the container process will be terminated
        # a new process will be started consuming the next task
        wait_future_running(3, future)
        print(future.running())
        future.cancel()
def main():
    run()
main()
time.sleep(3)
print("okokoko")

time.sleep(300)
#
#
# class LockFuture(ProcessPool):
#     def __init__(self):
#         super(LockFuture, self).__init__()
#         self._event_flag = threading.Event()
#         self._latch = None
#         self._func = None
#
#     def create_task(self, func, value):
#         self._latch = value
#         self._func = func
#
#     def result(self, timeout):
#         return self.result(timeout=timeout)
#
#     def wait_future_running(self, wait_time, future):
#         now = datetime.now().timestamp()
#         while datetime.now().timestamp() - now < wait_time:
#             if future.running():
#                 return True
#         raise CreateFutureTimeout(f"future took longer than {wait_time} seconds too create")
#
#     def wait(self, timeout):
#         self.future = self.schedule(self._func(self._event_flag, self._latch))
#         self.wait_future_running(wait_time=timeout, future=self.future)
#         return self
#
#     def stop(self):
#         self._event_flag.set()
#
#     def get_now(self):
#         return self._latch
#
#     def hello(self):
#         print('hello')
#
# def test():
#
#     print('test')
#
# future = LockFuture()
# future.hello()
# future.wait(10)
# print("okokokoko")
