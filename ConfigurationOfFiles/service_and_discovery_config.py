#For one database and one redis store its easy to mantain configuration
#However for many redis master slaves and db its difficuilt to mantain configuration

#A Configuartion file is stored on disk
#Every time we want to access a new database we might want to change our configuration file stored on disk
#Why not store this in Redis? i.e AUTO-CONFIGARTION


LAST_CHECKED = None;
IS_UNDER_MANTAINANCE = False;
def isunder_mantainance(conn):
    global LAST_CHECKED, IS_UNDER_MANTAINANCE
    if LAST_CHECKED < time.time() - 1:
        LAST_CHECKED = time.time()
        IS_UNDER_MANTAINANCE = bool(conn.get('is-under-mantainance'))
    return IS_UNDER_MANTAINANCE

#We can have different redis stores for different requirements but there is a drawback
#Unfortunately, as your number of servers and/or Redis databases increases, managing and distributing configuration information for all of those servers becomes more of a chore
def set_config(conn, type, component, config):
    conn.set('config:%s:%s(type,component)',json.dumps(config))

CONFIGS = {}
CHECKED = {}

def get_config(conn, type, component, wait=1):
    key = 'config:%s:%s'%(type, component)
    if CHECKED.get(key) < time.time() - wait:
        CHECKED[key] = time.time() #For a particular key We can, so update the last time we checked this connection.
        config = json.loads(conn.get(key) or '{}') # Fetch the config for this component
        config = dict((str(k), config[k]) for k in config) # Convert potentially Unicode keyword arguments into string keyword arguments
        old_config = CONFIGS.get(key)
        if config != old_config:
            CONFIGS[key] = config
    return CONFIGS.get(key)

REDIS_CONNECTIONS = {}

def redis_connection(component, wait=1):
    key = 'config:redis:' + component
    def wrapper(function):
        @functools.wraps(function)
        def call(*args, **kwargs):

            old_config = CONFIGS.get(key, object())
            _config = get_config(
                config_connection, 'redis', component, wait
            )
            config = {}
            for k, v in _config.iteritems():
                config[k.encode('utf-8')] = v
            if config != old_config:
                REDIS_CONNECTIONS[key] = redis.Redis(**config)

            return function(
                        REDIS_CONNECTIONS.get(key), *args, **kwargs
                    )
        return call
    return wrapper

