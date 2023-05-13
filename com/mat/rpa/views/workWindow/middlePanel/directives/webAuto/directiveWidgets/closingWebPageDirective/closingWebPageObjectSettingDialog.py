# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowSettingDialog
from com.mat.rpa.utils import webAutoSave
class ClosingWebPageObjectSettingDialog(flowSettingDialog.BasicFlowSettingDialog):
    def __init__(self, title, directive_id, id, parent=None):
        super().__init__(title, directive_id, id,parent)
        #参照修改infolabel的提示信息
        self.setInfoLabelText("关闭已打开的某个或所有网页")
        self.webSave = webAutoSave.WebAutoSave()
        __font = QFont()
        __font.setPixelSize(20)
        __font.setFamily("Courier")
        self.screenWidth = 1920
        self.screenHeight = 1030
        self.setFixedSize(self.screenWidth * 0.46, self.screenHeight * 0.5)
        # __font.setBold(True)
        # 改变图片
        self.changeImage(flowSettingDialog.BasicFlowSettingDialog.picPath + "openWebPageBig.png")
        self.errorHandingTab = QWidget()
        self.settingTabWidget.addTab(self.errorHandingTab, "错误处理")
        self.regularTabUI()
        self.errorHandingTabUI()
        self.settingTabWidget.currentChanged.connect(self.changeOpenWebPageObjectSettingDialogSize)

    def regularTabUI(self):
        __font = QFont()
        __font.setPixelSize(20)
        __font.setFamily("Courier")
        # 布局指令输入面板
        self.directiveInputSettingLayout = QGridLayout()
        self.directiveInputSettingLayout.setContentsMargins(50, 0, 20, 0)
        self.directiveInputSettingLayout.setSpacing(10)
        #self.directiveInputSettingLayout.setHorizontalSpacing(0)
        self.directiveInputSettingLayout.setVerticalSpacing(30)
        self.directiveInputSettingPanel.setLayout(self.directiveInputSettingLayout)
        self.operationLabel = QLabel()
        self.operationLabel.setFont(__font)
        self.operationLabel.setText("操作:")
        self.directiveInputSettingLayout.addWidget(self.operationLabel, 0, 0, 1, 1, Qt.AlignRight)
        self.operationCombobox = QComboBox()
        self.operationCombobox.setObjectName("operationCombobox")
        self.operationCombobox.setFont(__font)
        self.operationCombobox.setMinimumSize(600, 50)
        self.operationCombobox.addItems(["关闭指定网页", "关闭所有网页"])
        self.operationCombobox.currentIndexChanged.connect(self.changeRegularTab)
        self.operationCombobox.setItemDelegate(QStyledItemDelegate())
        self.operationCombobox.setStyleSheet(
            "QComboBox QAbstractItemView{selection-background-color: #f0f0f0;selection-color: #000;} QComboBox QAbstractItemView::item{min-height: 50px;}")
        self.directiveInputSettingLayout.addWidget(self.operationCombobox, 0, 1, 1, 2, Qt.AlignCenter)
        self.operationTipLabel = flowSettingDialog.createTipLabel("操作",
                                                                  "  选择要关闭一个指定的网页还是关闭\n  所有网页")
        self.directiveInputSettingLayout.addWidget(self.operationTipLabel, 0, 3, 1, 1, Qt.AlignLeft)

        self.webObjectLabel = QLabel()
        self.webObjectLabel.setFont(__font)
        self.webObjectLabel.setText("网页对象:")
        self.directiveInputSettingLayout.addWidget(self.webObjectLabel, 1, 0, 1, 1, Qt.AlignRight)
        self.webObjectCombobox = QComboBox()
        self.webObjectCombobox.setFont(__font)
        self.webObjectCombobox.setMinimumSize(600, 50)
        self.webObjectCombobox.setEditable(True)  # 设置可以编辑
        self.directiveInputSettingLayout.addWidget(self.webObjectCombobox, 1, 1, 1, 2, Qt.AlignCenter)
        self.webObjectTipLabel = flowSettingDialog.createTipLabel("网页对象",
                                                                  "  输入一个获取到的或者通过\"打开网\n  页\"创建的网页对象")
        self.directiveInputSettingLayout.addWidget(self.webObjectTipLabel, 1, 3, 1, 1, Qt.AlignLeft)
        self.directiveInputSettingLayout.setColumnStretch(0, 20)
        self.directiveInputSettingLayout.setColumnStretch(1, 15)
        self.directiveInputSettingLayout.setColumnStretch(2, 55)
        self.directiveInputSettingLayout.setColumnStretch(3, 10)

        self.directiveOutputSettingLayout = QGridLayout()
        self.directiveOutputSettingLayout.setContentsMargins(10, 0, 0, 20)
        self.directiveOutputSettingLayout.setSpacing(10)
        self.directiveOutputSettingPanel.setLayout(self.directiveOutputSettingLayout)

        self.emptyLabel = QLabel()
        self.emptyLabel.setFont(__font)
        self.emptyLabel.setText("（当前指令不包含任何输出项）")
        self.emptyLabel.setStyleSheet("color:#838b8b;font-size:16px;font-family:Courier")
        self.emptyLabel.setAlignment(Qt.AlignCenter)
        self.directiveOutputSettingLayout.addWidget(self.emptyLabel, 0, 0, 1, 1, Qt.AlignCenter)

    def changeRegularTab(self):
        __font = QFont()
        __font.setPixelSize(20)
        __font.setFamily("Courier")
        if self.operationCombobox.currentIndex() == 0:
            i = 7
            while i > 2:
                item = self.directiveInputSettingLayout.itemAt(i)
                i -= 1
                if item:
                    self.directiveInputSettingLayout.removeItem(item)
                    item.widget().deleteLater()
            self.webObjectLabel = QLabel()
            self.webObjectLabel.setFont(__font)
            self.webObjectLabel.setText("网页对象:")
            self.directiveInputSettingLayout.addWidget(self.webObjectLabel, 1, 0, 1, 1, Qt.AlignRight)
            self.webObjectCombobox = QComboBox()
            self.webObjectCombobox.setFont(__font)
            self.webObjectCombobox.setMinimumSize(600, 50)
            self.webObjectCombobox.setEditable(True)  # 设置可以编辑
            self.directiveInputSettingLayout.addWidget(self.webObjectCombobox, 1, 1, 1, 2, Qt.AlignCenter)
            self.webObjectTipLabel = flowSettingDialog.createTipLabel("网页对象",
                                                                      "  输入一个获取到的或者通过\"打开网\n  页\"创建的网页对象")
            self.directiveInputSettingLayout.addWidget(self.webObjectTipLabel, 1, 3, 1, 1, Qt.AlignLeft)
            self.setFixedSize(self.screenWidth*0.46,self.screenHeight*0.5)
        elif self.operationCombobox.currentIndex() == 1:
            i = 5
            while i > 2:
                item = self.directiveInputSettingLayout.itemAt(i)
                i -= 1
                if item:
                    self.directiveInputSettingLayout.removeItem(item)
                    item.widget().deleteLater()
            self.operateBrowserLabel = QLabel()
            self.operateBrowserLabel.setFont(__font)
            self.operateBrowserLabel.setText("操作浏览器:")
            self.directiveInputSettingLayout.addWidget(self.operateBrowserLabel, 1, 0, 1, 1, Qt.AlignRight)
            self.operateBrowserCombobox = QComboBox()
            self.operateBrowserCombobox.setObjectName("operateBrowserCombobox")
            self.operateBrowserCombobox.setFont(__font)
            self.operateBrowserCombobox.setMinimumSize(600, 50)
            self.operateBrowserCombobox.addItems(["RPA浏览器", "Google Chrome浏览器",
                                               "MicroSoft Edge浏览器", "Internet Explorer浏览器",
                                               "360安全浏览器"])
            self.operateBrowserCombobox.setItemDelegate(QStyledItemDelegate())
            self.operateBrowserCombobox.setStyleSheet(
                "QComboBox QAbstractItemView{selection-background-color: #f0f0f0;selection-color: #000;} QComboBox QAbstractItemView::item{min-height: 50px;}")
            self.directiveInputSettingLayout.addWidget(self.operateBrowserCombobox, 1, 1, 1, 2, Qt.AlignCenter)
            self.operateBrowserTipLabel = flowSettingDialog.createTipLabel("操作浏览器",
                                                                        "  选择想要操作的浏览器对象")
            self.directiveInputSettingLayout.addWidget(self.operateBrowserTipLabel, 1, 3, 1, 1, Qt.AlignLeft)

            self.terminateBrowserProcessCheckbox = QCheckBox()
            self.terminateBrowserProcessCheckbox.setText("终止浏览器进程")
            self.terminateBrowserProcessCheckbox.setFont(__font)
            self.directiveInputSettingLayout.addWidget(self.terminateBrowserProcessCheckbox, 2, 1, 1, 1, Qt.AlignLeft)
            self.terminateBrowserProcessTipLabel = flowSettingDialog.createTipLabel("终止浏览器进程", "  如果勾选，将强制结束属于当前用户的\n  指定浏览器进程和由它启动的所有子\n  进程")
            self.directiveInputSettingLayout.addWidget(self.terminateBrowserProcessTipLabel, 2, 2, 1, 1, Qt.AlignLeft)
            self.setFixedSize(self.screenWidth * 0.46, self.screenHeight * 0.6)

    def errorHandingTabUI(self):
        __font = QFont()
        __font.setPixelSize(20)
        __font.setFamily("Courier")
        self.errorHandingLayout = QGridLayout()
        self.errorHandingTab.setLayout(self.errorHandingLayout)
        self.errorHandingLayout.setContentsMargins(10, 20, 0, 20)
        self.errorHandingLayout.setSpacing(10)
        self.errorHandingLayout.setVerticalSpacing(20)
        self.errorHandingLayout.setColumnStretch(0, 20)
        self.errorHandingLayout.setColumnStretch(1, 7)
        self.errorHandingLayout.setColumnStretch(2, 7)
        self.errorHandingLayout.setColumnStretch(3, 3)
        self.errorHandingLayout.setColumnStretch(4, 10)
        self.errorHandingLayout.setColumnStretch(5, 10)
        self.errorHandingLayout.setColumnStretch(6, 31)
        self.errorHandingLayout.setColumnStretch(7, 10)

        self.printErrorLogsCheckbox = QCheckBox()
        self.printErrorLogsCheckbox.setText("打印错误日志")
        self.printErrorLogsCheckbox.setFont(__font)
        self.printErrorLogsCheckbox.setChecked(True)
        self.errorHandingLayout.addWidget(self.printErrorLogsCheckbox, 0, 1, 1, 2, Qt.AlignLeft)
        self.printErrorLogsTipLabel = flowSettingDialog.createTipLabel("打印错误日志", "  当出现错误时打印错误日志到日志面\n  版")
        self.errorHandingLayout.addWidget(self.printErrorLogsTipLabel, 0, 3, 1, 1, Qt.AlignLeft)

        self.handleErrorWayLabel = QLabel()
        self.handleErrorWayLabel.setFont(__font)
        self.handleErrorWayLabel.setText("处理方式")
        self.errorHandingLayout.addWidget(self.handleErrorWayLabel, 1, 0, 1, 1, Qt.AlignRight)
        self.handleErrorWayCombobox = QComboBox()
        self.handleErrorWayCombobox.setFont(__font)
        self.handleErrorWayCombobox.setMinimumSize(600, 50)
        self.handleErrorWayCombobox.setObjectName("handleErrorWayCombobox")
        self.handleErrorWayCombobox.addItems(["终止流程", "忽略异常并继续执行", "重试此指令"])
        self.handleErrorWayCombobox.setItemDelegate(QStyledItemDelegate())
        self.handleErrorWayCombobox.setStyleSheet(
            "QComboBox QAbstractItemView{selection-background-color: #f0f0f0;selection-color: #000;} QComboBox QAbstractItemView::item{min-height: 50px;}")
        self.handleErrorWayCombobox.currentIndexChanged.connect(self.changeErrorHandingTab)
        self.errorHandingLayout.addWidget(self.handleErrorWayCombobox, 1, 1, 1, 6, Qt.AlignCenter)
        self.handleErrorWayTipLabel = flowSettingDialog.createTipLabel("选择错误处理方式",
                                                                       "  选择错误处理方式，当出现错误时默\n  认终止流程，也可以选择忽略错误或\n  者重试当前指令")
        self.errorHandingLayout.addWidget(self.handleErrorWayTipLabel, 1, 7, 1, 1, Qt.AlignLeft)

    def changeErrorHandingTab(self):
        __font = QFont()
        __font.setPixelSize(20)
        __font.setFamily("Courier")
        if self.handleErrorWayCombobox.currentIndex() == 2:
            self.retryCountLabel = QLabel()
            self.retryCountLabel.setFont(__font)
            self.retryCountLabel.setText("重试次数")
            self.errorHandingLayout.addWidget(self.retryCountLabel, 2, 1, 1, 1, Qt.AlignLeft)
            self.retryCountSpinbox = QSpinBox()
            self.retryCountSpinbox.setFont(__font)
            self.retryCountSpinbox.setMinimumSize(7, 50)
            self.retryCountSpinbox.setMinimum(1)
            self.retryCountSpinbox.setMaximum(100000000)
            self.retryCountSpinbox.setValue(1)
            self.errorHandingLayout.addWidget(self.retryCountSpinbox, 2, 2, 1, 1, Qt.AlignLeft)
            self.retryIntervalLabel = QLabel()
            self.retryIntervalLabel.setFont(__font)
            self.retryIntervalLabel.setText("重试间隔(秒)")
            self.errorHandingLayout.addWidget(self.retryIntervalLabel, 2, 4, 1, 1, Qt.AlignCenter)
            self.retryIntervalSpinbox = QSpinBox()
            self.retryIntervalSpinbox.setFont(__font)
            self.retryIntervalSpinbox.setMinimumSize(7, 50)
            self.retryIntervalSpinbox.setMinimum(1)
            self.retryIntervalSpinbox.setMaximum(100000000)
            self.retryIntervalSpinbox.setValue(1)
            self.errorHandingLayout.addWidget(self.retryIntervalSpinbox, 2, 5, 1, 1, Qt.AlignLeft)
            self.setFixedSize(self.screenWidth * 0.44, self.screenHeight * 0.37)
        else:
            i = 8
            while i > 4:
                item = self.errorHandingLayout.itemAt(i)
                i -= 1
                if item:
                    self.errorHandingLayout.removeItem(item)
                    item.widget().deleteLater()
            self.setFixedSize(self.screenWidth * 0.44, self.screenHeight * 0.3)

    def changeOpenWebPageObjectSettingDialogSize(self):
        if self.settingTabWidget.currentIndex()==0:
            if self.operationCombobox.currentIndex() == 0:
                self.setFixedSize(self.screenWidth*0.46,self.screenHeight*0.5)
            elif self.operationCombobox.currentIndex() == 1:
                self.setFixedSize(self.screenWidth * 0.46, self.screenHeight * 0.6)
            self.center()
        elif self.settingTabWidget.currentIndex()==1:
            if self.handleErrorWayCombobox.currentIndex() == 2:
                self.setFixedSize(self.screenWidth * 0.44, self.screenHeight * 0.37)
            else:
                self.setFixedSize(self.screenWidth * 0.44, self.screenHeight * 0.3)
            self.center()

    def executeStep(self):
        if self.operationCombobox.currentIndex() == 0:
            try:
                handle = self.webSave.getWebObjectHandle(self.webObjectCombobox.currentText())
                client = self.webSave.getWebObjectClient(self.webObjectCombobox.currentText())
                client.switch_to.window(handle)
                client.close()
            except Exception as e:
                print(e)
        elif self.operationCombobox.currentIndex() == 1:
            try:
                webObjectNames = self.webSave.getWebObjectName()
                for webObjectName in webObjectNames:
                    handle = self.webSave.getWebObjectHandle(webObjectName)
                    client = self.webSave.getWebObjectClient(webObjectName)
                    client.switch_to.window(handle)
                    client.close()
            except Exception as e:
                print(e)

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2-80)

    #实现确认和取消按钮点击事件
    def handleQuestionBtnClicked(self):
        print("点击获取信息按钮")

    def handleConfirmBtnClicked(self):
        self.accept()

    def handleCancelBtnClicked(self):
        self.reject()

    #def handleExecutionBtnClicked(self): 根据情况实现指令执行按钮事件
    #   print("点击执行按钮)

