# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowStepWidget
from . import ifFileExistsObjectSettingDialog
from ...conditionConstants import ConditionConstants

class IfFileExistsFlowWidget(flowStepWidget.FlowStepWidget):
    isFirstShow = True
    def __init__(self, lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent=None):
        super().__init__(lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent)
        self.settingDialog = ifFileExistsObjectSettingDialog.IfFileExistsObjectSettingDialog(flowTitle, self)
        self.infoPanel.imgLabel.setPixmap(QPixmap(self.picPath + "ifFileExistsBig.png").scaled(23, 19))
        self.directive["command"] = ConditionConstants.ifFileExistsDirective
        self.directive["data"] = {"file_path": "",
                                  "exist": 0}
        self.infoFormat = u"如果文件%s%s，则执行以下操作"
        self.updateSecondLineInfo()

    def showEvent(self, a0: QShowEvent) -> None:
        if self.isFirstShow:
            self.isFirstShow = False
            self.parent().insertWidget(int(self.lineNumberLabel.text()), "leaf|endIfDirective|End If", self.indentLevel)
        super().showEvent(a0)

    def getSettingData(self):
        data = self.parent().getDirectiveSettingDataFromDB(self.directive["_id"])
        self.settingDialog.filePathLineEdit.setText(data["file_path"])
        self.settingDialog.fileExistsComboBox.setCurrentIndex(data["exist"])
        self.directive["data"] = data

    def updateSettingData(self):
        self.directive["data"]["file_path"] = self.settingDialog.filePathLineEdit.text()
        self.directive["data"]["exist"] = self.settingDialog.fileExistsComboBox.currentIndex()
        self.parent().updateDirectiveData2DB(self.directive["_id"], self.directive["data"])
        self.updateSecondLineInfo()

    def updateSecondLineInfo(self, info: tuple = ()):
        super().updateSecondLineInfo((self.directive["data"]["file_path"],
                                      self.settingDialog.fileExistsComboBox.itemText(self.directive["data"]["exist"])))