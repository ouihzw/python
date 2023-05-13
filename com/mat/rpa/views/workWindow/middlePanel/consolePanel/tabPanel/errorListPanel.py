# -*- coding:utf-8 -*-
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from com.mat.rpa.views.workWindow.middlePanel.consolePanel.tabPanel import basicConsolePanel


class ErrorListPanel(basicConsolePanel.BasicConsolePanel):
    def __init__(self, parent=None):
        super(ErrorListPanel, self).__init__(parent)
        self.hintLabel.setText("错误列表")
        self.errorListTable = QTableWidget()
        self.centerPanelLayout.addWidget(self.errorListTable,0,0,2,2)
        self.errorListTable.setColumnCount(3)
        self.errorListTable.setHorizontalHeaderLabels(["错误信息","流程名称","行号"])
        desktop=QApplication.desktop()
        rect=desktop.availableGeometry()
        screenWidth=rect.width()
        self.tableWidth=screenWidth*0.54
        self.errorListTable.setColumnWidth(0,self.tableWidth*0.7)
        self.errorListTable.setColumnWidth(1,self.tableWidth*0.2)
        self.errorListTable.horizontalHeader().setStretchLastSection(True)