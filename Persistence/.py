# Types of persistence
# 1.SnapShot persistance - Takes data as it is and writrs it to disk
# 2.AOF - Copying write commands to the disk as they happen

#Assuption
#AOF updates to file; at a time APPENDS to a file
#SnapShot writes to disk (file format?) waits until all data at once can be loaded to disk


# Link: https://redis.io/topics/persistence
# Options for persistence configuartion available in Redis (Examples)

#----Snapshotting persistence Options----
# save 60 1000
# stop-writes-on-bgsave-error no
# rdbcompression yes
# dbfilename dump.rdb

#----Append-only file persistence Options----
# appendonly no
# appendsync everysec
# no-append-sync-no-write-no
# auto-aof-rewrite percentagr 100
# auto-aof-rewrite-min-size 64mb

#----Shared Option, where ti store the snapshot or append-only file---
# dir ./

#Persisting disk with (Snapshots)








