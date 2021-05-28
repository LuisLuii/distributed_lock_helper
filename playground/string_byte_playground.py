# channelName = "lock_helper__channel:{apples2}"
# #print(hash(channelName)%50)
import time

import redis
# connect with redis server as Bob
bob_r = redis.Redis(host='localhost', port=6379, db=0)
bob_p = bob_r.pubsub()
# subscribe to classical music
bob_p.subscribe('classical_music')
while 1:
    time.sleep(1)
    #print(bob_p.get_message())