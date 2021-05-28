from threading import Thread, Event

class WatchDog(Thread):
    """Call a function after a specified number of seconds:
              t = WatchDog(30.0, f, args=[], kwargs={})
              t.start()
              t.cancel() # stop the timer's action if it's still waiting
      """

    def __init__(self, interval, function, args=[], kwargs={}):
        Thread.__init__(self)
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.finished = Event()

    def cancel(self):
        """Stop the timer if it hasn't finished yet"""
        self.finished.set()

    def run(self):
        while not self.finished.is_set():
            locked = self.function(*self.args, **self.kwargs)
            if not locked:
                self.cancel()
            else:
                self.finished.wait(self.interval)
