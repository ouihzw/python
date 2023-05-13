# -*- coding:utf-8 -*-
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from com.mat.rpa.views.workWindow.middlePanel.consolePanel.tabPanel import basicConsolePanel

class LogPanel(basicConsolePanel.BasicConsolePanel):
    picPath = "./com/mat/rpa/views/workWindow/middlePanel/consolePanel/tabPanel/images/"
    def __init__(self, parent=None):
        super(LogPanel, self).__init__(parent)
        self.hintLabel.setText("运行日志")
        self.exportBtn = QPushButton()
        self.exportBtn.setIcon(
            QIcon(QPixmap(LogPanel.picPath + "export.png")))
        self.btnPanelLayout.addWidget(self.exportBtn)
        self.deleteBtn = QPushButton()
        self.deleteBtn.setIcon(
            QIcon(QPixmap(LogPanel.picPath + "delete.png")))
        self.btnPanelLayout.addWidget(self.deleteBtn)
        self.runningLogPanelTable = QTableWidget()
        self.centerPanelLayout.addWidget(self.runningLogPanelTable,0,0,2,2)
        self.runningLogPanelTable.setColumnCount(3)
        self.runningLogPanelTable.setHorizontalHeaderLabels(["类型", "时间", "内容"])
        desktop = QApplication.desktop()
        rect = desktop.availableGeometry()
        screenWidth = rect.width()
        self.tableWidth = screenWidth * 0.54
        self.runningLogPanelTable.setColumnWidth(0, self.tableWidth*0.1)
        self.runningLogPanelTable.setColumnWidth(1, self.tableWidth*0.2)
        self.runningLogPanelTable.horizontalHeader().setStretchLastSection(True)