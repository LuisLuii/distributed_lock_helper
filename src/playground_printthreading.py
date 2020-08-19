from sys       import stdout
from time      import sleep
from random    import randint
from threading import Thread

def worker(name):
  wait=randint(2,7)
  sleep(1)
  #print( "I'm",name,"and waited",wait,"seconds.")


t1=Thread(target=worker,args=("thread 1",))

t1.start()
