# -*- coding:utf-8 -*-
from com.mat.rpa.dao import databaseDict
from PyQt5.QtCore import *

class appDataDao(QObject):
    def __init__(self):
        super().__init__()
        db = databaseDict.DatabaseDict().dbDict["MongoDB"].db
        self.appData = db.get_collection("appData")

    def insert(self, data):
        result = self.appData.insert_one(data)
        return result

    def delete(self, data):
        self.appData.delete_one(data)

    def getOneByAppid(self, id):
        result = self.appData.find_one({"robotId": id})
        return result

    def update(self, old, data):
        self.appData.replace_one(old, data)

    def deleteAll(self):
        self.appData.delete_many()

    def findAll(self):
        result = self.appData.find()
        return result
