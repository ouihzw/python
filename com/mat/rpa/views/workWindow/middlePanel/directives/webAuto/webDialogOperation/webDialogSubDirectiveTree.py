# -*- coding:utf-8 -*-

from com.mat.rpa.utils.globalConstants import GlobalConstants
from com.mat.rpa.views.workWindow.leftPanel.directiveTree import treeItem
from . import webDialogContants

class WebDialogSubDirectiveTree(treeItem.TreeItemWithID):
    def __init__(self, parent):
        super(WebDialogSubDirectiveTree, self).__init__(parent)
        self.createWebDialogTreeNode()

    def createWebDialogTreeNode(self):
        self.nodeType = GlobalConstants.treeBranchType
        self.directiveType = "webDialogOperation"
        self.setText(0,"Web对话框处理")
        self.createTreeNode(GlobalConstants.treeLeafType,
                            self, webDialogContants.WebDialogConstants.uploadingFileDirective, "上传文件")
        self.createTreeNode(GlobalConstants.treeLeafType,
                            self, webDialogContants.WebDialogConstants.downloadingFileDirective, "下载文件")
        self.createTreeNode(GlobalConstants.treeLeafType,
                            self, webDialogContants.WebDialogConstants.processingDownloadDialogDirective, "处理下载对话框")
        self.createTreeNode(GlobalConstants.treeLeafType,
                            self, webDialogContants.WebDialogConstants.processingUploadDialogDirective, "处理上传对话框")
        self.createTreeNode(GlobalConstants.treeLeafType,
                            self, webDialogContants.WebDialogConstants.processingWebDialogDirective, "处理网页对话框")