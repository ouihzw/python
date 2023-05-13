# -*- coding:utf-8 -*-
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowStepWidget
from . import processingUploadDialogObjectSettingDialog

class ProcessingUploadDialogFlowWidget(flowStepWidget.FlowStepWidget):
    def __init__(self, lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent=None):
        super(ProcessingUploadDialogFlowWidget, self).__init__(lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent)
        self.settingDialog = processingUploadDialogObjectSettingDialog.ProcessingUploadDialogObjectSettingDialog(flowTitle, self)

    def mouseDoubleClickEvent(self, event):
        self.settingDialog.show()




