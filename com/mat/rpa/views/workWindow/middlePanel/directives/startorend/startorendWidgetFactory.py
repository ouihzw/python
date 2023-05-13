# -- coding: utf-8 --
from com.mat.rpa.views.workWindow.middlePanel.directives.startorend.directiveWidgets.endDirective.endFlowStepWidget import \
    EndFlowStepWidget
from com.mat.rpa.views.workWindow.middlePanel.directives.startorend.directiveWidgets.startDirective.startFlowStepWidget import \
    StartFlowStepWidget
from com.mat.rpa.views.workWindow.middlePanel.directives.startorend.startorendContants import StartorEndConstants


class StartOrEndWidgetFactory(object):
    __instance = None
    __isFirstInit = True

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(StartOrEndWidgetFactory, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        cls = type(self)
        if cls.__isFirstInit:
            super(StartOrEndWidgetFactory, self).__init__()
            cls.__isFirstInit = False

    def createStartOrEndWidget(self, scene, text, directiveType, id):
        if directiveType == StartorEndConstants.startDirective:
            return StartFlowStepWidget(scene, text, directiveType, id, inputs=[1], outputs=[])
        elif directiveType == StartorEndConstants.endDirective:
            return EndFlowStepWidget(scene, text, directiveType, id, inputs=[1], outputs=[])
        return None
