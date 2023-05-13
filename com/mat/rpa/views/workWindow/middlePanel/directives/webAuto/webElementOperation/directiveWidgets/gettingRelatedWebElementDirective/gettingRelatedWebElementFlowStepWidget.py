# -*- coding:utf-8 -*-
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowStepWidget
from . import gettingRelatedWebElementObjectSettingDialog
from ....webAutoConstants import WebAutoConstants

class GettingRelatedWebElementFlowWidget(flowStepWidget.FlowStepWidget):
    def __init__(self, scene, title="Undefined Node", type = " Node ", id = None,inputs=[], outputs=[]):
        super(GettingRelatedWebElementFlowWidget, self).__init__(scene, title, type, id, inputs=[1, 2, 3, 4], outputs=[])
        self.directive["line_number"] = 1
        self.directive["command"] = WebAutoConstants.webElementOperationContants.settingWebElementValueDirective
        self.directive["data"] = {"browser_type": 0,
                                  "element": "",
                                  "value": ""}
        self.directive["flow_id"] = self.id
        self.directive["_id"] = self.directiveDaoObj.insertDirective(self.directive)
        self.dialog = gettingRelatedWebElementObjectSettingDialog.GettingRelatedWebElementObjectSettingDialog(self.title,
                                                                                                            self.directive[
                                                                                                                "_id"],
                                                                                                            self.id)

    def setDialog(self, data):
        self.directive["line_number"] = 1
        self.directive["command"] =  WebAutoConstants.webElementOperationContants.settingWebElementValueDirective
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
        self.dialog =gettingRelatedWebElementObjectSettingDialog.GettingRelatedWebElementObjectSettingDialog(self.title,
                                                                                                            self.directive[
                                                                                                                "_id"],
                                                                                                            self.id)
        self.dialog.deserialize(data)



