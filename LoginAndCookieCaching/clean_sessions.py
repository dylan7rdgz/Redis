import time

QUIT = False
LIMIT = 10000000

def clean_sessions(conn):
    while not QUIT:
        size = conn.zcard('recent:')
        if size <= LIMIT:
            time.sleep(1)
            continue
    end_index = min(size - LIMIT, 100)
    tokens = conn.zrange('recent :', 0, end_index-1)

    session_keys = []
    #update code
