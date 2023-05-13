# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowStepWidget
from . import elseIfObjectSettingDialog
from ...conditionConstants import ConditionConstants

class ElseIfFlowWidget(flowStepWidget.FlowStepWidget):
    def __init__(self, lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent=None):
        if indentLevel > 1:
            indentLevel -= 1
        super().__init__(lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent)
        self.settingDialog = elseIfObjectSettingDialog.ElseIfObjectSettingDialog(flowTitle, self)
        self.infoPanel.imgLabel.setPixmap(QPixmap(self.picPath + "elseIfBig.png").scaled(23, 19))
        self.directive["command"] = ConditionConstants.elseIfDirective
        self.directive["data"] = {"obj1": "",
                                  "relation": "等于",
                                  "obj2": ""}
        self.infoFormat = "如果%s%s%s，则执行以下操作"
        self.updateSecondLineInfo()

    def setIndentLevel(self, indentLevel):
        if indentLevel > 1:
            indentLevel -= 1
        super().setIndentLevel(indentLevel)

    # 从数据库读取设置信息
    def getSettingData(self):
        data = self.parent().getDirectiveSettingDataFromDB(self.directive["_id"])
        self.settingDialog.objectOneComboBox.setCurrentText(data["obj1"])
        self.settingDialog.relationComboBox.setCurrentText(data["relation"])
        self.settingDialog.objectTwoComboBox.setCurrentText(data["obj2"])
        self.directive["data"] = data

    # 将设置信息更新到数据库
    def updateSettingData(self):
        self.directive["data"]["obj1"] = self.settingDialog.objectOneComboBox.currentText()
        self.directive["data"]["relation"] = self.settingDialog.relationComboBox.currentText()
        self.directive["data"]["obj2"] = self.settingDialog.objectTwoComboBox.currentText()
        self.parent().updateDirectiveData2DB(self.directive["_id"], self.directive["data"])
        self.updateSecondLineInfo()

    # 重写面板信息更新函数，重新组织显示信息
    def updateSecondLineInfo(self, info: tuple = ()):
        super().updateSecondLineInfo((self.directive["data"]["obj1"],
                                      self.directive["data"]["relation"],
                                      self.directive["data"]["obj2"]))

    def isEnd(self):
        return 1