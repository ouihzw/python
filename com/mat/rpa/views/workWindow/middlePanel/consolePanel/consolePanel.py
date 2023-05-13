# -*- coding:utf-8 -*-
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from com.mat.rpa.views.workWindow.middlePanel.consolePanel.tabPanel import elementLibPanel
from com.mat.rpa.views.workWindow.middlePanel.consolePanel.tabPanel import imagePanel
from com.mat.rpa.views.workWindow.middlePanel.consolePanel.tabPanel import errorListPanel
from com.mat.rpa.views.workWindow.middlePanel.consolePanel.tabPanel import logPanel
from com.mat.rpa.views.workWindow.middlePanel.consolePanel.tabPanel import dataTablePanel
from com.mat.rpa.views.workWindow.middlePanel.consolePanel.tabPanel import flowParameterPanel
class ConsolePanel(QStackedWidget):
    def __init__(self, parent=None):
        super(ConsolePanel, self).__init__(parent)
        self.parentPanel = parent
        self.elementLibPanel = elementLibPanel.ElementLibPanel()
        self.addWidget(self.elementLibPanel)
        self.imageLibPanel = imagePanel.ImagePanel(self)
        self.addWidget(self.imageLibPanel)
        self.errorList = errorListPanel.ErrorListPanel()
        self.addWidget(self.errorList)
        self.runninglogPanel = logPanel.LogPanel()
        self.addWidget(self.runninglogPanel)
        self.dataTablePanel = dataTablePanel.DataTablePanel()
        self.addWidget(self.dataTablePanel)
        self.flowParameterPanel = flowParameterPanel.FlowParameterPanel()
        self.addWidget(self.flowParameterPanel)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ConsolePanel()
    win.show()
    app.exec_()