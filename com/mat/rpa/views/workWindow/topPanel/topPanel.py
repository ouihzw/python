# -*- coding:utf-8 -*-
import sys
import traceback

from com.mat.rpa.views.loginWindow import loginWindow
from com.mat.rpa.views.workWindow.middlePanel.middleWindow.node_graphics_view import QDMGraphicsView
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
# 即用于加入上方工具栏的RPA浏览器功能
from com.mat.rpa.views.workWindow.topPanel.rpaWebBrowser import rpaWebBrowser
# 用于编辑应用信息，并保存的
from com.mat.rpa.views.workWindow.topPanel.appInfoEditorDialog.appInfoEditorDialog import AppInfoEditorDialog
# 控制撤销、重做操作的按键
from com.mat.rpa.utils.action import ActionManager
# 用于导出应用信息
from com.mat.rpa.views.workWindow.topPanel.export.exportFlow import ExportFlow

styleSheet = """
QToolBar {
    border-radius: 8px;
    border-style: none;
    background-color: #fff;
    margin: 7px;
    padding: 5px;
}
QToolButton {
    min-width: 50px;
    min-height: 40px;
}
"""


class TopBar(QToolBar):
    picPath = "./com/mat/rpa/views/workWindow/topPanel/images/"
    Signal_fullscreen = pyqtSignal()

    def __init__(self, parent=None, flowTabWindow=None):
        super(TopBar, self).__init__(parent)
        self.parentWindow = parent
        self.flowTabWindow = flowTabWindow
        self.initUI()
        self.setContentsMargins(0, 0, 0, 0)
        self.appId = None

    def initUI(self):
        __font = QFont()
        __font.setPixelSize(11)
        __font.setFamily("Microsoft YaHei")
        self.setFont(__font)
        self.setFloatable(False)
        self.setMovable(False)
        # 编辑应用信息按钮
        self.editAppInfoBtn = QToolButton()
        self.editAppInfoBtn.setText("退出登录")
        self.editAppInfoBtn.setIcon(QIcon(TopBar.picPath + "editInfo.png"))
        self.editAppInfoBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.editAppInfoBtn.clicked.connect(self.editAppInfo)
        self.addWidget(self.editAppInfoBtn)
        # 添加分割线
        self.addSeparator()
        # 添加RPA浏览器按钮
        self.webBrowserBtn = QToolButton()
        self.webBrowserBtn.clicked.connect(self.openRpaWebBrowser)
        self.isWebBrowserExists = False
        self.webBrowserBtn.setText("RPA浏览器")
        self.webBrowserBtn.setIcon(QIcon(TopBar.picPath + "webBrowser.png"))
        self.webBrowserBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.addWidget(self.webBrowserBtn)
        # 添加分割线
        self.addSeparator()
        # 添加分割线
        self.addSeparator()
        # 添加执行按钮
        self.runBtn = QToolButton()
        self.runBtn.setText("运行")
        self.runBtn.setIcon(QIcon(TopBar.picPath + "run.png"))
        self.runBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.runBtn.clicked.connect(self.handleRunBtn)
        self.addWidget(self.runBtn)
        # 添加分割线
        self.addSeparator()
        # 添加连线按钮
        self.edgeBtn = QToolButton()
        self.edgeBtn.setText("不连线")
        self.edgeBtn.setIcon(QIcon(TopBar.picPath + "connect.png"))
        self.edgeBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.edgeBtn.clicked.connect(self.ifConnect)
        self.addWidget(self.edgeBtn)
        self.addSeparator()
        # 添加流程图全屏按钮
        self.fullscreenBtn = QToolButton()
        self.fullscreenBtn.setText("全屏")
        self.fullscreenBtn.setIcon(QIcon(TopBar.picPath + "fullscreen.jfif"))
        self.fullscreenBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.fullscreenBtn.clicked.connect(self.fullscreen)
        self.addWidget(self.fullscreenBtn)
        self.addSeparator()

        self.setStyleSheet(styleSheet)
        shadow = QGraphicsDropShadowEffect()
        shadow.setOffset(0, 0)
        shadow.setBlurRadius(9)
        shadow.setColor(QColor(70, 70, 70))
        self.setGraphicsEffect(shadow)

        self.flowTabWindow.currentChanged.connect(self.Typechange)

    def fullscreen(self):
        # 发射全屏信号
        self.Signal_fullscreen.emit()

    def editAppInfo(self, window: loginWindow.LoginWindow):
        self.loginWindow = window
        self.hide()
        loginWindowObj = self.loginWindow
        result = loginWindowObj.exec()
        if result != QDialog.Accepted:
            sys.exit()
        # 重新初始化工程管理页面
        self.__init__()
        self.show()
        self.setLoginWindow(loginWindowObj)

    # 导出当前Flow
    def exportCurrentFlow(self):
        try:
            currentFlowId = self.parent().middleWorkPanel.flowTabWidget.currentWidget().innerWidget.id
            ExportFlow(currentFlowId).save()
        except Exception as e:
            traceback.print_exc()

    def saveFlow(self):
        try:
            self.flowTabWindow.flowIdxDict[self.flowTabWindow.currentIndex()].grScene.scene.saveToMongo(self.appId)
            return
        except Exception as e:
            print("e")

    def ifConnect(self):
        # self.grScene.ifconnetableChange()
        self.ifConnectable = self.flowTabWindow.flowIdxDict[
            self.flowTabWindow.currentIndex()].grScene.ifconnetableChange()
        if self.ifConnectable:
            self.edgeBtn.setText("可连线")
        else:
            self.edgeBtn.setText("不可连线")

    def Typechange(self):
        self.ifConnectable = self.flowTabWindow.flowIdxDict[self.flowTabWindow.currentIndex()].grScene.getType()
        if self.ifConnectable:
            self.edgeBtn.setText("可连线")
        else:
            self.edgeBtn.setText("不可连线")

    # 打开RPA浏览器
    def openRpaWebBrowser(self):
        if self.isWebBrowserExists and self.webBrowser.isVisible():
            if self.webBrowser.isHidden():
                self.webBrowser.show()
            elif self.webBrowser.isMinimized():
                self.webBrowser.showNormal()
                self.webBrowser.raise_()
            else:
                self.webBrowser.raise_()
        else:
            self.isWebBrowserExists = True
            self.webBrowser = rpaWebBrowser.RPAWebBrowser()
            self.webBrowser.show()

    # 运行按钮
    def handleRunBtn(self):
        self.flowTabWindow.flowIdxDict[self.flowTabWindow.currentIndex()].grScene.scene.run()
        return
        # middlePanel = self.parentWindow.middleWorkPanel
        # flowTabWidget = middlePanel.flowTabWidget
        # mainFlowTab = flowTabWidget.mainFlowTab
        # innerWidget = mainFlowTab.innerWidget
        # innerWidgetLayout = innerWidget.innerWidgetLayout
        # i = 0
        # print("开始运行")
        # while i < innerWidgetLayout.count() - 1:
        #     item = innerWidgetLayout.itemAt(i).widget()
        #     item.executeStep()
        #     i += 1

    def setAppId(self, id):
        self.appId = id
        self.flowTabWindow.flowIdxDict[self.flowTabWindow.currentIndex()].grScene.scene.loadFromMongo(id)
