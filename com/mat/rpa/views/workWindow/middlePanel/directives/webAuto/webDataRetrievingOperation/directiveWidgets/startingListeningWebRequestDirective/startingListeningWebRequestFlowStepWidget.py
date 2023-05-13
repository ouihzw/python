# -*- coding:utf-8 -*-
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowStepWidget
from . import startingListeningWebRequestObjectSettingDialog
from ..webPageScreenshotDirective import webPageScreenshotObjectSettingDialog
from ...webDataRetrievingContants import WebDataRetrievingConstants


class StartingListeningWebRequestFlowWidget(flowStepWidget.FlowStepWidget):
    def __init__(self, scene, title="Undefined Node", type = " Node ", id = None,inputs=[], outputs=[]):
        super(StartingListeningWebRequestFlowWidget, self).__init__(scene, title, type, id, inputs=[1, 2, 3, 4], outputs=[])
        self.directive["command"] = WebDataRetrievingConstants.startingListeningWebRequestDirective
        self.directive["data"] = {
            "web_object": "",
            "source_url": "",
            "filter_resource_type": "全部"
        }
        self.directive["line_number"] = 1
        self.directive["flow_id"] = self.id
        self.directive["_id"] = self.directiveDaoObj.insertDirective(self.directive)
        self.dialog = startingListeningWebRequestObjectSettingDialog.StartingListeningWebRequestObjectSettingDialog(self.title, self.directive["_id"], self.id)
        self.infoFormat = "开始抓取%s中的请求信息"






