import sys

from PyQt5.QtWidgets import QApplication

from com.mat.rpa.views.workWindow.middlePanel.directives.webAuto.directiveWidgets.openningWebPageDirective import \
    openWebPageObjectSettingDialog
from com.mat.rpa.views.workWindow.middlePanel.directives.webAuto.webAutoConstants import WebAutoConstants
from com.mat.rpa.views.workWindow.middlePanel.flowPanel.flowStepWidget import FlowStepWidget



class OpenWebPageObjectFlowWidget(FlowStepWidget):
    def __init__(self, scene, title="Undefined Node", type = " Node ", id = None,inputs=[], outputs=[]):
        super(OpenWebPageObjectFlowWidget, self).__init__(scene, title, type, id, inputs=[1, 2, 3, 4], outputs=[])
        self.directive["line_number"] = 1
        self.directive["command"] = WebAutoConstants.openningWebPageDirective
        self.directive["data"] = {"browser_type": 0,
                                  "url": "",
                                  "output": "web_page",
                                  "wait": True,
                                  "time_out_period": 15,
                                  "on_time_out": 0,
                                  "cli_parameter": "",
                                  "exe_path": "",
                                  "log": True,
                                  "handle": 0,
                                  "on_error_output_value": "",
                                  "retry_count": 1,
                                  "retry_interval": 1}
        self.directive["flow_id"] = self.id
        self.directive["_id"] = self.directiveDaoObj.insertDirective(self.directive)
        self.dialog = openWebPageObjectSettingDialog.OpenWebPageObjectSettingDialog(self.title, self.directive["_id"], self.id)
        self.setgrNodeTip("打开网页，实现网页自动化")


    def setDialog(self, data):
        self.directive["line_number"] = 1
        self.directive["command"] = WebAutoConstants.openningWebPageDirective
        self.directive["data"] = {"browser_type": 0,
                                  "url": "",
                                  "output": "web_page",
                                  "wait": True,
                                  "time_out_period": 15,
                                  "on_time_out": 0,
                                  "cli_parameter": "",
                                  "exe_path": "",
                                  "log": True,
                                  "handle": 0,
                                  "on_error_output_value": "",
                                  "retry_count": 1,
                                  "retry_interval": 1}
        self.directive["flow_id"] = self.id
        self.directive["_id"] = self.directiveDaoObj.insertDirective(self.directive)
        self.dialog = openWebPageObjectSettingDialog.OpenWebPageObjectSettingDialog(self.title, self.directive["_id"], self.id)
        self.dialog.deserialize(data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = OpenWebPageObjectFlowWidget(None)
    win.show()
    app.exec_()