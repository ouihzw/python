# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowStepWidget
from . import fillingInPasswordWebInputObjectSettingDialog
from ....webAutoConstants import WebAutoConstants

class FillingInPasswordWebInputFlowWidget(flowStepWidget.FlowStepWidget):
    def __init__(self, lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent=None):
        super(FillingInPasswordWebInputFlowWidget, self).__init__(lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent)
        self.settingDialog = fillingInPasswordWebInputObjectSettingDialog.FillingInPasswordWebInputObjectSettingDialog(flowTitle, self)
        self.directive["command"] = WebAutoConstants.fillingInWebInputDirective
        self.directive["data"] = {"browser_type": 0,
                                  "element": ""}
        self.infoFormat = u"在网页%s的%s中，模拟人工输入密码"
        self.updateSecondLineInfo()

    def getSettingData(self):
        data = self.parent().getDirectiveSettingDataFromDB(self.directive["_id"])
        self.settingDialog.browserTypeCombobox.setCurrentIndex(data["browser_type"])
        self.settingDialog.elementLabel.setText(data["element"])
        self.directive["data"] = data

    def updateSettingData(self):
        data = self.directive["data"]
        data["browser_type"] = self.settingDialog.browserTypeCombobox.currentIndex()
        data["element"] = self.settingDialog.elementLabel.text()
        self.parent().updateDirectiveData2DB(self.directive["_id"], self.directive["data"])
        self.updateSecondLineInfo()

    def updateSecondLineInfo(self, info: tuple = ()):
        data = self.directive["data"]
        super().updateSecondLineInfo((self.settingDialog.browserTypeCombobox.itemText(data["browser_type"]),
                                      data["element"]))
