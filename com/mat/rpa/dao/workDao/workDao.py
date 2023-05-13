# -*- coding:utf-8 -*-
import datetime

from .. import databaseDict
from PyQt5.QtCore import *
from bson import ObjectId

class WorkDao(QObject):
    __instance = None  # 单例模式
    _isFirstInit = True  # 判断首次构造的标记

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super(WorkDao, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        if WorkDao._isFirstInit:
            super().__init__()
            db = databaseDict.DatabaseDict().dbDict['MongoDB'].db
            self.app = db.get_collection("app")
            self.directive = db.get_collection("directive")
            self.variable = db.get_collection("variable")
            WorkDao._isFirstInit = False

    # 新建App，临时插入文档
    def insertNewApp(self):
        # 清理上一个没有与MySQL绑定的临时文档
        result = self.app.find_one({'status': -1})
        if result:
            flows = []
            for item in result["flow"]:
                flows.append(item["id"])
            self.directive.delete_many({"flow_id": {"$in": flows}})
            flows.append(result["_id"])
            self.variable.delete_many({"parent_id": {"$in": flows}})
            self.app.delete_one({"_id": result["_id"]})
        # 生成主流程文件的id
        mainFlowId = ObjectId()
        # 插入新的临时文档
        result = self.app.insert_one({'name': '未命名应用',
                                      'status': -1,
                                      'class': 0,
                                      'update_time': datetime.datetime.now(),
                                      'flow': [{'id': mainFlowId,
                                                'type': 0,
                                                'flow_name': '主流程.flow'}]})
        return result.inserted_id, mainFlowId

    # 导入App，去掉_id项，去掉flow项
    def importNewApp(self, appDict):
        result = self.app.insert_one(appDict)
        return result.inserted_id

    # 保存APP信息
    def saveAppInfo(self, appId: ObjectId, appInfo: dict):
        appInfo["status"] = 0
        self.app.update_one({"_id": appId}, {"$set": appInfo})

    # 读取APP
    def loadApp(self, appId: ObjectId = None):
        result = self.app.find_one({"_id": appId})
        return result

    # 新建Flow文件
    def insertSubFlow(self, appId: ObjectId, name: str):
        flowId = ObjectId()
        subFlow = {"id": flowId,
                   "type": 1,
                   "flow_name": name}
        self.app.update_one({"_id": appId}, {"$push": {"flow": subFlow}})
        return flowId

    # 导入Flow文件(通过导入App)
    def importFlow(self, appId: ObjectId, flowDict: dict):
        flowId = ObjectId()
        flowDict["id"] = flowId
        self.app.update_one({"_id": appId}, {"$push": {"flow": flowDict}})
        return flowId

    # 查询所有的Flow文件
    def getFlows(self, appId: ObjectId):
        result = self.app.find_one({"_id": appId})
        return result["flow"]

    # 查询所有的Flow文件名
    def getFlowNames(self, appId: ObjectId):
        result = self.app.find_one({"_id": appId})
        names = set()
        for item in result["flow"]:
            names.add(item["flow_name"])
        return names

    # 更新Flow文件名
    def updateFlowName(self, appId: ObjectId, flowId: ObjectId, flowName: str):
        result = self.app.update_one({"_id": appId, "flow.id": flowId},
                                     {"$set": {"flow.$.flow_name": flowName}})
        print("update:", result.modified_count)

    # 删除Flow文件
    def deleteSubFlow(self, appId: ObjectId, flowId: ObjectId):
        result = self.app.update_one({"_id": appId}, {"$pull": {"flow": {"id": flowId}}})
        print("delete:", result.modified_count)
        result = self.directive.delete_many({"flow_id": flowId})
        print("deleted directives:", result.deleted_count)
        result = self.variable.delete_many({"parent"
                                            "._id": flowId})
        print("deleted variables:", result.deleted_count)

    # *删除所有的指令*，不保存临时文档时清理所有指令
    def deleteAllDirectives(self, appId: ObjectId):
        result = self.app.find_one({"_id": appId})
        flows = []
        for item in result["flow"]:
            flows.append(item["id"])
        result = self.directive.delete_many({"flow_id": {"$in": flows}})
        self.variable.delete_many({"parent_id": {"$in": flows}})
        print("deleted directives:", result.deleted_count)

    # 删除对应的APP文档，删除APP前请务必删除APP的所有指令
    def deleteApp(self, appId: ObjectId):
        self.deleteAllDirectives(appId)
        self.variable.delete_many({"parent_id": appId})
        result = self.app.delete_one({"_id": appId})
        print("app delete:", result.deleted_count)