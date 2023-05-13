# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from com.mat.rpa.views.workWindow.rightPanel.flowModulePanel import flowModulePanel

from com.mat.rpa.views.workWindow.rightPanel.globalVariablePanel import globalVariablePanel
import sys

class RightPanel(QFrame):
    def __init__(self, parent=None):
        super(RightPanel, self).__init__(parent)
        self.parentPanel = parent
        self.entireLayout = QHBoxLayout()
        self.entireLayout.setContentsMargins(0,0,0,0)
        self.entireLayout.setSpacing(0)
        self.setLayout(self.entireLayout)
        #设置布局管理器
        self.topBottomSplitter = QSplitter(self)
        self.entireLayout.addWidget(self.topBottomSplitter)
        self.topBottomSplitter.setMinimumSize(QSize(0, 100))
        self.topBottomSplitter.setOrientation(Qt.Vertical)
        self.topBottomSplitter.setChildrenCollapsible(False)
        self.topBottomSplitter.setObjectName("rightPanelTopBottomSplitter")
        self.topBottomSplitter.setSizes([800, 200])
        #添加flowModulePanel
        self.flowManagementPanel = flowModulePanel.FlowModulePanel(self)
        self.topBottomSplitter.addWidget(self.flowManagementPanel)
        #添加全部变量表
        self.variableTable = globalVariablePanel.GlobalVariablePanel(self)
        self.topBottomSplitter.addWidget(self.variableTable)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = RightPanel()
    win.show()
    app.exec_()