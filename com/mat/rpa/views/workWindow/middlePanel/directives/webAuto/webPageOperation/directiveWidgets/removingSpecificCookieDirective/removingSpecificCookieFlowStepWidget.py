# -*- coding:utf-8 -*-
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowStepWidget
from . import removingSpecificCookieObjectSettingDialog
from ...webPageOperationConstants import WebPageOperationConstants

class RemovingSpecificCookieFlowWidget(flowStepWidget.FlowStepWidget):
    def __init__(self, scene, title="Undefined Node", type = " Node ", id = None,inputs=[], outputs=[]):
        super(RemovingSpecificCookieFlowWidget, self).__init__(scene, title, type, id, inputs=[1, 2, 3, 4], outputs=[])
        self.directive["line_number"] = 1
        self.directive["command"] = WebPageOperationConstants.removingSpecificCookieDirective
        self.directive["data"] = {"setting_mode": 0,
                                  "web_object": "",
                                  "browser_type": 0,
                                  "cookie_url": "",
                                  "cookie_name": "",
                                  "log": True,
                                  "handle": 0,
                                  "retry_count": 1,
                                  "retry_interval": 1}
        self.directive["flow_id"] = self.id
        self.directive["_id"] = self.directiveDaoObj.insertDirective(self.directive)
        self.dialog = removingSpecificCookieObjectSettingDialog.RemovingSpecificCookieObjectSettingDialog(self.title, self.directive["_id"], self.id)

    def getSettingData(self):
        data = self.parent().getDirectiveSettingDataFromDB(self.directive["_id"])
        self.settingDialog.urlSpecificationMethodCombobox.setCurrentIndex(data["setting_mode"])
        self.settingDialog.webObjectCombobox.setCurrentText(data["web_object"])
        self.settingDialog.browserTypeCombobox.setCurrentIndex(data["browser_type"])
        self.settingDialog.cookieUrlLineEdit.setText(data["cookie_url"])
        self.settingDialog.cookieNameLineEdit.setText(data["cookie_name"])
        self.settingDialog.printErrorLogsCheckbox.setChecked(data["log"])
        self.settingDialog.handleErrorWayCombobox.setCurrentIndex(data["handle"])
        self.settingDialog.retryCountSpinbox.setValue(data["retry_count"])
        self.settingDialog.retryIntervalSpinbox.setValue(data["retry_interval"])
        self.directive["data"] = data

    def updateSettingData(self):
        data = self.directive["data"]
        data["setting_mode"] = self.settingDialog.urlSpecificationMethodCombobox.currentIndex()
        data["web_object"] = self.settingDialog.webObjectCombobox.currentText()
        data["browser_type"] = self.settingDialog.browserTypeCombobox.currentIndex()
        data["cookie_url"] = self.settingDialog.cookieUrlLineEdit.text()
        data["cookie_name"] = self.settingDialog.cookieNameLineEdit.text()
        data["log"] = self.settingDialog.printErrorLogsCheckbox.isChecked()
        data["handle"] = self.settingDialog.handleErrorWayCombobox.currentIndex()
        data["retry_count"] = self.settingDialog.retryCountSpinbox.value()
        data["retry_interval"] = self.settingDialog.retryIntervalSpinbox.value()
        self.parent().updateDirectiveData2DB(self.directive["_id"], self.directive["data"])
        self.updateSecondLineInfo()

    def updateSecondLineInfo(self, info: tuple = ()):
        data = self.directive["data"]
        if data["setting_mode"] == 0:
            self.infoFormat = u"移除网页%s中cookie名称为%s的cookie"
            super().updateSecondLineInfo(("${" + data["web_object"] + "}", data["cookie_name"]))
        elif data["setting_mode"] == 1:
            self.infoFormat = u"移除cookie url为%s、cookie名称为%s的cookie"
            super().updateSecondLineInfo((data["cookie_url"], data["cookie_name"]))



