import asyncio
import asyncio_redis
from asyncio_redis.encoders import StringEncoder, BytesEncoder, BaseEncoder

from asyncio_redis.encoders import BytesEncoder, StringEncoder, UTF8Encoder


async def example():
    # Create Redis connection
    connection = await asyncio_redis.Connection.create(host='34.123.202.162', port=6379,encoder=UTF8Encoder())

    # Set a key
    # await connection.set('my_key', 'my_value')

    # set with lua script
    """
    Reentrant Lock 
    """
    reentrant_lock_code = """
                local ttl = tonumber(ARGV[1])
                if (redis.call('exists', KEYS[1]) == 0) then 
                    redis.call('hincrby', KEYS[1], ARGV[2], 1)
                    redis.call('pexpire', KEYS[1], ttl)
                    return nil
                    end
                if (redis.call('hexists', KEYS[1], ARGV[2]) == 1) then 
                    redis.call('hincrby', KEYS[1], ARGV[2], 1)
                    redis.call('pexpire', KEYS[1], ttl)
                    return nil
                    end
                return redis.call('pttl', KEYS[1])
                """
    multiply = await connection.register_script(reentrant_lock_code)
    should_none_because_there_is_no_lock_exist = await multiply.run(keys=["async_redis_lock_test3"],args=["100000","thread1:1"]) # s * 3
    should_ttl_because_there_is_lock_exist = await multiply.run(keys=["async_redis_lock_test3"],args=["100000","thread2:1"]) # s * 3
    # When finished, close the connection.
    result1 = await should_none_because_there_is_no_lock_exist.return_value()
    result2 = await should_ttl_because_there_is_lock_exist.return_value()
    # it should return None , because it is first to at the lock, and the thread is same, that is support reentrant lock
    ##print(result1)
    # it shoud return ttl
    ##print(result2)
    connection.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(example())