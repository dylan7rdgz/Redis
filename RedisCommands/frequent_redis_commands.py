import redis
conn = redis.Redis()

#String Commands
conn.incr('key')                                     # 1   No previously specified key So Redis interprets this as 0
conn.get('key')                                      #'1'
conn.incr('key',1)                                   # 2
conn.incrby('key',5)                                 # 7
conn.incrbyfloat('key',5.3)                          # 12.3
conn.set('key',13)                                   # true
conn.incr('key')                                     # 14
conn.append('new-string-key', 'hello ')              #6L
conn.append('new-string-key', 'world!')              #12L
conn.substr('new-string-key', 3, 7)                  #'lo wo'
conn.setrange('new-string-key', 0, 'H')              #12
conn.get('new-string-key')                           #'Hello world!' (Notice that H is become a Capital)
conn.setrange('new-string-key', 11, ', how are you?')#25
conn.get('new-string-key')                           #'Hello World, how are you?'

#List Commands
conn.rpush('list-key', 'last')                       #3L
conn.lpush('list-key', 'first')                      #4L
conn.rpush('list-key', 'new last')                   #5L
conn.lrange('list-key', 0, -1)                       #['first', 'last', 'new last'] -1 means till end of list -1 means ultimate -2 means penultimate
conn.lpop('list-key')                                #'first'
conn.lpop('list-key')                                #'last'
conn.lrange('list-key', 0, -1)                       #['new last']
conn.rpush('list-key', 'a', 'b', 'c')                #4L
conn.lrange('list-key', 0, -1)                       #['new last', 'a', 'b', 'c']
conn.ltrim('list-key', 2, -1)                        #True
conn.lrange('list-key', 0, -1)                       #['b', 'c']
conn.rpush('list', 'item1')                          #1 (1 means sixe of list)
conn.rpush('list', 'item2')                          #2
conn.rpush('list2', 'item3')                         #1
conn.brpoplpush('list2', 'list', 1)                  #'item3'
conn.brpoplpush('list2', 'list', 1)                  #Nothing is displayed                                           #When a list is empty, the blocking pop will stall for the timeout, and return None (which isn’t displayed in the interactive  console).
conn.lrange('list', 0, -1)                           #['item3', 'item1', 'item2']
conn.brpoplpush('list', 'list2', 1)                  #'item2'
conn.blpop(['list', 'list2'], 1)                     #('list', 'item3')
conn.blpop(['list', 'list2'], 1)                     #('list', 'item1')
conn.blpop(['list', 'list2'], 1)                     #('list2', 'item2')
conn.blpop(['list', 'list2'], 1)                     #Nothing is displayed

#Set commands
conn.sadd('set-key', 'a', 'b', 'c')                 #3 (i.e the number of values that are added to set-key)
conn.smembers('set-key','c','d')                    #set(['a', 'c', 'b'])
conn.srem('set-key', 'c', 'd')                      #1 (True)   c and d both are present so it was succussful in removing and returns true
conn.srem('set-key','c','d')                        #0 (False)  c and d are not present so it failed in removing and returns false
conn.scard('set-key')                               #2  Returns the cardinality of the set
conn.smembers('set-key')                            #set(['a', 'b'])
conn.smove('set-key', 'set-key2', 'a')              #True
conn.smove('set-key', 'set-key2', 'c')              #False
conn.smembers('set-key2')                           #set(['a'])
conn.sadd('skey1', 'a', 'b', 'c', 'd')              #4
conn.sadd('skey2', 'c', 'd', 'e', 'f')              #4
conn.sdiff('skey1', 'skey2')                        #set(['a', 'b'])
conn.sinter('skey1', 'skey2')                       #set(['c', 'd'])
conn.sunion('skey1', 'skey2')                       #set(['a', 'c', 'b', 'e', 'd', 'f'])


#Hash commands
conn.hmset('hash-key', {'k1':'v1', 'k2':'v2', 'k3':'v3'})  #True
conn.hmget('hash-key', ['k2', 'k3'])                       #['v2', 'v3']
conn.hlen('hash-key')                                      #3
conn.hdel('hash-key', 'k1', 'k3')                          #True
conn.hmset('hash-key2', {'short':'hello', 'long':1000*'1'})#True
conn.hkeys('hash-key2')                                    #['long', 'short']
conn.hexists('hash-key2', 'num')                           #False
conn.hincrby('hash-key2', 'num')                           #1L
conn.hexists('hash-key2', 'num')                           #True

#Sorted Set Commands
conn.zadd('zset-key', 'a', 3, 'b', 2, 'c', 1)              #3
conn.zcard('zset-key')                                     #3
conn.zincrby('zset-key', 'c', 3)                           #4.0
conn.zscore('zset-key', 'b')                               #2.0
conn.zrank('zset-key', 'c')                                #2
conn.zcount('zset-key', 0, 3)                              #2L
conn.zrem('zset-key', 'b')                                 #True
conn.zrange('zset-key', 0, -1, withscores=True)            #[('a', 3.0), ('c', 4.0)]

conn.zadd('zset-1', 'a', 1, 'b', 2, 'c', 3)                #3
conn.zadd('zset-2', 'b', 4, 'c', 1, 'd', 0)                #3
conn.zinterstore('zset-i', ['zset-1', 'zset-2'])           #2L
conn.zrange('zset-i', 0, -1, withscores=True)              #[('c', 4.0), ('b', 6.0)]
conn.zunionstore('zset-u', ['zset-1', 'zset-2'], aggregate='min') #4L
conn.zrange('zset-u', 0, -1, withscores=True)              #[('d', 0.0), ('a', 1.0), ('c', 1.0), ('b', 2.0)]
conn.sadd('set-1', 'a', 'd')                               #2
conn.zunionstore('zset-u2', ['zset-1', 'zset-2', 'set-1']) #4L
conn.zrange('zset-u2', 0, -1, withscores=True)             #[('d', 1.0), ('a', 2.0), ('c', 4.0), ('b', 6.0)]