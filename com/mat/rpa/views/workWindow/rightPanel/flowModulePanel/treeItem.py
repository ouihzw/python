# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *


class TreeItemWithID(QTreeWidgetItem):
    def __init__(self, parent=None):
        self.nodeName = "name"  # 表示节点对应的指令类型
        self.flowId = None
        super(TreeItemWithID, self).__init__(parent)

    def setNodeName(self, nodeName):
        self.nodeName = nodeName

    def createTreeNode(self, parentNode, nodeName, text, icon=None):
        node = TreeItemWithID(parentNode)
        node.setNodeName(nodeName)
        node.setText(0, text)
        if icon != None:
            node.setIcon(0, icon)
        return node
