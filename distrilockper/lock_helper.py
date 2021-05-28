import uuid

import nest_asyncio

from distrilockper.config.config import Config
from distrilockper.connection.BaseConnectionManager import BaseConnectionManager
from distrilockper.util.reentrant_lock import RLock

nest_asyncio.apply()


class LockHelper(object):
    def __init__(self, watch_dog_run_interval: int = 30):
        self.connection_manager = None
        self.__id = str(uuid.uuid1())

    def create(self, config: Config = Config()):
        if not isinstance(config, Config):
            raise TypeError("Only support config instance")
        self.connection_manager = BaseConnectionManager()
        self.connection_manager.create_connection(config)

    def get_reentrant_lock(self, key: str):
        if not self.connection_manager:
            raise ValueError("Please user .create() with input key argument first")
        input_parameter = locals()
        param = {'name': key}
        lock_instance = RLock(**param, connection=self.connection_manager, id=self.__id)
        return lock_instance

    def get_fair_lock(self, key: str):
        pass
