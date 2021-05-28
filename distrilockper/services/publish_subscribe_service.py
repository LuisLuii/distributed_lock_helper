import threading


class PublishSubscribeService():
    def __init__(self):
        freePubSubLock = threading.Semaphore(0)
        self.__name2PubSubConnection = {}
        locks = [0] * 50
        sem = threading.Semaphore()
        # freePubSubLock.acquire()

    def __subscribe_runner(self, method_instance):
        pass
