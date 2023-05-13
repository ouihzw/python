# -*- coding:utf-8 -*-
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class BasicConsolePanel(QFrame):
    picPath = "./com/mat/rpa/views/workWindow/middlePanel/consolePanel/images/"
    def __init__(self, parent=None):
        super(BasicConsolePanel, self).__init__(parent)
        #设置布局
        self.entireLayout = QVBoxLayout()
        self.setLayout(self.entireLayout)
        self.entireLayout.setContentsMargins(0,0,0,0)
        self.entireLayout.setSpacing(0)
        #创建顶部面板
        self.topPanel = QWidget()
        self.topPanelLayout = QHBoxLayout()
        self.topPanelLayout.setContentsMargins(0,0,0,0)
        self.topPanelLayout.setSpacing(0)
        ##安装提示label
        self.hintLabel = QLabel()
        self.hintLabel.setText("默认信息")
        self.topPanelLayout.addWidget(self.hintLabel)
        ##安装弹簧
        self.topPanelLayout.addStretch(1)
        ##安装stackedWidget
        self.stackedWidget = QStackedWidget()
        self.stackedWidget.setContentsMargins(0, 0, 0, 0)
        self.topPanelLayout.addWidget(self.stackedWidget)
        self.topPanel.setLayout(self.topPanelLayout)
        ###安装按钮Panel
        self.btnPanel=QWidget()
        self.btnPanelLayout=QHBoxLayout()
        self.btnPanel.setLayout(self.btnPanelLayout)
        self.btnPanelLayout.setContentsMargins(0,0,0,0)
        self.btnPanelLayout.setSpacing(0)
        self.btnPanelLayout.addStretch(1)
        self.stackedWidget.addWidget(self.btnPanel)
        self.stackedWidget.setCurrentIndex(0)
        ###安装搜素面板
        self.searchBoxPanel=QWidget()
        self.searchBoxPanelLayout=QHBoxLayout()
        self.searchBoxPanel.setLayout(self.searchBoxPanelLayout)
        self.searchBoxPanelLayout.setContentsMargins(0,0,0,0)
        self.searchBoxPanelLayout.setSpacing(0)
        self.searchBoxPanelLayout.addStretch(1)
        self.searchBox=QLineEdit()
        self.searchBoxPanelLayout.addWidget(self.searchBox)
        self.searchBtn_2=QPushButton()
        self.searchBtn_2.setIcon(QIcon(BasicConsolePanel.picPath+"Search.png"))
        self.searchBoxPanelLayout.addWidget(self.searchBtn_2)
        self.closeSearchBtn=QPushButton()
        self.closeSearchBtn.setIcon(QIcon(BasicConsolePanel.picPath+"closeSearch.png"))
        self.searchBoxPanelLayout.addWidget(self.closeSearchBtn)
        self.stackedWidget.addWidget(self.searchBoxPanel)
        self.entireLayout.addWidget(self.topPanel,0.5)
        #添加网格布局
        self.stackedWidget_2=QStackedWidget()
        self.stackedWidget_2.setContentsMargins(0, 0, 0, 0)
        self.entireLayout.addWidget(self.stackedWidget_2,9.5)
        self.centerPanel = QWidget()
        self.stackedWidget_2.addWidget(self.centerPanel)
        self.centerPanelLayout = QGridLayout()
        self.centerPanel.setLayout(self.centerPanelLayout)
        self.centerPanelLayout.setContentsMargins(0, 0, 0, 0)
        self.centerPanelLayout.setSpacing(10)
        self.centerPanelLayout.setColumnStretch(0,2)
        self.centerPanelLayout.setColumnStretch(1,1)
        self.centerPanelLayout.setRowStretch(0, 2)
        self.centerPanelLayout.setRowStretch(1, 3)
        self.stackedWidget_2.setCurrentIndex(0)
        self.displayImagePanel=QScrollArea()
        self.displayImagePanel.setWidgetResizable(True)
        self.stackedWidget_2.addWidget(self.displayImagePanel)
        self.scrollAreaWidgetContents=QWidget()
        self.scrollAreaWidgetContents.setStyleSheet('''QWidget{background-color:white;}''')
        self.displayImagePanelLayout=QGridLayout()
        self.displayImagePanelLayout.setContentsMargins(10, 10, 10, 0)
        self.displayImagePanelLayout.setSpacing(10)
        self.scrollAreaWidgetContents.setLayout(self.displayImagePanelLayout)
        for i in range(0, 9):
            self.displayImagePanelLayout.setColumnStretch(i, 1)
        for i in range(0, 9):
            self.displayImagePanelLayout.setRowStretch(i, 1)
        rowCount=self.displayImagePanelLayout.rowCount()
        for i in range(0,rowCount):
            self.displayImagePanelLayout.setRowMinimumHeight(i,100)
        self.displayImagePanel.setWidget(self.scrollAreaWidgetContents)


    def handlefolddingBtnClicked(self):
        pass

