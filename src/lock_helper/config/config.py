from lock_helper.config.custer_redis import ClusterServersConfig

class Config(ClusterServersConfig):

    def __init__(self):
        self.cluster_config: ClusterServersConfig = None
        self.cluster_mode = False

    def use_cluster_servers(self) -> ClusterServersConfig:
        self.cluster_mode = True
        return self.cluster_server_config(ClusterServersConfig())

    def cluster_server_config(self, ClusterConfig: ClusterServersConfig):
        """
        TODO:
            checkMasterSlaveServersConfig();
            checkSentinelServersConfig();
            checkSingleServerConfig();
            checkReplicatedServersConfig();
        :return:
        """
        if not self.cluster_config:
            self.cluster_config = ClusterConfig
        return self.cluster_config

    @property
    def get_node(self):
        return self.cluster_config.get_node

    @property
    def mode(self):
        return self.cluster_mode

    def redis(self):
        pass

if __name__ == '__main__':
    Config().use_cluster_servers().add_node_address(port=123).add_node_address(host="123",port=123).add_node_address(host="123",port=123)