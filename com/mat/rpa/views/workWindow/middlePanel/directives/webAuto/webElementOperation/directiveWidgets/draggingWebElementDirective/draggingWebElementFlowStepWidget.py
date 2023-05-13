# -*- coding:utf-8 -*-
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowStepWidget
from . import draggingWebElementObjectSettingDialog

class DraggingWebElementFlowWidget(flowStepWidget.FlowStepWidget):
    def __init__(self, scene, title="Undefined Node", type = " Node ", id = None,inputs=[], outputs=[]):
        super(DraggingWebElementFlowWidget, self).__init__(scene, title, type, id, inputs=[1, 2, 3, 4], outputs=[])
        self.dialog = draggingWebElementObjectSettingDialog.DraggingWebElementObjectSettingDialog(flowTitle, self)






