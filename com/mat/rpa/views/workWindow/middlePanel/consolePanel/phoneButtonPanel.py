from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class ButtonPanel(QFrame):
    picPath = "./com/mat/rpa/views/workWindow/middleWindow/consolePanel/images/"
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
        barlayout.addWidget(self.imageLibBtn, Qt.AlignLeft)
        self.errorListBtn = QPushButton("错误列表", self)
        self.errorListBtn.setMaximumWidth(100)
        self.errorListBtn.clicked.connect(self.errorListShow)
        barlayout.addWidget(self.errorListBtn, Qt.AlignLeft)
        self.runningLogBtn = QPushButton("运行日志", self)
        self.runningLogBtn.setMaximumWidth(100)
        self.runningLogBtn.clicked.connect(self.runningLogPanelShow)
        barlayout.addWidget(self.runningLogBtn, Qt.AlignLeft)
        self.dataTableBtn = QPushButton("数据表格", self)
        self.dataTableBtn.setMaximumWidth(100)
        self.dataTableBtn.clicked.connect(self.dataTablePanelShow)
        barlayout.addWidget(self.dataTableBtn, Qt.AlignLeft)
        self.flowParamBtn = QPushButton("流程参数", self)
        self.flowParamBtn.setMaximumWidth(100)
        self.flowParamBtn.clicked.connect(self.flowParameterPanelShow)
        barlayout.addWidget(self.flowParamBtn, Qt.AlignLeft)

        barlayout.addStretch(1)

        self.folddingUpBtn = QPushButton()
        self.folddingUpBtn.clicked.connect(self.handleFolddingUp)
        self.foldded = True #默认splitter关闭下边内容
        self.folddingUpBtn.setIcon(QIcon(QPixmap(ButtonPanel.picPath+"foldup.png")))
        self.folddingUpBtn.setMaximumWidth(32)
        barlayout.addWidget(self.folddingUpBtn)


    def handleFolddingUp(self):
        print("点击打开")

    def getConsolePanel(self, consolePanel):
        self.consolePanel=consolePanel
    def elementLibPanelShow(self):
        self.consolePanel.setCurrentIndex(0)
    def errorListShow(self):
        self.consolePanel.setCurrentIndex(2)
    def runningLogPanelShow(self):
        self.consolePanel.setCurrentIndex(3)
    def dataTablePanelShow(self):
        self.consolePanel.setCurrentIndex(4)
    def flowParameterPanelShow(self):
        self.consolePanel.setCurrentIndex(5)