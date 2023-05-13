# -*- coding:utf-8 -*-W
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowStepWidget
from . import settingWebComboboxObjectSettingDialog
from ....webAutoConstants import WebAutoConstants

class SettingWebComboboxFlowWidget(flowStepWidget.FlowStepWidget):
    def __init__(self, lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent=None):
        super(SettingWebComboboxFlowWidget, self).__init__(lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent)
        self.settingDialog = settingWebComboboxObjectSettingDialog.SettingWebComboboxObjectSettingDialog(flowTitle, self)
        self.directive["command"] = WebAutoConstants.webElementOperationContants.settingWebCheckBoxDirective
        self.directive["data"] = {"browser_type": 0,
                                  "object": 0,
                                  "element": "",
                                  "value": ""}
        self.infoFormat = u"在网页%s中%s下拉%s中等于%s的项"
        self.updateSecondLineInfo()

    def getSettingData(self):
        data = self.parent().getDirectiveSettingDataFromDB(self.directive["_id"])
        self.settingDialog.browserTypeCombobox.setCurrentIndex(data["browser_type"])
        self.settingDialog.objectComboBox.setCurrentIndex(data["object"])
        self.settingDialog.elementLabel.setText(data["element"])
        self.settingDialog.selectValueLineEdit.setText(data["value"])
        self.directive["data"] = data

    def updateSettingData(self):
        data = self.directive["data"]
        data["browser_type"] = self.settingDialog.browserTypeCombobox.currentIndex()
        data["object"] = self.settingDialog.objectComboBox.currentIndex()
        data["element"] = self.settingDialog.elementLabel.text()
        data["value"] = self.settingDialog.selectValueLineEdit.text()
        self.parent().updateDirectiveData2DB(self.directive["_id"], self.directive["data"])
        self.updateSecondLineInfo()

    def updateSecondLineInfo(self, info: tuple = ()):
        data = self.directive["data"]
        super().updateSecondLineInfo((self.settingDialog.browserTypeCombobox.itemText(data["browser_type"]),
                                      self.settingDialog.objectComboBox.itemText(data["object"]),
                                      data["element"],
                                      data["value"]))
