from redis import Redis
from rediscluster import RedisCluster

from distrilockper.pubsub.async_semaphore import AsyncSemaphore


class BaseConnectionManager:
    def __init__(self):
        self.locks = [AsyncSemaphore(0) for i in range(50)]
        self.free_pub_sub_lock = AsyncSemaphore(0)
        for i in range(len(self.locks)):
            self.locks[i] = AsyncSemaphore(0)
        self.connection_instance = None

    def get_semaphore(self, channel_name: str) -> AsyncSemaphore:
        _ = self.locks[hash(channel_name) % len(self.locks)]
        return _

    def create_connection(self, config):
        if config.cluster_mode:
            self.connection_instance = RedisCluster(startup_nodes=config.get_node, decode_responses=True,
                                                    **config.get_config)
        else:
            self.connection_instance = Redis(**config.get_config)

    def get_connection(self):
        return self.connection_instance

    def lua_execute(self, lua_script, keys, args):
        script = self.connection_instance.register_script(lua_script)
        return script(keys, args)

