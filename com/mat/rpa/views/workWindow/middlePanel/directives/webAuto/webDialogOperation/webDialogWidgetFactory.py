# -*- coding:utf-8 -*-
from . import webDialogContants
from .directiveWidgets.uploadingFileDirective import uploadingFileFlowStepWidget
from .directiveWidgets.downloadingFileDirective import downloadingFileFlowStepWidget
from .directiveWidgets.processingDownloadDialogDirective import processingDownloadDialogFlowStepWidget
from .directiveWidgets.processingUploadDialogDirective import processingUploadDialogFlowStepWidget
from .directiveWidgets.processingWebDialogDirective import processingWebDialogFlowStepWidget

class WebDialogOperationWidgetFactory(object):
    __instance = None
    __isFirstInit = True
    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super(WebDialogOperationWidgetFactory, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        cls = type(self)
        if cls.__isFirstInit:
            super(WebDialogOperationWidgetFactory, self).__init__()
            cls.__isFirstInit = False

    def createWebDialogOperationWidget(self, scene, text, directiveType, id):
        if directiveType == webDialogContants.WebDialogConstants.uploadingFileDirective:
            return uploadingFileFlowStepWidget.UploadingFileFlowWidget(scene, text, directiveType, id, inputs=[1, 2, 3, 4], outputs=[])
        elif directiveType == webDialogContants.WebDialogConstants.downloadingFileDirective:
            return downloadingFileFlowStepWidget.DownloadingFileFlowWidget(scene, text, directiveType, id, inputs=[1, 2, 3, 4], outputs=[])
        elif directiveType == webDialogContants.WebDialogConstants.processingDownloadDialogDirective:
            return processingDownloadDialogFlowStepWidget.ProcessingDownloadDialogFlowWidget(scene, text, directiveType, id, inputs=[1, 2, 3, 4], outputs=[])
        elif directiveType == webDialogContants.WebDialogConstants.processingUploadDialogDirective:
            return processingUploadDialogFlowStepWidget.ProcessingUploadDialogFlowWidget(scene, text, directiveType, id, inputs=[1, 2, 3, 4], outputs=[])
        elif directiveType == webDialogContants.WebDialogConstants.processingWebDialogDirective:
            return processingWebDialogFlowStepWidget.ProcessingWebDialogFlowWidget(scene, text, directiveType, id, inputs=[1, 2, 3, 4], outputs=[])
        else:
            return None