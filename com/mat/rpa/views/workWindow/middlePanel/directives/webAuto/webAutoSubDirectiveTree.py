# -*- coding:utf-8 -*-

from com.mat.rpa.utils.globalConstants import GlobalConstants
from com.mat.rpa.views.workWindow.leftPanel.directiveTree import treeItem
from . import webAutoConstants
from .webElementOperation import webElementOperationSubDirectiveTree
from .webPageOperation import webPageOperationSubDirectiveTree
from .webDataRetrievingOperation import webDataRetrievingSubDirectiveTree

class WebAutoSubDirectiveTree(treeItem.TreeItemWithID):
    def __init__(self, parent):
        super(WebAutoSubDirectiveTree, self).__init__(parent)
        self.createWebAutoTreeNode()

    def createWebAutoTreeNode(self):
        self.nodeType = GlobalConstants.treeBranchType
        self.directiveType = "webAutoNode"
        self.setText(0,"网页自动化")
        self.createTreeNode(GlobalConstants.treeLeafType,
                            self, webAutoConstants.WebAutoConstants.openningWebPageDirective, "打开网页")
        self.createTreeNode(GlobalConstants.treeLeafType,
                            self, webAutoConstants.WebAutoConstants.clickingWebElementDirective, "点击元素(Web)")
        self.createTreeNode(GlobalConstants.treeLeafType,
                            self, webAutoConstants.WebAutoConstants.mouseHoveringOverWebElementDirective, "鼠标悬停在元素上(Web)")
        self.createTreeNode(GlobalConstants.treeLeafType,
                            self, webAutoConstants.WebAutoConstants.fillingInWebInputDirective, "填写输入框")
        self.createTreeNode(GlobalConstants.treeLeafType,
                            self, webAutoConstants.WebAutoConstants.closingWebPageDirective, "关闭网页")
        webElementOperationSubDirectiveTree.WebElementOperationSubDirectiveTree(self) #挂载元素操作子节点
        webPageOperationSubDirectiveTree.WebPageOperationSubDirectiveTree(self) #挂载web网页操作节点
        webDataRetrievingSubDirectiveTree.WebDataRetrievingSubDirectiveTree(self) #挂载数据抓取子节点
