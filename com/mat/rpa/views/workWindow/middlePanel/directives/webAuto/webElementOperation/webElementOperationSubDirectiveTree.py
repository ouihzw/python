# -*- coding:utf-8 -*-

from com.mat.rpa.utils.globalConstants import GlobalConstants
from com.mat.rpa.views.workWindow.leftPanel.directiveTree import treeItem
from . import webElementOperationConstants

class WebElementOperationSubDirectiveTree(treeItem.TreeItemWithID):
    def __init__(self, parent):
        super(WebElementOperationSubDirectiveTree, self).__init__(parent)
        self.createWebElementOperationTreeNode()

    def createWebElementOperationTreeNode(self):
        self.nodeType = GlobalConstants.treeBranchType
        self.directiveType = "webElementOperation"
        self.setText(0,"Web元素操作")
        self.createTreeNode(GlobalConstants.treeLeafType,
                            self, webElementOperationConstants.WebElementOperationConstants.draggingWebElementDirective, "拖拽元素(Web)")
        self.createTreeNode(GlobalConstants.treeLeafType,
                            self, webElementOperationConstants.WebElementOperationConstants.waitingForWebElementDirective, "等待元素(Web)")
        self.createTreeNode(GlobalConstants.treeLeafType,
                            self, webElementOperationConstants.WebElementOperationConstants.fillingInPasswordWebInputDirective, "填写密码框(Web)")
        self.createTreeNode(GlobalConstants.treeLeafType,
                            self, webElementOperationConstants.WebElementOperationConstants.settingWebComboboxDirective, "设置下拉框(Web)")
        self.createTreeNode(GlobalConstants.treeLeafType,
                            self, webElementOperationConstants.WebElementOperationConstants.settingWebCheckBoxDirective, "设置复选框(Web)")
