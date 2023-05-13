from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class ButtonPanel(QFrame):
    picPath = "./com/mat/rpa/views/workWindow/middlePanel/consolePanel/images/"
    def __init__(self, parent=None):
        super(ButtonPanel, self).__init__(parent)
        self.parentPanel=parent
        self.consolePanel=None
        self.setStyleSheet("ButtonPanel {background-color:white;}")
        barlayout = QHBoxLayout(self)
        barlayout.setContentsMargins(0,5,5,5)
        self.elementLibBtn = QPushButton("元素库", self)
        self.elementLibBtn.setMaximumWidth(100)
        self.elementLibBtn.clicked.connect(self.elementLibPanelShow)
        barlayout.addWidget(self.elementLibBtn, Qt.AlignLeft)
        # self.intelligentRecordBtn = QPushButton("智能录制", self)
        # self.intelligentRecordBtn.setMaximumWidth(100)
        # self.intelligentRecordBtn.clicked.connect(self.intelligentRecordPanelShow)
        # barlayout.addWidget(self.intelligentRecordBtn, Qt.AlignLeft)

        barlayout.addStretch(1)


    def handleFolddingUp(self):
        print("点击打开")

    def getConsolePanel(self, consolePanel):
        self.consolePanel=consolePanel
    def elementLibPanelShow(self):
        self.consolePanel.setCurrentIndex(0)
    # def intelligentRecordPanelShow(self):
    #     self.consolePanel.setCurrentIndex(6)