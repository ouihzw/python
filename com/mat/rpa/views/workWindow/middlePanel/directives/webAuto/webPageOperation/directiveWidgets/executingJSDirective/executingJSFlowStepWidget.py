# -*- coding:utf-8 -*-
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowStepWidget
from ...webPageOperationConstants import WebPageOperationConstants
from . import executingJSObjectSettingDialog

class ExecutingJSFlowWidget(flowStepWidget.FlowStepWidget):
    def __init__(self, scene, title="Undefined Node", type = " Node ", id = None,inputs=[], outputs=[]):
        super(ExecutingJSFlowWidget, self).__init__(scene, title, type, id, inputs=[1, 2, 3, 4], outputs=[])
        self.directive["line_number"] = 1
        self.directive["command"] = WebPageOperationConstants.executingJSDirective
        self.directive["data"] = {"web_object":"",
                                  "element_name":"",
                                  "parameter":"",
                                  "javascript":"function(element, input){\n  //在此处编写您的Javascript代码\n  //element表示选择的操作目标(HTML元素)\n  //input表示输入的参数(字符串)\n\n  return null;\n}",
                                  "output": "web_js_result",
                                  "time_out_period": "20",
                                  "log": True,
                                  "handle": 0,
                                  "on_error_output_value": "",
                                  "retry_count": 1,
                                  "retry_interval": 1}
        self.directive["flow_id"] = self.id
        self.directive["_id"] = self.directiveDaoObj.insertDirective(self.directive)
        self.dialog = executingJSObjectSettingDialog.ExecutingJSObjectSettingDialog(self.title,self.directive["_id"],self.id)

    def getSettingData(self):
        data = self.parent().getDirectiveSettingDataFromDB(self.directive["_id"])
        self.dialog.webObjectCombobox.setCurrentText(data["web_object"])
        self.dialog.elementLabel.setText(data["element_name"])
        self.dialog.parameterLineEdit.setText(data["parameter"])
        self.dialog.javascriptFunctionTextEdit.setText(data["javascript"])
        self.dialog.outputVariableNameLineEdit.setText(data["output"])
        self.dialog.waitForElementAppearLineEdit.setText(data["time_out_period"])
        self.dialog.printErrorLogsCheckbox.setChecked(data["log"])
        self.dialog.handleErrorWayCombobox.setCurrentIndex(data["handle"])
        self.dialog.onErrorOutputVariableLineEdit.setText(data["on_error_output_value"])
        self.dialog.retryCountSpinbox.setValue(data["retry_count"])
        self.dialog.retryIntervalSpinbox.setValue(data["retry_interval"])
        self.directive["data"] = data

    def updateSettingData(self):
        data = self.directive["data"]
        data["web_object"] = self.settingDialog.webObjectCombobox.currentText()
        data["element_name"]=self.settingDialog.elementLabel.text()
        data["parameter"]=self.settingDialog.parameterLineEdit.text()
        data["javascript"]=self.settingDialog.javascriptFunctionTextEdit.toPlainText()
        data["output"] = self.settingDialog.outputVariableNameLineEdit.text()
        data["time_out_period"] = self.settingDialog.waitForElementAppearLineEdit.text()
        data["handle"] = self.settingDialog.handleErrorWayCombobox.currentIndex()
        data["on_error_output_value"] = self.settingDialog.onErrorOutputVariableLineEdit.text()
        data["retry_count"] = self.settingDialog.retryCountSpinbox.value()
        data["retry_interval"] = self.settingDialog.retryIntervalSpinbox.value()
        self.parent().updateDirectiveData2DB(self.directive["_id"], self.directive["data"])
        self.updateSecondLineInfo()

    def updateSecondLineInfo(self, info: tuple = ()):
        data = self.directive["data"]
        super().updateSecondLineInfo(("${" + data["web_object"] + "}",data["element_name"],
                                      "${" + data["output"] + "}"))




