import time
from queue import Queue
from threading import Lock, Thread


class LockedQueue(Queue):

    def __init__(self, *args, **kwargs):
        self._lock = Lock()
        self.queue = super().__init__()
        super(LockedQueue, self).__init__(*args, **kwargs)

    def size(self):
        with self._lock:
            return super(LockedQueue, self).qsize()

    def add(self,value):
        super(LockedQueue, self).put(value)
    def peek(self):
        with self._lock:
            if self.queue:
                return self.queue[0]
            return None

    def clear(self):
        with self._lock:
            self.queue.clear()

    def get(self):
        return super(LockedQueue, self).get()

if __name__ == '__main__':
    q = LockedQueue()
    a = 0
    def produce():
        for i in range(1000000):
            q.add(i)
            time.sleep(0.0001)

    def consume():
        for i in range(1000000):
            _ = q.get()
            #print(_)
            time.sleep(0.0001)

    Thread(target=produce).start()
    Thread(target=consume).start()
    Thread(target=consume).start()