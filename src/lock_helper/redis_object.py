class RedisObject():
    def suffix_name(self, name, suffix):
        if '{' in name:
            return name + ':' + suffix
        return "{" + name + "}" + suffix


    def prefix_name(self,prefix, name):
        if "{" in name:
            return prefix + ":" + prefix
        return prefix + ":{" + name + "}"