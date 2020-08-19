from rediscluster import RedisCluster
from typing import Type  # you have to import Type

def redis(arg: Type[RedisCluster]):
    pass

def redis():
    redis_instance : RedisCluster