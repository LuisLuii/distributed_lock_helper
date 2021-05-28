from distrilockper import exception

class ClusterServersConfig(object):
    def __init__(self):
        self.__node: list or dict = None
        self.__config = {}

    def add_node_address(self, host: str = None, port: int = None, **kwargs) -> 'ClusterServersConfig':
        """
        Add Redis cluster node address.
        :param host:
        :param port:
        :return: ClusterServersConfig()
        """
        if self.__node and not isinstance(self.__node , list ):
            raise ValueError('Your are already config the redis conenct')
        if not self.__node:
            self.__node = []
        if not host or not port:
            raise exception.ArgumentError("Both argument of host and port are required: "
                                          "host should be a str type; "
                                          "port should be a int type")

        connection_config = {'host': host, 'port': port}
        if kwargs:
            connection_config = {**connection_config, **kwargs}
        self.__node.append(connection_config)

        return self

    def set_config(self,**kwargs):
        """
            add the other config, refer to the python redis library
        """
        self.__config = {**kwargs}


    @property
    def get_config(self):
        """
            the redis response message is default byte, we can use the decode_response to let the response message to be string
        """
        if not self.__node:
            return {'host': '127.0.0.1', 'port': 6379,  "decode_responses":True}
        if isinstance(self.__node, list):
            for node in self.__node:
                if "decode_responses" not in node:
                    node['decode_responses'] = True
        if isinstance(self.__node, dict):
            if "decode_responses" not in self.__node:
                self.__node['decode_responses'] = True
        return self.__node
