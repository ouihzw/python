# -*- coding:utf-8 -*-
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowStepWidget
from . import stoppingListeningWebRequestObjectSettingDialog
from ...webDataRetrievingContants import WebDataRetrievingConstants


class StoppingListeningWebRequestFlowWidget(flowStepWidget.FlowStepWidget):
    def __init__(self, scene, title="Undefined Node", type = " Node ", id = None,inputs=[], outputs=[]):
        super(StoppingListeningWebRequestFlowWidget, self).__init__(scene, title, type, id, inputs=[1, 2, 3, 4], outputs=[])
        self.dialog = stoppingListeningWebRequestObjectSettingDialog.StoppingListeningWebRequestObjectSettingDialog(self.title, self.directive["_id"], self.id)
        self.directive["command"] = WebDataRetrievingConstants.stoppingListeningWebRequestDirective
        self.directive["line_number"] = 1
        self.directive["flow_id"] = self.id
        self.directive["data"] = {
            "web_object": ""
        }
        self.directive["_id"] = self.directiveDaoObj.insertDirective(self.directive)
        self.infoFormat = "结束抓取网页%s中的请求信息"




