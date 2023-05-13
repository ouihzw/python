# -*- coding:utf-8 -*-
from com.mat.rpa.utils.globalConstants import GlobalConstants
from com.mat.rpa.views.workWindow.leftPanel.directiveTree import treeItem
from . import similarElementConstants

class SimilarElementSubDirectiveTree(treeItem.TreeItemWithID):
    def __init__(self, parent):
        super(SimilarElementSubDirectiveTree, self).__init__(parent)
        self.createsimilarElementSubTreeNode()

    def createsimilarElementSubTreeNode(self):
        self.nodeType = GlobalConstants.treeBranchType
        self.directiveType = "similarElement"
        self.setText(0, "相似元素操作")
        self.createTreeNode(GlobalConstants.treeLeafType,
                            self, similarElementConstants.SimilarElementConstants.circulatingSimilarWebElementDirective, "循环相似元素(Web)")
        self.createTreeNode(GlobalConstants.treeLeafType,
                            self, similarElementConstants.SimilarElementConstants.circulatingSimilarWinElementDirective, "循环相似元素(Win)")
        self.createTreeNode(GlobalConstants.treeLeafType,
                            self, similarElementConstants.SimilarElementConstants.gettingSimilarWebElementListDirective, "获取相似元素(Web)")
        self.createTreeNode(GlobalConstants.treeLeafType,
                            self, similarElementConstants.SimilarElementConstants.gettingSimilarWinElementListDirective, "获取相似元素(Win)")