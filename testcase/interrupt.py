from distrilockper import Config
from distrilockper.lock_helper import DistributerLockHelper

import _thread

config = Config()
config.use_single_server().set_config(host='0.0.0.0', port=6379)
helper = DistributerLockHelper()
helper.create(config)

class ticketSalse():
  def __init__(self):
    self.ticket_count = 1

  def buy(self):
    print('run')
    _thread.exit()
    print("kill")
    Locker1 = helper.get_reentrant_lock(key='ticketSalse')
    re1 = Locker1.try_lock(2, 10, 'second')
    print("get lock:", re1)
    if re1:
      if self.ticket_count > 0:
        self.ticket_count -= 1
        print("sale one, remain: ", self.ticket_count)
        Locker1.unlock()
      Locker1.unlock()
    else:
      print("get lock failed")
    print(self.ticket_count)

  def ticket_num(self):
    print(self.ticket_count)


import threading
import time
sale = ticketSalse()
threads = []
for i in range(100):
  # print(i)
  threads.append(threading.Thread(target = sale.buy))
  threads[i].start()

