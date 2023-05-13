# -*- coding:utf-8 -*-

from com.mat.rpa.utils.globalConstants import GlobalConstants
from com.mat.rpa.views.workWindow.leftPanel.directiveTree import treeItem
from . import webPageOperationConstants

class WebPageOperationSubDirectiveTree(treeItem.TreeItemWithID):
    def __init__(self, parent):
        super(WebPageOperationSubDirectiveTree, self).__init__(parent)
        self.createWebPageOperationTreeNode()

    def createWebPageOperationTreeNode(self):
        self.nodeType = GlobalConstants.treeBranchType
        self.directiveType = "webPageOperation"
        self.setText(0,"Web页面操作")
        self.createTreeNode(GlobalConstants.treeLeafType,
                            self, webPageOperationConstants.WebPageOperationConstants.redirectingToNewWebPageDirective, "跳转至新页面")
        self.createTreeNode(GlobalConstants.treeLeafType,
                            self, webPageOperationConstants.WebPageOperationConstants.waitingForLoadingPageDirective, "等待网页加载完成")
        self.createTreeNode(GlobalConstants.treeLeafType,
                            self, webPageOperationConstants.WebPageOperationConstants.stoppingLoadingPageDirective, "停止网页加载")
        self.createTreeNode(GlobalConstants.treeLeafType,
                            self, webPageOperationConstants.WebPageOperationConstants.mouseScrollingPageDirective, "鼠标滚动网页")
        self.createTreeNode(GlobalConstants.treeLeafType,
                            self, webPageOperationConstants.WebPageOperationConstants.executingJSDirective, "执行JS脚本")
