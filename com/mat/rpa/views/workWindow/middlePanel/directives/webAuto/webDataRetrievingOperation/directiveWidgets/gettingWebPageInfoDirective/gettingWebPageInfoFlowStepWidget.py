# -*- coding:utf-8 -*-
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowStepWidget
from . import gettingWebPageInfoObjectSettingDialog
from ...webDataRetrievingContants import WebDataRetrievingConstants

class GettingWebPageInfoFlowWidget(flowStepWidget.FlowStepWidget):
    def __init__(self, scene, title="Undefined Node", type = " Node ", id = None,inputs=[], outputs=[]):
        super(GettingWebPageInfoFlowWidget, self).__init__(scene, title, type, id, inputs=[1, 2, 3, 4], outputs=[])
        self.directive["line_number"] = 1
        self.directive["command"] = WebDataRetrievingConstants. gettingWebPageInfoDirective
        self.directive["data"] = {"web_object": "",
                                  "operation": 0,
                                  "output": "web_page_attribute",
                                  "log": True,
                                  "handle": 0,
                                  "on_error_output_value": "",
                                  "retry_count": 1,
                                  "retry_interval": 1}
        self.infoFormat = u"%s,目标网页为%s，将结果保存到%s"
        self.directive["flow_id"] = self.id
        self.directive["_id"] = self.directiveDaoObj.insertDirective(self.directive)
        self.dialog = gettingWebPageInfoObjectSettingDialog.GettingWebPageInfoObjectSettingDialog(self.title,self.directive["_id"],self.id)
        self.dialog.confirmButton.clicked.connect(self.updateSettingData)

    def getSettingData(self):
        data = self.parent().getDirectiveSettingDataFromDB(self.directive["_id"])
        self.dialog.webObjectCombobox.setCurrentText(data["web_object"])
        self.dialog.operationCombobox.setCurrentIndex(data["operation"])
        self.dialog.outputVariableNameLineEdit.setText(data["output"])
        self.dialog.printErrorLogsCheckbox.setChecked(data["log"])
        self.dialog.handleErrorWayCombobox.setCurrentIndex(data["handle"])
        self.dialog.onErrorOutputVariableLineEdit.setText(data["on_error_output_value"])
        self.dialog.retryCountSpinbox.setValue(data["retry_count"])
        self.dialog.retryIntervalSpinbox.setValue(data["retry_interval"])
        self.directive["data"] = data


    '''
    data["web_object"]:网页对象
    data["operation"]:操作的索引值
    data["output"]:输出结果的变量名
    '''
    def updateSettingData(self):
        data = self.directive["data"]
        data["web_object"] = self.dialog.webObjectCombobox.currentText()
        data["operation"] = self.dialog.operationCombobox.currentIndex()
        data["output"] = self.dialog.outputVariableNameLineEdit.text()
        data["log"] = self.dialog.printErrorLogsCheckbox.isChecked()
        data["handle"] = self.dialog.handleErrorWayCombobox.currentIndex()
        data["on_error_output_value"] = self.dialog.onErrorOutputVariableLineEdit.text()
        data["retry_count"] = self.dialog.retryCountSpinbox.value()
        data["retry_interval"] = self.dialog.retryIntervalSpinbox.value()
        self.updateDirectiveData2DB(self.directive["_id"], self.directive["data"])
        self.updateSecondLineInfo()

    def updateSecondLineInfo(self):
        data = self.directive["data"]
        if data["operation"] == 0:
            self.infoFormat = u"获取网址,目标网页为%s，将结果保存到%s"
            super().updateSecondLineInfo(("${"+data["web_object"]+"}",data["output"]))
        elif data["operation"] == 1:
            self.infoFormat = u"获取网页标题,目标网页为%s，将结果保存到%s"
            super().updateSecondLineInfo(("${"+data["web_object"]+"}",data["output"]))
        elif data["operation"] == 2:
            self.infoFormat = u"获取网页源代码,目标网页为%s，将结果保存到%s"
            super().updateSecondLineInfo(("${"+data["web_object"]+"}",data["output"]))
        elif data["operation"] == 3:
            self.infoFormat = u"获取网页文本内容,目标网页为%s，将结果保存到%s"
            super().updateSecondLineInfo(("${"+data["web_object"]+"}",data["output"]))