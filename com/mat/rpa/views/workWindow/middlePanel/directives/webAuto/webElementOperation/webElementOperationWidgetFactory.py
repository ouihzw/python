# -*- coding:utf-8 -*-
from . import webElementOperationConstants
from .directiveWidgets.draggingWebElementDirective import draggingWebElementFlowStepWidget
from .directiveWidgets.waitingForWebElementDirective import waitingForWebElementFlowStepWidget
from .directiveWidgets.fillingInPasswordWebInputDirective import fillingInPasswordWebInputFlowStepWidget
from .directiveWidgets.settingWebComboboxDirective import settingWebComboboxFlowStepWidget
from .directiveWidgets.settingWebCheckBoxDirective import settingWebCheckBoxFlowStepWidget
from .directiveWidgets.settingWebElementValueDirective import settingWebElementValueFlowStepWidget
from .directiveWidgets.settingWebElementPropertyDirective import settingWebElementPropertyFlowStepWidget
from .directiveWidgets.gettingWebElementObjectDirective import gettingWebElementObjectFlowStepWidget
from .directiveWidgets.gettingRelatedWebElementDirective import gettingRelatedWebElementFlowStepWidget
from .directiveWidgets.gettingSimilarWebElementListDirective import gettingSimilarWebElementListFlowStepWidget
class WebElementOperationWidgetFactory(object):
    __instance = None
    __isFirstInit = True
    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super(WebElementOperationWidgetFactory, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        cls = type(self)
        if cls.__isFirstInit:
            super(WebElementOperationWidgetFactory, self).__init__()
            cls.__isFirstInit = False

    def createWebElementOperationWidget(self, scene, text, directiveType, id):
        if directiveType == webElementOperationConstants.WebElementOperationConstants.draggingWebElementDirective:
            return draggingWebElementFlowStepWidget.DraggingWebElementFlowWidget(scene, text, directiveType, id, inputs=[1, 2, 3, 4], outputs=[])
        elif directiveType == webElementOperationConstants.WebElementOperationConstants.waitingForWebElementDirective:
            return waitingForWebElementFlowStepWidget.WaitingForWebElementFlowWidget(scene, text, directiveType, id, inputs=[1, 2, 3, 4], outputs=[])
        elif directiveType == webElementOperationConstants.WebElementOperationConstants.fillingInPasswordWebInputDirective:
            return fillingInPasswordWebInputFlowStepWidget.FillingInPasswordWebInputFlowWidget(scene, text, directiveType, id, inputs=[1, 2, 3, 4], outputs=[])
        elif directiveType == webElementOperationConstants.WebElementOperationConstants.settingWebComboboxDirective:
            return settingWebComboboxFlowStepWidget.SettingWebComboboxFlowWidget(scene, text, directiveType, id, inputs=[1, 2, 3, 4], outputs=[])
        elif directiveType == webElementOperationConstants.WebElementOperationConstants.settingWebCheckBoxDirective:
            return settingWebCheckBoxFlowStepWidget.SettingWebCheckBoxFlowWidget(scene, text, directiveType, id, inputs=[1, 2, 3, 4], outputs=[])
        elif directiveType == webElementOperationConstants.WebElementOperationConstants.settingWebElementValueDirective:
            return settingWebElementValueFlowStepWidget.SettingWebElementValueFlowWidget(scene, text, directiveType, id, inputs=[1, 2, 3, 4], outputs=[])
        elif directiveType == webElementOperationConstants.WebElementOperationConstants.settingWebElementPropertyDirective:
            return settingWebElementPropertyFlowStepWidget.SettingWebElementPropertyFlowWidget(scene, text, directiveType, id, inputs=[1, 2, 3, 4], outputs=[])
        elif directiveType == webElementOperationConstants.WebElementOperationConstants.gettingWebElementObjectDirective:
            return gettingWebElementObjectFlowStepWidget.GettingWebElementObjectFlowWidget(scene, text, directiveType, id, inputs=[1, 2, 3, 4], outputs=[])
        elif directiveType == webElementOperationConstants.WebElementOperationConstants.gettingRelatedWebElementDirective:
            return gettingRelatedWebElementFlowStepWidget.GettingRelatedWebElementFlowWidget(scene, text, directiveType, id, inputs=[1, 2, 3, 4], outputs=[])
        elif directiveType == webElementOperationConstants.WebElementOperationConstants.gettingSimilarWebElementListDirective:
            return gettingSimilarWebElementListFlowStepWidget.GettingSimilarWebElementListFlowWidget(scene, text, directiveType, id, inputs=[1, 2, 3, 4], outputs=[])
        else:
            return None