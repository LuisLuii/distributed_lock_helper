import threading
from datetime import datetime

from pebble import  ThreadPool

from distrilockper.misc.exceptions import CreateFutureTimeout

# why use process: https://docs.oracle.com/javase/1.5.0/docs/guide/misc/threadPrimitiveDeprecation.html
# docs https://pythonhosted.org/Pebble/
class LockPromise(ThreadPool):
    def __init__(self):
        super(LockPromise, self).__init__()
        self._event_flag = threading.Event()
        self._latch = None
        self._func = None

    def create_task(self, func, value):
        self._latch = value
        self._func = func

    def result(self, timeout):
        return self.result(timeout=timeout)

    def wait_future_running(self, wait_time, future):
        now = datetime.now().timestamp()
        while datetime.now().timestamp() - now < wait_time:
            if future.running():
                return True
        raise CreateFutureTimeout(f"future took longer than {wait_time} seconds too create")

    def wait(self, timeout):
        self.future = self.schedule(self._func, args=[self._event_flag, self._latch] )
        self.wait_future_running(wait_time=timeout, future=self.future)
        return self

    def stop(self):
        self._event_flag.set()

    def get_now(self):
        return self._latch
