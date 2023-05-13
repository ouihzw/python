# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from com.mat.rpa.utils.globalConstants import GlobalConstants

class TreeItemWithID(QTreeWidgetItem):
    def __init__(self, parent=None):
        self.directiveType = "id" #表示节点对应的指令类型
        self.nodeType = GlobalConstants.treeLeafType #判断节点类型:branch表示树节点，leaf表示树叶，树叶允许放入，而树枝不允许
        super(TreeItemWithID, self).__init__(parent)

    def setDirectiveType(self, directiveType):
        self.directiveType = directiveType

    def setNodeType(self, nodeType):
        self.nodeType = nodeType

    def getDirectiveType(self):
        return self.directiveType

    def createTreeNode(self, nodeType, parentNode, directiveType, text):
        node = TreeItemWithID(parentNode)
        node.setNodeType(nodeType)
        node.setDirectiveType(directiveType)
        node.setText(0, text)
        return node