# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowStepWidget
from . import ifWindowContainsObjectSettingDialog
from ...conditionConstants import ConditionConstants

class IfWindowContainsFlowWidget(flowStepWidget.FlowStepWidget):
    isFirstShow = True
    def __init__(self, lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent=None):
        super().__init__(lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent)
        self.settingDialog = ifWindowContainsObjectSettingDialog.IfWindowContainsObjectSettingDialog(flowTitle, self)
        self.infoPanel.imgLabel.setPixmap(QPixmap(self.picPath + "ifContainBig.png").scaled(23, 19))
        self.directive["command"] = ConditionConstants.ifWindowContainsDirective
        self.directive["data"] = {"window": "",
                                  "detect": 0,
                                  "element": ""}
        self.infoFormat = u"检测窗口%s中是否%s%s"
        self.updateSecondLineInfo()

    def showEvent(self, a0: QShowEvent) -> None:
        if self.isFirstShow:
            self.isFirstShow = False
            self.parent().insertWidget(int(self.lineNumberLabel.text()), "leaf|endIfDirective|End If", self.indentLevel)
        super().showEvent(a0)

    def getSettingData(self):
        data = self.parent().getDirectiveSettingDataFromDB(self.directive["_id"])
        self.settingDialog.windowObjectComboBox.setCurrentText(data["window"])
        self.settingDialog.detectComboBox.setCurrentIndex(data["detect"])
        self.settingDialog.elementLineEdit.setText(data["element"])
        self.directive["data"] = data

    def updateSettingData(self):
        data = self.directive["data"]
        data["window"] = self.settingDialog.windowObjectComboBox.currentText()
        data["detect"] = self.settingDialog.detectComboBox.currentIndex()
        data["element"] = self.settingDialog.elementLineEdit.text()
        self.parent().updateDirectiveData2DB(self.directive["_id"], self.directive["data"])
        self.updateSecondLineInfo()

    def updateSecondLineInfo(self, info: tuple = ()):
        super().updateSecondLineInfo((self.directive["data"]["window"],
                                      self.settingDialog.detectComboBox.itemText(self.directive["data"]["detect"]),
                                      self.directive["data"]["element"]))