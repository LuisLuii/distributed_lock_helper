import threading
import redis

class Listener(threading.Thread):
    def __init__(self, r, p):
        threading.Thread.__init__(self)
        self.redis = r
        self.pubsub = self.redis.pubsub()
        self.pubsub.psubscribe(p)

    def run(self):
        for m in self.pubsub.listen():
            if 'pmessage' != m['type']:
                continue
            if '__admin__' == m['channel'] and 'shutdown' == m['data']:
                #print ('Listener shutting down, bye bye.')
                break
            #print (m)

if __name__ == "__main__":
    r = redis.StrictRedis(decode_responses=True)
    client = Listener(r, '*')
    client.start()

    r.publish('channel1', 'message1')
    r.publish('channel2', 'message2')
    r.publish('channel1', 'message3')

    r.publish('__admin__', 'shutdown')
    #print ('Main ended.')