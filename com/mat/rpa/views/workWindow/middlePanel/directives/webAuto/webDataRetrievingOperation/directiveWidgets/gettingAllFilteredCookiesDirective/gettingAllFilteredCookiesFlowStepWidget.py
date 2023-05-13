# -*- coding:utf-8 -*-
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowStepWidget
from . import gettingAllFilteredCookiesObjectSettingDialog

class GettingAllFilteredCookiesFlowWidget(flowStepWidget.FlowStepWidget):
    def __init__(self, lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent=None):
        super(GettingAllFilteredCookiesFlowWidget, self).__init__(lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent)
        self.settingDialog = gettingAllFilteredCookiesObjectSettingDialog.GettingAllFilteredCookiesObjectSettingDialog(flowTitle, self)

    def mouseDoubleClickEvent(self, event):
        self.settingDialog.show()




