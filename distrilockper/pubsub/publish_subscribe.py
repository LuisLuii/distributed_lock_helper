from distrilockper.misc.lock_promisc import LockPromise
from distrilockper.util.lock_entry import MyLockEntry
from distrilockper.pubsub.pubsub_executor import PubSubThread
from distrilockper.util.Runnable import Runnable
from distrilockper.services.publish_subscribe_service import PublishSubscribeService

import threading


class PublishSubscribe():
    def __init__(self):
        self.service = PublishSubscribeService()
        self.entries = {}
        self.entries_thread_safe_lock = threading.Lock()
        self.semaphore = None
        self.promise = None

    def subscribe(self, entry_name: str, channel_name: str, connection):
        # listener_holder: ListenerHolder = ListenerHolder()
        self.semaphore = connection.get_semaphore(channel_name)
        new_promise = LockPromise()

        def run(semaphore, connection, channel_name, entry_name, new_promise):
            entry = self.entries.get(entry_name, None)
            if entry is not None:
                entry.acquire()
                semaphore.release()
                entry.get_promise().add_complete_callback()

            value = MyLockEntry(new_promise)
            value.acquire()

            if entry_name in self.entries:
                old_value = self.entries[entry_name]
            else:
                self.entries[entry_name] = value
                old_value = None

            if old_value is not None:
                old_value.acquire()
                semaphore.release()
                old_value.get_promise().add_complete_callback()
                return
            else:
                PubSubThread(connection, self.semaphore, channel_name,new_promise, value)

        Runnable(run, self.semaphore, connection, channel_name, entry_name, new_promise).run()
        self.promise = new_promise
        return new_promise

    def unsubscribe(self, entry, entry_name, channel_name):
        self.semaphore.acquire()
        if not entry.release():
            removed = self.entries.pop(entry_name) == entry
            if not removed:
                print("error, can not remove")
            else:
                self.promise.stop()
        else:
            entry.release()


    """
    

    public RFuture<E> subscribe(String entryName, String channelName) {
        AtomicReference<Runnable> listenerHolder = new AtomicReference<Runnable>();
        AsyncSemaphore semaphore = service.getSemaphore(new ChannelName(channelName));
        RPromise<E> newPromise = new RedissonPromise<E>() {
            @Override
            public boolean cancel(boolean mayInterruptIfRunning) {
                return semaphore.remove(listenerHolder.get());
            }
        };

        Runnable listener = new Runnable() {

            @Override
            public void run() {
                E entry = entries.get(entryName);
                if (entry != null) {
                    entry.acquire();
                    semaphore.release();
                    entry.getPromise().onComplete(new TransferListener<E>(newPromise));
                    return;
                }
                
                E value = createEntry(newPromise);
                value.acquire();
                
                E oldValue = entries.putIfAbsent(entryName, value);
                if (oldValue != null) {
                    oldValue.acquire();
                    semaphore.release();
                    oldValue.getPromise().onComplete(new TransferListener<E>(newPromise));
                    return;
                }
                
                RedisPubSubListener<Object> listener = createListener(channelName, value);
                service.subscribe(LongCodec.INSTANCE, channelName, semaphore, listener);
            }
        };


        semaphore.acquire(listener);
        listenerHolder.set(listener);
        
        return newPromise;
    }

    """
