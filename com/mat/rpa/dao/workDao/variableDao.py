# -*- coding:utf-8 -*-
from .. import databaseDict
from PyQt5.QtCore import *
from bson import ObjectId

class VariableDao(QObject):
    def __init__(self):
        super().__init__()
        db = databaseDict.DatabaseDict().dbDict["MongoDB"].db
        self.variable = db.get_collection("variable")
        #self.variable.delete_one()

    # 新建变量
    def newVariable(self, document: dict):
        result = self.variable.insert_one(document)
        return result.inserted_id

    # 更新变量，若不存在则创建
    def updateVariable(self, document: dict):
        result = self.variable.update_one({"directive_id": document["directive_id"]},
                                          {"$set": document}, upsert=True)
        return result.upserted_id


    # 获取指定变量信息
    def getVariable(self, _id: ObjectId):
        result = self.variable.find_one({"_id": _id})
        return result

    # 获取指定行号之前的所有变量
    def getLocalVariablesByLineNumber(self, flow_id: ObjectId, lineNumber: int):
        # 先通过directive_id字段筛选局部变量，再与directive集合进行关联查询
        # 将关联后的directive字段的数组展开，然后进行投影，最后筛选行号，进行排序
        result = self.variable.aggregate([
            {
                "$match": {
                    "parent_id": flow_id,
                }
            }, {
                "$lookup": {
                    "from": "directive",
                    "localField": "directive_id",
                    "foreignField": "_id",
                    "as": "directive"
                }
            }, {
                "$unwind": "$directive"
            }, {
                "$project": {
                    "name": 1,
                    "type": 1,
                    "line_number": "$directive.line_number"
                }
            }, {
                "$match": {
                    "line_number": {
                        "$lt": lineNumber
                    }
                }
            }, {
                "$sort": {
                    "name": 1,
                    "line_number": -1
                }
            }])

        if result:
            resultDict = {}
            former = None
            for item in result:
                if item["name"] != former:
                    resultDict[item["name"]] = item["type"]
                    former = item["name"]
            return resultDict
        return result

    def getGlobalVariables(self, app_id):
        resultDict = {}
        if app_id:
            result = self.variable.find({"parent_id": app_id})
            for item in result:
                resultDict[item["name"]] = item["type"]
        return resultDict
