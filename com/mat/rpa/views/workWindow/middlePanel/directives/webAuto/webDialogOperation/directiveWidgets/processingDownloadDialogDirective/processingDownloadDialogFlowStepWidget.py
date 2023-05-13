# -*- coding:utf-8 -*-
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowStepWidget
from . import processingDownloadDialogObjectSettingDialog

class ProcessingDownloadDialogFlowWidget(flowStepWidget.FlowStepWidget):
    def __init__(self, lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent=None):
        super(ProcessingDownloadDialogFlowWidget, self).__init__(lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent)
        self.settingDialog = processingDownloadDialogObjectSettingDialog.ProcessingDownloadDialogObjectSettingDialog(flowTitle, self)

    def mouseDoubleClickEvent(self, event):
        self.settingDialog.show()




