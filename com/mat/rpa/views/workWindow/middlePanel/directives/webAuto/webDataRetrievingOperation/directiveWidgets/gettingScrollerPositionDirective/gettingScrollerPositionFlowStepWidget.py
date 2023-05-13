# -*- coding:utf-8 -*-
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowStepWidget
from . import gettingScrollerPositionObjectSettingDialog
from ...webDataRetrievingContants import WebDataRetrievingConstants


class GettingScrollerPositionFlowWidget(flowStepWidget.FlowStepWidget):
    def __init__(self, scene, title="Undefined Node", type = " Node ", id = None,inputs=[], outputs=[]):
        super(GettingScrollerPositionFlowWidget, self).__init__(scene, title, type, id, inputs=[1, 2, 3, 4], outputs=[])
        self.directive["command"] = WebDataRetrievingConstants.gettingScrollerPositionDirective
        self.directive["data"] = {"web_object":"",
                                  "element_Scroller":False,
                                  "element_name":"",
                                  "autoSearch":False,
                                  "Scroller_chosen":0,
                                  "position_chosen":0,
                                  "output":"scroll_value",
                                  "time_out_period": "20",
                                  "log": True,
                                  "handle": 0,
                                  "on_error_output_value": "",
                                  "retry_count": 1,
                                  "retry_interval": 1}
        self.directive["line_number"] = 1
        self.directive["flow_id"] = self.id
        self.directive["_id"] = self.directiveDaoObj.insertDirective(self.directive)
        self.dialog = gettingScrollerPositionObjectSettingDialog.GettingScrollerPositionObjectSettingDialog(self.title,self.directive["_id"],self.id)
        self.infoFormat = u"获取网页%s的%s，将滚动条位置保存到%s"
        self.dialog.confirmButton.clicked.connect(self.updateSettingData)


    def getSettingData(self):
        data = self.parent().getDirectiveSettingDataFromDB(self.directive["_id"])
        self.dialog.webObjectCombobox.setCurrentText(data["web_object"])
        self.dialog.elementScrollerCheckBox.setChecked(data["element_Scroller"])
        self.dialog.elementLabel.setText(data["element_name"])
        self.dialog.elementHasNoScrollerCheckBox.setChecked(data["autoSearch"])
        self.dialog.scrollerCombobox.setCurrentIndex(data["Scroller_chosen"])
        self.dialog.positionCombobox.setCurrentIndex(data["position_chosen"])
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
        data["web_object"] = self.dialog.webObjectCombobox.currentText()
        data["element_Scroller"] = self.dialog.elementScrollerCheckBox.isChecked()
        data["element_name"] = self.dialog.elementLabel.text()
        data["autoSearch"] = self.dialog.elementHasNoScrollerCheckBox.isChecked()
        data["Scroller_chosen"] = self.dialog.scrollerCombobox.currentIndex()
        data["position_chosen"] = self.dialog.positionCombobox.currentIndex()
        data["output"] = self.dialog.outputVariableNameLineEdit.text()
        data["time_out_period"] = self.dialog.waitForElementAppearLineEdit.text()
        data["log"] = self.dialog.printErrorLogsCheckbox.isChecked()
        data["handle"] = self.dialog.handleErrorWayCombobox.currentIndex()
        data["on_error_output_value"] = self.dialog.onErrorOutputVariableLineEdit.text()
        data["retry_count"] = self.dialog.retryCountSpinbox.value()
        data["retry_interval"] = self.dialog.retryIntervalSpinbox.value()
        self.updateDirectiveData2DB(self.directive["_id"],self.directive["data"])
        self.updateSecondLineInfo()


    def updateSecondLineInfo(self):
        data = self.directive["data"]
        scroller_trans = {0:"纵向滚动条",1:"横向滚动条"}
        position_trans = {0:"当前位置",1:"底部位置"}
        #选中之后将是元素+某一个滚动条
        if data["element_Scroller"] == True:
            if data["autoSearch"] == False:
                self.infoFormat = u"获取元素%s%s的%s，将滚动条位置保存到%s"
                super().updateSecondLineInfo(("${"+data["element_name"]+"}",scroller_trans[data["Scroller_chosen"]],position_trans[data["position_chosen"]],"${"+data["output"]+"}"))
            else:
                self.infoFormat = u"获取元素%s%s的%s(若当前元素无滚动条，则自动向上查找)，将滚动条位置保存到%s"
                super().updateSecondLineInfo(("${" + data["element_name"] + "}" , scroller_trans[data["Scroller_chosen"]],position_trans[data["position_chosen"]], "${" + data["output"] + "}"))
        else:
            self.infoFormat = u"获取网页%s%s的%s，将滚动条位置保存到%s"
            super().updateSecondLineInfo(("${" + data["web_object"] + "}" , scroller_trans[data["Scroller_chosen"]],position_trans[data["position_chosen"]], "${" + data["output"] + "}"))
