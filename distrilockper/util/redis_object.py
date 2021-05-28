class RedisObject():
    @staticmethod
    def suffix_name( name, suffix):
        if '{' in name:
            return name + ':' + suffix
        return "{" + name + "}" + suffix


    @staticmethod
    def prefix_name(prefix, name):
        if "{" in name:
            return prefix + ":" + prefix
        return prefix + ":{" + name + "}"