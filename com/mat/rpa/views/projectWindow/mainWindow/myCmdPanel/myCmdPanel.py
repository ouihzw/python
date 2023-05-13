# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from ..leftpanel import leftPanel
from ..mainPanel.btnAndTablePanel import btnsAndTablePanel
from com.mat.rpa.views.workWindow import mainWindow
class MyCmdPanel(QWidget):
    picPath = "./com/mat/rpa/views/projectWindow/mainWindow/myAppPanel/images/"
    def __init__(self, parent=None):
        super(MyCmdPanel, self).__init__(parent)
        self.parentPanel = parent
        #整体布局
        self.entireLayout = QHBoxLayout()
        self.setLayout(self.entireLayout)
        self.entireLayout.setContentsMargins(0,0,0,0)
        self.entireLayout.setSpacing(0)
        #左边面板
        self.leftPanelWidget = leftPanel.LeftPanel(self)
        self.leftPanelWidget.setCreateBtnText("新建指令")
        #添加菜单子项
        self.PCAutosubAction = QAction(QIcon(self.picPath+"PCAuto.png"), "PC自动化指令")
        self.leftPanelWidget.addActionToMenu(self.PCAutosubAction )
        self.phoneAutosubAction = QAction(QIcon(self.picPath+"phoneAuto.png"), "手机自动化指令")
        self.leftPanelWidget.addActionToMenu(self.phoneAutosubAction)
        # 绑定信号
        self.PCAutosubAction.triggered.connect(self.createPCAutoApp)
        self.phoneAutosubAction.triggered.connect(self.createPhoneAutoApp)
        self.entireLayout.addWidget(self.leftPanelWidget,2)
        #添加树节点
        ##我开发的指令节点
        myAppTreeItem = self.leftPanelWidget.getTreeNodeAtFirstLevel()
        myAppTreeItem.setText(0, '我开发的指令')
        myAppTreeItem.setIcon(0, QIcon(self.picPath+"myapps.png"))
        ###回收站节点
        garbageBinTreeItem = QTreeWidgetItem(myAppTreeItem)
        garbageBinTreeItem.setText(0,"回收站")
        garbageBinTreeItem.setIcon(0, QIcon(self.picPath + "garbageBin.png"))
        #中间工作面板
        self.middlePanel = btnsAndTablePanel.BtnsAndTablePanel(self)
        self.entireLayout.addWidget(self.middlePanel,8)
        #添加app编辑窗口
        self.editAppWindow = workmainWindow.WorkMainWindow(self)

    def createPCAutoApp(self):
        self.editAppWindow.show()

    def createPhoneAutoApp(self):
        print("打开手机自动化指令编辑界面")
