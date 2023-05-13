# -*- coding:utf-8 -*-W
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowStepWidget
from . import settingWebCheckBoxObjectSettingDialog
from ....webAutoConstants import WebAutoConstants


class SettingWebCheckBoxFlowWidget(flowStepWidget.FlowStepWidget):
    def __init__(self, scene, title="Undefined Node", type = " Node ", id = None,inputs=[], outputs=[]):
        super(SettingWebCheckBoxFlowWidget, self).__init__(scene, title, type, id, inputs=[1, 2, 3, 4], outputs=[])
        self.directive["line_number"] = 1
        self.directive["command"] = WebAutoConstants.webElementOperationContants.settingWebCheckBoxDirective
        self.directive["data"] = {"browser_type": 0,
                                  "object": 0,
                                  "element": ""}
        self.directive["flow_id"] = self.id
        self.directive["_id"] = self.directiveDaoObj.insertDirective(self.directive)
        self.dialog = settingWebCheckBoxObjectSettingDialog.SettingWebCheckBoxObjectSettingDialog(self.title,
                                                                                              self.directive["_id"],
                                                                                              self.id)

    def getSettingData(self):
        data = self.parent().getDirectiveSettingDataFromDB(self.directive["_id"])
        self.settingDialog.browserTypeCombobox.setCurrentIndex(data["browser_type"])
        self.settingDialog.objectComboBox.setCurrentIndex(data["object"])
        self.settingDialog.elementLabel.setText(data["element"])
        self.directive["data"] = data

    def updateSettingData(self):
        data = self.directive["data"]
        data["browser_type"] = self.settingDialog.browserTypeCombobox.currentIndex()
        data["object"] = self.settingDialog.objectComboBox.currentIndex()
        data["element"] = self.settingDialog.elementLabel.text()
        self.parent().updateDirectiveData2DB(self.directive["_id"], self.directive["data"])
        self.updateSecondLineInfo()

    def updateSecondLineInfo(self, info: tuple = ()):
        data = self.directive["data"]
        super().updateSecondLineInfo((self.settingDialog.browserTypeCombobox.itemText(data["browser_type"]),
                                      self.settingDialog.objectComboBox.itemText(data["object"]),
                                      data["element"]))
