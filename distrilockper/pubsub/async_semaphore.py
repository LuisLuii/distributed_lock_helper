import threading

from atomos.atomic import AtomicInteger

from distrilockper.util import Runnable
from distrilockper.util.count_down_latch import CountDownLatch
from threading import Lock

from distrilockper.util.thread_safe_queue import LockedQueue
from distrilockper.util.thread_safe_set import LockedSet

class AsyncSemaphore():
    def __init__(self, permits:int):
        self.counter = AtomicInteger(permits)
        self.lock = Lock
        self.listeners = LockedQueue()
        self.removedListeners = LockedSet()

    def try_acquire(self,timeout_milis):
        latch = CountDownLatch(1)
        def run():
            latch.count_down()
        self._acquire(Runnable(run))
        latch.await_count_down()


    def _acquire_uninterruptibly(self):
        latch = CountDownLatch(1)
        def runnable():
            latch.count_down()

        self._acquire(runnable)
        try:
            latch.await_count_down()
        except  :
            threading.current_thread()


    def _acquire(self, runnable : Runnable):
        run: bool = False
        with self.lock:
            if self.counter == 0:
                self.listeners.add(runnable)
                return
            if self.counter > 0:
                self.count -= 1
                run = True
        # self.__acquire_result(thread_runable, 1)

        if run :
            Runnable.start()

    # def __acquire_result(self,thread_runable, permits):
    #     run = False
    #     with self.lock:
    #         if self.counter < permits:
    #             self.listeners.add(Entry())



    """
     public void acquire(Runnable listener) {
        acquire(listener, 1);
    }
    
    """