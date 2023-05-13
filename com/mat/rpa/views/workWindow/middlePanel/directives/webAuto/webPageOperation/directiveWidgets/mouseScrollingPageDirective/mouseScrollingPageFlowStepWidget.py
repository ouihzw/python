# -*- coding:utf-8 -*-
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowStepWidget
from . import mouseScrollingPageObjectSettingDialog
from ...webPageOperationConstants import WebPageOperationConstants

class MouseScrollingPageFlowWidget(flowStepWidget.FlowStepWidget):
    def __init__(self, scene, title="Undefined Node", type = " Node ", id = None,inputs=[], outputs=[]):
        super(MouseScrollingPageFlowWidget, self).__init__(scene, title, type, id, inputs=[1, 2, 3, 4], outputs=[])
        self.directive["command"] = WebPageOperationConstants.mouseScrollingPageDirective
        self.directive["data"] = {"web_object": "",
                                  "scroll_range": False,
                                  "element":"",
                                  "element_scroller":False,
                                  "scroller_position": 0,
                                  "abscissa": "0",
                                  "ordinate": "0",
                                  "scroller_effect":0,
                                  "time_out":"20",
                                  "log": True,
                                  "handle": 0,
                                  "retry_count": 1,
                                  "retry_interval": 1}
        self.directive["line_number"] = 1
        self.directive["flow_id"] = self.id
        self.directive["_id"] = self.directiveDaoObj.insertDirective(self.directive)
        self.dialog = mouseScrollingPageObjectSettingDialog.MouseScrollingPageObjectSettingDialog(self.title, self.directive["_id"], self.id)

    def getSettingData(self):
        data = self.dialog.getDirectiveSettingDataFromDB(self.directive["_id"])
        self.dialog.webObjectCombobox.setCurrentText(data["web_object"])
        self.dialog.scrollOverSpecifiedElementCheckbox.setChecked(data["scroll_range"])
        self.dialog.elementLabel.setText(data["element"])
        self.dialog.elementHasNoScrollerCheckbox.setChecked(data["element_scroller"])
        self.dialog.scrollPositionCombobox.setCurrentIndex(data["scroller_position"])
        self.dialog.abscissaLineEdit.setText(data["abscissa"])
        self.dialog.ordinateLineEdit.setText(data["ordinate"])
        self.dialog.scrollEffectCombobox.setCurrentIndex(data["scroller_effect"])
        self.dialog.waitElementExistLineEdit.setText(data["time_out"])
        self.dialog.printErrorLogsCheckbox.setChecked(data["log"])
        self.dialog.handleErrorWayCombobox.setCurrentIndex(data["handle"])
        self.dialog.retryCountSpinbox.setValue(data["retry_count"])
        self.dialog.retryIntervalSpinbox.setValue(data["retry_interval"])
        self.directive["data"] = data

    def updateSettingData(self):
        data = self.directive["data"]
        data["web_object"] = self.settingDialog.webObjectCombobox.currentText()
        data["scroll_range"]=self.settingDialog.scrollOverSpecifiedElementCheckbox.isChecked()
        data["element"]=self.settingDialog.elementLabel.text()
        data["element_scroller"]= self.settingDialog.elementHasNoScrollerCheckbox.isChecked()
        data["scroller_position"]=self.settingDialog.scrollPositionCombobox.currentIndex()
        data["abscissa"]=self.settingDialog.abscissaLineEdit.text()
        data["ordinate"]=self.settingDialog.ordinateLineEdit.text()
        data["scroller_effect"]=self.settingDialog.scrollEffectCombobox.currentIndex()
        data["time_out"]=self.settingDialog.waitElementExistLineEdit.text()
        data["log"] = self.settingDialog.printErrorLogsCheckbox.isChecked()
        data["handle"] = self.settingDialog.handleErrorWayCombobox.currentIndex()
        data["retry_count"] = self.settingDialog.retryCountSpinbox.value()
        data["retry_interval"] = self.settingDialog.retryIntervalSpinbox.value()
        self.parent().updateDirectiveData2DB(self.directive["_id"], self.directive["data"])
        self.updateSecondLineInfo()

    def updateSecondLineInfo(self, info: tuple = ()):
        data = self.directive["data"]
        if data["scroll_range"] == False:
            if data["scroller_position"]==2:
                self.infoFormat = u"在网页%s中将鼠标%s（%s，%s），滚动效果为%s"
                super().updateSecondLineInfo(("${" + data["web_object"] + "}",
                                              self.settingDialog.scrollPositionCombobox.itemText(
                                                  data["scroller_position"]), data["abscissa"], data["ordinate"],
                                              self.settingDialog.scrollEffectCombobox.itemText(
                                                  data["scroller_effect"])))
            else:
                self.infoFormat = u"在网页%s中将鼠标%s，滚动效果为%s"
                super().updateSecondLineInfo(("${" + data["web_object"] + "}",
                                              self.settingDialog.scrollPositionCombobox.itemText(
                                                  data["scroller_position"]),
                                              self.settingDialog.scrollEffectCombobox.itemText(
                                                  data["scroller_effect"])))
        else:
            if data["scroller_position"]==2:
                self.infoFormat = u"在网页%s中的元素%s上将鼠标%s（%s，%s），滚动效果为%s"
                super().updateSecondLineInfo(("${" + data["web_object"] + "}",data["element"],
                                              self.settingDialog.scrollPositionCombobox.itemText(
                                                  data["scroller_position"]), data["abscissa"], data["ordinate"],
                                              self.settingDialog.scrollEffectCombobox.itemText(
                                                  data["scroller_effect"])))
            else:
                self.infoFormat = u"在网页%s中的元素%s上将鼠标%s，滚动效果为%s"
                super().updateSecondLineInfo(("${" + data["web_object"] + "}",data["element"],
                                              self.settingDialog.scrollPositionCombobox.itemText(
                                                  data["scroller_position"]),
                                              self.settingDialog.scrollEffectCombobox.itemText(
                                                  data["scroller_effect"])))






