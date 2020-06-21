import time

SEVERITY = {
    logging.DEBUG: 'debug',
    logging.INFO: 'info',
    logging.WARNING: 'warning',
    logging.ERROR: 'error',
    logging.CRITICAL: 'critical',
}
# if there is a pipe present then we rename the destiantion to common type of logs and trim that destination
# otherwise we will just trim the recent type of logs
def log_recent(conn, name, message, severity=logging.INFO, pipe=None):
    severity = str(SEVERITY.get(severity, severity)).lower()
    destination = 'recent:%s:%s'%(name, severity)
    message = time.asctime() + ' ' + message
    pipe = pipe or conn.pipeline()
    pipe.lpush(destination, message)
    pipe.ltrim(destination, 0, 99)
    pipe.execute()


#types of keys in redis
# A) destination:start
# B) destination:last
# C) destination:pstart

#We have a function called log_common which is called through our code
#For a particular name and severity
# if the same kind of name and severity key gets logged many times within an hour
# then that should be stored in our archive
# or
# the recent logs are always trimed
# and all common logs are just stored in archive
def log_common(conn, name, message, severity=logging.INFO, timeout=5):
    severity = str(SEVERITY.get(severity, severity)).lower()
    destination = 'common:%s:%s'%(name, severity)
    start_key = destination + ':start'
    pipe = conn.pipeline()
    end = time.time() + timeout
    while time.time() < end: #Continously run for 5 secs
        try:
            pipe.watch(start_key) #log_common could be called somewhere else and start_key is currently being updated
            now = datetime.utcnow().timetuple()
            hour_start = datetime(*now[:4]).isoformat()
            existing = pipe.get(start_key) #get the time at start_key
            pipe.multi()
            if existing and existing < hour_start: #if there is a start key in common logs section
                #For this particular hour
                pipe.rename(destination, destination + ':last')# rename common:name:severity to common:name:severity:last
                pipe.rename(start_key, destination + ':pstart')# rename common:name:severity:start to common:name:severity:pstart
                pipe.set(start_key, hour_start)                # common:name:severity:pstart equals to this hour
            pipe.zincrby(destination, message)
            log_recent(pipe, name, message, severity, pipe)
            return
        except redis.exceptions.WatchError:
            continue
