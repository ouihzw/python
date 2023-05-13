# -*- coding:utf-8 -*-
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowStepWidget
from . import gettingWebElementInfoObjectSettingDialog
from ...webDataRetrievingContants import WebDataRetrievingConstants

class GettingWebElementInfoFlowWidget(flowStepWidget.FlowStepWidget):
    def __init__(self, scene, title="Undefined Node", type = " Node ", id = None,inputs=[], outputs=[]):
        super(GettingWebElementInfoFlowWidget, self).__init__(scene, title, type, id, inputs=[1, 2, 3, 4], outputs=[])
        self.directive["line_number"] = 1
        self.directive["command"] = WebDataRetrievingConstants.gettingWebElementInfoDirective
        self.directive["data"] = {"web_object": "",
                                  "element": "",
                                  "operation": 0,
                                  "intelligent_identification": False,
                                  "propert_name": "",
                                  "output": "web_element_attribute",
                                  "time_out": "20",
                                  "log": True,
                                  "handle": 0,
                                  "on_error_output_value": "",
                                  "retry_count": 1,
                                  "retry_interval": 1}
        self.directive["flow_id"] = self.id
        self.directive["_id"] = self.directiveDaoObj.insertDirective(self.directive)
        self.infoFormat = u"%s，目标元素为%s，将结果保存到%s"
        self.dialog = gettingWebElementInfoObjectSettingDialog.GettingWebElementInfoObjectSettingDialog(self.title,self.directive["_id"],self.id)
        self.dialog.confirmButton.clicked.connect(self.updateSettingData)

    def getSettingData(self):
        data = self.parent().getDirectiveSettingDataFromDB(self.directive["_id"])
        self.dialog.webObjectCombobox.setCurrentText(data["web_object"])
        self.dialog.elementLabel.setText(data["element"])
        self.dialog.operationCombobox.setCurrentIndex(data["operation"])
        self.dialog.intelligentIdentificationCheckbox.setChecked(data["intelligent_identification"])
        self.dialog.propertyNameLineEdit.setText(data["propert_name"])
        self.dialog.outputVariableNameLineEdit.setText(data["output"])
        self.dialog.waitElementExistLineEdit.setText(data["time_out"])
        self.dialog.printErrorLogsCheckbox.setChecked(data["log"])
        self.dialog.handleErrorWayCombobox.setCurrentIndex(data["handle"])
        self.dialog.onErrorOutputVariableLineEdit.setText(data["on_error_output_value"])
        self.dialog.retryCountSpinbox.setValue(data["retry_count"])
        self.dialog.retryIntervalSpinbox.setValue(data["retry_interval"])
        self.directive["data"] = data

    def updateSettingData(self):
        data = self.directive["data"]
        data["web_object"] = self.dialog.webObjectCombobox.currentText()
        data["element"] = self.dialog.elementLabel.text()
        data["operation"] = self.dialog.operationCombobox.currentIndex()
        data["intelligent_identification"] = self.dialog.intelligentIdentificationCheckbox.isChecked()
        data["propert_name"] = self.dialog.propertyNameLineEdit.text()
        data["output"] = self.dialog.outputVariableNameLineEdit.text()
        data["time_out"] = self.dialog.waitElementExistLineEdit.text()
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
            self.infoFormat = u"获取元素文本内容，目标元素为%s，将结果保存到%s"
            super().updateSecondLineInfo(("${" + data["element"] + "}","${" + data["output"] + "}"))
        elif data["operation"] == 1:
            self.infoFormat = u"获取元素源代码，目标元素为%s，将结果保存到%s"
            super().updateSecondLineInfo(("${" + data["element"] + "}","${" + data["output"] + "}"))
        elif data["operation"] == 2:
            self.infoFormat = u"获取元素值，目标元素为%s，将结果保存到%s"
            super().updateSecondLineInfo(("${" + data["element"] + "}", "${" + data["output"] + "}"))
        elif data["operation"] == 3:
            self.infoFormat = u"获取网页链接地址，目标元素为%s，将结果保存到%s"
            super().updateSecondLineInfo(("${" + data["element"] + "}", "${" + data["output"] + "}"))
        elif data["operation"] == 4:
            self.infoFormat = u"获取元素属性，目标元素为%s，将结果保存到%s"
            super().updateSecondLineInfo(("${" + data["element"] + "}", "${" + data["output"] + "}"))




