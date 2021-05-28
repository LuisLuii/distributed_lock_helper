from distrilockper.pubsub.publish_subscribe import PublishSubscribe
from distrilockper import lock_entry
class LockPubSub(PublishSubscribe):
    def __init__(self):
        super().__init__()
        self.UNLOCK_MESSAGE = 0 ** 64
        self.LOCK_MESSAGE = 1 ** 64

    def create_entry(self, promise):
        return lock_entry.MyLockEntry(promise)

    def on_message(self):
        pass