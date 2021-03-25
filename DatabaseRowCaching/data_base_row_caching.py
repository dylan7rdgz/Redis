QUIT = False
import time
#Certain data is shown in the frontend
#There could be changes in backend
#The front end has to reflect what is actually present in the database

#Each time we reflect the correct changes in front end we have to
#make database calls which is a very heavy operation

#We have to predict the rate at which the data(ex: INVENTORY) in DB changes

#In the following function set delay to a high value if the data (NNOTE: SUBSET of rows) does not change often
#Set delay to a small value if the data of certain rows change fast

#Schedule determines the time
def schedule_row_cache(conn, row_id, delay):
    conn.zadd('delay:', row_id, delay)
    conn.zadd('schedule:', row_id, time.time())

def cache_rows(conn):
    while not QUIT:
        next = conn.zrange('schedule:', 0, 0, withscores=True)
        now = time.time()
        if not next or next[0][1] > now:
            time.sleep(.05)
            continue
        row_id = next[0][0]
        delay = conn.zscore('delay:', row_id)
        if delay <= 0:
            conn.zrem('delay:', row_id)
            conn.zrem('schedule:', row_id)
            conn.delete('inv:' + row_id)
            continue
        row = Inventory.get(row_id)
        conn.zadd('schedule:', row_id, now + delay)
        conn.set('inv:' + row_id, json.dumps(row.to_dict()))