from lock_helper import exception



class ClusterServersConfig(object):
    def __init__(self):
        self.__node: list = []
        self.config = {}

    def add_node_address(self, host: str = None, port: int = None) -> 'ClusterServersConfig':
        """
        Add Redis cluster node address.
        :param host:
        :param port:
        :return: ClusterServersConfig()
        """
        if not host or not port:
            raise exception.ArgumentError("Both argument of host and port are required: "
                                          "host should be a str type; "
                                          "port should be a int type")
        #print(f'{host},{port}')
        self.__node.append({'host': host, 'port': port})
        return self

    def add_config(self, **kwargs):
        """
            kwargs:
                :startup_nodes:
                    List of nodes that initial bootstrapping can be done from
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
        self.config = kwargs

    @property
    def get_node(self):
        if not self.__node:
            return {'host': '127.0.0.1', 'port': 6379}
        return self.__node
