# -*- coding:utf-8 -*-
from PyQt5.QtGui import *
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowStepWidget
from . import forCircleDialog
from com.mat.rpa.views.workWindow.middlePanel.directives.condition.conditionConstants import ConditionConstants

class ForCircleWidget(flowStepWidget.FlowStepWidget):
    isFirstShow = True
    def __init__(self, lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent=None):
        super().__init__(lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent)
        self.settingDialog = forCircleDialog.IfConditionObjectSettingDialog(flowTitle, self)
        self.infoPanel.imgLabel.setPixmap(QPixmap(self.picPath + "ifConditionBig.png").scaled(23, 19))
        self.directive["command"] = ConditionConstants.ifConditionDirective
        self.directive["data"] = {"obj1": "",
                                  "relation": "等于",
                                  "obj2": ""}
        self.infoFormat = u"如果%s%s%s，则执行以下操作"
        self.updateSecondLineInfo()

    def showEvent(self, a0: QShowEvent) -> None:
        if self.isFirstShow:
            self.isFirstShow = False
            self.parent().insertWidget(int(self.lineNumberLabel.text()), "leaf|endIfDirective|End If", self.indentLevel)
        super().showEvent(a0)

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
