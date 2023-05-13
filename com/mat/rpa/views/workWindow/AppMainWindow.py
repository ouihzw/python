# -*- coding:utf-8 -*-
import datetime
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from com.mat.rpa.views.workWindow.topPanel import topPanel
from com.mat.rpa.views.workWindow.leftPanel import leftPanel
from com.mat.rpa.views.workWindow.middlePanel import middlePanel
from com.mat.rpa.dao.workDao.workDao import WorkDao
from com.mat.rpa.utils.variable import VariableManager
from com.mat.rpa.views.workWindow.topPanel.appInfoEditorDialog.appInfoEditorDialog import AppInfoEditorDialog

class WorkMainWindow(QMainWindow):
    def __init__(self, parent=None):
        self.workDaoObj = WorkDao()
        try:
            super(WorkMainWindow, self).__init__(parent)
            # 添加图标和标题
            self.setWindowIcon(QIcon('./com/mat/rpa/views/images/logo32.png'))
            self.setWindowTitle("未命名应用")
            self.parentPanel = parent
            self.centralWidget = QWidget(self)
            self.centralWidget.setObjectName("centralwidget")
            self.horizontalLayout = QHBoxLayout(self.centralWidget)
            self.horizontalLayout.setContentsMargins(5, 0, 5, 5)
            self.horizontalLayout.setSpacing(0)
            self.horizontalLayout.setObjectName("horizontalLayout")
            self.centralWidget.setLayout(self.horizontalLayout)
            self.setCentralWidget(self.centralWidget)

            # 创建左中分割条
            self.leftCenterSplitter = QSplitter(self.centralWidget)
            self.horizontalLayout.addWidget(self.leftCenterSplitter)
            self.leftCenterSplitter.setOrientation(Qt.Horizontal)
            self.leftCenterSplitter.setChildrenCollapsible(False)
            self.leftCenterSplitter.setObjectName("leftCenterSplitter")
            self.leftPanel = leftPanel.LeftPanel(self)
            self.leftCenterSplitter.addWidget(self.leftPanel)
            # 创建中右分割条
            self.centerRightSplitter = QSplitter(self.leftCenterSplitter)
            self.leftCenterSplitter.addWidget(self.centerRightSplitter)
            self.centerRightSplitter.setMinimumSize(QSize(200, 0))
            self.centerRightSplitter.setOrientation(Qt.Horizontal)
            self.centerRightSplitter.setChildrenCollapsible(False)
            self.centerRightSplitter.setObjectName("centerRightSplitter")
            # 添加中间工作面板
            self.middleWorkPanel = middlePanel.MiddlePanel(self)
            self.centerRightSplitter.addWidget(self.middleWorkPanel)
            # 添加顶部工具菜单栏
            self.topBar = topPanel.TopBar(self,flowTabWindow=self.middleWorkPanel.flowTabWidget)
            self.addToolBar(self.topBar)
            # 设置全屏显示
            self.setDisplayFullScreen()
            self.connectSignalSlot()
            self.isNewApp = True
            __font = QFont()
            __font.setFamily("Microsoft YaHei")
            self.setFont(__font)
            #接收全屏信号
            self.topBar.Signal_fullscreen.connect(self.setfullscreen)
        except Exception as e:
            print(e)


    #全屏
    def setfullscreen(self):
        self.leftPanel.setVisible(False)
        self.topBar.setVisible(False)
        self.rightPanel.setVisible(False)

    def giveupfullscreen(self):
        self.leftPanel.setVisible(True)
        self.topBar.setVisible(True)
        self.rightPanel.setVisible(True)

    #键盘事件
    def keyPressEvent(self, event):
        if (event.key() == Qt.Key_Escape):
            self.giveupfullscreen()

    # 绑定槽函数
    def connectSignalSlot(self):
        # 打开flow文件
        self.rightPanel.flowManagementPanel.flowTree.openSubFlowSignal.connect(
            self.middleWorkPanel.flowTabWidget.openNewTab)
        # 关闭flow文件
        self.rightPanel.flowManagementPanel.flowTree.closeSubFlowSignal.connect(
            self.middleWorkPanel.flowTabWidget.closeTab)
        # flow文件改名
        self.rightPanel.flowManagementPanel.flowTree.nameChangedSignal.connect(
            self.middleWorkPanel.flowTabWidget.changeTabName)
        # 绑定undo/redo
        self.topBar.undoBtn.clicked.connect(self.middleWorkPanel.flowTabWidget.undo)
        self.topBar.redoBtn.clicked.connect(self.middleWorkPanel.flowTabWidget.redo)

    # 新建应用
    def newApp(self):
        appId, mainFlowId = self.workDaoObj.insertNewApp()
        VariableManager().setAppId(appId)
        self.middleWorkPanel.flowTabWidget.mainFlowTab.grScene.id = mainFlowId

    # 打开保存的应用
    def openApp(self, appId):
        #print(appId)
        VariableManager().setAppId(appId)
        appData = self.workDaoObj.loadApp(appId)
        if appData["status"] != -1:
            self.isNewApp = False
        self.middleWorkPanel.flowTabWidget.mainFlowTab.grScene.id = appData["flow"][0]["id"]
        # self.middleWorkPanel.flowTabWidget.mainFlowTab.grScene.buildFlowWidgetsFromDB()
        self.setWindowTitle(appData["name"])
        self.rightPanel.flowManagementPanel.flowTree.loadSubFlows(appData["flow"][1:])

    def setDisplayFullScreen(self):
        # 得到桌面控件
        desktop = QApplication.desktop()
        # 得到屏幕可显示尺寸
        self.rect = desktop.availableGeometry()
        # 获取标题栏高度
        titleBar = self.style().pixelMetric(QStyle.PM_TitleBarHeight)
        # 设置窗口尺寸
        self.setGeometry(self.rect.x(), self.rect.y(),
                         self.rect.width(), self.rect.height() - titleBar - 15)
        self.move(0, 0)  # 把窗口移动到（0,0）坐标

    def closeEvent(self, e):
        # 检测是否为新创建的临时App
        if self.isNewApp:
            messageBox = QMessageBox(QMessageBox.Question, "保存应用",
                                     "当前应用尚未保存，退出将放弃所有\n修改，是否保存？",
                                     QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            yesBtn = messageBox.button(QMessageBox.Yes)
            yesBtn.setText("是")
            yesBtn.setStyleSheet("background-color: red; color: white;")
            messageBox.button(QMessageBox.No).setText("否")
            messageBox.button(QMessageBox.Cancel).setText("取消")
            messageBox.setStyleSheet("QMessageBox {background-color: white}")
            messageBox.setContentsMargins(6, 8, 6, 4)
            reply = messageBox.exec()
            if reply == QMessageBox.Yes:
                editDialog = AppInfoEditorDialog()
                result = editDialog.exec()
                # 如果未设置应用信息则视为取消
                if result != QDialog.Accepted:
                    e.ignore()
                    return
            elif reply == QMessageBox.No:
                # 临时数据清理
                self.workDaoObj.deleteApp(VariableManager().getAppId())
            else:
                e.ignore()
                return
        else:
            self.workDaoObj.saveAppInfo(VariableManager().getAppId(), {"update_time": datetime.datetime.now()})
        self.deleteLater()

    def saveApp(self):
        pass
if __name__=='__main__':
    app=QApplication(sys.argv)
    fms=WorkMainWindow()
    fms.show()
    sys.exit(app.exec_())
