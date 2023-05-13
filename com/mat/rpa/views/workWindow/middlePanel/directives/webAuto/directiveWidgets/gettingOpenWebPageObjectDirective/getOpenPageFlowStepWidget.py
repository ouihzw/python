from com.mat.rpa.views.workWindow.middlePanel.flowPanel.flowStepWidget import FlowStepWidget
from . import getOpenPageObjectSettingDialog
from ...webAutoConstants import WebAutoConstants

class GetOpenPageObjectFlowWidget(FlowStepWidget):
    def __init__(self, scene, title="Undefined Node", type=" Node ", id=None, inputs=[], outputs=[]):
        super(GetOpenPageObjectFlowWidget, self).__init__(scene, title, type, id, inputs=[1, 2, 3, 4], outputs=[])
        self.directive["line_number"] = 1
        self.directive["command"] = WebAutoConstants.gettingOpenWebPageObjectDirective
        self.directive["flow_id"] = self.id
        self.directive["_id"] = self.directiveDaoObj.insertDirective(self.directive)
        self.dialog = getOpenPageObjectSettingDialog.GetOpenPageObjectSettingDialog(self.title, self.directive["_id"], self.id)

    def setDialog(self, data):
        self.directive["line_number"] = 1
        self.directive["command"] = WebAutoConstants.gettingOpenWebPageObjectDirective
        self.directive["flow_id"] = self.id
        self.directive["_id"] = self.directiveDaoObj.insertDirective(self.directive)
        self.dialog = getOpenPageObjectSettingDialog.GetOpenPageObjectSettingDialog(self.title, self.directive["_id"],
                                                                                    self.id)
        self.dialog.deserialize(data)




