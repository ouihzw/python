# -*- coding:utf-8 -*-
from . import webAutoConstants
from .directiveWidgets.openningWebPageDirective import openWebPageFlowStepWidget
from .directiveWidgets.gettingOpenWebPageObjectDirective import getOpenPageFlowStepWidget
from .directiveWidgets.clickingWebElementDirective import clickingWebElementFlowStepWidget
from .directiveWidgets.mouseHoveringOverWebElementDirective import mouseHoveringOverWebElementFlowStepWidget
from .directiveWidgets.fillingInWebInputDirective import fillingInWebInputFlowStepWidget
from .directiveWidgets.closingWebPageDirective import closingWebPageFlowStepWidget
from .webDataRetrievingOperation.webDataRetrievingWidgetFactory import WebDataRetrievingWidgetFactory
from .webPageOperation import webPageOperationWidgetFactory
from .webPageOperation.directiveWidgets.waitingForLoadingPageDirective import waitingForLoadingPageFlowStepWidget
from .webDialogOperation import webDialogWidgetFactory

class WebAutoWidgetFactory(object):
    __instance = None
    __isFirstInit = True
    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super(WebAutoWidgetFactory, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        cls = type(self)
        if cls.__isFirstInit:
            super(WebAutoWidgetFactory, self).__init__()
            self.webPageOperationWidgetFactory = webPageOperationWidgetFactory.WebPageOperationWidgetFactory()
            self.webDataRetrievingWidgetFactory = WebDataRetrievingWidgetFactory()
            self.webDialogWidgetFactory = webDialogWidgetFactory.WebDialogOperationWidgetFactory()
            cls.__isFirstInit = False

    def createWebAutoWidget(self, scene, text, directiveType, id):
        if directiveType == webAutoConstants.WebAutoConstants.openningWebPageDirective:
            return openWebPageFlowStepWidget.OpenWebPageObjectFlowWidget(scene, text, directiveType, id, inputs=[1, 2, 3, 4], outputs=[])
        elif directiveType == webAutoConstants.WebAutoConstants.gettingOpenWebPageObjectDirective:
            return getOpenPageFlowStepWidget.GetOpenPageObjectFlowWidget(scene, text, directiveType, id, inputs=[1, 2, 3, 4], outputs=[])
        elif directiveType == webAutoConstants.WebAutoConstants.clickingWebElementDirective:
            return clickingWebElementFlowStepWidget.ClickingWebElementFlowWidget(scene, text, directiveType, id, inputs=[1, 2, 3, 4], outputs=[])
        elif directiveType == webAutoConstants.WebAutoConstants.mouseHoveringOverWebElementDirective:
            return mouseHoveringOverWebElementFlowStepWidget.MouseHoveringOverWebElementFlowWidget(scene, text, directiveType, id, inputs=[1, 2, 3, 4], outputs=[])
        elif directiveType == webAutoConstants.WebAutoConstants.fillingInWebInputDirective:
            return fillingInWebInputFlowStepWidget.FillingInWebInputFlowWidget(scene, text, directiveType, id, inputs=[1, 2, 3, 4], outputs=[])
        elif directiveType == webAutoConstants.WebAutoConstants.closingWebPageDirective:
            return closingWebPageFlowStepWidget.ClosingWebPageFlowWidget(scene, text, directiveType, id, inputs=[1, 2, 3, 4], outputs=[])

        flowWidget = self.webPageOperationWidgetFactory.createWebPageOperationWidget(scene, text, directiveType, id)

        if flowWidget:
            return flowWidget

        flowWidget = self.webDataRetrievingWidgetFactory.createWebDataRetrievingWidget(scene, text, directiveType, id)

        if flowWidget:
            return flowWidget

        flowWidget = self.webDialogWidgetFactory.createWebDialogOperationWidget(scene, text, directiveType, id)

        if flowWidget:
            return flowWidget

        return None