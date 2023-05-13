# -*- coding:utf-8 -*-
from .startorend.startorendWidgetFactory import StartOrEndWidgetFactory
from .webAuto import webAutoWidgetFactory
# from .condition import conditionWidgetFactory
# from .dataProcess import dataProcessingWidgetFactory
# from .mouseKeyboard import mouseAndKeyboardWidgetFactory

class DirectiveWidgetFactory(object):
    __instance = None
    __isFirstInit = True

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super(DirectiveWidgetFactory, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        cls = type(self)
        if cls.__isFirstInit:
            super(DirectiveWidgetFactory, self).__init__()
            self.webAutoWidgetFactory = webAutoWidgetFactory.WebAutoWidgetFactory()
            self.startOrEndWidgetFactory = StartOrEndWidgetFactory()
            # self.conditionWidgetFactory = conditionWidgetFactory.ConditionWidgetFactory()
            # self.dataProcessWidgetFactory = dataProcessingWidgetFactory.DataProcessingWidgetFactory()
            # self.mouseAndKeyboardWidgetFactory = mouseAndKeyboardWidgetFactory.mouseAndKeyboardWidgetFactory()
            cls.__isFirstInit = False

    def createDirectiveWidget(self, scene, text, directiveType, id):
        flowWidget = self.webAutoWidgetFactory.createWebAutoWidget(scene, text, directiveType, id)

        if flowWidget:
            return flowWidget

        flowWidget = self.startOrEndWidgetFactory.createStartOrEndWidget(scene, text, directiveType, id)

        if flowWidget:
            return flowWidget

        return None


