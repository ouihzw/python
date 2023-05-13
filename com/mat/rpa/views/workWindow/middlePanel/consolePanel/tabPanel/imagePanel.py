import sys,time,os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from com.mat.rpa.views.workWindow.middlePanel.consolePanel.tabPanel import basicConsolePanel


class ImagePanel(basicConsolePanel.BasicConsolePanel):
    picPath = "./com/mat/rpa/views/workWindow/middlePanel/consolePanel/tabPanel/images/"
    picPath_2="./com/mat/rpa/views/workWindow/middleWindow/consolePanel/tabPanel/screenShot/"
    def __init__(self, parent=None):
        super(ImagePanel, self).__init__(parent)
        self.parentPanel = parent