import time
from threading import Lock, Thread


class LockedSet(set):
    """A set where add(), remove(), and 'in' operator are thread-safe"""

    def __init__(self, *args, **kwargs):
        self._lock = Lock()
        super(LockedSet, self).__init__(*args, **kwargs)

    def add(self, elem):
        with self._lock:
            super(LockedSet, self).add(elem)

    def remove(self, elem):
        with self._lock:
            return super(LockedSet, self).remove(elem)

    def __contains__(self, elem):
        with self._lock:
            super(LockedSet, self).__contains__(elem)

if __name__ == '__main__':

    if __name__ == '__main__':
        q = LockedSet()

        q.add(1)
        q.add(1)
        q.add(1)
        q.add(1)
        #print(q)
        q.remove(1)

        q.remove(1)

        q.remove(1)
        #print(q)