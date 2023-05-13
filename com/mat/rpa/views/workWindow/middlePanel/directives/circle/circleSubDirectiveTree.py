# -*- coding:utf-8 -*-
from com.mat.rpa.utils.globalConstants import GlobalConstants
from com.mat.rpa.views.workWindow.leftPanel.directiveTree import treeItem
from . import circleGlobalConstants

class CircleSubDirectiveTree(treeItem.TreeItemWithID):
    def __init__(self, parent):
        super(CircleSubDirectiveTree, self).__init__(parent)
        self.createCircleSubTreeNode()

    def createCircleSubTreeNode(self):
        self.nodeType = GlobalConstants.treeBranchType
        self.directiveType = "circle"
        self.setText(0, "循环")
        self.createTreeNode(GlobalConstants.treeLeafType,
                              self, circleGlobalConstants.CircleConstants.forCircleDirective, "For次数循环")
        self.createTreeNode(GlobalConstants.treeLeafType,
                              self, circleGlobalConstants.CircleConstants.whileCircleDirective, "While条件循环")
        self.createTreeNode(GlobalConstants.treeLeafType,
                              self, circleGlobalConstants.CircleConstants.forEachListCircleDirective, "ForEach列表循环")
        self.createTreeNode(GlobalConstants.treeLeafType,
                              self, circleGlobalConstants.CircleConstants.forEachDictCircleDirective, "ForEach字典循环")
        self.createTreeNode(GlobalConstants.treeLeafType,
                              self, circleGlobalConstants.CircleConstants.endlessCircleDirective, "无限循环")
        self.createTreeNode(GlobalConstants.treeLeafType,
                              self, circleGlobalConstants.CircleConstants.circulatingSimilaWebElementDirective, "循环相似元素(Web)")
        self.createTreeNode(GlobalConstants.treeLeafType,
                              self, circleGlobalConstants.CircleConstants.circulatingSimilaWinElementDirective, "循环相似元素(Win)")
        self.createTreeNode(GlobalConstants.treeLeafType,
                            self, circleGlobalConstants.CircleConstants.circulatingExcelDirective, "循环Excel内容")
        self.createTreeNode(GlobalConstants.treeLeafType,
                            self, circleGlobalConstants.CircleConstants.circulatingDataTableDirective, "循环数据表格内容")
        self.createTreeNode(GlobalConstants.treeLeafType,
                            self, circleGlobalConstants.CircleConstants.continueNextCircleDirective, "继续下一次循环")
        self.createTreeNode(GlobalConstants.treeLeafType,
                            self, circleGlobalConstants.CircleConstants.breakCircleDirective, "循环退出")
        self.createTreeNode(GlobalConstants.treeLeafType,
                            self, circleGlobalConstants.CircleConstants.endCircleDirective, "循环结束")