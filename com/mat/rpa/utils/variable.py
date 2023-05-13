# -*- coding:utf-8 -*-
from com.mat.rpa.dao.workDao.variableDao import VariableDao
from bson import ObjectId
import math
import re


# 解析字符串，如果为变量则去除标识符，否则返回None
def parseVariable(text: str):
    if text.startswith("${") and text.endswith("}"):
        return text[2:-1]
    return None


# 含变量纯文本字符串解析，将${变量名}替换为变量值
def replacePlainTextVariable(text: str, flowId: ObjectId):
    starter = None
    variableList = []
    for i in range(len(text)):
        if text[i] == '$':
            if text[i + 1] == '{':
                starter = i
        elif text[i] == '}':
            if starter is not None:
                variableList.append(text[starter + 2: i])
                starter = None
    if variableList:
        vm = VariableManager()
        for item in variableList:
            newValue = vm.getVariable(flowId, item)
            if newValue:
                text = text.replace("${" + item + "}", str(newValue))
    return text


# 变量管理器
class VariableManager(object):
    __instance = None  # 单例模式
    _isFirstInit = True  # 判断首次构造的标记

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super(VariableManager, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        # 获取type类
        cls = type(self)
        # 判断类的构造函数是否初次执行
        if cls._isFirstInit:
            self.variableDaoObj = VariableDao()
            self.variables = {"global": {}}
            self._appId = None
            cls._isFirstInit = False

    # 设置当前AppID
    def setAppId(self, appId: ObjectId):
        self._appId = appId

    # 读取AppID
    def getAppId(self):
        return self._appId

    # 新建局部变量信息
    def newLocalVariableInfo(self, name, type, flow_id, directive_id):
        doc = {
            "name": name,
            "type": type,
            "parent_id": flow_id,
            "directive_id": directive_id
        }
        return self.variableDaoObj.newVariable(doc)

    # 更新局部变量信息
    def updateLocalVariableInfo(self, flowId, value, type, name, directive_id):
        doc = {
            "flowId": flowId,
            "value": value,
            "name": name,
            "type": type,
            "directive_id": directive_id
        }
        return self.variableDaoObj.updateVariable(doc)

    # 新建全局变量
    def newGlobalVariable(self, type, name):
        doc = {
            "name": name,
            "type": type,
            "parent_id": self._appId
        }
        return self.variableDaoObj.newVariable(doc)

    # 新建全局常量
    def newGlobalConstants(self, type, name, value):
        doc = {
            "name": name,
            "type": type,
            "parent_id": self._appId,
            "value": value
        }
        return self.variableDaoObj.newVariable(doc)

    # 按行号获取可用变量字典
    def getVariableDictByLineNumber(self, flow_id, lineNumber: int):
        variableDict = self.variableDaoObj.getGlobalVariables(self._appId)
        variableDict.update(self.variableDaoObj.getLocalVariablesByLineNumber(flow_id, lineNumber))
        return variableDict

    # 创建指定数据类型对象
    def createSelectedDataTypeObject(self, type, value, flow_id):
        try:
            restrictionDict = {"math": math}
            restrictionDict.update(self.variables["global"])
            restrictionDict.update(self.variables[flow_id])
            print(type)
            if type == 0:
                result = eval(value, {"__builtins__": None}, restrictionDict)
            elif type == 1:
                result = int(eval(value, {"__builtins__": None}, restrictionDict))
                print(restrictionDict)
            elif type == 2:
                result = float(eval(value, {"__builtins__": None}, restrictionDict))
            elif type == 3:
                result = bool(eval(value, {"__builtins__": None}, restrictionDict))
            elif type == 4:
                result = str(value)
            elif type == 5:
                result = str(eval(value, {"__builtins__": None}, restrictionDict))
            else:
                result = None  # todo 写完
            return result
        except Exception as e:
            print(e)
            return None

    # 变量赋值
    def setVariable(self, flow_id, type, name, value):
        flow_id = str(flow_id)
        if flow_id not in self.variables:
            self.variables[flow_id] = {}
        self.variables[flow_id][name] = self.createSelectedDataTypeObject(type, value, flow_id)



    # 读取变量
    def getVariable(self, flow_id, name):
        try:
            flow_id = str(flow_id)
            if name in self.variables[flow_id]:
                return self.variables[flow_id][name]
            elif name in self.variables["global"]:
                return self.variables["global"][name]
            else:
                return None
        except Exception as e:
            return None
