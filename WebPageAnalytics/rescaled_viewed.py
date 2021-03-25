import time
QUIT = 0 # not sure abouth this line
def rescaled_viewed(conn):
    while not QUIT:
        conn.zremrangebyrank('viewed:',2000, -1)
        conn.zinterstore('viewed:', {'viewed': .5}) #Sometimes intersection that is zinterstore is used as a self assignment operatore
        time.sleep(300)