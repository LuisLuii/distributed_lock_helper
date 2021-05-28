# channelName = "lock_helper__channel:{apples2}"
# ##print(hash(channelName)%50)


import redis
alice_r = redis.Redis(host='localhost', port=6379, db=0)
# publish new music in the channel epic_music
alice_r.publish('classical_music', 'Alice Music')