# -*- coding:utf-8 -*-
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowStepWidget
from . import gettingWebPageObjectListObjectSettingDialog
from ...webPageOperationConstants import WebPageOperationConstants

class GettingWebPageObjectListFlowWidget(flowStepWidget.FlowStepWidget):
    def __init__(self, scene, title="Undefined Node", type = " Node ", id = None,inputs=[], outputs=[]):
        super(GettingWebPageObjectListFlowWidget, self).__init__(scene, title, type, id, inputs=[1, 2, 3, 4], outputs=[])
        self.directive["line_number"] = 1
        self.directive["command"] = WebPageOperationConstants.gettingWebPageObjectListDirective
        self.directive["data"] = {"browser_type":0,
                                  "match_way": 0,
                                  "title":"",
                                  "url": "",
                                  "match_wildcard": False,
                                  "output": "web_page_list",
                                  "log": True,
                                  "handle": 0,
                                  "on_error_output_value": "",
                                  "retry_count": 1,
                                  "retry_interval": 1}
        self.directive["flow_id"] = self.id
        self.directive["_id"] = self.directiveDaoObj.insertDirective(self.directive)
        self.dialog = gettingWebPageObjectListObjectSettingDialog.GettingWebPageObjectListObjectSettingDialog(self.title, self.directive["_id"], self.id)

    def getSettingData(self):
        data = self.parent().getDirectiveSettingDataFromDB(self.directive["_id"])
        self.settingDialog.browserTypeCombobox.setCurrentIndex(data["browser_type"])
        self.settingDialog.matchWayCombobox.setCurrentIndex(data["match_way"])
        self.settingDialog.titleLineEdit.setText(data["title"])
        self.settingDialog.webLineEdit.setText(data["url"])
        self.settingDialog.matchByWildcardCheckbox.setChecked(data["match_wildcard"])
        self.settingDialog.outputVariableNameLineEdit.setText(data["output"])
        self.settingDialog.printErrorLogsCheckbox.setChecked(data["log"])
        self.settingDialog.handleErrorWayCombobox.setCurrentIndex(data["handle"])
        self.settingDialog.onErrorOutputVariableLineEdit.setText(data["on_error_output_value"])
        self.settingDialog.retryCountSpinbox.setValue(data["retry_count"])
        self.settingDialog.retryIntervalSpinbox.setValue(data["retry_interval"])
        self.directive["data"] = data

    def updateSettingData(self):
        data = self.directive["data"]
        data["browser_type"] = self.settingDialog.browserTypeCombobox.currentIndex()
        data["match_way"] = self.settingDialog.matchWayCombobox.currentIndex()
        data["title"] = self.settingDialog.titleLineEdit.text()
        data["url"]= self.settingDialog.webLineEdit.text()
        data["match_wildcard"] = self.settingDialog.matchByWildcardCheckbox.isChecked()
        data["output"] = self.settingDialog.outputVariableNameLineEdit.text()
        data["log"] = self.settingDialog.printErrorLogsCheckbox.isChecked()
        data["handle"] = self.settingDialog.handleErrorWayCombobox.currentIndex()
        data["on_error_output_value"] = self.settingDialog.onErrorOutputVariableLineEdit.text()
        data["retry_count"] = self.settingDialog.retryCountSpinbox.value()
        data["retry_interval"] = self.settingDialog.retryIntervalSpinbox.value()
        self.parent().updateDirectiveData2DB(self.directive["_id"], self.directive["data"])
        self.updateSecondLineInfo()

    def updateSecondLineInfo(self, info: tuple = ()):
        data = self.directive["data"]
        if data["match_way"] == 0:
            self.infoFormat = u"在%s中筛选所有已打开的网页列表，将该列表保存到%s"
            super().updateSecondLineInfo((self.settingDialog.browserTypeCombobox.itemText(data["browser_type"]),
                                          "${" + data["output"] + "}",))
        elif data["match_way"] == 1:
            self.infoFormat = u"在%s中根据标题%s筛选已打开的网页列表，将该列表保存到%s"
            super().updateSecondLineInfo((self.settingDialog.browserTypeCombobox.itemText(data["browser_type"]),
                                          data["title"],"${" + data["output"] + "}",))
        else:
            self.infoFormat = u"在%s中根据网址%s筛选已打开的网页列表，将该列表保存到%s"
            super().updateSecondLineInfo((self.settingDialog.browserTypeCombobox.itemText(data["browser_type"]),
                                          data["url"], "${" + data["output"] + "}",))

