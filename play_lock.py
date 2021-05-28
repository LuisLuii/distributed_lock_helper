import time
from threading import Thread


if __name__ == '__main__':
from distrilockper import Config
from distrilockper import LockHelper
from multiprocessing.dummy import Pool as ThreadPool

config = Config()
config.use_single_server().set_config(host='0.0.0.0', port=6379)

helper = LockHelper()
helper.create(config)

for i in range(10):
    Locker1 = helper.get_reentrant_lock(key='apples')
    re1 = Locker1.try_lock(60, 10, 'second')
    assert re1 == True
    print("get lock", re1)
    assert Locker1.is_exists() == True
    print('exists', Locker1.is_exists())

