# -*- coding:utf-8 -*-
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowStepWidget
from . import redirectingToNewWebPageObjectSettingDialog
from ...webPageOperationConstants import WebPageOperationConstants

class RedirectingToNewWebPageFlowWidget(flowStepWidget.FlowStepWidget):
    def __init__(self, scene, title="Undefined Node", type = " Node ", id = None,inputs=[], outputs=[]):
        super(RedirectingToNewWebPageFlowWidget, self).__init__(scene, title, type, id, inputs=[1, 2, 3, 4], outputs=[])
        #self.settingDialog = redirectingToNewWebPageObjectSettingDialog.RedirectingToNewWebPageObjectSettingDialog(flowTitle, self)
        self.directive["line_number"] = 1
        self.directive["command"] = WebPageOperationConstants.redirectingToNewWebPageDirective
        self.directive["data"] = {"web_object": "",
                                  "jump_method": 0,
                                  "new_url": "",
                                  "ignore_Cache": False,
                                  "time_out": "20",
                                  "log": True,
                                  "handle": 0,
                                  "retry_count": 1,
                                  "retry_interval": 1}
        #self.updateSecondLineInfo()

        self.directive["flow_id"] = self.id
        self.directive["_id"] = self.directiveDaoObj.insertDirective(self.directive)
        self.dialog = redirectingToNewWebPageObjectSettingDialog.RedirectingToNewWebPageObjectSettingDialog(self.title, self.directive["_id"], self.id)


    def setDialog(self, data):
        self.directive["line_number"] = 1
        self.directive["command"] = WebPageOperationConstants.redirectingToNewWebPageDirective
        self.directive["data"] = {"web_object": "",
                                  "jump_method": 0,
                                  "new_url": "",
                                  "ignore_Cache": False,
                                  "time_out": "20",
                                  "log": True,
                                  "handle": 0,
                                  "retry_count": 1,
                                  "retry_interval": 1}
        self.directive["flow_id"] = self.id
        self.directive["_id"] = self.directiveDaoObj.insertDirective(self.directive)
        self.dialog = redirectingToNewWebPageObjectSettingDialog.RedirectingToNewWebPageObjectSettingDialog(self.title, self.directive["_id"],
                                                                                    self.id)
        self.dialog.deserialize(data)