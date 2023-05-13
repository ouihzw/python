# -*- coding:utf-8 -*-
from .webElementOperation import webElementOperationConstants
from .webPageOperation import webPageOperationConstants
from .webDataRetrievingOperation import webDataRetrievingContants
from .webDialogOperation import webDialogContants
class WebAutoConstants():
    openningWebPageDirective = "openningWebPageDirective"
    gettingOpenWebPageObjectDirective = "gettingOpenWebPageObjectDirective"
    clickingWebElementDirective = "clickingWebElementDirective"
    mouseHoveringOverWebElementDirective = "mouseHoveringOverWebElementDirective"
    fillingInWebInputDirective = "fillingInWebInputDirective"
    closingWebPageDirective = "closingWebPageDirective"
    webElementOperationContants = webElementOperationConstants.WebElementOperationConstants()
    webPageOperationContants = webPageOperationConstants.WebPageOperationConstants()
    webDataRetrievingContants = webDataRetrievingContants.WebDataRetrievingConstants()
    webDialogContants = webDialogContants.WebDialogConstants()


