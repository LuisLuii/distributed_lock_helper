class Node():
    def __init__(self, pre  = None, data = None, next = None,):
        self.pre = pre
        self.data = data
        self.next = next



class LinkedDict(Node):
    def __init__(self):
        self.node = None


    def put(self,data : dict):
        if not self.node:
            self.node = Node(pre = None, data = data, next = None)
            return
        if self.node.data:
            current_node = self.node

            while 1:
                if not current_node.next:
                    appended_node = Node()
                    appended_node.data = data
                    appended_node.pre = current_node
                    current_node.next = appended_node
                    appended_node.next = None
                    return
                if current_node.next:
                    current_node = current_node.next

    @property
    def get_first(self):
        if not self.node:
            return None
        else:
            res= self.node.data

        return res

    def get(self, key):
        current_node = self.node
        if not current_node:
            return None
        while current_node:
            data = current_node.data
            if key not in data.keys():
                current_node = current_node.next
                continue
            return data

    def show(self):
        res = []
        current_node = self.node
        if not current_node:
            return None
        while current_node:
            # print(current_node.data)
            res.append(current_node.data)
            current_node = current_node.next
        return res

    def clear(self):
        self.data = None
        self.pre = None
        self.next = None

    def remove_thread_id(self, thread_id):
        current_node = self.node
        if not current_node:
            return None
        while current_node:
            if thread_id in current_node.data.keys():
                pass

    def get_or_default(self,key, default):
        res = self.get(key)
        if not res:
            return default
        return res

    @property
    def empty(self):
        if not self.node:
            return True
        return False

if __name__ == '__main__':
    linked_list = LinkedDict()
    linked_list.put({'1':1})
    linked_list.put({'2':2})
    linked_list.put({'3':3})
    linked_list.put({'4':4})
    a = linked_list.get_first
    #print(linked_list.get_or_default('1', 'pppp'))
    linked_list.show()