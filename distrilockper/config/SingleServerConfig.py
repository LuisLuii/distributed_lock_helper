class SingleServerConfig():
    def __init__(self):
        self.redis_config = None

    def set_config(self, **kwargs):
        """
            kwargs:

                :host:
                    Can be used to point to a startup node
                :port:
                    Can be used to point to a startup node
                :max_connections:
                    Maximum number of connections that should be kept open at one time
                :readonly_mode:
                    enable READONLY mode. You can read possibly stale data from slave.
                :skip_full_coverage_check:
                    Skips the check of cluster-require-full-coverage config, useful for clusters
                    without the CONFIG command (like aws)
                :nodemanager_follow_cluster:
                    The node manager will during initialization try the last set of nodes that
                    it was operating on. This will allow the client to drift along side the cluster
                    if the cluster nodes move around alot.
                :**kwargs:
                    Extra arguments that will be sent into Redis instance when created
                    (See Official redis-py doc for supported kwargs
                    [https://github.com/andymccurdy/redis-py/blob/master/redis/client.py])
                    Some kwargs is not supported and will raise RedisClusterException
                    - db (Redis do not support database SELECT in cluster mode)
                """

        self.__node = {**kwargs}

    @property
    def get_config(self):
        if not self.__node: raise ValueError("The config is empty")
        if "decode_responses" not in self.__node:
            self.__node['decode_responses'] = True
        return self.__node