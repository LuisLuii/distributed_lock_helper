from threading import Thread, Event
import traceback

class Runnable(Thread):
    def __init__(self,func , *args , **kwargs):
        Thread.__init__(self)
        self._func = func
        self._args = args
        self._kwargs = kwargs
        self.task_done = False
        self.task_result = False
        self.task_exception = None

    def run(self):
        try:
            self.task_result = self._func(*self._args, **self._kwargs)
        except :
            traceback.print_exc()
            self.task_exception = traceback.format_exc()
        self.task_done = True

    def cancel(self):
        """Stop the timer if it hasn't finished yet"""
        self.finished.set()


if __name__ == '__main__':
    def run():
        import time
        time.sleep(5)
        #print("ok")
        a = 1 + 1


    runnable = Runnable(run)
    runnable.start()
    #print("done")