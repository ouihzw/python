# -*- coding:utf-8 -*-
from . import webPageOperationConstants
from .directiveWidgets.redirectingToNewWebPageDirective import redirectingToNewWebPageFlowStepWidget
from .directiveWidgets.waitingForLoadingPageDirective import waitingForLoadingPageFlowStepWidget
from .directiveWidgets.stoppingLoadingPageDirective import stoppingLoadingPageFlowStepWidget
from .directiveWidgets.mouseScrollingPageDirective import mouseScrollingPageFlowStepWidget
from .directiveWidgets.executingJSDirective import executingJSFlowStepWidget
from .directiveWidgets.gettingWebPageObjectListDirective import gettingWebPageObjectListFlowStepWidget
from .directiveWidgets.settingWebCookieDirective import settingWebCookieFlowStepWidget
from .directiveWidgets.removingSpecificCookieDirective import removingSpecificCookieFlowStepWidget
class WebPageOperationWidgetFactory(object):
    __instance = None
    __isFirstInit = True
    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super(WebPageOperationWidgetFactory, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        cls = type(self)
        if cls.__isFirstInit:
            super(WebPageOperationWidgetFactory, self).__init__()
            cls.__isFirstInit = False

    def createWebPageOperationWidget(self, scene, text, directiveType, id):
        if directiveType == webPageOperationConstants.WebPageOperationConstants.waitingForLoadingPageDirective:
            return waitingForLoadingPageFlowStepWidget.WaitingForLoadingPageFlowWidget(scene, text, directiveType, id, inputs=[1, 2, 3, 4], outputs=[])
        elif directiveType == webPageOperationConstants.WebPageOperationConstants.redirectingToNewWebPageDirective:
            return redirectingToNewWebPageFlowStepWidget.RedirectingToNewWebPageFlowWidget(scene, text, directiveType, id, inputs=[1, 2, 3, 4], outputs=[])
        elif directiveType == webPageOperationConstants.WebPageOperationConstants.stoppingLoadingPageDirective:
            return stoppingLoadingPageFlowStepWidget.StoppingLoadingPageFlowWidget(scene, text, directiveType, id, inputs=[1, 2, 3, 4], outputs=[])
        elif directiveType == webPageOperationConstants.WebPageOperationConstants.mouseScrollingPageDirective:
            return mouseScrollingPageFlowStepWidget.MouseScrollingPageFlowWidget(scene, text, directiveType, id, inputs=[1, 2, 3, 4], outputs=[])
        elif directiveType == webPageOperationConstants.WebPageOperationConstants.executingJSDirective:
            return executingJSFlowStepWidget.ExecutingJSFlowWidget(scene, text, directiveType, id, inputs=[1, 2, 3, 4], outputs=[])
        elif directiveType == webPageOperationConstants.WebPageOperationConstants.gettingWebPageObjectListDirective:
            return gettingWebPageObjectListFlowStepWidget.GettingWebPageObjectListFlowWidget(scene, text, directiveType, id, inputs=[1, 2, 3, 4], outputs=[])
        elif directiveType == webPageOperationConstants.WebPageOperationConstants.settingWebCookieDirective:
            return settingWebCookieFlowStepWidget.SettingWebCookieFlowWidget(scene, text, directiveType, id, inputs=[1, 2, 3, 4], outputs=[])
        elif directiveType == webPageOperationConstants.WebPageOperationConstants.removingSpecificCookieDirective:
            return removingSpecificCookieFlowStepWidget.RemovingSpecificCookieFlowWidget(scene, text, directiveType, id, inputs=[1, 2, 3, 4], outputs=[])

        return None
