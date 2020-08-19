import functools

from rediscluster import RedisCluster, exceptions
from uuid import uuid1

from lock_helper.util.logger import logger_register
from src.lock_helper.expiration_factory import ExpirationFactory
import asyncio
import threading
from src.lock_helper.util import time_to_milisecond
from lock_helper.Executor.watch_dog_thread import WatchDog
from lock_helper.pubsub.lock_pub_sub import LockPubSub
from lock_helper.redis_object import RedisObject
import logging

logging.getLogger('lock_helper')

class HelperLock(object):  # should have a expire record instance

    def __init__(self, redis_instance, name):
        logger_register()
        input_parameter = locals()
        uuid = str(uuid1())
        self.__redis_instance = redis_instance
        self.__name = name
        self.__id = uuid
        self.entry_name = uuid + ":" + name
        self.__internal_lock_lease_time = 30
        self.__internal_lock_lease_unit = 's'
        self.EXPIRATION_RENEWAL_DICTIONARY = {}
        self.expiration_entry = ExpirationFactory()
        self.pubsub = LockPubSub()

    def lock_interruptibly(self, lease_time: int = -1, unit: str = None):
        ttl = self.__try_acquire(lease_time, unit)
        # success, and it is None if it is not expire and the value is same
        # it is a int if the lock is not us
        if not ttl:
            logging.info('get lock success')
            return True

        # thread_id = threading.current_thread().ident
        # self.__subscribe(thread_id)


    def lock(self, lease_time: int = -1, unit: str = None):
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
        # if lease_time is  -1 = no limit

        # try to get lock
        ttl = self.__try_acquire(lease_time, unit)
        if not ttl:
            logging.info("get lock successed")
            return True
        else:
            logging.info("get lock failed")
            return False

        #thread_id = threading.current_thread().ident

    def __try_acquire(self, expire_time, unit):
        future = self.__try_acquire_async(expire_time, unit, threading.current_thread().ident)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(future)
        a = future.result()
        return a

    def __subscribe(self, thread_id):
        return self.pubSub.subscribe(self.__get_lock_name(), self.__get_channel_name());

    def __get_channel_name(self):
        return RedisObject.prefix_name("redisson_lock__channel", self.getName());

    async def renew_inner_expiration_async(self):
        """
            for watchdog mode, update the lock
        :return:
        """
        script = '''if (redis.call('hexists', KEYS[1], ARGV[2]) == 1) then 
                        redis.call('pexpire', KEYS[1], ARGV[1]);  
                        return 1; 
                    end; 
                    return 0;
                    '''
        script = self.__redis_instance.register_script(script)
        return script(keys=[self.__name],
                      args=[time_to_milisecond(time=self.__internal_lock_lease_time,
                                               unit=self.__internal_lock_lease_unit),
                            self.__get_lock_name()])

    def __try_acquire_async(self, expire_time, unit, thread_id):
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
            task = asyncio.ensure_future(self.__try_lock_inner_async(expire_time, unit, thread_id))
            return task

        def done_cb(fut):
            if fut.exception():
                logging.error("raise the error when lock help at the watchdog mode trying to renew the expiration",
                              extra={'error_message':fut.exception()})
                return
            if not fut.result():
                self.schedle_expiration_renewal(thread_id)
                return

        future = asyncio.ensure_future(self.__try_lock_inner_async(self.__internal_lock_lease_time,
                                                                   self.__internal_lock_lease_unit,
                                                                   thread_id))
        future.add_done_callback(done_cb)
        return future

    async def __try_lock_inner_async(self, expire_time, unit, thread_id):
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
        script = '''
                            if (redis.call('exists', KEYS[1]) == 0) then 
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
                            '''
        script = self.__redis_instance.register_script(script)
        return script(keys=[self.__name],
                      args=[time_to_milisecond(time=expire_time, unit=unit), self.__get_lock_name(thread_id)])

    def schedle_expiration_renewal(self, thread_id):
        existing_thread_id = self.__get_lock_name()
        if existing_thread_id in self.EXPIRATION_RENEWAL_DICTIONARY.keys():
            old_entry = self.EXPIRATION_RENEWAL_DICTIONARY[existing_thread_id]
            old_entry.add_thread_id(thread_id)
        else:
            new_entry = ExpirationFactory()
            new_entry.add_thread_id(thread_id)
            self.EXPIRATION_RENEWAL_DICTIONARY[self.__get_lock_name()] = new_entry
            self.__renew_expiration()

    def __renew_expiration(self):
        ee = self.EXPIRATION_RENEWAL_DICTIONARY.get(self.__get_lock_name())
        if not ee:
            return
        timeout = WatchDog(self.__internal_lock_lease_time/3,self.__watch_dog_runner, args=[], kwargs={}).start()
        ee.set_timeout(timeout)


    def __watch_dog_runner(self):
        """
            如果一个场景：现在有A，B在执行业务，A加了分布式锁，
            但是生产环境是各种变化的，如果万一A锁超时了，但是A的业务还在跑。
            而这时由于A锁超时释放，B拿到锁，B执行业务逻辑。这样分布式锁就失去了意义？

            所以引入了watch dog的概念，当A获取到锁执行后，如果锁没过期，有个后台线程会自动延长锁的过期时间，
            防止因为业务没有执行完而锁过期的情况。
        :return:
        """
        ent = self.EXPIRATION_RENEWAL_DICTIONARY[self.__get_lock_name()]
        if not ent: return
        thread_id = ent.get_first_thread_id()
        if not thread_id: return
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(self.renew_inner_expiration_async())
        loop.run_until_complete(future)
        if future.exception():
            logging.error("Can't update lock " + self.__get_lock_name() + " expiration", future.exception())
        if future.result():
           self.__renew_expiration()


    def __get_lock_name(self, thread_id):
        return self.__id + ":" + str(thread_id)

