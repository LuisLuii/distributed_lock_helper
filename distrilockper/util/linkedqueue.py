from threading import Lock

class linkedQueue(object):
    class Node(object):
        def __init__(self, value=None):
            self.value = value
            self.next = None

    def __init__(self):
        self.head = None
        self.tail = None
        #self.head.next = self.tail
        self.length = 0

    def is_empty(self):
        return self.length == 0

    def size(self):
        return self.length

    def enqueue(self, value):
        node = self.Node(value)
        if self.is_empty():
            self.head = node
        else:
            self.tail.next = node
        self.tail = node
        self.length += 1

    def dequeue(self):
        if self.is_empty():
            raise Exception("queue is empty !")
        item = self.head.value
        self.head =  self.head.next
        self.length -= 1
        return item

    def poll(self):
        return self.dequeue()
if __name__ == '__main__':

    link = linkedQueue()
    link.enqueue(1)
    link.enqueue(2)
    link.enqueue(3)
    link.enqueue(4)
    #print("queue size：",link.size())
    link.dequeue()
    link.dequeue()