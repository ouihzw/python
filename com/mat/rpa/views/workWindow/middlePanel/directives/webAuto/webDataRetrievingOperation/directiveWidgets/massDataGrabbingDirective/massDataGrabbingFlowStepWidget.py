# -*- coding:utf-8 -*-
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowStepWidget
from . import massDataGrabbingObjectSettingDialog
from ...webDataRetrievingContants import WebDataRetrievingConstants


class MassDataGrabbingFlowWidget(flowStepWidget.FlowStepWidget):
    def __init__(self, scene, title="Undefined Node", type = " Node ", id = None,inputs=[], outputs=[]):
        super(MassDataGrabbingFlowWidget, self).__init__(scene, title, type, id, inputs=[1, 2, 3, 4], outputs=[])
        self.directive["line_number"] = 1
        self.directive["command"] = WebDataRetrievingConstants.massDataGrabbingDirective
        self.directive["flow_id"] = self.id
        self.directive["_id"] = self.directiveDaoObj.insertDirective(self.directive)
        self.dialog = massDataGrabbingObjectSettingDialog.MassDataGrabbingObjectSettingDialog(self.title, self.directive["_id"], self.id)






