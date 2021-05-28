import threading

from collections import deque


class MyLockEntry:
    def __init__(self, promise):
        self._counter: int = 0
        self._latch: threading.Semaphore = threading.Semaphore(0)

        self._listeners: deque = deque()
        self._promise = promise

    def acquire(self):
        self._counter += 1

    def release(self):
        self._counter -= 1

    def get_promise(self):
        return self._promise

    def add_listener(self, listener):
        self._listeners.append(listener)

    def remove_listener(self, listener):
        self._listeners.remove(listener)

    def get_listeners(self) -> deque:
        return self._listeners

    def get_latch(self) -> threading.Semaphore:
        return self._latch
