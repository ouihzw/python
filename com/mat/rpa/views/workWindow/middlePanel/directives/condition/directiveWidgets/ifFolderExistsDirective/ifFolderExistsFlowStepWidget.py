# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowStepWidget
from . import ifFolderExistsObjectSettingDialog
from ...conditionConstants import ConditionConstants

class IfFolderExistsFlowWidget(flowStepWidget.FlowStepWidget):
    isFirstShow = True
    def __init__(self, lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent=None):
        super().__init__(lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent)
        self.settingDialog = ifFolderExistsObjectSettingDialog.IfFolderExistsObjectSettingDialog(flowTitle, self)
        self.infoPanel.imgLabel.setPixmap(QPixmap(self.picPath + "ifFolderExistsBig.png").scaled(23, 19))
        self.directive["command"] = ConditionConstants.ifFolderExistsDirective
        self.directive["data"] = {"folder_path": "",
                                  "exist": 0}
        self.infoFormat = u"如果文件夹%s%s，则执行以下操作"
        self.updateSecondLineInfo()

    def showEvent(self, a0: QShowEvent) -> None:
        if self.isFirstShow:
            self.isFirstShow = False
            self.parent().insertWidget(int(self.lineNumberLabel.text()), "leaf|endIfDirective|End If", self.indentLevel)
        super().showEvent(a0)

    def getSettingData(self):
        data = self.parent().getDirectiveSettingDataFromDB(self.directive["_id"])
        self.settingDialog.folderPathLineEdit.setText(data["folder_path"])
        self.settingDialog.folderExistsComboBox.setCurrentIndex(data["exist"])
        self.directive["data"] = data


    def updateSettingData(self):
        self.directive["data"]["folder_path"] = self.settingDialog.folderPathLineEdit.text()
        self.directive["data"]["exist"] = self.settingDialog.folderExistsComboBox.currentIndex()
        self.parent().updateDirectiveData2DB(self.directive["_id"], self.directive["data"])
        self.updateSecondLineInfo()

    def updateSecondLineInfo(self, info: tuple = ()):
        data = self.directive["data"]
        super().updateSecondLineInfo((data["folder_path"],
                                      self.settingDialog.folderExistsComboBox.itemText(data["exist"])))