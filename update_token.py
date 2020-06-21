import time

def update_token(conn, token, user, item=None):
    timestamp = time.time()
    conn.hset('login:',token, user)
    conn.zadd('recent:', token, timestamp)
    if item:
        conn.zadd('viewed:' + token , item, timestamp)
        #How can we do better if in case we are not interested in timestamp
        #1.create a list having a list-name as viewed
        #2.add key value pair as 'token':'item'
        #This is suppose to save our memory
        #But how? #semantics should be same
        conn.zremrangebyrank('viewed:'+token, 0, -26)