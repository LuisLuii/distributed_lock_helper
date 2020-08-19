from lock_helper.util.count_down_latch import CountDownLatch
from threading import Lock, Thread

class Entry():
    def __init__(self,thread_runable, permits):
        self.thread_runable = thread_runable
        self.permits = permits

    @property
    def get_permits(self):
        return self.permits

    @property
    def get_permits(self):
        return self.thread_runable

    def hashCode(self):
        prime = 31
        result = 1
        result = prime * result + (lambda x : 0 if  x == None else self.thread_runable + 1)

class AsyncSemaphore():
    def __init__(self, permits:int):
        self.counter = permits
        self.lock = Lock
        self.listeners = set()

    def try_acquire(self,timeout_milis):
        latch = CountDownLatch(1)


    def __acquire_(self, thread_runable):
        self.__acquire_result(thread_runable, 1)

    def __acquire_result(self,thread_runable, permits):
        run = False
        with self.lock:
            if self.counter < permits:
                self.listeners.add(Entry())



    """
     public void acquire(Runnable listener) {
        acquire(listener, 1);
    }
    
    """