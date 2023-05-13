# -*- coding:utf-8 -*-
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowStepWidget
from . import uploadingFileObjectSettingDialog

class UploadingFileFlowWidget(flowStepWidget.FlowStepWidget):
    def __init__(self, lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent=None):
        super(UploadingFileFlowWidget, self).__init__(lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent)
        self.settingDialog = uploadingFileObjectSettingDialog.UploadingFileObjectSettingDialog(flowTitle, self)

    def mouseDoubleClickEvent(self, event):
        self.settingDialog.show()




