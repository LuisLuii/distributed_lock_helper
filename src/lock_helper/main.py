from lock_helper.config.config import Config
from lock_helper.util.helper_lock import HelperLock
from rediscluster import RedisCluster , exceptions
import redis

class DistributerLockHelper(object):
    def __init__(self):
        self.redis_instance = None
        pass

    def create(self, config: Config = Config()):
        if not isinstance(config,Config):
            raise TypeError("Only support config instance")

        if config.mode:
            self.redis_instance = RedisCluster(startup_nodes=config.get_node,decode_responses=True)


    def get_lock(self, key: str):
        if not self.redis_instance:
            raise ValueError("Please user .create() with input key argument first")
        input_parameter = locals()
        param = {'name': key}
        # self.redis_instance.set(**param)
        lock_instance = HelperLock(**param, redis_instance=self.redis_instance)
        return lock_instance

if __name__ == '__main__':
    from src.lock_helper.config.config import Config

    config = Config()
    config.use_cluster_servers().add_node_address(host='0.0.0.0', port=7000) \
                                .add_node_address(host='0.0.0.0', port=7001) \
                                .add_node_address(host='0.0.0.0', port=7002) \
                                .add_node_address(host='0.0.0.0', port=7003) \
                                .add_node_address(host='0.0.0.0', port=7004) \
                                .add_node_address(host='0.0.0.0', port=7005)
    helper = DistributerLockHelper()
    helper.create(config)
    # helper.eval()
    Locker = helper.get_lock(key='apple')
    Locker.lock(50, 'second')
    Locker.lock(50, 'second')
    Locker.lock(50, 'second')
    Locker.lock(50, 'second')

    import time
    for i in range(0,1000000000000000):
        pass

#