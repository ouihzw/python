import sys
import cgitb
from PyQt5.QtGui import QIcon, QColor, QFont, QPen, QBrush, QPalette
from PyQt5.QtWidgets import QApplication, QToolBar, QAction, QPushButton, QGraphicsItem, QTextEdit, QWidget, QLayout, \
    QVBoxLayout, QTabBar, QTabWidget, QLabel
from PyQt5.QtCore import Qt, QFile
from PyQt5.QtWidgets import QMainWindow

from com.mat.rpa.utils.action import ActionManager
from com.mat.rpa.utils.globalConstants import GlobalConstants
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowScrollAreaWidget
from com.mat.rpa.views.workWindow.middlePanel.flowPanel.flowTabWidget import tabBarStyleSheet
from com.mat.rpa.views.workWindow.middlePanel.middleWindow.node_graphics_view import QDMGraphicsView
from com.mat.rpa.views.workWindow.middlePanel.middleWindow.node_scene import Scene
from com.mat.rpa.views.workWindow.middlePanel.middleWindow.node_node import Node, BeginNode, EndNode


class flowTabWindow(QTabWidget):
    def __init__(self):
        super().__init__()
        # self.setTabsClosable(True)
        # self.setMovable(True)
        # self.setAcceptDrops(True)
        self.setObjectName("flowTabWidget")
        self.mainFlowTab = middleWindow()
        self.mainFlowTab.title = "主流程.flow"
        self.addTab(self.mainFlowTab, "主流程.flow")
        self.tabBar().setTabButton(0, QTabBar.RightSide, None)
        self.tabBar().setStyleSheet(tabBarStyleSheet)
        self.actionManager = ActionManager()
        self.currentChanged.connect(self.tabChanged)
        self.flowTabDict = {}
        __font = QFont()
        __font.setFamily("Microsoft YaHei")
        self.setFont(__font)
        self.flowIdxDict={}
        self.flowIdxDict[self.currentIndex()]=self.mainFlowTab
    # 打开新页面
    def openNewTab(self, flowId, flowName):
        if flowId not in self.flowTabDict:
            newTab = middleWindow(self)
            newTab.grScene.id = flowId
            # newTab.innerWidget.buildFlowWidgetsFromDB()
            closeButton = QPushButton()
            closeButton.setIcon(QIcon("./com/mat/rpa/views/workWindow/images/close.png"))
            closeButton.clicked.connect(lambda: self.closeTab(flowId))
            newTab.title = flowName
            idx = self.addTab(newTab, flowName)
            self.flowTabDict[flowId] = newTab
            self.tabBar().setTabButton(idx, QTabBar.RightSide, closeButton)
            self.flowIdxDict[idx]=newTab
            self.setCurrentIndex(idx)


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
        self.actionManager.changeTab(self.widget(idx).grScene.id)


class middleWindow(QWidget):
    instances = []
    def __init__(self,parent=None):
        super(middleWindow,self).__init__(parent)

        self.scene = Scene()
        self.grScene = self.scene.grScene

        self.view = QDMGraphicsView(self.grScene, self)
        self.setMinimumHeight(500)
        self.setMinimumWidth(500)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.view)
        self.setLayout(self.layout)
        self.setWindowTitle("Graphics Demo")
        self.stylesheet_filename = 'qss/nestle.qss'
        self.loadStylesheet(self.stylesheet_filename)
        self.setAcceptDrops(True)
        self.flowTabDict= {}
        self.x = 0
        self.y = 0
        self.type = None
        self.title = None
        self.objectName = None
        middleWindow.instances.append(self)

    def getPos(self, event):
        self.x = event.x()
        self.y = event.y()


    def loadStylesheet(self, filename):
        file = QFile(filename)
        file.open(QFile.ReadOnly | QFile.Text)
        stylesheet = file.readAll()
        QApplication.instance().setStyleSheet(str(stylesheet, encoding='utf-8'))


    def setFlowMode(self, flowMode):
        self.flowMode = flowMode
        self.grScene.setFlowMode(flowMode)


