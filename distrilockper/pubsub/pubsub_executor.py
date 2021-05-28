import asyncio
import concurrent
import ctypes
import time
from pebble import concurrent

import redis


class PubSubThread():
    def __init__(self, connection, r, topic, promise, value):
        ##print("Initializing Async...")

        self._pub_sub_connection = connection.get_connection().pubsub()
        self.__topic = topic
        self._promise = promise
        self.task = self._promise.create_task(self.subscribe, value)
        # self.latch = value
        # except concurrent.futures.TimeoutError:

        # thread_executor_pool = concurrent.futures.ThreadPoolExecutor(max_workers=multiprocessing.cpu_count())
        # loop = event_loop
        # thread = threading.Thread(target=loop.run_forever)
        # thread.start()**

    # def subscribe(self):
    # self.latch.get_latch.acquire()
    # return self._sub_exec

    def unsubscribe(self):
        # self.latch.get_latch.release()
        self.task.interrupt()

    def _terminate_thread(self, thread):
        """Terminates a python thread from another thread.

        :param thread: a threading.Thread instance
        """
        if not thread.isAlive():
            return

        exc = ctypes.py_object(SystemExit)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
            ctypes.c_long(thread.ident), exc)
        if res == 0:
            raise ValueError("nonexistent thread id")
        elif res > 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

    def subscribe(self, stop, value):
        self._pub_sub_connection.subscribe(self.__topic)

        while not stop.is_set():
            time.sleep(1)
            pub_data = self._pub_sub_connection.get_message()
            if pub_data:
                if pub_data['data'] == '0' and pub_data['channel'] == self.__topic:
                    value.get_latch().release()
                    self._pub_sub_connection.unsubscribe()
        return


if __name__ == '__main__':
    import nest_asyncio

    nest_asyncio.apply()
    try:
        r = redis.Redis('127.0.0.1', decode_responses=True)
        loop = asyncio.get_event_loop()
        at = PubSubThread(loop, r, 'lock_helper__channel:{apple}')
        task = at.subscribe()
        ##print(task)
        ##print("--->", loop.run_until_complete(asyncio.wait_for(task, 3)))
        # loop.run_until_complete(asyncio.wait_for(task,3))

    except concurrent.futures._base.TimeoutError:
        at.unsubscribe()
        ##print("False")
