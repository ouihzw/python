# -*- coding:utf-8 -*-
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowStepWidget
from . import gettingWebElementObjectSettingDialog
from ....webAutoConstants import WebAutoConstants

class GettingWebElementObjectFlowWidget(flowStepWidget.FlowStepWidget):
    def __init__(self, lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent=None):
        super(GettingWebElementObjectFlowWidget, self).__init__(lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent)
        self.settingDialog = gettingWebElementObjectSettingDialog.GettingWebElementObjectSettingDialog(flowTitle, self)
        self.directive["command"] = WebAutoConstants.webElementOperationContants.settingWebElementValueDirective
        self.directive["data"] = {"browser_type": 0,
                                  "element": "",
                                  "value": ""}
        self.infoFormat = u"获取网%s页中的%s对象,将对象保存到%s"
        self.updateSecondLineInfo()

    def getSettingData(self):
        data = self.parent().getDirectiveSettingDataFromDB(self.directive["_id"])
        self.settingDialog.browserTypeCombobox.setCurrentIndex(data["browser_type"])
        self.settingDialog.elementLabel.setText(data["element"])
        self.settingDialog.elementValueLineEdit.setText(data["value"])
        self.directive["data"] = data

    def updateSettingData(self):
        data = self.directive["data"]
        data["browser_type"] = self.settingDialog.browserTypeCombobox.currentIndex()
        data["element"] = self.settingDialog.elementLabel.text()
        data["value"] = self.settingDialog.elementValueLineEdit.text()
        self.parent().updateDirectiveData2DB(self.directive["_id"], self.directive["data"])
        self.updateSecondLineInfo()

    def updateSecondLineInfo(self, info: tuple = ()):
        data = self.directive["data"]
        super().updateSecondLineInfo((self.settingDialog.browserTypeCombobox.itemText(data["browser_type"]),
                                      data["element"],
                                      data["value"]))

    def mouseDoubleClickEvent(self, event):
        self.settingDialog.show()




