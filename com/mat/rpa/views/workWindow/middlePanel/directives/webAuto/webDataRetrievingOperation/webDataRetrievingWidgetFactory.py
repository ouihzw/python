# -*- coding:utf-8 -*-
from . import webDataRetrievingContants
from .directiveWidgets.massDataGrabbingDirective import massDataGrabbingFlowStepWidget
from .directiveWidgets.webPageScreenshotDirective import webPageScreenshotFlowStepWidget
from .directiveWidgets.gettingWebElementInfoDirective import gettingWebElementInfoFlowStepWidget
from .directiveWidgets.gettingWebElementPositionDirective import gettingWebElementPositionFlowStepWidget
from .directiveWidgets.gettingWebComboBoxOptionDirective import gettingWebComboBoxOptionFlowStepWidget
from .directiveWidgets.gettingWebPageInfoDirective import gettingWebPageInfoFlowStepWidget
from .directiveWidgets.gettingScrollerPositionDirective import gettingScrollerPositionFlowStepWidget
from .directiveWidgets.gettingWebDialogContentDirective import gettingWebDialogContentFlowStepWidget
from .directiveWidgets.gettingAllFilteredCookiesDirective import gettingAllFilteredCookiesFlowStepWidget
from .directiveWidgets.gettingSpecifiedCookieInfoDirective import gettingSpecifiedCookieInfoFlowStepWidget
from .directiveWidgets.startingListeningWebRequestDirective import startingListeningWebRequestFlowStepWidget
from .directiveWidgets.stoppingListeningWebRequestDirective import stoppingListeningWebRequestFlowStepWidget
from .directiveWidgets.gettingWebRequestResultDirective import gettingWebRequestResultFlowStepWidget

class WebDataRetrievingWidgetFactory(object):
    __instance = None
    __isFirstInit = True
    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super(WebDataRetrievingWidgetFactory, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        cls = type(self)
        if cls.__isFirstInit:
            super(WebDataRetrievingWidgetFactory, self).__init__()
            cls.__isFirstInit = False

    def createWebDataRetrievingWidget(self, scene, text, directiveType, id):
        if directiveType == webDataRetrievingContants.WebDataRetrievingConstants.massDataGrabbingDirective:
            return massDataGrabbingFlowStepWidget.MassDataGrabbingFlowWidget(scene, text, directiveType, id, inputs=[1, 2, 3, 4], outputs=[])
        elif directiveType == webDataRetrievingContants.WebDataRetrievingConstants.webPageScreenshotDirective:
            return webPageScreenshotFlowStepWidget.WebPageScreenshotFlowWidget(scene, text, directiveType, id, inputs=[1, 2, 3, 4], outputs=[])
        elif directiveType == webDataRetrievingContants.WebDataRetrievingConstants.gettingWebElementInfoDirective:
            return gettingWebElementInfoFlowStepWidget.GettingWebElementInfoFlowWidget(scene, text, directiveType, id, inputs=[1, 2, 3, 4], outputs=[])
        # elif widgetType == webDataRetrievingContants.WebDataRetrievingConstants.gettingWebElementPositionDirective:
        #     return gettingWebElementPositionFlowStepWidget.GettingWebElementPositionFlowWidget(lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent)
        # elif widgetType == webDataRetrievingContants.WebDataRetrievingConstants.gettingWebComboBoxOptionDirective:
        #     return gettingWebComboBoxOptionFlowStepWidget.GettingWebComboBoxOptionFlowWidget(lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent)
        elif directiveType == webDataRetrievingContants.WebDataRetrievingConstants.gettingWebPageInfoDirective:
            return gettingWebPageInfoFlowStepWidget.GettingWebPageInfoFlowWidget(scene, text, directiveType, id, inputs=[1, 2, 3, 4], outputs=[])
        elif directiveType == webDataRetrievingContants.WebDataRetrievingConstants.gettingScrollerPositionDirective:
            return gettingScrollerPositionFlowStepWidget.GettingScrollerPositionFlowWidget(scene, text, directiveType, id, inputs=[1, 2, 3, 4], outputs=[])
        # elif widgetType == webDataRetrievingContants.WebDataRetrievingConstants.gettingWebDialogContentDirective:
        #     return gettingWebDialogContentFlowStepWidget.GettingWebDialogContentFlowWidget(lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent)
        # elif widgetType == webDataRetrievingContants.WebDataRetrievingConstants.gettingAllFilteredCookiesDirective:
        #     return gettingAllFilteredCookiesFlowStepWidget.GettingAllFilteredCookiesFlowWidget(lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent)
        # elif widgetType == webDataRetrievingContants.WebDataRetrievingConstants.gettingSpecifiedCookieInfoDirective:
        #     return gettingSpecifiedCookieInfoFlowStepWidget.GettingSpecifiedCookieInfoFlowWidget(lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent)
        elif directiveType == webDataRetrievingContants.WebDataRetrievingConstants.startingListeningWebRequestDirective:
            return startingListeningWebRequestFlowStepWidget.StartingListeningWebRequestFlowWidget(scene, text, directiveType, id, inputs=[1, 2, 3, 4], outputs=[])
        elif directiveType == webDataRetrievingContants.WebDataRetrievingConstants.stoppingListeningWebRequestDirective:
            return stoppingListeningWebRequestFlowStepWidget.StoppingListeningWebRequestFlowWidget(scene, text, directiveType, id, inputs=[1, 2, 3, 4], outputs=[])
        elif directiveType == webDataRetrievingContants.WebDataRetrievingConstants.gettingWebRequestResultDirective:
            return gettingWebRequestResultFlowStepWidget.GettingWebRequestResultFlowWidget(scene, text, directiveType, id, inputs=[1, 2, 3, 4], outputs=[])

        return None