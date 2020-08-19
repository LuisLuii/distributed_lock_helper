from threading import Condition

# ref https://blog.csdn.net/hxpjava1/article/details/54344182
class CountDownLatch:
    def __init__(self, count):
        self.count = count
        self.condition = Condition()

    def wait(self):
        try:
            self.condition.acquire()
            while self.count > 0:
                self.condition.wait()
        finally:
            self.condition.release()

    def countDown(self):
        try:
            self.condition.acquire()
            self.count -= 1
            self.condition.notifyAll()
        finally:
            self.condition.release()
