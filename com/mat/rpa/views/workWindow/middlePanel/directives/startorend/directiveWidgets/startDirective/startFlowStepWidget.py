# -- coding: utf-8 --
from com.mat.rpa.views.workWindow.middlePanel.directives.startorend.directiveWidgets.startDirective.startObjectSettingDialog import \
    StartObjectSettingDialog
from com.mat.rpa.views.workWindow.middlePanel.directives.startorend.startorendContants import StartorEndConstants
from com.mat.rpa.views.workWindow.middlePanel.flowPanel.flowStepWidget import FlowStepWidget
from com.mat.rpa.views.workWindow.middlePanel.middleWindow.node_graphics_node import QMGraphicsBeginNode


class StartFlowStepWidget(FlowStepWidget):
    def __init__(self, scene, title="Undefined Node", type=" Node ", id=None, inputs=[], outputs=[]):
        super(StartFlowStepWidget, self).__init__(scene, title, type, id, inputs=inputs, outputs=outputs)
        self.node_type = 4
        self.grNode = QMGraphicsBeginNode(self)
        self.directive["line_number"] = 1
        self.directive["command"] = StartorEndConstants.startDirective
        self.directive["flow_id"] = self.id
        self.directive["_id"] = self.directiveDaoObj.insertDirective(self.directive)
        self.dialog = StartObjectSettingDialog(self.title, self.directive["_id"], self.id)

