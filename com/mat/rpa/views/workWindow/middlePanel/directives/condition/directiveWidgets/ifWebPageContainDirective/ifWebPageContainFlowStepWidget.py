# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowStepWidget
from . import ifWebPageContainObjectSettingDialog
from ...conditionConstants import ConditionConstants


class IfWebPageContainFlowWidget(flowStepWidget.FlowStepWidget):
    isFirstShow = True

    def __init__(self, lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent=None):
        super().__init__(lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent)
        self.settingDialog = ifWebPageContainObjectSettingDialog.IfWebPageContainObjectSettingDialog(flowTitle, self)
        self.infoPanel.imgLabel.setPixmap(QPixmap(self.picPath + "ifContainBig.png").scaled(23, 19))
        self.directive["command"] = ConditionConstants.ifWebPageContainDirective
        self.directive["data"] = {"web_page": "",
                                  "detect": 0,
                                  "element": "",
                                  "text": ""}
        self.infoFormat = u"检测网页%s中是否%s %s"
        self.updateSecondLineInfo()

    def showEvent(self, a0: QShowEvent) -> None:
        if self.isFirstShow:
            self.isFirstShow = False
            self.parent().insertWidget(int(self.lineNumberLabel.text()), "leaf|endIfDirective|End If", self.indentLevel)
        super().showEvent(a0)

    def getSettingData(self):
        data = self.parent().getDirectiveSettingDataFromDB(self.directive["_id"])
        self.settingDialog.webPageObjectComboBox.setCurrentText(data["web_page"])
        self.settingDialog.detectComboBox.setCurrentIndex(data["detect"])
        self.settingDialog.elementLineEdit.setText(data["element"])
        self.settingDialog.textArea.setPlainText(data["text"])
        self.directive["data"] = data

    def updateSettingData(self):
        self.directive["data"]["web_page"] = self.settingDialog.webPageObjectComboBox.currentText()
        self.directive["data"]["detect"] = self.settingDialog.detectComboBox.currentIndex()
        self.directive["data"]["element"] = self.settingDialog.elementLineEdit.text()
        self.directive["data"]["text"] = self.settingDialog.textArea.toPlainText()
        self.parent().updateDirectiveData2DB(self.directive["_id"], self.directive["data"])
        self.updateSecondLineInfo()

    def updateSecondLineInfo(self, info: tuple = ()):
        if self.directive["data"]["detect"] < 2:
            text = self.directive["data"]["element"]
        else:
            text = self.directive["data"]["text"]
            # 若文本过长则截取35字符后添加省略号
            if len(text) > 35:
                text = text[:35] + "..."
            text = '"' + text + '"'
        super().updateSecondLineInfo((self.directive["data"]["web_page"],
                                      self.settingDialog.detectComboBox.itemText(self.directive["data"]["detect"]),
                                      text))
