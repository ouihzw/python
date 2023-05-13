# -*- coding:utf-8 -*-
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowStepWidget
from . import gettingSpecifiedCookieInfoObjectSettingDialog

class GettingSpecifiedCookieInfoFlowWidget(flowStepWidget.FlowStepWidget):
    def __init__(self, lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent=None):
        super(GettingSpecifiedCookieInfoFlowWidget, self).__init__(lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent)
        self.settingDialog = gettingSpecifiedCookieInfoObjectSettingDialog.GettingSpecifiedCookieInfoObjectSettingDialog(flowTitle, self)

    def mouseDoubleClickEvent(self, event):
        self.settingDialog.show()




