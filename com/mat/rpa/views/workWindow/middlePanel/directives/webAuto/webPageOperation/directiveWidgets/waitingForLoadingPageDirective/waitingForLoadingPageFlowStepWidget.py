# -*- coding:utf-8 -*-
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowStepWidget
from . import waitingForLoadingPageObjectSettingDialog
from ...webPageOperationConstants import WebPageOperationConstants

class WaitingForLoadingPageFlowWidget(flowStepWidget.FlowStepWidget):
    def __init__(self, scene, title="Undefined Node", type = " Node ", id = None,inputs=[], outputs=[]):
        super(WaitingForLoadingPageFlowWidget, self).__init__(scene, title, type, id, inputs=[1, 2, 3, 4], outputs=[])
        self.directive["line_number"] = 1
        self.directive["flow_id"] = self.id
        self.directive["command"] = WebPageOperationConstants.waitingForLoadingPageDirective
        self.directive["data"] = {"web_object": "",
                                  "time_out": "20",
                                  "execute_error": 0,
                                  "log": True,
                                  "handle": 0,
                                  "retry_count": 1,
                                  "retry_interval": 1}
        self.directive["_id"] = self.directiveDaoObj.insertDirective(self.directive)
        self.dialog = waitingForLoadingPageObjectSettingDialog.WaitingForLoadingPageObjectSettingDialog(self.title, self.directive["_id"], self.id)
        self.infoFormat = u"等待网页%s加载完成，等待时间%s秒"


    def getSettingData(self):
        data = self.parent().getDirectiveSettingDataFromDB(self.directive["_id"])
        self.settingDialog.webObjectCombobox.setCurrentText(data["web_object"])
        self.settingDialog.webLoadTimeOutPeriodLineEdit.setText(data["time_out"])
        self.settingDialog.executeAfterLoadTimesOutCombobox.setCurrentIndex(data["execute_error"])
        self.settingDialog.printErrorLogsCheckbox.setChecked(data["log"])
        self.settingDialog.handleErrorWayCombobox.setCurrentIndex(data["handle"])
        self.settingDialog.retryCountSpinbox.setValue(data["retry_count"])
        self.settingDialog.retryIntervalSpinbox.setValue(data["retry_interval"])
        self.directive["data"] = data

    def updateSettingData(self):
        data = self.directive["data"]
        data["web_object"] = self.settingDialog.webObjectCombobox.currentText()
        data["time_out"] = self.settingDialog.webLoadTimeOutPeriodLineEdit.text()
        data["execute_error"] = self.settingDialog.executeAfterLoadTimesOutCombobox.currentIndex()
        data["log"] = self.settingDialog.printErrorLogsCheckbox.isChecked()
        data["handle"] = self.settingDialog.handleErrorWayCombobox.currentIndex()
        data["retry_count"] = self.settingDialog.retryCountSpinbox.value()
        data["retry_interval"] = self.settingDialog.retryIntervalSpinbox.value()
        self.parent().updateDirectiveData2DB(self.directive["_id"], self.directive["data"])
        self.updateSecondLineInfo()






