# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from com.mat.rpa.utils import webAutoSave
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowSettingDialog
class GetOpenPageObjectSettingDialog(flowSettingDialog.BasicFlowSettingDialog):
    def __init__(self, title, directive_id, id, parent=None):
        super().__init__(title, directive_id, id, parent)
        self.setInfoLabelText("获取网址或标题匹配的已打开的网页，或者获取在当前浏览器中选中的网页")
        __font = QFont()
        __font.setPixelSize(20)
        __font.setFamily("Courier")
        self.screenWidth = 1920
        self.screenHeight = 1030
        self.setFixedSize(self.screenWidth * 0.46, self.screenHeight * 0.63)
        self.center()
        # 改变图片
        self.changeImage(flowSettingDialog.BasicFlowSettingDialog.picPath + "openWebPageBig.png")
        self.seniorTab = QWidget()
        self.settingTabWidget.addTab(self.seniorTab, "高级")
        self.errorHandingTab = QWidget()
        self.settingTabWidget.addTab(self.errorHandingTab, "错误处理")
        self.regularTabUI()
        self.seniorTabUI()
        self.errorHandingTabUI()
        self.settingTabWidget.currentChanged.connect(self.changeOpenWebPageObjectSettingDialogSize)
        self.webSave = webAutoSave.WebAutoSave()

    def regularTabUI(self):
        __font = QFont()
        __font.setPixelSize(20)
        __font.setFamily("Courier")
        # 布局指令输入面板
        self.directiveInputSettingLayout = QGridLayout()
        self.directiveInputSettingLayout.setContentsMargins(50, 0, 20, 0)
        self.directiveInputSettingLayout.setSpacing(10)
        self.directiveInputSettingLayout.setVerticalSpacing(30)
        self.directiveInputSettingPanel.setLayout(self.directiveInputSettingLayout)
        self.browserTypeLabel = QLabel()
        self.browserTypeLabel.setFont(__font)
        self.browserTypeLabel.setText("浏览器类型:")
        self.directiveInputSettingLayout.addWidget(self.browserTypeLabel, 0, 0, 1, 1, Qt.AlignRight)
        self.browserTypeCombobox = QComboBox()
        self.browserTypeCombobox.setObjectName("browserTypeCombobox")
        self.browserTypeCombobox.setFont(__font)
        self.browserTypeCombobox.setMinimumSize(600, 50)
        self.browserTypeCombobox.addItems(["RPA浏览器", "Google Chrome浏览器",
                                           "MicroSoft Edge浏览器", "Internet Explorer浏览器",
                                           "360安全浏览器"])
        self.browserTypeCombobox.setItemDelegate(QStyledItemDelegate())
        self.browserTypeCombobox.setStyleSheet(
            "QComboBox QAbstractItemView{selection-background-color: #f0f0f0;selection-color: #000;} QComboBox QAbstractItemView::item{min-height: 50px;}")
        self.directiveInputSettingLayout.addWidget(self.browserTypeCombobox, 0, 1, 1, 2, Qt.AlignCenter)
        self.browserTypeTipLabel = flowSettingDialog.createTipLabel("浏览器类型",
                                                                    "  选择浏览器类型，Google Chrome浏\n  览器、Microsoft Edge浏览器需要\n  安装插件才能实现自动化")
        self.directiveInputSettingLayout.addWidget(self.browserTypeTipLabel, 0, 3, 1, 1, Qt.AlignLeft)

        self.matchWayLabel = QLabel()
        self.matchWayLabel.setFont(__font)
        self.matchWayLabel.setText("匹配方式:")
        self.directiveInputSettingLayout.addWidget(self.matchWayLabel, 1, 0, 1, 1, Qt.AlignRight)
        self.matchWayCombobox = QComboBox()
        self.matchWayCombobox.setObjectName("matchWayCombobox")
        self.matchWayCombobox.setFont(__font)
        self.matchWayCombobox.setMinimumSize(600, 50)
        self.matchWayCombobox.addItems(["根据标题匹配", "根据网址匹配","匹配当前选中的网页"])
        self.matchWayCombobox.currentIndexChanged.connect(self.changeRegularTab)
        self.matchWayCombobox.setItemDelegate(QStyledItemDelegate())
        self.matchWayCombobox.setStyleSheet(
            "QComboBox QAbstractItemView{selection-background-color: #f0f0f0;selection-color: #000;} QComboBox QAbstractItemView::item{min-height: 50px;}")
        self.directiveInputSettingLayout.addWidget(self.matchWayCombobox, 1, 1, 1, 2, Qt.AlignCenter)
        self.matchWayTipLabel = flowSettingDialog.createTipLabel("匹配方式", "  选择获取已打开网页的匹配方式")
        self.directiveInputSettingLayout.addWidget(self.matchWayTipLabel, 1, 3, 1, 1, Qt.AlignLeft)

        self.titleLabel = QLabel()
        self.titleLabel.setFont(__font)
        self.titleLabel.setText("标题:")
        self.directiveInputSettingLayout.addWidget(self.titleLabel, 2, 0, 1, 1, Qt.AlignRight)
        self.titleCombobox = QComboBox()
        self.titleCombobox.setFont(__font)
        self.titleCombobox.setMinimumSize(600, 50)
        self.titleCombobox.setEditable(True)  # 设置可以编辑
        self.directiveInputSettingLayout.addWidget(self.titleCombobox, 2, 1, 1, 2, Qt.AlignCenter)
        self.titleTipLabel = flowSettingDialog.createTipLabel("标题",
                                                                             "  输入要匹配的网页标题，支持模\n  糊匹配")
        self.directiveInputSettingLayout.addWidget(self.titleTipLabel, 2, 3, 1, 1, Qt.AlignLeft)

        self.matchByWildcardCheckbox=QCheckBox()
        self.matchByWildcardCheckbox.setText("根据通配符匹配")
        self.matchByWildcardCheckbox.setFont(__font)
        self.directiveInputSettingLayout.addWidget(self.matchByWildcardCheckbox, 3, 1,1,1, Qt.AlignCenter)
        self.matchByWildcardTipLabel = flowSettingDialog.createTipLabel("根据通配符匹配","  根据通配符匹配")
        self.directiveInputSettingLayout.addWidget(self.matchByWildcardTipLabel, 3, 2, 1, 1,Qt.AlignLeft)

        # 设置表格三列的比例
        self.directiveInputSettingLayout.setColumnStretch(0, 20)
        self.directiveInputSettingLayout.setColumnStretch(1, 15)
        self.directiveInputSettingLayout.setColumnStretch(2, 55)
        self.directiveInputSettingLayout.setColumnStretch(3, 10)

        self.directiveOutputSettingLayout = QGridLayout()
        self.directiveOutputSettingLayout.setContentsMargins(10, 0, 0, 20)
        self.directiveOutputSettingLayout.setSpacing(10)
        # self.directiveOutputSettingLayout.setHorizontalSpacing(10)
        self.directiveOutputSettingPanel.setLayout(self.directiveOutputSettingLayout)

        self.saveWebPageObjectLabel = QLabel()
        self.saveWebPageObjectLabel.setFont(__font)
        self.saveWebPageObjectLabel.setText("保存网页对象至:")
        self.directiveOutputSettingLayout.addWidget(self.saveWebPageObjectLabel, 0, 0, 1, 1, Qt.AlignRight)
        self.saveWebPageObjectCombobox = QComboBox()
        self.saveWebPageObjectCombobox.setFont(__font)
        self.saveWebPageObjectCombobox.setMinimumSize(600, 50)
        self.saveWebPageObjectCombobox.setEditable(True)  # 设置可以编辑
        self.directiveOutputSettingLayout.addWidget(self.saveWebPageObjectCombobox, 0, 1, 1, 1, Qt.AlignCenter)
        self.saveWebPageObjectTipLabel = flowSettingDialog.createTipLabel("保存网页对象至",
                                                                          "  该变量保存的是网页对象，使用此网页\n  对象可以对网页进行自动化操作")
        self.directiveOutputSettingLayout.addWidget(self.saveWebPageObjectTipLabel, 0, 2, 1, 1, Qt.AlignLeft)
        self.directiveOutputSettingLayout.setColumnStretch(0, 20)  # 第一列占10/100
        self.directiveOutputSettingLayout.setColumnStretch(1, 70)  # 第二列占80/100
        self.directiveOutputSettingLayout.setColumnStretch(2, 10)  # 第三列占10/100

    def changeRegularTab(self):
        __font = QFont()
        __font.setPixelSize(20)
        __font.setFamily("Courier")
        if self.matchWayCombobox.currentIndex() == 0:
            i = 10
            while i > 5:
                item = self.directiveInputSettingLayout.itemAt(i)
                i -= 1
                if item:
                    self.directiveInputSettingLayout.removeItem(item)
                    item.widget().deleteLater()
            self.titleLabel = QLabel()
            self.titleLabel.setFont(__font)
            self.titleLabel.setText("标题:")
            self.directiveInputSettingLayout.addWidget(self.titleLabel, 2, 0, 1, 1, Qt.AlignRight)
            self.titleCombobox = QComboBox()
            self.titleCombobox.setFont(__font)
            self.titleCombobox.setMinimumSize(600, 50)
            self.titleCombobox.setEditable(True)  # 设置可以编辑
            self.directiveInputSettingLayout.addWidget(self.titleCombobox, 2, 1, 1, 2, Qt.AlignCenter)
            self.titleTipLabel = flowSettingDialog.createTipLabel("标题",
                                                                  "  输入要匹配的网页标题，支持模\n  糊匹配")
            self.directiveInputSettingLayout.addWidget(self.titleTipLabel, 2, 3, 1, 1, Qt.AlignLeft)
            self.matchByWildcardCheckbox = QCheckBox()
            self.matchByWildcardCheckbox.setText("根据通配符匹配")
            self.matchByWildcardCheckbox.setFont(__font)
            self.directiveInputSettingLayout.addWidget(self.matchByWildcardCheckbox, 3, 1, 1, 1, Qt.AlignCenter)
            self.matchByWildcardTipLabel = flowSettingDialog.createTipLabel("根据通配符匹配", "  根据通配符匹配")
            self.directiveInputSettingLayout.addWidget(self.matchByWildcardTipLabel, 3, 2, 1, 1, Qt.AlignLeft)
            self.setFixedSize(self.screenWidth * 0.46, self.screenHeight * 0.63)
            self.center()
        elif self.matchWayCombobox.currentIndex() == 1:
            i = 10
            while i > 5:
                item = self.directiveInputSettingLayout.itemAt(i)
                i -= 1
                if item:
                    self.directiveInputSettingLayout.removeItem(item)
                    item.widget().deleteLater()
            self.webLabel = QLabel()
            self.webLabel.setFont(__font)
            self.webLabel.setText("网址:")
            self.directiveInputSettingLayout.addWidget(self.webLabel, 2, 0, 1, 1, Qt.AlignRight)
            self.webCombobox = QComboBox()
            self.webCombobox.setFont(__font)
            self.webCombobox.setMinimumSize(600, 50)
            self.webCombobox.setEditable(True)  # 设置可以编辑
            self.directiveInputSettingLayout.addWidget(self.webCombobox, 2, 1, 1, 2, Qt.AlignCenter)
            self.webTipLabel = flowSettingDialog.createTipLabel("网址",
                                                                  "  输入要匹配的网址，支持模糊匹配")
            self.directiveInputSettingLayout.addWidget(self.webTipLabel, 2, 3, 1, 1, Qt.AlignLeft)
            self.matchByWildcardCheckbox = QCheckBox()
            self.matchByWildcardCheckbox.setText("根据通配符匹配")
            self.matchByWildcardCheckbox.setFont(__font)
            self.directiveInputSettingLayout.addWidget(self.matchByWildcardCheckbox, 3, 1, 1, 1, Qt.AlignCenter)
            self.matchByWildcardTipLabel = flowSettingDialog.createTipLabel("根据通配符匹配", "  根据通配符匹配")
            self.directiveInputSettingLayout.addWidget(self.matchByWildcardTipLabel, 3, 2, 1, 1, Qt.AlignLeft)
            self.setFixedSize(self.screenWidth * 0.46, self.screenHeight * 0.63)
            self.center()
        elif self.matchWayCombobox.currentIndex() == 2:
            i = 10
            while i > 5:
                item = self.directiveInputSettingLayout.itemAt(i)
                i -= 1
                if item:
                    self.directiveInputSettingLayout.removeItem(item)
                    item.widget().deleteLater()
            self.setFixedSize(self.screenWidth * 0.46, self.screenHeight * 0.5)
            self.center()

    def seniorTabUI(self):
        __font = QFont()
        __font.setPixelSize(20)
        __font.setFamily("Courier")
        self.seniorTabLayout = QGridLayout()
        self.seniorTab.setLayout(self.seniorTabLayout)
        self.seniorTabLayout.setContentsMargins(10, 20, 20, 20)
        self.seniorTabLayout.setSpacing(10)
        self.seniorTabLayout.setVerticalSpacing(20)
        self.seniorTabLayout.setColumnStretch(0, 20)
        self.seniorTabLayout.setColumnStretch(1, 17)
        self.seniorTabLayout.setColumnStretch(2, 1)
        self.seniorTabLayout.setColumnStretch(3, 32)
        self.seniorTabLayout.setColumnStretch(4, 10)

        self.waitWebLoadCheckbox = QCheckBox()
        self.waitWebLoadCheckbox.setText("等待网页加载完成")
        self.waitWebLoadCheckbox.setFont(__font)
        self.waitWebLoadCheckbox.setChecked(True)
        self.seniorTabLayout.addWidget(self.waitWebLoadCheckbox, 0, 1, 1, 1,Qt.AlignLeft)
        self.waitWebLoadTipLabel = flowSettingDialog.createTipLabel("等待网页加载完成", "  是否等待网页加载完成")
        self.seniorTabLayout.addWidget(self.waitWebLoadTipLabel, 0, 2, 1, 1, Qt.AlignLeft)

        self.webLoadTimeOutPeriodLabel = QLabel()
        self.webLoadTimeOutPeriodLabel.setFont(__font)
        self.webLoadTimeOutPeriodLabel.setText("网页加载超时时间（秒）:")
        self.seniorTabLayout.addWidget(self.webLoadTimeOutPeriodLabel, 1, 0, 1, 1, Qt.AlignRight)
        self.webLoadTimeOutPeriodCombobox = QComboBox()
        self.webLoadTimeOutPeriodCombobox.setFont(__font)
        self.webLoadTimeOutPeriodCombobox.setMinimumSize(600, 50)
        self.webLoadTimeOutPeriodCombobox.setEditable(True)  # 设置可以编辑
        self.seniorTabLayout.addWidget(self.webLoadTimeOutPeriodCombobox, 1, 1, 1, 3, Qt.AlignCenter)
        self.webLoadTimeOutPeriodTipLabel = flowSettingDialog.createTipLabel("网页加载超时时间（秒）:", "  等待网页加载完成的超时时间")
        self.seniorTabLayout.addWidget(self.webLoadTimeOutPeriodTipLabel, 1, 4, 1, 1, Qt.AlignLeft)

        self.executeAfterLoadTimesOutLabel = QLabel()
        self.executeAfterLoadTimesOutLabel.setFont(__font)
        self.executeAfterLoadTimesOutLabel.setText("加载超时后执行:")
        self.seniorTabLayout.addWidget(self.executeAfterLoadTimesOutLabel, 2, 0, 1, 1, Qt.AlignRight)
        self.executeAfterLoadTimesOutCombobox = QComboBox()
        self.executeAfterLoadTimesOutCombobox.setFont(__font)
        self.executeAfterLoadTimesOutCombobox.setMinimumSize(600, 50)
        self.executeAfterLoadTimesOutCombobox.setObjectName("executeAfterLoadTimesOutCombobox")
        self.executeAfterLoadTimesOutCombobox.addItems(["执行\"错误\"处理", "停止网页加载"])
        self.executeAfterLoadTimesOutCombobox.setItemDelegate(QStyledItemDelegate())
        self.executeAfterLoadTimesOutCombobox.setStyleSheet(
            "QComboBox QAbstractItemView{selection-background-color: #f0f0f0;selection-color: #000;} QComboBox QAbstractItemView::item{min-height: 50px;}")
        self.seniorTabLayout.addWidget(self.executeAfterLoadTimesOutCombobox, 2, 1, 1, 3, Qt.AlignCenter)
        self.executeAfterLoadTimesOutTipLabel = flowSettingDialog.createTipLabel("加载超时后执行", "  等待网页加载完成超时后希望执行的\n  操作")
        self.seniorTabLayout.addWidget(self.executeAfterLoadTimesOutTipLabel, 2, 4, 1, 1, Qt.AlignLeft)

        self.openNewWebPageCheckbox = QCheckBox()
        self.openNewWebPageCheckbox.setText("匹配失败时打开新网页")
        self.openNewWebPageCheckbox.setFont(__font)
        self.seniorTabLayout.addWidget(self.openNewWebPageCheckbox, 3, 1, 1, 2,Qt.AlignLeft)
        self.openNewWebPageTipLabel = flowSettingDialog.createTipLabel("匹配失败时打开新网页", "  根据网页标题或网址匹配失败时，打\n  开新网页")
        self.seniorTabLayout.addWidget(self.openNewWebPageTipLabel, 3, 3, 1, 1, Qt.AlignLeft)

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
        if self.handleErrorWayCombobox.currentIndex() == 0:
            i = 8
            while i > 4:
                item = self.errorHandingLayout.itemAt(i)
                i -= 1
                if item:
                    self.errorHandingLayout.removeItem(item)
                    item.widget().deleteLater()
            self.setFixedSize(self.screenWidth * 0.44, self.screenHeight * 0.3)
        elif self.handleErrorWayCombobox.currentIndex() == 1:
            i = 8
            while i > 4:
                item = self.errorHandingLayout.itemAt(i)
                i -= 1
                if item:
                    self.errorHandingLayout.removeItem(item)
                    item.widget().deleteLater()
            self.blankLabel = QLabel()
            self.blankLabel.setMaximumHeight(0)
            self.errorHandingLayout.addWidget(self.blankLabel, 2, 0, 1, 1, Qt.AlignRight)
            self.outputValueOfInstructionLabel = QLabel()
            self.outputValueOfInstructionLabel.setFont(__font)
            self.outputValueOfInstructionLabel.setText("设置异常情况下指令的输出值")
            self.outputValueOfInstructionLabel.setStyleSheet("color:#808080;")
            self.errorHandingLayout.addWidget(self.outputValueOfInstructionLabel, 3, 1, 1, 7, Qt.AlignLeft)
            self.webPageFunctionLabel = QLabel()
            self.webPageFunctionLabel.setFont(__font)
            self.webPageFunctionLabel.setText("web_page:")
            self.errorHandingLayout.addWidget(self.webPageFunctionLabel, 4, 1, 1, 2, Qt.AlignRight)
            self.webPageFunctionCombobox = QComboBox()
            self.webPageFunctionCombobox.setFont(__font)
            self.webPageFunctionCombobox.setMinimumSize(400, 50)
            self.webPageFunctionCombobox.setEditable(True)  # 设置可以编辑
            self.errorHandingLayout.addWidget(self.webPageFunctionCombobox, 4, 3, 1, 4, Qt.AlignLeft)
            self.setFixedSize(self.screenWidth * 0.44, self.screenHeight * 0.42)
        elif self.handleErrorWayCombobox.currentIndex() == 2:
            i = 8
            while i > 4:
                item = self.errorHandingLayout.itemAt(i)
                i -= 1
                if item:
                    self.errorHandingLayout.removeItem(item)
                    item.widget().deleteLater()
            self.retryCountLabel = QLabel()
            self.retryCountLabel.setFont(__font)
            self.retryCountLabel.setText("重试次数")
            self.errorHandingLayout.addWidget(self.retryCountLabel, 2, 1, 1, 1, Qt.AlignLeft)
            self.retryCountSpinbox = QSpinBox()
            self.retryCountSpinbox.setFont(__font)
            self.retryCountSpinbox.setMinimumSize(7, 50)
            self.retryCountSpinbox.setMinimum(1)
            self.retryCountSpinbox.setMaximum(100000000)
            self.retryCountSpinbox.setValue(3)
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
            self.retryIntervalSpinbox.setValue(3)
            self.errorHandingLayout.addWidget(self.retryIntervalSpinbox, 2, 5, 1, 1, Qt.AlignLeft)
            self.setFixedSize(self.screenWidth * 0.44, self.screenHeight * 0.37)

    def changeOpenWebPageObjectSettingDialogSize(self):
        if self.settingTabWidget.currentIndex() == 0:
            if self.matchWayCombobox.currentIndex() == 2:
                self.setFixedSize(self.screenWidth * 0.46, self.screenHeight * 0.5)
            else:
                self.setFixedSize(self.screenWidth * 0.46, self.screenHeight * 0.63)
            self.center()
        elif self.settingTabWidget.currentIndex() == 1:
            self.setFixedSize(self.screenWidth * 0.50, self.screenHeight * 0.42)
            self.center()
        elif self.settingTabWidget.currentIndex() == 2:
            if self.handleErrorWayCombobox.currentIndex() == 0:
                self.setFixedSize(self.screenWidth * 0.44, self.screenHeight * 0.3)
            elif self.handleErrorWayCombobox.currentIndex() == 1:
                self.setFixedSize(self.screenWidth * 0.44, self.screenHeight * 0.42)
            else:
                self.setFixedSize(self.screenWidth * 0.44, self.screenHeight * 0.37)
            self.center()
    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2-80)


    #实现确认和取消按钮点击事件
    def handleQuestionBtnClicked(self):
        print("点击获取信息按钮")

    def handleConfirmBtnClicked(self):
        print("点击确认按钮")
        self.webSave.webObjectSave(self.saveWebPageObjectCombobox.currentText(), None, None)
        self.accept()

    def handleCancelBtnClicked(self):
        print("点击取消按钮")
        self.reject()

    #def handleExecutionBtnClicked(self): 根据情况实现指令执行按钮事件
    #   print("点击执行按钮)

