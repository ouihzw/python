# -*- coding:utf-8 -*-W
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowStepWidget
from . import waitingForWebElementObjectSettingDialog
from ....webAutoConstants import WebAutoConstants

class WaitingForWebElementFlowWidget(flowStepWidget.FlowStepWidget):
    def __init__(self, lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent=None):
        super(WaitingForWebElementFlowWidget, self).__init__(lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent)
        self.settingDialog = waitingForWebElementObjectSettingDialog.WaitingForWebElementObjectSettingDialog(flowTitle, self)
        self.directive["command"] = WebAutoConstants.webElementOperationContants.waitingForWebElementDirective
        self.directive["data"] = {"browser_type": 0,
                                  "element": "",
                                  "method": 0,
                                  "value": ""}
        self.infoFormat = u"等待网页%s中元素%s%s，最多等待%s秒"
        self.updateSecondLineInfo()

    def getSettingData(self):
        data = self.parent().getDirectiveSettingDataFromDB(self.directive["_id"])
        self.settingDialog.browserTypeCombobox.setCurrentIndex(data["browser_type"])
        self.settingDialog.elementLabel.setText(data["element"])
        self.settingDialog.waitTypeCombobox.setCurrentIndex(data["method"])
        self.settingDialog.waitTimeLineEdit.setText(data["value"])
        self.directive["data"] = data

    def updateSettingData(self):
        data = self.directive["data"]
        data["browser_type"] = self.settingDialog.browserTypeCombobox.currentIndex()
        data["element"] = self.settingDialog.elementLabel.text()
        data["method"] = self.settingDialog.waitTypeCombobox.currentIndex()
        data["value"] = self.settingDialog.waitTimeLineEdit.text()
        self.parent().updateDirectiveData2DB(self.directive["_id"], self.directive["data"])
        self.updateSecondLineInfo()

    def updateSecondLineInfo(self, info: tuple = ()):
        data = self.directive["data"]
        if self.settingDialog.waitCheckbox.isChecked() is True:
            self.infoFormat = u"等待网页%s中元素%s%s，最多等待%s秒"
            super().updateSecondLineInfo((self.settingDialog.browserTypeCombobox.itemText(data["browser_type"]),
                                          data["element"],
                                          self.settingDialog.waitTypeCombobox.itemText(data["method"])[4:],
                                          data["value"]))
        else:
            self.infoFormat = u"一直等待网页%s中元素%s%s"
            super().updateSecondLineInfo((self.settingDialog.browserTypeCombobox.itemText(data["browser_type"]),
                                          data["element"],
                                          self.settingDialog.waitTypeCombobox.itemText(data["method"])[4:]))





