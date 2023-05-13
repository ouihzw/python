# -*- coding:utf-8 -*-
from collections import deque
from PyQt5.QtCore import *


class ActionManager(QObject):
    __instance = None
    _isFirstInit = True
    # 控制撤销、重做按钮的可用性
    undoAvailabilitySignal = pyqtSignal(bool)
    redoAvailabilitySignal = pyqtSignal(bool)

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(ActionManager, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self):
        cls = type(self)
        if cls._isFirstInit:
            super().__init__()
            self.flowDict = {}
            cls._isFirstInit = False

    # 插入双端队列，action：0-创建，1-删除，2-修改，3-移位
    def insertUndoAction(self, flowId, action: int, lineNumber: int, newDirective=None, oldDirective=None):
        flowId = str(flowId)
        if flowId not in self.flowDict:
            self.flowDict[flowId] = [deque(maxlen=50), list()]
        self.flowDict[flowId][0].append([action, lineNumber, newDirective, oldDirective])
        self.flowDict[flowId][1].clear()
        self.redoAvailabilitySignal.emit(False)
        self.undoAvailabilitySignal.emit(True)

    # 点击撤销后从undo双端队列右端pop一项，移入redo列表
    def undo(self, flowId):
        flowId = str(flowId)
        if self.flowDict[flowId][0]:
            action = self.flowDict[flowId][0].pop()
            self.flowDict[flowId][1].append(action)
            if not self.flowDict[flowId][0]:
                self.undoAvailabilitySignal.emit(False)
            self.redoAvailabilitySignal.emit(True)
            return action
        else:
            self.undoAvailabilitySignal.emit(False)
            return None

    # 点击重做后从redo列表右端pop一项，压入undo队列
    def redo(self, flowId):
        flowId = str(flowId)
        if self.flowDict[flowId][1]:
            action = self.flowDict[flowId][1].pop()
            self.flowDict[flowId][0].append(action)
            if not self.flowDict[flowId][1]:
                self.redoAvailabilitySignal.emit(False)
            self.undoAvailabilitySignal.emit(True)
            return action
        else:
            self.redoAvailabilitySignal.emit(False)
            return None

    # 更改当前页面后重新检测撤销重做可用性
    def changeTab(self, flowId):
        flowId = str(flowId)
        if flowId not in self.flowDict:
            self.flowDict[flowId] = [deque(maxlen=50), list()]
            self.undoAvailabilitySignal.emit(False)
            self.redoAvailabilitySignal.emit(False)
        else:
            if self.flowDict[flowId][0]:
                self.undoAvailabilitySignal.emit(True)
            else:
                self.undoAvailabilitySignal.emit(False)
            if self.flowDict[flowId][1]:
                self.redoAvailabilitySignal.emit(True)
            else:
                self.redoAvailabilitySignal.emit(False)
