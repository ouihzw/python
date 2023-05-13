# -*- coding:utf-8 -*-
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from com.mat.rpa.views.workWindow.middlePanel.consolePanel import consolePanel, buttonPanel
from com.mat.rpa.views.workWindow.middlePanel.middleWindow.middleWindow import middleWindow, flowTabWindow


class MiddlePanel(QWidget):
    def __init__(self, parent=None):
        super(MiddlePanel, self).__init__(parent)
        self.parentPanel = parent
        self.entireLayout = QVBoxLayout()
        self.entireLayout.setContentsMargins(0,0,0,0)
        self.entireLayout.setSpacing(0)
        self.setLayout(self.entireLayout)
        #添加splitter
        self.topBottomSplitter = QSplitter(self)
        self.topBottomSplitter.setOrientation(Qt.Vertical)
        self.topBottomSplitter.setChildrenCollapsible(False)
        self.topBottomSplitter.splitterMoved.connect(self.splitterMoveRespose)
        self.entireLayout.addWidget(self.topBottomSplitter)
        # #添加flowTabWidget
        # self.flowTabWidget = flowTabWidget.FlowTabWidget(self)
        # self.topBottomSplitter.addWidget(self.flowTabWidget)
        #添加中间流程图部分
        self.flowTabWidget=flowTabWindow()
        self.topBottomSplitter.addWidget(self.flowTabWidget)
        #添加consoleTabWidget
        self.consoleWidget = consolePanel.ConsolePanel(self)
        self.topBottomSplitter.addWidget(self.consoleWidget)
        #调整位置
        self.topBottomSplitter.setSizes([990,0])
        #安装按钮面板
        self.btnPanel = buttonPanel.ButtonPanel(self)
        self.btnPanel.getConsolePanel(self.consoleWidget)
        self.entireLayout.addWidget(self.btnPanel)

    def splitterMoveRespose(self, index):
        print("splitterMoveRespose")

    def getConsolePanel(self,consolePanel):
        self.btnPanel.getConsolePanel(consolePanel)

if __name__=='__main__':
    app=QApplication(sys.argv)
    fms=MiddlePanel()
    fms.show()
    sys.exit(app.exec_())

