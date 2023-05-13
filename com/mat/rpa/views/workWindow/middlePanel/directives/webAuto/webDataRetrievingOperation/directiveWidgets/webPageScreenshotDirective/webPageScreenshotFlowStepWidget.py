# -*- coding:utf-8 -*-
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowStepWidget
from . import webPageScreenshotObjectSettingDialog
from ...webDataRetrievingContants import WebDataRetrievingConstants

class WebPageScreenshotFlowWidget(flowStepWidget.FlowStepWidget):
    def __init__(self, scene, title="Undefined Node", type = " Node ", id = None,inputs=[], outputs=[]):
        super(WebPageScreenshotFlowWidget, self).__init__(scene, title, type, id, inputs=[1, 2, 3, 4], outputs=[])
        self.directive["command"] = WebDataRetrievingConstants.webPageScreenshotDirective
        self.directive["data"] = {"web_object":"",
                                  "screenshot_area":0,
                                  "element_name":"",
                                  "save_location":False,
                                  "save_location_name":"",
                                  "name":True,
                                  "custom_name":"",
                                  "name_way":True,
                                  "output": "screenshot_save_file_name",
                                  "time_out_period": "20",
                                  "log": True,
                                  "handle": 0,
                                  "on_error_output_value": "",
                                  "retry_count": 1,
                                  "retry_interval": 1}
        self.directive["line_number"] = 1
        self.directive["flow_id"] = self.id
        self.directive["_id"] = self.directiveDaoObj.insertDirective(self.directive)
        self.dialog = webPageScreenshotObjectSettingDialog.WebPageScreenshotObjectSettingDialog(self.title, self.directive["_id"], self.id)
        self.infoFormat = u"在网页中对元素进行截图，将结果保存到文件夹中，将存图路径保存到%s"
        self.dialog.confirmButton.clicked.connect(self.updateSettingData)

    def getSettingData(self):
        data = self.parent().getDirectiveSettingDataFromDB(self.directive["_id"])
        self.dialog.webObjectCombobox.setCurrentText(data["web_object"])
        self.dialog.screenshotAreaCombobox.setCurrentIndex(data["screenshot_area"])
        self.dialog.elementLabel.setText(data["element_name"])
        self.dialog.savePictureToClipboardCheckbox.setChecked(data["save_location"])
        self.dialog.filePathLineEdit.setText(data["save_location_name"])
        self.dialog.useAutomaticRandomFileNamesCheckbox.setChecked(data["name"])
        self.dialog.customFileNameLineEdit.setText(data["custom_name"])
        self.dialog.overwriteIfFileExistsCheckbox.setChecked(data["name_way"])
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
        data["screenshot_area"]=self.dialog.screenshotAreaCombobox.currentIndex()
        data["element_name"]=self.dialog.elementLabel.text()
        data["save_location"]=self.dialog.savePictureToClipboardCheckbox.isChecked()
        data["save_location_name"]=self.dialog.filePathLineEdit.text()
        data["name"]=self.dialog.useAutomaticRandomFileNamesCheckbox.isChecked()
        data["custom_name"]=self.dialog.customFileNameLineEdit.text()
        data["name_way"]=self.dialog.overwriteIfFileExistsCheckbox.isChecked()
        data["output"] = self.dialog.outputVariableNameLineEdit.text()
        data["time_out_period"] = self.dialog.waitForElementAppearLineEdit.text()
        data["log"]=self.dialog.printErrorLogsCheckbox.isChecked()
        data["handle"] = self.dialog.handleErrorWayCombobox.currentIndex()
        data["on_error_output_value"] = self.dialog.onErrorOutputVariableLineEdit.text()
        data["retry_count"] = self.dialog.retryCountSpinbox.value()
        data["retry_interval"] = self.dialog.retryIntervalSpinbox.value()
        self.updateDirectiveData2DB(self.directive["_id"], self.directive["data"])
        self.updateSecondLineInfo()

    def updateSecondLineInfo(self):
        data = self.directive["data"]
        if data["screenshot_area"] == 0:
            if data["save_location"]==True:
                self.infoFormat = u"在网页%s中对%s元素进行截图，将结果保存到剪切板中"
                super().updateSecondLineInfo(("${" + data["web_object"] + "}", data["element_name"]))
            else:
                if data["name"]==True:
                    self.infoFormat = u"在网页%s中对%s元素进行截图，将结果保存到文件夹%s中，为截图自动生成不重复的文件名（以时间戳命名），将存图路径保存到%s"
                    super().updateSecondLineInfo(("${" + data["web_object"] + "}", data["element_name"],data["save_location_name"],"${" + data["output"] + "}"))
                else:
                    self.infoFormat = u"在网页%s中对%s元素进行截图，将结果保存到文件夹%s中，使用自定义文件名%s，将存图路径保存到%s"
                    super().updateSecondLineInfo(("${" + data["web_object"] + "}", data["element_name"],data["save_location_name"], data["custom_name"],"${" + data["output"] + "}",))
        elif data["screenshot_area"] == 1:
            if data["save_location"]==True:
                self.infoFormat = u"对网页%s可视区域进行截图，将结果保存到剪切板中"
                super().updateSecondLineInfo(("${" + data["web_object"] + "}",))
            else:
                if data["name"]==True:
                    self.infoFormat = u"对网页%s可视区域进行截图，将结果保存到文件夹%s中，为截图自动生成不重复的文件名（以时间戳命名），将存图路径保存到%s"
                    super().updateSecondLineInfo(("${" + data["web_object"] + "}",data["save_location_name"],"${" + data["output"] + "}"))
                else:
                    self.infoFormat = u"对网页%s可视区域进行截图，将结果保存到文件夹%s中，使用自定义文件名%s，将存图路径保存到%s"
                    super().updateSecondLineInfo(("${" + data["web_object"] + "}",data["save_location_name"], data["custom_name"],"${" + data["output"] + "}"))
        else:
            if data["save_location"]==True:
                self.infoFormat = u"对整个网页%s进行截图，将结果保存到剪切板中"
                super().updateSecondLineInfo(("${" + data["web_object"] + "}",))
            else:
                if data["name"]==True:
                    self.infoFormat = u"对整个网页%s进行截图，将结果保存到文件夹%s中，为截图自动生成不重复的文件名（以时间戳命名），将存图路径保存到%s"
                    super().updateSecondLineInfo(("${" + data["web_object"] + "}",data["save_location_name"],"${" + data["output"] + "}"))
                else:
                    self.infoFormat = u"对整个网页%s进行截图，将结果保存到文件夹%s中，使用自定义文件名%s，将存图路径保存到%s"
                    super().updateSecondLineInfo(("${" + data["web_object"] + "}",data["save_location_name"], data["custom_name"],"${" + data["output"] + "}"))




