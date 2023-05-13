# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowStepWidget
from . import elseObjectSettingDialog
from ...conditionConstants import ConditionConstants

class ElseFlowWidget(flowStepWidget.FlowStepWidget):
    def __init__(self, lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent=None):
        if indentLevel > 1:
            indentLevel -= 1
        super().__init__(lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent)
        self.settingDialog = elseObjectSettingDialog.ElseObjectSettingDialog(flowTitle, self)
        self.infoPanel.imgLabel.setPixmap(QPixmap(self.picPath + "elseBig.png").scaled(23, 19))
        self.directive["command"] = ConditionConstants.elseDirective
        self.infoFormat = u"否则执行以下操作"
        self.updateSecondLineInfo()

    def setIndentLevel(self, indentLevel):
        if indentLevel > 1:
            indentLevel -= 1
        super().setIndentLevel(indentLevel)

    def mouseDoubleClickEvent(self, a0: QMouseEvent) -> None:
        self.settingDialog.show()

    def isEnd(self):
        return 1