from distrilockper.config.ClusterServersConfig import ClusterServersConfig
from distrilockper.config.SingleServerConfig import SingleServerConfig
from distrilockper.connection.BaseConnectionManager import BaseConnectionManager


class Config(BaseConnectionManager):

    def __init__(self):
        super().__init__()
        self.__cluster_config = None
        self.__cluster_mode: bool = False
        self.__single_config = None

    def use_cluster_servers(self) -> ClusterServersConfig:
        self.__cluster_mode = True
        return self.__cluster_server_config(ClusterServersConfig())

    def __cluster_server_config(self, ClusterConfig: ClusterServersConfig):
        """
        TODO:
            checkMasterSlaveServersConfig();
            checkSentinelServersConfig();
            checkSingleServerConfig();
            checkReplicatedServersConfig();
        :return:
        """
        if not self.__cluster_config:
            self.__cluster_config: ClusterServersConfig = ClusterConfig
        return self.__cluster_config

    def use_single_server(self):
        self.__cluster_mode = False
        return self.__single_server_config()

    def __single_server_config(self):
        self.__single_config = SingleServerConfig()
        return self.__single_config

    @property
    def get_node(self):
        return self.__cluster_config.get_node

    @property
    def cluster_mode(self):
        """
            return true for cluster mode and false for single mode
        """
        return self.__cluster_mode

    @property
    def get_config(self):
        if self.__cluster_config:
            return self.__cluster_config.get_config
        if self.__single_config:
            return self.__single_config.get_config


if __name__ == '__main__':
    # Config().use_cluster_servers().add_node_address(host=123,port=123).add_node_address(host="123",port=123).add_node_address(host="123",port=123)
    _ = Config()
    _.use_single_server().set_config(host=123,port=123)
    o = _.get_config()
    ##print(o)