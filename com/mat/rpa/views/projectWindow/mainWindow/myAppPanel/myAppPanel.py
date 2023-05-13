# -*- coding:utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from com.mat.rpa.views.workWindow import mainWindow    #在打开新窗口时需要用到
from com.mat.rpa.views.workWindow import AppMainWindow

from ..leftpanel import leftPanel
#左边的选项全都由该模块来初始化

from ..mainPanel.btnAndTablePanel import btnsAndTablePanel


class MyAppPanel(QWidget):
    picPath = "./com/mat/rpa/views/projectWindow/mainWindow/myAppPanel/images/"
    def __init__(self, parent=None):
        super(MyAppPanel, self).__init__(parent)
        self.parentPanel = parent
        #整体布局
        self.entireLayout = QHBoxLayout()
        self.setLayout(self.entireLayout)
        self.entireLayout.setContentsMargins(0,0,0,0)
        self.entireLayout.setSpacing(0)
        #左边面板
        self.leftPanelWidget = leftPanel.LeftPanel(self)
        self.leftPanelWidget.setCreateBtnText("新建应用")
        #添加菜单子项
        self.PCAutosubAction = QAction(QIcon(MyAppPanel.picPath+"PCAuto.png"), "PC自动化应用")
        self.leftPanelWidget.addActionToMenu(self.PCAutosubAction )
        self.phoneAutosubAction = QAction(QIcon(MyAppPanel.picPath+"phoneAuto.png"), "手机自动化应用")
        self.leftPanelWidget.addActionToMenu(self.phoneAutosubAction)
        # 绑定信号
        self.PCAutosubAction.triggered.connect(self.createPCAutoApp)
        self.phoneAutosubAction.triggered.connect(self.createPhoneAutoApp)
        self.entireLayout.addWidget(self.leftPanelWidget,2)
        #添加树节点
        ##我创建的应用节点
        myAppTreeItem = self.leftPanelWidget.getTreeNodeAtFirstLevel()
        myAppTreeItem.setText(0, '我创建的应用')
        myAppTreeItem.setIcon(0, QIcon(MyAppPanel.picPath+"myapps.png"))
        ###回收站节点
        garbageBinTreeItem = QTreeWidgetItem(myAppTreeItem)
        garbageBinTreeItem.setText(0,"回收站")
        garbageBinTreeItem.setIcon(0, QIcon(MyAppPanel.picPath + "garbageBin.png"))
        ##我获得的应用
        getAppTreeItem = self.leftPanelWidget.getTreeNodeAtFirstLevel()
        getAppTreeItem.setText(0, '我获得的应用')
        getAppTreeItem.setIcon(0, QIcon(MyAppPanel.picPath + "getApps.png"))
        #中间工作面板
        self.middlePanel = btnsAndTablePanel.BtnsAndTablePanel(self)
        self.entireLayout.addWidget(self.middlePanel,8)
        # 连接信号槽
        self.middlePanel.tablePanel.openAppSignal.connect(self.openPCAutoApp)
        # 不知道为什么，但是如果这里等待时间不够的话，程序有几率崩溃，应该和异步操作有关
        # sleep(1)

    # 新建App
    def createPCAutoApp(self):
        #添加app编辑窗口
        self.editAppWindow = mainWindow.WorkMainWindow() #第一次创建，应该是单例
        self.editAppWindow.setWindowModality(Qt.WindowModal)
        self.editAppWindow.newApp()
        self.editAppWindow.destroyed.connect(self.refreshTable)
        self.editAppWindow.show()

    # 打开已有的App
    def openPCAutoApp(self, appId):
        self.editAppWindow = mainWindow.WorkMainWindow() #这里错了，应该是单例清除历史，重新填写内容
        self.editAppWindow.setWindowModality(Qt.WindowModal)
        self.editAppWindow.openApp(appId) #填写内容
        self.editAppWindow.destroyed.connect(self.refreshTable)
        self.editAppWindow.show()

    # 在编辑器关闭时，刷新一下列表
    def refreshTable(self):
        self.middlePanel.tablePanel.refreshTable()

    def createPhoneAutoApp(self):
        print("打开手机自动化流程编辑界面")
        self.editAppWindow = AppMainWindow.WorkMainWindow()
        self.editAppWindow.setWindowModality(Qt.WindowModal)
        self.editAppWindow.newApp()
        self.editAppWindow.destroyed.connect(self.refreshTable)
        self.editAppWindow.show()

        # 打开已有的手机App工程
    def openPhoneAutoApp(self, appId):
        self.editAppWindow = mainWindow.WorkMainWindow()
        self.editAppWindow.setWindowModality(Qt.WindowModal)
        self.editAppWindow.openApp(appId)
        self.editAppWindow.destroyed.connect(self.refreshTable)
        self.editAppWindow.show()