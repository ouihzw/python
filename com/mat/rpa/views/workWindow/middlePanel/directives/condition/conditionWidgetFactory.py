# -*- coding:utf-8 -*-
from . import conditionConstants
from .directiveWidgets.ifConditionDirective import ifConditionFlowStepWidget
from .directiveWidgets.ifMultiConditionDirective import ifMultiConditionFlowStepWidget
from .directiveWidgets.ifWebPageContainDirective import ifWebPageContainFlowStepWidget
from .directiveWidgets.ifWebElementVisibleDirective import ifWebElementVisibleFlowStepWidget
from .directiveWidgets.ifWindowExistsDirective import ifWindowExistsFlowStepWidget
from .directiveWidgets.ifWindowContainsDirective import ifWindowContainsFlowStepWidget
from .directiveWidgets.ifImageExistsDirective import ifImageExistsFlowStepWidget
from .directiveWidgets.ifTextExistsOnScreenOCRDirective import ifTextExistsOnScreenOCRFlowStepWidget
from .directiveWidgets.ifFileExistsDirective import ifFileExistsFlowStepWidget
from .directiveWidgets.ifFolderExistsDirective import ifFolderExistsFlowStepWidget
from .directiveWidgets.elseIfDirective import elseIfFlowStepWidget
from .directiveWidgets.elseIfMultiConditionDirective import elseIfMultiConditionFlowStepWidget
from .directiveWidgets.elseDirective import elseFlowStepWidget
from .directiveWidgets.endIfDirective import endIfFlowStepWidget

class ConditionWidgetFactory(object):
    __instance = None
    __isFirstInit = True

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super(ConditionWidgetFactory, cls).__new__(cls)
            return cls.__instance

    def __init__(self):
        cls = type(self)
        if cls.__isFirstInit:
            super().__init__()
            cls.__isFirstInit = False

    def createConditionWidget(self, widgetType, lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent):
        if widgetType == conditionConstants.ConditionConstants.ifConditionDirective:
            return ifConditionFlowStepWidget.IfConditionFlowWidget(lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent)
        elif widgetType == conditionConstants.ConditionConstants.ifMultiConditionDirective:
            return ifMultiConditionFlowStepWidget.IfMultiConditionFlowWidget(lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent)
        elif widgetType == conditionConstants.ConditionConstants.ifWebPageContainDirective:
            return ifWebPageContainFlowStepWidget.IfWebPageContainFlowWidget(lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent)
        elif widgetType == conditionConstants.ConditionConstants.ifWebElementVisibleDirective:
            return ifWebElementVisibleFlowStepWidget.IfWebElementVisibleFlowWidget(lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent)
        elif widgetType == conditionConstants.ConditionConstants.ifWindowExistsDirective:
            return ifWindowExistsFlowStepWidget.IfWindowExistsFlowWidget(lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent)
        elif widgetType == conditionConstants.ConditionConstants.ifWindowContainsDirective:
            return ifWindowContainsFlowStepWidget.IfWindowContainsFlowWidget(lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent)
        elif widgetType == conditionConstants.ConditionConstants.ifImageExistsDirective:
            return ifImageExistsFlowStepWidget.IfImageExistsFlowWidget(lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent)
        elif widgetType == conditionConstants.ConditionConstants.ifTextExistsOnScreenOCRDirective:
            return ifTextExistsOnScreenOCRFlowStepWidget.IfTextExistsOnScreenOCRFlowWidget(lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent)
        elif widgetType == conditionConstants.ConditionConstants.ifFileExistsDirective:
            return ifFileExistsFlowStepWidget.IfFileExistsFlowWidget(lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent)
        elif widgetType == conditionConstants.ConditionConstants.ifFolderExistsDirective:
            return ifFolderExistsFlowStepWidget.IfFolderExistsFlowWidget(lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent)
        elif widgetType == conditionConstants.ConditionConstants.elseIfDirective:
            return elseIfFlowStepWidget.ElseIfFlowWidget(lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent)
        elif widgetType == conditionConstants.ConditionConstants.elseIfMultiConditionDirective:
            return elseIfMultiConditionFlowStepWidget.ElseIfMultiConditionFlowWidget(lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent)
        elif widgetType == conditionConstants.ConditionConstants.elseDirective:
            return elseFlowStepWidget.ElseFlowWidget(lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent)
        elif widgetType == conditionConstants.ConditionConstants.endIfDirective:
            return endIfFlowStepWidget.EndIfFlowWidget(lineNumber, indentLevel, flowTitle, lineNumberWidthSignal, parent)

        return None