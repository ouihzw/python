# -*- coding:utf-8 -*-
from .. import databaseDict
from PyQt5.QtCore import *
from bson import ObjectId

class DirectiveDao(QObject):
    def __init__(self):
        super().__init__()
        db = databaseDict.DatabaseDict().dbDict["MongoDB"].db
        self.directive = db.get_collection("directive")

    # 插入指令，指令中包含command(指令名)，line_number(行号)，flow_id(流程文件id)，
    # comment(注释)，target(首选目标)，targets(备选目标)，value(值)，data(其他数据)
    def insertDirective(self, directive: dict):
        if directive["line_number"] < 1:
            return
        result = self.directive.update_many({"flow_id": directive["flow_id"],
                                             "line_number": {"$gte": directive["line_number"]}},
                                            {"$inc": {"line_number": 1}})
        print("updated:", result.modified_count)
        result = self.directive.insert_one(directive)
        return result.inserted_id

    # 更新指令
    def updateDirective(self, _id: ObjectId, update: dict):
        result = self.directive.update_one({"_id": _id}, {"$set": update})
        print("updated:", result.modified_count)

    # 修改行号，lineNumber为行号修改的起始值，change是行号的变动值
    def updateLineNumber(self, flowId: ObjectId, lineNumber: int, change: int):
        result = self.directive.update_many({"flow_id": flowId, "line_number": {"$gte": lineNumber}},
                                            {"$inc": {"line_number": change}})
        print("line number updated:", result.modified_count)

    # 获取所有指令
    def getAllDirectives(self, flowId: ObjectId):
        result = self.directive.find({"flow_id": flowId}).sort([("line_number", 1)]).batch_size(500)
        return result

    # 读取指定的一条指令
    def getOneDirective(self, _id: ObjectId):
        result = self.directive.find_one({"_id": _id})
        return result

    # 删除指定的一条指令
    def deleteOneDirective(self, _id: ObjectId):
        self.directive.delete_one({"_id": _id})
