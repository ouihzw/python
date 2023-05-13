# -- coding: utf-8 --
from com.mat.rpa.views.workWindow.middlePanel.directives.startorend.directiveWidgets.endDirective.endObjectSettingDialog import \
    EndObjectSettingDialog
from com.mat.rpa.views.workWindow.middlePanel.directives.startorend.startorendContants import StartorEndConstants
from com.mat.rpa.views.workWindow.middlePanel.flowPanel.flowStepWidget import FlowStepWidget
from com.mat.rpa.views.workWindow.middlePanel.middleWindow.node_graphics_node import QMGraphicsBeginNode


class EndFlowStepWidget(FlowStepWidget):
    def __init__(self, scene, title="Undefined Node", type=" Node ", id=None, inputs=[], outputs=[]):
        super(EndFlowStepWidget, self).__init__(scene, title, type, id, inputs=inputs, outputs=outputs)
        self.node_type = 5
        self.grNode = QMGraphicsBeginNode(self)
        self.directive["line_number"] = 1
        self.directive["command"] = StartorEndConstants.endDirective
        self.directive["flow_id"] = self.id
        self.directive["_id"] = self.directiveDaoObj.insertDirective(self.directive)
        self.dialog = EndObjectSettingDialog(self.title, self.directive["_id"], self.id)

