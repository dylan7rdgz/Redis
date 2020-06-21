import time
import threading
import redis
conn = redis.Redis()

def publisher():
    time.sleep(1)                 #waits for the subscriber to connect so that it starts listening fro messages
    for i in range(n):
        conn.publish('channel', i) #Python client that calls publish of redis
                                   #we publish to a 'channel'
        time.sleep(1)

def run_pubsub():
    threading.Thread(target=publisher, args=(3,)).start()
    pubsub = conn.pubsub()         #Python client that calls pubsub of redis
    pubsub.subscribe(['channel'])  #We Subscribe from a channel
    count = 0
    for item in pubsub.listen():   #Once we have subscribed we can enjoy the service 
                                   #and just listen
        print(item)
        count += 1
        if count == 4:
            pubsub.unsubscribe()
        if count == 5:
            break

run_pubsub()