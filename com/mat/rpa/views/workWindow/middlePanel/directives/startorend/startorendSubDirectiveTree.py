# -*- coding:utf-8 -*-
from com.mat.rpa.utils.globalConstants import GlobalConstants
from com.mat.rpa.views.workWindow.leftPanel.directiveTree import treeItem
from . import startorendContants

class StartorEndSubDirectiveTree(treeItem.TreeItemWithID):
    def __init__(self, parent):
        super(StartorEndSubDirectiveTree, self).__init__(parent)
        self.createstartorEndSubTreeNode()

    def createstartorEndSubTreeNode(self):
        self.nodeType = GlobalConstants.treeBranchType
        self.directiveType = "startorend"
        self.setText(0, "开始结束")
        self.createTreeNode(GlobalConstants.treeLeafType,
                            self, startorendContants.StartorEndConstants.startDirective, "开始")
        self.createTreeNode(GlobalConstants.treeLeafType,
                            self, startorendContants.StartorEndConstants.endDirective, "结束")