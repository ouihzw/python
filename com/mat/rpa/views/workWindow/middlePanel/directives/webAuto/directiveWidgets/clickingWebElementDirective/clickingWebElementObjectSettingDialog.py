# -*- coding:utf-8 -*-
import time

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowSettingDialog
from com.mat.rpa.utils import webAutoSave
from com.mat.rpa.dao.elementDao import elementDao
from selenium.webdriver.common.by import By

class ClickingWebElementObjectSettingDialog(flowSettingDialog.BasicFlowSettingDialog):
    flowTextList = pyqtSignal(list)
    def __init__(self, title, directive_id, id, parent=None):
        super().__init__(title, directive_id, id,parent)
        self.webSave = webAutoSave.WebAutoSave()
        self.elementDaoMongo = elementDao.ElementDao()
        self.setInfoLabelText(u'\u70b9\u51fb\u7f51\u9875\u4e2d\u7684\u6309\u94ae\u3001\u94fe\u63a5\u6216\u8005\u5176\u5b83\u4efb\u4f55\u5143\u7d20')
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
        self.settingTabWidget.addTab(self.seniorTab, u"\u9ad8\u7ea7")
        self.errorHandingTab = QWidget()
        self.settingTabWidget.addTab(self.errorHandingTab, u"\u9519\u8bef\u5904\u7406")
        self.regularTabUI()
        self.seniorTabUI()
        self.errorHandingTabUI()
        self.settingTabWidget.currentChanged.connect(self.changeOpenWebPageObjectSettingDialogSize)

    def regularTabUI(self):
        __font = QFont()
        __font.setPixelSize(20)
        __font.setFamily("Courier")
        # 布局指令输入面板
        self.directiveInputSettingLayout = QGridLayout()
        self.directiveInputSettingLayout.setContentsMargins(0, 0, 0, 0)
        self.directiveInputSettingLayout.setSpacing(10)
        self.directiveInputSettingLayout.setVerticalSpacing(30)
        self.directiveInputSettingPanel.setLayout(self.directiveInputSettingLayout)
        self.browserTypeLabel = QLabel()
        self.browserTypeLabel.setFont(__font)
        self.browserTypeLabel.setText(u"\u7f51\u9875\u5bf9\u8c61\u003a")
        self.directiveInputSettingLayout.addWidget(self.browserTypeLabel, 0, 0, 1, 1, Qt.AlignRight)
        self.browserTypeCombobox = QComboBox()
        self.browserTypeCombobox.setObjectName("browserTypeCombobox")
        self.browserTypeCombobox.setEditable(False)  # 设置不可以编辑
        for i in range(len(self.webSave.getWebObjectName())):
            self.browserTypeCombobox.addItem(self.webSave.getWebObjectName()[i])
        self.browserTypeCombobox.setFont(__font)
        self.browserTypeCombobox.setMinimumSize(600, 50)
        self.browserTypeCombobox.setItemDelegate(QStyledItemDelegate())
        self.browserTypeCombobox.setStyleSheet(
            "QComboBox QAbstractItemView{selection-background-color: #f0f0f0;selection-color: #000;} QComboBox QAbstractItemView::item{min-height: 50px;}")
        self.directiveInputSettingLayout.addWidget(self.browserTypeCombobox, 0, 1, 1, 2, Qt.AlignLeft)
        self.browserTypeTipLabel = flowSettingDialog.createTipLabel("\u7f51\u9875\u5bf9\u8c61",
                                                                    "  \u8f93\u5165\u4e00\u4e2a\u83b7\u53d6\u5230\u7684\u6216\u8005\u901a\u8fc7\u201c\u6253\u5f00\u7f51\n  \u9875\u201d\u521b\u5efa\u7684\u7f51\u9875\u5bf9\u8c61")
        self.directiveInputSettingLayout.addWidget(self.browserTypeTipLabel, 0, 3, 1, 1, Qt.AlignLeft)

        self.objectLabel = QRadioButton()
        #self.objectLabel = QLabel()
        self.objectLabel.setFont(__font)
        self.objectLabel.setText("\u64cd\u4f5c\u76ee\u6807\u003a")
        self.directiveInputSettingLayout.addWidget(self.objectLabel, 1, 0, 1, 1, Qt.AlignRight)
        self.elementLayout = QHBoxLayout()
        self.elementLayout.setSpacing(10)
        self.elementLabel = QLineEdit()
        self.elementLabel.setObjectName("objectLabel")
        self.elementLabel.setEnabled(False)  # 设置不可以编辑
        self.elementLabel.setFont(__font)
        self.elementLabel.setMinimumSize(390, 50)
        self.elementLayout.addWidget(self.elementLabel, 5)
        self.pointoutButton = flowSettingDialog.readElementFunctionButton(self.elementLabel, self)
        self.elementLayout.addWidget(self.pointoutButton, 1)
        self.directiveInputSettingLayout.addLayout(self.elementLayout, 1, 1, 1, 2, Qt.AlignLeft)
        self.matchWayTipLabel = flowSettingDialog.createTipLabel("\u64cd\u4f5c\u76ee\u6807", "  \u9009\u62e9\u8981\u64cd\u4f5c\u7684\u7f51\u9875\u5143\u7d20")
        self.directiveInputSettingLayout.addWidget(self.matchWayTipLabel, 1, 3, 1, 1, Qt.AlignLeft)

        self.objectLabel1 = QRadioButton(self)
        self.objectLabel1.setFont(__font)
        self.objectLabel1.setText("输入路径:")
        self.directiveInputSettingLayout.addWidget(self.objectLabel1, 2, 0, 1, 1, Qt.AlignRight)
        self.manualInputXpathCombobox = QLineEdit()
        self.manualInputXpathCombobox.setFont(__font)
        self.manualInputXpathCombobox.setMinimumSize(600, 50)
        self.manualInputXpathCombobox.setObjectName("manualInputXpathCombobox")
        self.directiveInputSettingLayout.addWidget(self.manualInputXpathCombobox, 2, 1, 1, 3, Qt.AlignLeft)
        self.matchWayTipLabel1 = flowSettingDialog.createTipLabel("\u64cd\u4f5c\u76ee\u6807",
                                                                 "输入操作目标的Xpath路径")
        self.directiveInputSettingLayout.addWidget(self.matchWayTipLabel1, 2, 3, 1, 1, Qt.AlignLeft)

        self.objectLabel.setChecked(True)
        self.manualInputXpathCombobox.setEnabled(False)
        self.objectLabel.clicked.connect(self.selectCapturedElement)
        self.objectLabel1.clicked.connect(self.selectManualInputXpath)

        # 设置表格三列的比例
        self.directiveInputSettingLayout.setColumnStretch(0, 20)
        self.directiveInputSettingLayout.setColumnStretch(1, 50)
        self.directiveInputSettingLayout.setColumnStretch(2, 20)
        self.directiveInputSettingLayout.setColumnStretch(3, 10)

        outputHLayout = QHBoxLayout(self.directiveOutputSettingPanel)
        self.directiveOutputSettingPanel.setLayout(outputHLayout)
        nothingOutputLabel = QLabel(text="(当前指令不包含任何输出项)", font=__font)
        outputHLayout.addWidget(nothingOutputLabel, 1, Qt.AlignCenter)
        outputHLayout.setContentsMargins(0, 20, 0, 40)

    def selectCapturedElement(self):
        self.manualInputXpathCombobox.setEnabled(False)
        self.pointoutButton.setEnabled(True)

    def selectManualInputXpath(self):
        self.manualInputXpathCombobox.setEnabled(True)
        self.pointoutButton.setEnabled(False)

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
        self.waitWebLoadCheckbox.setText("模拟人工点击")
        self.waitWebLoadCheckbox.setFont(__font)
        self.waitWebLoadCheckbox.setChecked(True)
        self.seniorTabLayout.addWidget(self.waitWebLoadCheckbox, 0, 1, 1, 1, Qt.AlignLeft)
        self.waitWebLoadTipLabel = flowSettingDialog.createTipLabel("模拟人工点击", "  如果使用模拟人工点击则通过模拟人\n  工的方式触发点击事件，否则将根据目\n  标元素的自动化接口触发点击")
        self.seniorTabLayout.addWidget(self.waitWebLoadTipLabel, 0, 2, 1, 1, Qt.AlignLeft)

        self.waitWebLoad2Checkbox = QCheckBox()
        self.waitWebLoad2Checkbox.setText("显示鼠标移动轨迹")
        self.waitWebLoad2Checkbox.setFont(__font)
        self.waitWebLoad2Checkbox.setChecked(False)
        self.seniorTabLayout.addWidget(self.waitWebLoad2Checkbox, 1, 1, 1, 1, Qt.AlignLeft)
        self.waitWebLoadTip2Label = flowSettingDialog.createTipLabel("显示鼠标移动轨迹",
                                                                    "  是否显示鼠标移动轨迹")
        self.seniorTabLayout.addWidget(self.waitWebLoadTip2Label, 1, 2, 1, 1, Qt.AlignLeft)

        self.webLoadTimeOutPeriodLabel = QLabel()
        self.webLoadTimeOutPeriodLabel.setFont(__font)
        self.webLoadTimeOutPeriodLabel.setText("点击方式:")
        self.seniorTabLayout.addWidget(self.webLoadTimeOutPeriodLabel, 2, 0, 1, 1, Qt.AlignRight)
        self.webLoadTimeOutPeriodCombobox = QComboBox()
        self.webLoadTimeOutPeriodCombobox.setFont(__font)
        self.webLoadTimeOutPeriodCombobox.setMinimumSize(600, 50)
        self.webLoadTimeOutPeriodCombobox.addItems(["单击", "双击"])
        self.webLoadTimeOutPeriodCombobox.setItemDelegate(QStyledItemDelegate())
        self.webLoadTimeOutPeriodCombobox.setStyleSheet(
            "QComboBox QAbstractItemView{selection-background-color: #f0f0f0;selection-color: #000;} QComboBox QAbstractItemView::item{min-height: 50px;}")
        self.seniorTabLayout.addWidget(self.webLoadTimeOutPeriodCombobox, 2, 1, 1, 3, Qt.AlignCenter)
        self.webLoadTimeOutPeriodTipLabel = flowSettingDialog.createTipLabel("点击方式", "  选择点击的方式是单击还是双击")
        self.seniorTabLayout.addWidget(self.webLoadTimeOutPeriodTipLabel, 2, 4, 1, 1, Qt.AlignLeft)

        self.webLoadTimeOutPeriod2Label = QLabel()
        self.webLoadTimeOutPeriod2Label.setFont(__font)
        self.webLoadTimeOutPeriod2Label.setText("鼠标按钮:")
        self.seniorTabLayout.addWidget(self.webLoadTimeOutPeriod2Label, 3, 0, 1, 1, Qt.AlignRight)
        self.webLoadTimeOutPeriod2Combobox = QComboBox()
        self.webLoadTimeOutPeriod2Combobox.setFont(__font)
        self.webLoadTimeOutPeriod2Combobox.setMinimumSize(600, 50)
        self.webLoadTimeOutPeriod2Combobox.addItems(["鼠标左键", "鼠标右键"])
        self.webLoadTimeOutPeriod2Combobox.setItemDelegate(QStyledItemDelegate())
        self.webLoadTimeOutPeriod2Combobox.setStyleSheet(
            "QComboBox QAbstractItemView{selection-background-color: #f0f0f0;selection-color: #000;} QComboBox QAbstractItemView::item{min-height: 50px;}")
        self.seniorTabLayout.addWidget(self.webLoadTimeOutPeriod2Combobox, 3, 1, 1, 3, Qt.AlignCenter)
        self.webLoadTimeOutPeriodTip2Label = flowSettingDialog.createTipLabel("鼠标按钮", "  选择用于触发点击的鼠标按键")
        self.seniorTabLayout.addWidget(self.webLoadTimeOutPeriodTip2Label, 3, 4, 1, 1, Qt.AlignLeft)

        self.webLoadTimeOutPeriod3Label = QLabel()
        self.webLoadTimeOutPeriod3Label.setFont(__font)
        self.webLoadTimeOutPeriod3Label.setText("辅助按键:")
        self.seniorTabLayout.addWidget(self.webLoadTimeOutPeriod3Label, 4, 0, 1, 1, Qt.AlignRight)
        self.webLoadTimeOutPeriod3Combobox = QComboBox()
        self.webLoadTimeOutPeriod3Combobox.setFont(__font)
        self.webLoadTimeOutPeriod3Combobox.setMinimumSize(600, 50)
        self.webLoadTimeOutPeriod3Combobox.addItems(["无", "Alt", "Ctrl", "Shift", "Win"])
        self.webLoadTimeOutPeriod3Combobox.setItemDelegate(QStyledItemDelegate())
        self.webLoadTimeOutPeriod3Combobox.setStyleSheet(
            "QComboBox QAbstractItemView{selection-background-color: #f0f0f0;selection-color: #000;} QComboBox QAbstractItemView::item{min-height: 50px;}")
        self.seniorTabLayout.addWidget(self.webLoadTimeOutPeriod3Combobox, 4, 1, 1, 3, Qt.AlignCenter)
        self.webLoadTimeOutPeriodTip3Label = flowSettingDialog.createTipLabel("辅助按键", "  在点击时需要按下的键盘功能键")
        self.seniorTabLayout.addWidget(self.webLoadTimeOutPeriodTip3Label, 4, 4, 1, 1, Qt.AlignLeft)

        self.executeAfterLoadTimesOutLabel = QLabel()
        self.executeAfterLoadTimesOutLabel.setFont(__font)
        self.executeAfterLoadTimesOutLabel.setText("执行后延迟(s):")
        self.seniorTabLayout.addWidget(self.executeAfterLoadTimesOutLabel, 5, 0, 1, 1, Qt.AlignRight)
        self.executeAfterLoadTimesOutCombobox = QLineEdit()
        self.executeAfterLoadTimesOutCombobox.setFont(__font)
        self.executeAfterLoadTimesOutCombobox.setMinimumSize(600, 50)
        self.executeAfterLoadTimesOutCombobox.setObjectName("executeAfterLoadTimesOutCombobox")
        self.executeAfterLoadTimesOutCombobox.setText("0")
        self.seniorTabLayout.addWidget(self.executeAfterLoadTimesOutCombobox, 5, 1, 1, 3, Qt.AlignCenter)
        self.executeAfterLoadTimesOutTipLabel = flowSettingDialog.createTipLabel("执行后延迟(s)", "  执行指令完成后的等待时间")
        self.seniorTabLayout.addWidget(self.executeAfterLoadTimesOutTipLabel, 5, 4, 1, 1, Qt.AlignLeft)

        self.webLoadTimeOutPeriod4Label = QLabel()
        self.webLoadTimeOutPeriod4Label.setFont(__font)
        self.webLoadTimeOutPeriod4Label.setText("鼠标点击位置")
        self.seniorTabLayout.addWidget(self.webLoadTimeOutPeriod4Label, 6, 0, 1, 1, Qt.AlignRight)
        self.webLoadTimeOutPeriod4Combobox = QComboBox()
        self.webLoadTimeOutPeriod4Combobox.setFont(__font)
        self.webLoadTimeOutPeriod4Combobox.setMinimumSize(600, 50)
        self.webLoadTimeOutPeriod4Combobox.addItems(["中心点", "随机位置", "自定义"])
        self.webLoadTimeOutPeriod4Combobox.setItemDelegate(QStyledItemDelegate())
        self.webLoadTimeOutPeriod4Combobox.setStyleSheet(
            "QComboBox QAbstractItemView{selection-background-color: #f0f0f0;selection-color: #000;} QComboBox QAbstractItemView::item{min-height: 50px;}")
        self.seniorTabLayout.addWidget(self.webLoadTimeOutPeriod4Combobox, 6, 1, 1, 3, Qt.AlignCenter)
        self.webLoadTimeOutPeriodTip4Label = flowSettingDialog.createTipLabel("锚点", "  未填")
        self.seniorTabLayout.addWidget(self.webLoadTimeOutPeriodTip4Label, 6, 4, 1, 1, Qt.AlignLeft)

        self.executeAfterLoadTimesOut2Label = QLabel()
        self.executeAfterLoadTimesOut2Label.setFont(__font)
        self.executeAfterLoadTimesOut2Label.setText("等待元素存在(s):")
        self.seniorTabLayout.addWidget(self.executeAfterLoadTimesOut2Label, 7, 0, 1, 1, Qt.AlignRight)
        self.executeAfterLoadTimesOut2Combobox = QLineEdit()
        self.executeAfterLoadTimesOut2Combobox.setFont(__font)
        self.executeAfterLoadTimesOut2Combobox.setMinimumSize(600, 50)
        self.executeAfterLoadTimesOut2Combobox.setObjectName("executeAfterLoadTimesOutCombobox")
        self.executeAfterLoadTimesOut2Combobox.setText("20")
        self.seniorTabLayout.addWidget(self.executeAfterLoadTimesOut2Combobox, 7, 1, 1, 3, Qt.AlignCenter)
        self.executeAfterLoadTimesOutTip2Label = flowSettingDialog.createTipLabel("等待元素存在(s)", "  等待目标元素存在的超时时间")
        self.seniorTabLayout.addWidget(self.executeAfterLoadTimesOutTip2Label, 7, 4, 1, 1, Qt.AlignLeft)

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
            self.setFixedSize(self.screenWidth * 0.46, self.screenHeight * 0.5)
            self.center()
        elif self.settingTabWidget.currentIndex() == 1:
            self.setFixedSize(self.screenWidth * 0.50, self.screenHeight * 0.8)
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
                  (screen.height() - size.height()) / 2 - 80)

    def executeStep(self):
        try:
            print(self.browserTypeCombobox.currentText())
            handle = self.webSave.getWebObjectHandle(self.browserTypeCombobox.currentText())
            client = self.webSave.getWebObjectClient(self.browserTypeCombobox.currentText())
            client.switch_to.window(handle)
            if self.objectLabel.isChecked():
                webElement = client.find_element(By.XPATH, self.elementDaoMongo.getOneElement(self.elementLabel.text())["xpath"])
            else:
                webElement = client.find_element(By.XPATH, self.manualInputXpathCombobox.text())
            webElement.click()
        except Exception as e:
            print(e)
        sleepTime = float(self.executeAfterLoadTimesOutCombobox.text())
        if sleepTime > 0:
            time.sleep(sleepTime)

    # 实现确认和取消按钮点击事件
    def handleQuestionBtnClicked(self):
        print("点击获取信息按钮")

    def handleConfirmBtnClicked(self):
        flowText = [self.browserTypeCombobox.currentText(), self.webLoadTimeOutPeriod2Combobox.currentText(),
                    self.webLoadTimeOutPeriodCombobox.currentText(), self.elementLabel.text(),
                    self.webLoadTimeOutPeriod4Combobox.currentText()]
        self.flowTextList.emit(flowText)
        self.close()

    def handleCancelBtnClicked(self):
        self.close()

    def handleExecutionBtnClicked(self):
        self.executeStep()

    def serialize(self):
        from collections import OrderedDict
        dict = OrderedDict([
            ('browser_type', self.browserTypeCombobox.currentText()),
            ('element', self.elementLabel.text()),
            ('manual', self.manualInputXpathCombobox.text()),
        ])
        if(self.objectLabel.isChecked()):
            dict["choose"] = 0
        else:
            dict["choose"] = 1
        return dict

    def deserialize(self, data):
        self.browserTypeCombobox.addItem(data["browser_type"])
        self.browserTypeCombobox.setCurrentText(data["browser_type"])
        if data["choose"] == 0:
            self.objectLabel.setChecked(True)
            self.elementLabel.setText(data["element"])
        else:
            self.objectLabel1.setChecked(True)
            self.manualInputXpathCombobox.setText(data['manual'])
        self.accept()