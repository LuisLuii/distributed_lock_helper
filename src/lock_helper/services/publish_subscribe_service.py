import threading

class PublishSubscribeService():
    def __init__(self):
        freePubSubLock = threading.Semaphore(0)