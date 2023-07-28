globaldb:PRIMARY> db.user.createIndex({"_ts":1}, {expireAfterSeconds: 10})

globaldb:PRIMARY> db.user.getIndexes()

globaldb:PRIMARY> db.user.dropIndexes()
