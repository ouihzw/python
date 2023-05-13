# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowStepWidget
from . import settingWebElementPropertyObjectSettingDialog
from ....webAutoConstants import WebAutoConstants

class SettingWebElementPropertyFlowWidget(flowStepWidget.FlowStepWidget):
    def __init__(self, lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent=None):
        super(SettingWebElementPropertyFlowWidget, self).__init__(lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent)
        self.settingDialog = settingWebElementPropertyObjectSettingDialog.SettingWebElementPropertyObjectSettingDialog(flowTitle, self)
        self.directive["command"] = WebAutoConstants.webElementOperationContants.settingWebElementPropertyDirective
        self.directive["data"] = {"browser_type": 0,
                                  "element": "",
                                  "name": "",
                                  "value": ""}
        self.infoFormat = u"在网页%s中设置%s的属性%s值为%s"
        self.updateSecondLineInfo()

    def getSettingData(self):
        data = self.parent().getDirectiveSettingDataFromDB(self.directive["_id"])
        self.settingDialog.browserTypeCombobox.setCurrentIndex(data["browser_type"])
        self.settingDialog.elementLabel.setText(data["element"])
        self.settingDialog.elementPropertyNameLineEdit.setText(data["name"])
        self.settingDialog.elementPropertyValueLineEdit.setText(data["value"])
        self.directive["data"] = data

    def updateSettingData(self):
        data = self.directive["data"]
        data["browser_type"] = self.settingDialog.browserTypeCombobox.currentIndex()
        data["element"] = self.settingDialog.elementLabel.text()
        data["name"] = self.settingDialog.elementPropertyNameLineEdit.text()
        data["value"] = self.settingDialog.elementPropertyValueLineEdit.text()
        self.parent().updateDirectiveData2DB(self.directive["_id"], self.directive["data"])
        self.updateSecondLineInfo()

    def updateSecondLineInfo(self, info: tuple = ()):
        data = self.directive["data"]
        super().updateSecondLineInfo((self.settingDialog.browserTypeCombobox.itemText(data["browser_type"]),
                                      data["element"],
                                      data["name"],
                                      data["value"]))
