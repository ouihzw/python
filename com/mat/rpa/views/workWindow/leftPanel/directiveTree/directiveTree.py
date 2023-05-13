# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from com.mat.rpa.views.workWindow.middlePanel.directives.similarElement import similarElementSubDirectiveTree
from com.mat.rpa.views.workWindow.middlePanel.directives.webAuto import webAutoSubDirectiveTree
#负责建立节点树的，具体运作逻辑没有细看
from . import treeItem
#也是负责节点树的建立的，具体逻辑还不是很清楚
from com.mat.rpa.utils.globalConstants import GlobalConstants

from com.mat.rpa.views.workWindow.middlePanel.directives.condition import conditionSubDirectiveTree
from com.mat.rpa.views.workWindow.middlePanel.directives.circle import circleSubDirectiveTree
from com.mat.rpa.views.workWindow.middlePanel.directives.startorend import startorendSubDirectiveTree

#directiveTree负责引入其他的挂载节点，如网页自动化，桌面软件自动化等内容，由middlePanel的directives负责添加并且加入内容

class DirectiveTree(QTreeWidget):
    picPath = "./com/mat/rpa/views/workWindow/images/"
    def __init__(self, parent=None):
        super(DirectiveTree, self).__init__(parent)
        self.setColumnCount(2)
        # self.setHeaderLabels(["",""])
        self.setHeaderHidden(True) #隐藏标题头
        self.setStyleSheet("QTreeView::item {height: 30px;};")
        # 获得屏幕尺寸
        desktop = QApplication.desktop()
        rect = desktop.availableGeometry()
        screenWidth = rect.width()
        self.LeftWidth = screenWidth * 0.25
        self.setColumnWidth(0, self.LeftWidth*0.74)
        self.setColumnWidth(1, self.LeftWidth * 0.22)
        #向指令树添加开始结束子节点
        startorendSubDirectiveTree.StartorEndSubDirectiveTree(self)
        # #向指令树添加等待子节点
        #waitSubDirectiveTree.WaitSubDirectiveTree(self)
        #挂载网页自动化子节点
        webAutoSubDirectiveTree.WebAutoSubDirectiveTree(self)


    def createTreeNode(self, nodeType, parentNode, directiveType, text, icon=None):
        node = treeItem.TreeItemWithID(parentNode)
        node.setNodeType(nodeType)
        node.setDirectiveType(directiveType)
        node.setText(0, text)
        if icon != None:
            node.setIcon(0, icon)
        return node

    def handleGetDirectiveClicked(self):
        print("点击了获取指令")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.item = self.itemAt(event.pos())#####
            if self.item:
                self.setCurrentItem(self.item)
                print("mousePressEvent 当前选中", self.item.text(0))
            else:
                print("mousePressEvent 没有选中")
        super(DirectiveTree, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            if self.item:
                mimeData = QMimeData()
                mimeData.setObjectName("leaf")
                mimeData.setText(self.item.nodeType+"|"+self.item.directiveType+"|"+self.item.text(0))
                drag = QDrag(self)
                drag.setMimeData(mimeData)
                drag.exec_(Qt.MoveAction)
        # super(DirectiveTree, self).mouseMoveEvent(event)

