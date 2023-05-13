# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowStepWidget
from . import endIfObjectSettingDialog
from ...conditionConstants import ConditionConstants

class EndIfFlowWidget(flowStepWidget.FlowStepWidget):
    def __init__(self, lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent=None):
        super().__init__(lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent)
        self.settingDialog = endIfObjectSettingDialog.EndIfObjectSettingDialog(flowTitle, self)
        self.infoPanel.imgLabel.setPixmap(QPixmap(self.picPath + "endIfBig.png").scaled(23, 19))
        self.directive["command"] = ConditionConstants.endIfDirective
        self.infoFormat = u'结束判断'
        self.updateSecondLineInfo()

    def mouseDoubleClickEvent(self, a0: QMouseEvent) -> None:
        self.settingDialog.show()

    def isEnd(self):
        return 1