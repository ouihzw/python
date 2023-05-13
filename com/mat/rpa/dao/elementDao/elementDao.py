# -*- coding:utf-8 -*-
from com.mat.rpa.dao import databaseDict
from PyQt5.QtCore import *

class ElementDao(QObject):
    def __init__(self):
        super().__init__()
        db = databaseDict.DatabaseDict().dbDict["MongoDB"].db
        self.element = db.get_collection("element")

    def insertNewElement(self, element: dict):
        result = self.element.insert_one(element)
        return result

    def deleteOneElement(self, name: str):
        self.element.delete_one({"name": name})

    def getOneElement(self, name: str):
        result = self.element.find_one({"name": name})
        return result

    def updateElementName(self, name: str, nameupdate: str):
        result = self.element.update_one({"name": name}, {"$set": {"name": nameupdate}})
        return result

    def deleteAllElement(self):
        self.element.delete_many()

    def findAllElement(self):
        result = self.element.find()
        return result
