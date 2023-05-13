# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowStepWidget
from . import ifWindowExistsObjectSettingDialog
from ...conditionConstants import ConditionConstants

class IfWindowExistsFlowWidget(flowStepWidget.FlowStepWidget):
    isFirstShow = True

    def __init__(self, lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent=None):
        super().__init__(lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent)
        self.settingDialog = ifWindowExistsObjectSettingDialog.IfWindowExistsObjectSettingDialog(flowTitle, self)
        self.infoPanel.imgLabel.setPixmap(QPixmap(self.picPath + "ifContainBig.png").scaled(23, 19))
        self.directive["command"] = ConditionConstants.ifWindowExistsDirective
        self.directive["data"] = {"method": 0,
                                  "window": "",
                                  "element": "",
                                  "window_title": "",
                                  "checkbox": [False, False],
                                  "window_handle": "",
                                  "exist": 0}
        self.infoFormat = "检测%s %s%s是否%s"
        self.updateSecondLineInfo()

    def showEvent(self, a0: QShowEvent) -> None:
        if self.isFirstShow:
            self.isFirstShow = False
            self.parent().insertWidget(int(self.lineNumberLabel.text()), "leaf|endIfDirective|End If", self.indentLevel)
        super().showEvent(a0)

    def getSettingData(self):
        data = self.parent().getDirectiveSettingDataFromDB(self.directive["_id"])
        self.settingDialog.getWindowMethodComboBox.setCurrentIndex(data["method"])
        self.settingDialog.windowObjectComboBox.setCurrentText(data["window"])
        self.settingDialog.elementLineEdit.setText(data["element"])
        self.settingDialog.windowTitleComboBox.setCurrentText(data["window_title"])
        self.settingDialog.addWindowType.setChecked(data["checkbox"][0])
        self.settingDialog.wildCard.setChecked(data["checkbox"][1])
        self.settingDialog.windowHandleLineEdit.setText(data["window_handle"])
        self.settingDialog.existComboBox.setCurrentIndex(data["exist"])
        self.directive["data"] = data

    def updateSettingData(self):
        data = self.directive["data"]
        data["method"] = self.settingDialog.getWindowMethodComboBox.currentIndex()
        data["window"] = self.settingDialog.windowObjectComboBox.currentText()
        data["element"] = self.settingDialog.elementLineEdit.text()
        data["window_title"] = self.settingDialog.windowTitleComboBox.currentText()
        data["checkbox"] = [self.settingDialog.addWindowType.isChecked(),
                            self.settingDialog.wildCard.isChecked()]
        data["window_handle"] = self.settingDialog.windowHandleLineEdit.text()
        data["exist"] = self.settingDialog.existComboBox.currentIndex()
        self.parent().updateDirectiveData2DB(self.directive["_id"], self.directive["data"])
        self.updateSecondLineInfo()

    def updateSecondLineInfo(self, info: tuple = ()):
        behind = ""
        data = self.directive["data"]
        if data["method"] == 0:
            method = u"窗口"
            target = data["window"]
        elif data["method"] == 1:
            method = u"元素"
            target = data["element"]
            behind = u" 所在窗口"
        elif data["method"] == 2:
            method = u"窗口标题"
            target = data["window_title"]
        else:
            method = u"句柄为"
            target = data["window_handle"]
        super().updateSecondLineInfo((method, target, behind,
                                      self.settingDialog.existComboBox.itemText(data["exist"])))