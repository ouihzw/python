# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowStepWidget
from . import ifWebElementVisibleObjectSettingDialog
from ...conditionConstants import ConditionConstants

class IfWebElementVisibleFlowWidget(flowStepWidget.FlowStepWidget):
    isFirstShow = True
    def __init__(self, lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent=None):
        super().__init__(lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent)
        self.settingDialog = ifWebElementVisibleObjectSettingDialog.IfWebElementVisibleObjectSettingDialog(flowTitle,
                                                                                                           self)
        self.infoPanel.imgLabel.setPixmap(QPixmap(self.picPath + "ifContainBig.png").scaled(23, 19))
        self.directive["command"] = ConditionConstants.ifWebElementVisibleDirective
        self.directive["data"] = {"web_page": "",
                                  "detect": 0,
                                  "element": ""}
        self.infoFormat = u"检测网页%s中，元素%s是否%s"
        self.updateSecondLineInfo()

    def showEvent(self, a0: QShowEvent) -> None:
        if self.isFirstShow:
            self.isFirstShow = False
            self.parent().insertWidget(int(self.lineNumberLabel.text()), "leaf|endIfDirective|End If", self.indentLevel)
        super().showEvent(a0)

    def getSettingData(self):
        data = self.parent().getDirectiveSettingDataFromDB(self.directive["_id"])
        self.settingDialog.webPageObjectComboBox.setCurrentText(data["web_page"])
        self.settingDialog.detectComboBox.setCurrentIndex(data["detect"])
        self.settingDialog.elementLineEdit.setText(data["element"])
        self.directive["data"] = data

    def updateSettingData(self):
        self.directive["data"]["web_page"] = self.settingDialog.webPageObjectComboBox.currentText()
        self.directive["data"]["detect"] = self.settingDialog.detectComboBox.currentIndex()
        self.directive["data"]["element"] = self.settingDialog.elementLineEdit.text()
        self.parent().updateDirectiveData2DB(self.directive["_id"], self.directive["data"])
        self.updateSecondLineInfo()

    def updateSecondLineInfo(self, info: tuple = ()):
        super().updateSecondLineInfo((self.directive["data"]["web_page"],
                                      self.directive["data"]["element"],
                                      self.settingDialog.detectComboBox.itemText(self.directive["data"]["detect"])))