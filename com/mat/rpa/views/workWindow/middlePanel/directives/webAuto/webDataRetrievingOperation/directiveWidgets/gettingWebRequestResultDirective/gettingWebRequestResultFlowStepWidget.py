# -*- coding:utf-8 -*-
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowStepWidget
from . import gettingWebRequestResultObjectSettingDialog
from ...webDataRetrievingContants import WebDataRetrievingConstants


class GettingWebRequestResultFlowWidget(flowStepWidget.FlowStepWidget):
    def __init__(self, scene, title="Undefined Node", type = " Node ", id = None,inputs=[], outputs=[]):
        super(GettingWebRequestResultFlowWidget, self).__init__(scene, title, type, id, inputs=[1, 2, 3, 4], outputs=[])
        self.dialog = gettingWebRequestResultObjectSettingDialog.GettingWebRequestResultObjectSettingDialog(self.title, self.directive["_id"], self.id)
        self.directive["command"] = WebDataRetrievingConstants.gettingWebRequestResultDirective
        self.directive["line_number"] = 1
        self.directive["data"] = {
            "web_object": "",
            "save_list": ""
        }
        self.directive["flow_id"] = self.id
        self.directive["_id"] = self.directiveDaoObj.insertDirective(self.directive)
        self.infoFormat = "获取网页%s监听结果列表，将结果保存到%s"




