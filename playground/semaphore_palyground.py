# import time
# import threading
# import random
#
# data = {"banana7": False,
#         "banana1": False,
#         "banana2": False,
#         "banana3": False,
#         "banana4": False,
#         "banana5": False,
#         "banana6": False}
# semaphore = threading.Semaphore(0)
# class LockHelpTest():
#     def __init__(self, name):
#         # self.
#         self.name = name
#
#     def lock(self, s):
#         # GET THE PRODUCT LOCK, WAIT THE TTL IF IT IS FALSE,
#         # try_release()
#         ##print(f"existing semaphore {semaphore._value}")
#         if not data[self.name]: # is True
#             data[self.name] = True
#             ##print(f"get lock {self.name} success")
#             return True
#         ##print(f"{threading.currentThread().getName()} is waiting for {self.name}")
#         _ = semaphore.acquire()
#         ##print(f"{threading.currentThread().getName()} try get {self.name} again : {_}")
#
#         return True
#
#     def unlock(self):
#         # semaphore.acquire()
#
#         ##print(f" {self.name} lock release")
#         data[self.name] = False
#         semaphore.release()
#
# def boo(name):
#     lock_instance = LockHelpTest(name)
#     n = random.randint(0,9)
#     _ = threading.currentThread().getName()
#     # ##print(f"{name} try get lock and wait {n} if get failed")
#     _ = lock_instance.lock(int(n))
#     if _ :
#         ##print(f"{name} sleep {n}")
#         time.sleep(n)
#         ##print(f"{name}  release")
#         lock_instance.unlock()
#     else:
#         pass
#
# if __name__ == '__main__':
#     # ##print('1')
#     # semaphore.acquire()
#     # ##print('2')
#     #
#     # semaphore.acquire()
#     # ##print('3')
#     #
#     # semaphore.acquire()
#     # ##print('4')
#     #
#     # semaphore.acquire()
#     # ##print('5')
#
#     test = ["banana1","banana1","banana1","banana2","banana3","banana1","banana1","banana2","banana1","banana2","banana3","banana1","banana1","banana2"]
#     for i in range(2):
#         flag = False
#         t1 = threading.Thread(target=boo, args = [test[i],])
#         t1.start()

import threading
import time
sem = threading.Semaphore(5)

def fun1():
    while True:
        ##print("try get "+ threading.current_thread().name)
        sem.acquire()
        ##print( threading.current_thread().name + " get successfully")
        sem.release()
        ##print("release "+ threading.current_thread().name)

        time.sleep(3)
        #print()
        #print()
        #print()



t = threading.Thread(target = fun1)
t.start()
t2 = threading.Thread(target = fun1)
t2.start()
t3 = threading.Thread(target = fun1)
t3.start()