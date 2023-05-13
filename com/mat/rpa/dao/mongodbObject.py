# -*- coding:utf-8 -*-
import pymongo
class MongodbObject():
    def __init__(self, host, port, db_name):
        db_uri = "mongodb://" + host + ":" + str(port) + "/"
        self.client = pymongo.MongoClient(db_uri)
        self.db = self.client[db_name]

    def __del__(self):
        self.client.close()

    def process_item(self, item, collection_name):
        collection = self.db[collection_name]
        collection.insert_one(item)
