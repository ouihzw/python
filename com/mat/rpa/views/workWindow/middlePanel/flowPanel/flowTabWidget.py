# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from com.mat.rpa.utils.globalConstants import GlobalConstants
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowScrollAreaWidget
from com.mat.rpa.utils.action import ActionManager

tabBarStyleSheet = """
QTabBar::tab {
    height: 32px;
}
QPushButton {
    height: 20px;
    width: 20px;
    border-style: none;
    border-width: 0px;
    border-radius: 4px;
}
QPushButton:hover {
    background-color: #f8A0A0;
}
QPushButton:pressed {
    background-color: #FF8080;
}
"""


class FlowTabWidget(QTabWidget):
    def __init__(self, parent=None):
        super(FlowTabWidget, self).__init__(parent)
        self.parentPanel = parent
        self.setTabsClosable(True)
        self.setMovable(True)
        self.setAcceptDrops(True)
        self.setObjectName("flowTabWidget")
        self.mainFlowTab = flowScrollAreaWidget.FlowScrollAreaWidget(GlobalConstants.PCAppMode, self)
        self.addTab(self.mainFlowTab, "主流程.flow")
        self.tabBar().setTabButton(0, QTabBar.RightSide, None)
        self.tabBar().setStyleSheet(tabBarStyleSheet)
        self.actionManager = ActionManager()
        self.currentChanged.connect(self.tabChanged)
        self.flowTabDict = {}
        __font = QFont()
        __font.setFamily("Microsoft YaHei")
        self.setFont(__font)

    # 打开新页面
    def openNewTab(self, flowId, flowName):
        if flowId not in self.flowTabDict:
            newTab = flowScrollAreaWidget.FlowScrollAreaWidget(GlobalConstants.PCAppMode, self)
            newTab.innerWidget.id = flowId
            newTab.innerWidget.buildFlowWidgetsFromDB()
            closeButton = QPushButton()
            closeButton.setIcon(QIcon("./com/mat/rpa/views/workWindow/images/close.png"))
            closeButton.clicked.connect(lambda: self.closeTab(flowId))
            idx = self.addTab(newTab, flowName)
            self.flowTabDict[flowId] = newTab
            self.tabBar().setTabButton(idx, QTabBar.RightSide, closeButton)
            self.setCurrentIndex(idx)

    # 撤销
    def undo(self):
        self.currentWidget().innerWidget.undo()

    # 重做
    def redo(self):
        self.currentWidget().innerWidget.redo()

    # 更新页面名称
    def changeTabName(self, flowId, flowName):
        if flowId in self.flowTabDict:
            self.setTabText(self.indexOf(self.flowTabDict[flowId]), flowName)

    # 关闭窗口
    def closeTab(self, flowId):
        self.removeTab(self.indexOf(self.flowTabDict[flowId]))
        del self.flowTabDict[flowId]

    # 更新撤销重做状态
    def tabChanged(self, idx: int):
        self.actionManager.changeTab(self.widget(idx).innerWidget.id)