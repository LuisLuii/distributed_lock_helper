import concurrent
import logging
import math
import threading
import time
import uuid
from uuid import uuid1

from distrilockper.util.redis_object import RedisObject
from multipledispatch import dispatch

from distrilockper.Executor.watch_dog_thread import WatchDog
from distrilockper.connection.BaseConnectionManager import BaseConnectionManager
from distrilockper.pubsub.lock_pub_sub import LockPubSub
from distrilockper.expiration_factory import ExpirationFactory
from distrilockper.util import time_to_milisecond, time_to_unit

logging.getLogger('lock_helper')


class RLock(LockPubSub):
    def __init__(self, connection: BaseConnectionManager, name: str, id: uuid):
        """

        :param connection: use BaseConnectionManager to create redis connection instance
        :param name: the name of lock
        :param id: uuid, use the uuid and the thread id as the key of redis
        """
        super().__init__()
        input_parameter = locals()
        self._connection = connection
        self.__name = name
        self.__id = id
        self.entry_name = str(uuid1()) + ":" + name
        self.EXPIRATION_RENEWAL_DICTIONARY = {}
        self.expiration_entry = ExpirationFactory()
        self._lock_lease_time = 0
        self._lock_lease_unit = 's'
        self._internal_lock_lease_time = 30
        self._internal_lock_lease_unit = 's'
        self.pubsub = LockPubSub()

    @dispatch(int, str, bool)
    def lock(self, lease_time: int, unit: str, interruptibly: bool):
        # thread_id = threading.current_thread().ident
        # ttl = self._try_acquire(lease_time, unit, thread_id)
        # if ttl:
        #     subscribe_future = self._subscribe(thread_id)
        #     if interruptibly:
        #         pass
        raise NotImplementedError

    @dispatch(int, str)
    def lock(self, lease_time: int, unit: str):
        """
            using this method to doing lock operation
            lease_time default is -1,
                -- -1 for enable watch dog mode, keep update the lock until u doing unlock
                -- more than 0 for set as the remaining time of your lock
            unit is the time unit
        :param lease_time:
        :param unit: second / milisecond
        :return:
        """
        # # if lease_time is  -1 = no limit
        # thread_id = threading.current_thread().ident
        #
        # # try to get lock
        # ttl = self._try_acquire(lease_time, unit,thread_id)
        # if not ttl:
        #     logging.info("get lock success")
        #     return True
        # else:
        #     logging.info("get lock failed")
        #     return False
        #
        # # thread_id = threading.current_thread().ident
        raise NotImplementedError

    @dispatch()
    def lock(self):
        pass
        # try:
        #     self.lock(-1, None, False)
        # except InterruptedException as e:
        #     raise Exception(e)
        raise NotImplementedError

    @dispatch(int, int, str)
    def try_lock(self, wait_time: int, lease_time: int, time_unit: str) -> bool:
        '''

        :param wait_time: lock operation time out it is milliseconds
        :param lease_time: the release time of the lock
        :param time_unit: unit of lease_time and wait_time; support:seconds, s, hour, h, minute, m, milliseconds, ms
        :return: False as get lock success otherwise true
        '''
        assert time_unit in ['second', 's', 'hour', 'h', 'minute', 'm', 'milliseconds',
                             'ms'], f'unsupported unit: {time_unit}; Only support: seconds, s, hour, h, minute, m, milliseconds, ms '
        wait_time = time_to_unit(wait_time, time_unit)
        current = time.time()

        thread_id = threading.current_thread().ident
        ttl = self._try_acquire(lease_time, time_unit, thread_id)
        if ttl is None: return True
        wait_time -= time.time() - current
        if wait_time <= 0:
            # acquire_failed(wait_time, unit, thread_id)
            return False

        current = time.time()
        subscribe_future = self._subscribe(thread_id)
        # if subscription not success
        if not subscribe_future.wait(wait_time):
            # if cancel not success
            if not subscribe_future.cancel():
                pass
            return False
        future_result = None
        try:
            future_result = subscribe_future.wait(wait_time)
        except concurrent.futures._base.TimeoutError as e:
            self._unsubscribe(subscribe_future, thread_id)
        # unsubscribe the future if timeout
        if not future_result:
            self._unsubscribe(subscribe_future, thread_id)
            return False
        else:
            var14: bool = False
            try:
                wait_time -= time.time() - current
                if wait_time > 0:
                    var16: bool = False
                    while wait_time > 0:
                        current = time.time()
                        ttl = self._acquire_async(lease_time, time_unit, thread_id)

                        if ttl is None:
                            var16 = True
                            return var16

                        wait_time -= time.time() - current
                        # print("condition", wait_time)
                        if wait_time <= 0:
                            var16 = False
                            return var16
                        current = time.time()
                        ttl = ttl / 1000
                        if ttl >= 0 and ttl < wait_time:
                            # print(wait_time)
                            # print("wait for ttl", ttl)
                            subscribe_future.get_now().get_latch().acquire(timeout=math.ceil(ttl))
                        else:
                            # print("wait for max wait time")
                            subscribe_future.get_now().get_latch().acquire(timeout=math.ceil(wait_time))
                        # print("expired , try again")
                        # print('ttl', ttl)
                        # print('wait time', wait_time)
                        wait_time -= time.time() - current
                        # print("final", wait_time)
                    var16 = False
                    return var16
                var14 = False
            except Exception as e:
                logging.exception("raise exception while get the key", extra={"error_message": str(e)})
            finally:
                subscribe_future.stop()

            return var14


    @dispatch(int, str)
    def try_lock(self, wait_time_: int, time_unit: str):
        return self.try_lock(wait_time_, -1, time_unit)

    def _acquire_async(self, lease_time, unit, thread_id):
        return self._try_acquire(lease_time, unit, thread_id)

    def unlock(self):
        '''
        :return:
            None: the lock of current thread is not found
            1   : unlock success, all lock is unlocked
            0   : unlock success, there is other lock and the expire time is renew
        '''
        return self._unlock()

    def _unlock(self):
        res = self._unlock_inner(threading.current_thread().ident)
        return res

    def _unlock_inner(self, thread_id: str):
        return self._connection.lua_execute( \
            # if the thread of lease and thread of lock is not the same thread, return nulll
            '''
             if (redis.call('hexists', KEYS[1], ARGV[3]) == 0) then 
                 return nil;
             end;
             '''
            +
            # use decreasing one by hincrby to lease one lock and renew the expire time if the remaining time is more than one
            # publish the message if the lock has been leased
            '''
             local counter = redis.call('hincrby', KEYS[1], ARGV[3], -1);
             if (counter > 0) then
                 redis.call('pexpire', KEYS[1], ARGV[2]);
                 return 0;
             else 
                 redis.call('del', KEYS[1]);
                 redis.call('publish', KEYS[2], ARGV[1]);
                 return 1;
             end;
             return nil;
                     ''',
            keys=[self.__name, self._get_channel_name()],
            args=[self.UNLOCK_MESSAGE,
                  time_to_milisecond(time=self._lock_lease_time, unit=self._lock_lease_unit),
                  self._get_lock_name(thread_id)]
        )

    def _try_acquire(self, expire_time, unit, thread_id):
        """
            using this method to doing lock operation
            lease_time default is -1,
                -- -1 for enable watch dog mode, keep update the lock until u doing unlock
                -- more than 0 for set as the remaining time of your lock
            unit is the time unit
        :param lease_time:
        :param unit: second / milisecond
        :return:
        """
        return self._try_acquire(expire_time, unit, thread_id)

    def is_exists(self):
        return self._connection.get_connection().exists(self.__name)

    def _subscribe(self, thread_id):
        # return self.pubsub.subscribe(self.__get_lock_name(thread_id), self.__get_channel_name(), self._connection,
        #                              loop);
        return self.pubsub.subscribe(self._get_lock_name(thread_id), self._get_channel_name(),
                                     connection=self._connection)

    def _unsubscribe(self, future, thread_id):
        # TODO
        pass

    def _get_channel_name(self):
        return RedisObject.prefix_name(prefix="lock_helper__channel", name=self.__name);

    def _renew_inner_expiration(self, thread_id):
        """
            for watchdog mode, update the lock
        :return:
        """
        return self._connection.lua_execute('''if (redis.call('hexists', KEYS[1], ARGV[2]) == 1) then 
                                                    redis.call('pexpire', KEYS[1], ARGV[1]);  
                                                    return 1; 
                                                end; 
                                                return 0;
                                                             ''',
                                            keys=[self.__name],
                                            args=[time_to_milisecond(time=self._internal_lock_lease_time,
                                                                     unit=self._internal_lock_lease_unit),
                                                  self._get_lock_name(thread_id)]
                                            )

    def _try_acquire(self, expire_time, unit, thread_id):
        """
            if expire_time not -1, it will set the lock will specific time to be expired
            if expire time is -1, it will set the expire time and unit with the internal lock lease time and unit,
                and update the lock very 10s until the unlock method be call.
                there is are callback
        :param expire_time int: the expire time for when the lock will be expired
        :param unit str: the unit of expire time
        :param thread_id: your existing thread id
        :return: future object
        """
        if expire_time != -1:
            task = self._try_lock_inner(expire_time, unit, thread_id)
            return task
        try:
            print(self._try_lock_inner(self._internal_lock_lease_time,
                                       self._internal_lock_lease_unit,
                                       thread_id))
            self.schedule_expiration_renewal(thread_id)

        except Exception as e:
            logging.error("raise the error when lock help at the watchdog mode trying to renew the expiration",
                          extra={'error_message': str(e)})
            return False

    def _try_lock_inner(self, expire_time, unit, thread_id):
        """
            async method for lock the key
            execute the redis script on the method

            KEYS[1] ：“your key name”
            ARGV[2] ：“id + ":" + threadId”

            using the "exists" to condition the key whether exists. i will be 0 if not exist and exec the "hset" command
            store the "your key name   id:threadID 1" to redis.
            it should be looked like:
                "8743c9c0-0795-4907-87fd-6c719a6b4586:thread_id":1

            the lock is able to re-lock , the 1 mean how many time you lock, if you lock 5 time ,
            that will be 5, and you have to unlock 5 time to unlock successfully

        :param expire_time:
        :param unit:
        :param thread_id:
        :return:
        """
        self._lock_lease_time = expire_time
        self._lock_lease_unit = unit
        return self._connection.lua_execute('''if (redis.call('exists', KEYS[1]) == 0) then 
                                redis.call('hincrby', KEYS[1], ARGV[2], 1)
                                redis.call('pexpire', KEYS[1], ARGV[1])  
                                return nil
                                end
                            if (redis.call('hexists', KEYS[1], ARGV[2]) == 1) then 
                                redis.call('hincrby', KEYS[1], ARGV[2], 1)
                                redis.call('pexpire', KEYS[1], ARGV[1])
                                return nil
                                end
                            return redis.call('pttl', KEYS[1])
                                                                     ''',
                                            keys=[self.__name],
                                            args=[time_to_milisecond(time=expire_time, unit=unit),
                                                  self._get_lock_name(thread_id)]
                                            )

    def schedule_expiration_renewal(self, thread_id):
        existing_thread_id = self._get_lock_name(thread_id)
        if existing_thread_id in self.EXPIRATION_RENEWAL_DICTIONARY.keys():
            old_entry = self.EXPIRATION_RENEWAL_DICTIONARY[existing_thread_id]
            old_entry.add_thread_id(thread_id)
            self.EXPIRATION_RENEWAL_DICTIONARY[existing_thread_id] = old_entry
        else:
            new_entry = ExpirationFactory()
            new_entry.add_thread_id(thread_id)
            self.EXPIRATION_RENEWAL_DICTIONARY[existing_thread_id] = new_entry
            self._renew_expiration(thread_id)

    def _renew_expiration(self, thread_id):
        ee = self.EXPIRATION_RENEWAL_DICTIONARY.get(self._get_lock_name(thread_id))
        if not ee:
            return
        print(self._internal_lock_lease_time)
        timeout = WatchDog(self._internal_lock_lease_time / 3, self._watch_dog_runner,
                           kwargs={"thread_id": thread_id}).start()
        ee.set_timeout(timeout)
        self.EXPIRATION_RENEWAL_DICTIONARY[self._get_lock_name(thread_id)] = ee

    def _watch_dog_runner(self, thread_id):
        ent = self.EXPIRATION_RENEWAL_DICTIONARY[self._get_lock_name(thread_id)]
        if not ent: return
        thread_id_count = ent.get_first_thread_id()
        if not thread_id_count: return
        try:
            return self._renew_inner_expiration(thread_id)
        except Exception as e:
            logging.error("Can't update lock " + self._get_lock_name(thread_id) + " expiration", e.exception())
            raise e

    def _get_lock_name(self, thread_id):
        return self.__id + ":" + str(thread_id)
