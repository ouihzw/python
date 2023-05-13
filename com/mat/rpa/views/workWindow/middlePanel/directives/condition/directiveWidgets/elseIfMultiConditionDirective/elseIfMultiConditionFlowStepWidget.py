# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowStepWidget
from . import elseIfMultiConditionObjectSettingDialog
from ...conditionConstants import ConditionConstants

class ElseIfMultiConditionFlowWidget(flowStepWidget.FlowStepWidget):
    def __init__(self, lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent=None):
        if indentLevel > 1:
            indentLevel -= 1
        super().__init__(lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent)
        self.settingDialog = elseIfMultiConditionObjectSettingDialog.ElseIfMultiConditionObjectSettingDialog(flowTitle,
                                                                                                             self)
        self.infoPanel.imgLabel.setPixmap(QPixmap(self.picPath + "elseIfBig.png").scaled(23, 19))
        self.directive["command"] = ConditionConstants.ifMultiConditionDirective
        self.directive["data"] = {"condition_relation": 0,
                                  "conditions": [["", "等于", ""]]}
        self.infoFormat = u"满足%s条件%s，则执行以下操作"
        self.updateSecondLineInfo()

    def setIndentLevel(self, indentLevel):
        if indentLevel > 1:
            indentLevel -= 1
        super().setIndentLevel(indentLevel)

    def getSettingData(self):
        data = self.parent().getDirectiveSettingDataFromDB(self.directive["_id"])
        self.settingDialog.relationComboBox.setCurrentIndex(data["condition_relation"])
        count = len(data["conditions"])
        self.settingDialog.setNumberedConditions(count)
        for i in range(count):
            self.settingDialog.innerWidgetVLayout.itemAt(i).widget().setCondition(data["conditions"][i])
        self.directive["data"] = data

    def updateSettingData(self):
        self.directive["data"]["condition_relation"] = self.settingDialog.relationComboBox.currentIndex()
        self.directive["data"]["conditions"] = []
        for i in range(self.settingDialog.innerWidgetVLayout.count()):
            self.directive["data"]["conditions"].append(
                self.settingDialog.innerWidgetVLayout.itemAt(i).widget().getCondition())
        self.parent().updateDirectiveData2DB(self.directive["_id"], self.directive["data"])
        self.updateSecondLineInfo()

    def updateSecondLineInfo(self, info: tuple = ()):
        text = []
        if self.directive["data"]["condition_relation"] == 0:
            text.append("全部")
        else:
            text.append("任一")
        conditions = []
        for item in self.directive["data"]["conditions"]:
            conditions.append("".join(item))
        text.append("; ".join(conditions))
        super().updateSecondLineInfo(tuple(text))

    def isEnd(self):
        return 1