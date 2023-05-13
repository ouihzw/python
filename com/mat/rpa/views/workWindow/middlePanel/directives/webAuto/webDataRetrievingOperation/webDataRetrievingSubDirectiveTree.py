# -*- coding:utf-8 -*-

from com.mat.rpa.utils.globalConstants import GlobalConstants
from com.mat.rpa.views.workWindow.leftPanel.directiveTree import treeItem
from . import webDataRetrievingContants

class WebDataRetrievingSubDirectiveTree(treeItem.TreeItemWithID):
    def __init__(self, parent):
        super(WebDataRetrievingSubDirectiveTree, self).__init__(parent)
        self.createWebDataRetrievingTreeNode()

    def createWebDataRetrievingTreeNode(self):
        self.nodeType = GlobalConstants.treeBranchType
        self.directiveType = "webDataRetrievingOperation"
        self.setText(0,"Web页面数据提取")
        self.createTreeNode(GlobalConstants.treeLeafType,
                            self, webDataRetrievingContants.WebDataRetrievingConstants.massDataGrabbingDirective, "电商商品信息获取")
        self.createTreeNode(GlobalConstants.treeLeafType,
                            self, webDataRetrievingContants.WebDataRetrievingConstants.webPageScreenshotDirective, "网页截图")

