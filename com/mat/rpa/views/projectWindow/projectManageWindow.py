# -*- coding:utf-8 -*-
import traceback

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
from com.mat.rpa.views.projectWindow.topToolPanel import topToolBar  #上方的工具栏
from com.mat.rpa.views.projectWindow.mainWindow.myAppPanel import myAppPanel
#myAppPanel 为 stackedWidget的内部成分，为一个widget，包含了面板和所有选项
from com.mat.rpa.views.projectWindow.mainWindow.myCmdPanel import myCmdPanel
from com.mat.rpa.views.loginWindow import loginWindow

class ProjectManageWindow(QMainWindow):
    def __init__(self, parent=None):
        try:
            super(ProjectManageWindow, self).__init__(parent)
            self.setWindowIcon(QIcon('./com/mat/rpa/views/images/logo32.png'))
            self.setWindowTitle("RPA流程自动化Studio")
            #顶部按钮工具栏
            self.topToolBarPanel = topToolBar.TopToolBar(self)
            self.addToolBar(self.topToolBarPanel)
            #下边安装一个stackedWidget
            self.mainPanel = QStackedWidget()
            self.myappPanel = myAppPanel.MyAppPanel(self)
            # self.myCmdPanel = myCmdPanel.MyCmdPanel(self)
            self.mainPanel.addWidget(self.myappPanel)
            # self.mainPanel.addWidget(self.myCmdPanel)
            self.mainPanel.setCurrentIndex(0)
            self.setCentralWidget(self.mainPanel)
            self.connectSlot()
            #设置全屏显示
            self.setDisplayFullScreen()
        except Exception as e:
            traceback.print_exc()

    def setDisplayFullScreen(self):
        # 得到桌面控件
        desktop = QApplication.desktop()
        # 得到屏幕可显示尺寸
        self.rect = desktop.availableGeometry()
        # 获取标题栏高度
        titleBar = self.style().pixelMetric(QStyle.PM_TitleBarHeight)
        # 设置窗口尺寸
        self.setGeometry(self.rect.x(), self.rect.y(),
                         self.rect.width(), self.rect.height() - titleBar-15)
        self.move(0,0)#把窗口移动到（0,0）坐标

    def setInitSplitterRatio(self):
        #设置中右splitter的比例，当setStretchFactor无效时使用setSizes
        self.centerRightSplitter.setSizes([800, 200])
        # 设置左中splitter的比例,左边树占2，右边占8
        self.leftCenterSplitter.setStretchFactor(0, 2)
        self.leftCenterSplitter.setStretchFactor(1, 8)
        #设置上下splitter的比例，上边占9，下边占1
        self.topBottomSplitter.setStretchFactor(0, 9)
        self.topBottomSplitter.setStretchFactor(1, 1)

    # 连接信号槽
    def connectSlot(self):
        self.topToolBarPanel.myAppAction.triggered.connect(lambda: self.changePage(0))
        # self.topToolBarPanel.selfDefinedCommandAction.triggered.connect(lambda: self.changePage(1))

    # 切换界面
    def changePage(self, idx):
        self.mainPanel.setCurrentIndex(idx)

    # 获得用户登录窗体
    def setLoginWindow(self, window: loginWindow.LoginWindow):
        self.loginWindow = window
        # 刷新用户菜单的用户名标签
        self.topToolBarPanel.setUserName(self.loginWindow.individualForm.userName.currentText())
        # 绑定退出登录菜单项的槽函数
        self.topToolBarPanel.logoutAction.triggered.connect(self.logout)

    # 退出登录
    def logout(self):
        self.hide()
        loginWindowObj = self.loginWindow
        result = loginWindowObj.exec()
        if result != QDialog.Accepted:
            sys.exit()
        # 重新初始化工程管理页面
        self.__init__()
        self.show()
        self.setLoginWindow(loginWindowObj)


if __name__ == "__main__":
    app =  QApplication(sys.argv)
    win = ProjectManageWindow()
    win.show()
    sys.exit(app.exec_())