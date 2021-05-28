import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed, wait
import time
from concurrent.futures._base import ALL_COMPLETED
class Task:
    def __init__(self, max_number):
        self.max_number = max_number
        self.interrupt_requested = False

    def __call__(self):
        # ##print("Started:", datetime.datetime.now(), self.max_number)
        last_number = 0;
        for i in range(1, self.max_number + 1):
            if self.interrupt_requested:
                # ##print("Interrupted at", i)
                break
            last_number = i * i
        # ##print("Reached the end")
        return last_number

    def interrupt(self):
        self.interrupt_requested = True

def boo(stop):
    a = "okok"
    time.sleep(3)
    if not stop:
        ##print(a)
        return a
class LockPromise:
    def create_task(self,func, **kwargs):
        self._stop = False
        self.thread_exec = ThreadPoolExecutor(max_workers=1)
        task = self.thread_exec.submit(func,self._stop, **kwargs)
        return task
    def stop(self):
        self.stop = True

def task_done_func(obj):
    print('task is done', obj.result())
LP = LockPromise()
task = LP.create_task(boo)
##print(task.cancelled())
##print(task.add_done_callback(task_done_func))
##print('---.')
LP.stop()
import time
#
# async def boo(fut):
#     ##print("hello")
#     fut.set_result("complete")
#
# async def foo():
#
#     loop = asyncio.get_event_loop()
#     fut = loop.create_future()
#     loop.create_task(boo(fut))
#
#     time.sleep(2)
#     await fut
#     ##print(fut.done())
# asyncio.run(foo())

# def test(num):
#     import time
#     time.sleep(2)
#     return time.ctime(), num
#
#
# executor = futures.ThreadPoolExecutor(max_workers=1)
# future = executor.submit(test, 1)
#
# ##print(future.cancelled())
# ##print(future.result())
#
# ##print(future.cancel())
# ##print(future.cancelled())
# ##print(future.running())
# executor.shutdown()
# #
# class LockPromise(futures.ThreadPoolExecutor):
#     def __init__(self,):
#         super(LockPromise, self).__init__(max_workers=1)
#         self.thread_executor = super(LockPromise, self)
#         self.can_cancel = True
#
#
#     def set_uncancellable(self):
#         self.connection = False
#
#     def cancel(self):
#         if self.can_cancel:
#             return super(LockPromise, self).cancel()
#         else:
#             return False
#
#     def add_complete_callback(self, func , *args, **kwargs):
#         super(LockPromise, self).add_complete_callback(func(*args, **kwargs))
#
# _ = LockPromise()
# ##print()
