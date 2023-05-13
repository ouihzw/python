# -*- coding:utf-8 -*-
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowSettingDialog
from com.mat.rpa.utils import webAutoSave
from com.mat.rpa.dao.elementDao import elementDao
from selenium.webdriver.common.by import By
from com.mat.rpa.dao.workDao.directiveDao import DirectiveDao


class FillingInWebInputObjectSettingDialog(flowSettingDialog.BasicFlowSettingDialog):
    flowTextList = pyqtSignal(list)

    def __init__(self, title, directive_id, id, parent=None):
        super().__init__(title, directive_id, id, parent)
        self.webSave = webAutoSave.WebAutoSave()
        self.elementDaoMongo = elementDao.ElementDao()
        self.setInfoLabelText('在网页的输入框中输入内容')
        __font = QFont()
        __font.setPixelSize(20)
        __font.setFamily("Courier")
        self.screenWidth = 1920
        self.screenHeight = 1030
        self.setFixedSize(self.screenWidth * 0.46, self.screenHeight * 0.7)
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
        self.directiveDaoObj = DirectiveDao()
        self.directive = {"command": "",
                          "line_number": "",
                          "flow_title": "",
                          "data": {},
                          "comment": "",
                          "target": "",
                          "targets": [],
                          "value": ""
                          }
        self.directive["_id"] = directive_id
        self.directive["data"] = {"browser_type": 0,
                                  "element": "",
                                  "continue": False,
                                  "text": ""}

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
        print(len(self.webSave.getWebObjectName()))
        for i in range(len(self.webSave.getWebObjectName())):
            print("self.webSave.getWebObjectName()[i]", self.webSave.getWebObjectName()[i])
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

        self.objectLabel = QRadioButton(self)
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
        self.matchWayTipLabel = flowSettingDialog.createTipLabel("\u64cd\u4f5c\u76ee\u6807",
                                                                 "  \u9009\u62e9\u8981\u64cd\u4f5c\u7684\u7f51\u9875\u5143\u7d20")
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

        self.object1Label = QLabel()
        self.object1Label.setFont(__font)
        self.object1Label.setText("输入内容:")
        self.directiveInputSettingLayout.addWidget(self.object1Label, 3, 0, 1, 1, Qt.AlignRight)
        self.object1Edit = QTextEdit()
        self.object1Edit.setObjectName("object1Edit")
        self.object1Edit.setEnabled(True)  # 设置可以编辑
        self.object1Edit.setFont(__font)
        self.object1Edit.setMinimumSize(600, 50)
        self.directiveInputSettingLayout.addWidget(self.object1Edit, 3, 1, 1, 3, Qt.AlignLeft)
        self.TipLabel = flowSettingDialog.createTipLabel("输入内容",
                                                         "  填写要输入的内容")
        self.directiveInputSettingLayout.addWidget(self.TipLabel, 3, 3, 1, 1, Qt.AlignLeft)

        self.textInputLabel = QCheckBox("追加输入")
        self.textInputLabel.setChecked(False)
        self.directiveInputSettingLayout.addWidget(self.textInputLabel, 4, 1, 1, 1, Qt.AlignLeft)
        self.textInputTipLabel = flowSettingDialog.createTipLabel("追加输入",
                                                                  "  如果勾选追加输入则在现有内容后继\n  续追加输入，否则清空现有内容后再进\n  行输入")
        self.directiveInputSettingLayout.addWidget(self.textInputTipLabel, 4, 2, 1, 1, Qt.AlignLeft)

        # 设置表格三列的比例
        self.directiveInputSettingLayout.setColumnStretch(0, 20)
        self.directiveInputSettingLayout.setColumnStretch(1, 15)
        self.directiveInputSettingLayout.setColumnStretch(2, 55)
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
        self.waitWebLoadCheckbox.setText("输入内容包含快捷键")
        self.waitWebLoadCheckbox.setFont(__font)
        self.waitWebLoadCheckbox.setChecked(False)
        self.seniorTabLayout.addWidget(self.waitWebLoadCheckbox, 1, 1, 1, 1, Qt.AlignLeft)
        self.waitWebLoadTipLabel = flowSettingDialog.createTipLabel("模拟人工点击",
                                                                    "  如果使用模拟人工点击则通过模拟人\n  工的方式触发点击事件，否则将根据目\n  标元素的自动化接口触发点击")
        self.seniorTabLayout.addWidget(self.waitWebLoadTipLabel, 1, 2, 1, 1, Qt.AlignLeft)

        self.waitWebLoad2Checkbox = QCheckBox()
        self.waitWebLoad2Checkbox.setText("强制加载美式键盘(ENG)")
        self.waitWebLoad2Checkbox.setFont(__font)
        self.waitWebLoad2Checkbox.setChecked(False)
        self.seniorTabLayout.addWidget(self.waitWebLoad2Checkbox, 2, 1, 1, 1, Qt.AlignLeft)
        self.waitWebLoadTip2Label = flowSettingDialog.createTipLabel("显示鼠标移动轨迹",
                                                                     "  是否显示鼠标移动轨迹")
        self.seniorTabLayout.addWidget(self.waitWebLoadTip2Label, 2, 2, 1, 1, Qt.AlignLeft)

        self.webLoadTimeOutPeriodLabel = QLabel()
        self.webLoadTimeOutPeriodLabel.setFont(__font)
        self.webLoadTimeOutPeriodLabel.setText("输入方式:")
        self.seniorTabLayout.addWidget(self.webLoadTimeOutPeriodLabel, 0, 0, 1, 1, Qt.AlignRight)
        self.webLoadTimeOutPeriodCombobox = QComboBox()
        self.webLoadTimeOutPeriodCombobox.setFont(__font)
        self.webLoadTimeOutPeriodCombobox.setMinimumSize(600, 50)
        self.webLoadTimeOutPeriodCombobox.addItems(["模拟人工输入", "剪切板输入", "自动化接口输入"])
        self.webLoadTimeOutPeriodCombobox.setItemDelegate(QStyledItemDelegate())
        self.webLoadTimeOutPeriodCombobox.setStyleSheet(
            "QComboBox QAbstractItemView{selection-background-color: #f0f0f0;selection-color: #000;} QComboBox QAbstractItemView::item{min-height: 50px;}")
        self.seniorTabLayout.addWidget(self.webLoadTimeOutPeriodCombobox, 0, 1, 1, 3, Qt.AlignCenter)
        self.webLoadTimeOutPeriodTipLabel = flowSettingDialog.createTipLabel("点击方式",
                                                                             "  选择点击的方式是单击还是双击")
        self.seniorTabLayout.addWidget(self.webLoadTimeOutPeriodTipLabel, 0, 4, 1, 1, Qt.AlignLeft)

        self.webLoadTimeOutPeriod2Label = QLabel()
        self.webLoadTimeOutPeriod2Label.setFont(__font)
        self.webLoadTimeOutPeriod2Label.setText("按键输入间隔(ms):")
        self.seniorTabLayout.addWidget(self.webLoadTimeOutPeriod2Label, 3, 0, 1, 1, Qt.AlignRight)
        self.webLoadTimeOutPeriod2Combobox = QLineEdit()
        self.webLoadTimeOutPeriod2Combobox.setFont(__font)
        self.webLoadTimeOutPeriod2Combobox.setMinimumSize(600, 50)
        self.webLoadTimeOutPeriod2Combobox.setText("50")
        self.seniorTabLayout.addWidget(self.webLoadTimeOutPeriod2Combobox, 3, 1, 1, 3, Qt.AlignCenter)
        self.webLoadTimeOutPeriodTip2Label = flowSettingDialog.createTipLabel("鼠标按钮",
                                                                              "  选择用于触发点击的鼠标按键")
        self.seniorTabLayout.addWidget(self.webLoadTimeOutPeriodTip2Label, 3, 4, 1, 1, Qt.AlignLeft)

        self.webLoadTimeOutPeriod3Label = QLabel()
        self.webLoadTimeOutPeriod3Label.setFont(__font)
        self.webLoadTimeOutPeriod3Label.setText("焦点超时时间(ms):")
        self.seniorTabLayout.addWidget(self.webLoadTimeOutPeriod3Label, 4, 0, 1, 1, Qt.AlignRight)
        self.webLoadTimeOutPeriod3Combobox = QLineEdit()
        self.webLoadTimeOutPeriod3Combobox.setFont(__font)
        self.webLoadTimeOutPeriod3Combobox.setMinimumSize(600, 50)
        self.webLoadTimeOutPeriod3Combobox.setText("1000")
        self.seniorTabLayout.addWidget(self.webLoadTimeOutPeriod3Combobox, 4, 1, 1, 3, Qt.AlignCenter)
        self.webLoadTimeOutPeriodTip3Label = flowSettingDialog.createTipLabel("辅助按键",
                                                                              "  在点击时需要按下的键盘功能键")
        self.seniorTabLayout.addWidget(self.webLoadTimeOutPeriodTip3Label, 4, 4, 1, 1, Qt.AlignLeft)

        self.executeAfterLoadTimesOutLabel = QLabel()
        self.executeAfterLoadTimesOutLabel.setFont(__font)
        self.executeAfterLoadTimesOutLabel.setText("执行后延迟(s):")
        self.seniorTabLayout.addWidget(self.executeAfterLoadTimesOutLabel, 5, 0, 1, 1, Qt.AlignRight)
        self.executeAfterLoadTimesOutCombobox = QLineEdit()
        self.executeAfterLoadTimesOutCombobox.setFont(__font)
        self.executeAfterLoadTimesOutCombobox.setMinimumSize(600, 50)
        self.executeAfterLoadTimesOutCombobox.setObjectName("executeAfterLoadTimesOutCombobox")
        self.executeAfterLoadTimesOutCombobox.setText("1")
        self.seniorTabLayout.addWidget(self.executeAfterLoadTimesOutCombobox, 5, 1, 1, 3, Qt.AlignCenter)
        self.executeAfterLoadTimesOutTipLabel = flowSettingDialog.createTipLabel("执行后延迟(s)",
                                                                                 "  执行指令完成后的等待时间")
        self.seniorTabLayout.addWidget(self.executeAfterLoadTimesOutTipLabel, 5, 4, 1, 1, Qt.AlignLeft)

        self.clickCheckbox = QCheckBox()
        self.clickCheckbox.setText("输入前点击元素")
        self.clickCheckbox.setFont(__font)
        self.clickCheckbox.setChecked(True)
        self.seniorTabLayout.addWidget(self.clickCheckbox, 6, 1, 1, 1, Qt.AlignLeft)
        self.clickLabel = flowSettingDialog.createTipLabel("显示鼠标移动轨迹",
                                                           "  是否显示鼠标移动轨迹")
        self.seniorTabLayout.addWidget(self.clickLabel, 6, 2, 1, 1, Qt.AlignLeft)

        self.webLoadTimeOutPeriod4Label = QLabel()
        self.webLoadTimeOutPeriod4Label.setFont(__font)
        self.webLoadTimeOutPeriod4Label.setText("鼠标点击位置")
        self.seniorTabLayout.addWidget(self.webLoadTimeOutPeriod4Label, 7, 0, 1, 1, Qt.AlignRight)
        self.webLoadTimeOutPeriod4Combobox = QComboBox()
        self.webLoadTimeOutPeriod4Combobox.setFont(__font)
        self.webLoadTimeOutPeriod4Combobox.setMinimumSize(600, 50)
        self.webLoadTimeOutPeriod4Combobox.addItems(["中心点", "随机位置", "自定义"])
        self.webLoadTimeOutPeriod4Combobox.setItemDelegate(QStyledItemDelegate())
        self.webLoadTimeOutPeriod4Combobox.setStyleSheet(
            "QComboBox QAbstractItemView{selection-background-color: #f0f0f0;selection-color: #000;} QComboBox QAbstractItemView::item{min-height: 50px;}")
        self.seniorTabLayout.addWidget(self.webLoadTimeOutPeriod4Combobox, 7, 1, 1, 3, Qt.AlignCenter)
        self.webLoadTimeOutPeriodTip4Label = flowSettingDialog.createTipLabel("锚点", "  未填")
        self.seniorTabLayout.addWidget(self.webLoadTimeOutPeriodTip4Label, 7, 4, 1, 1, Qt.AlignLeft)

        self.executeAfterLoadTimesOut2Label = QLabel()
        self.executeAfterLoadTimesOut2Label.setFont(__font)
        self.executeAfterLoadTimesOut2Label.setText("等待元素存在(s):")
        self.seniorTabLayout.addWidget(self.executeAfterLoadTimesOut2Label, 8, 0, 1, 1, Qt.AlignRight)
        self.executeAfterLoadTimesOut2Combobox = QLineEdit()
        self.executeAfterLoadTimesOut2Combobox.setFont(__font)
        self.executeAfterLoadTimesOut2Combobox.setMinimumSize(600, 50)
        self.executeAfterLoadTimesOut2Combobox.setObjectName("executeAfterLoadTimesOutCombobox")
        self.executeAfterLoadTimesOut2Combobox.setText("20")
        self.seniorTabLayout.addWidget(self.executeAfterLoadTimesOut2Combobox, 8, 1, 1, 3, Qt.AlignCenter)
        self.executeAfterLoadTimesOutTip2Label = flowSettingDialog.createTipLabel("等待元素存在(s)",
                                                                                  "  等待目标元素存在的超时时间")
        self.seniorTabLayout.addWidget(self.executeAfterLoadTimesOutTip2Label, 8, 4, 1, 1, Qt.AlignLeft)

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
        self.printErrorLogsTipLabel = flowSettingDialog.createTipLabel("打印错误日志",
                                                                       "  当出现错误时打印错误日志到日志面\n  版")
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
            self.setFixedSize(self.screenWidth * 0.46, self.screenHeight * 0.8)
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
        print(self.object1Edit.toPlainText())
        try:
            print("self.browserTypeCombobox.currentText()", self.browserTypeCombobox.currentText())
            handle = self.webSave.getWebObjectHandle(self.browserTypeCombobox.currentText())
            client = self.webSave.getWebObjectClient(self.browserTypeCombobox.currentText())
            client.switch_to.window(handle)
            if self.objectLabel.isChecked():
                webElement = client.find_element(By.XPATH,
                                                 self.elementDaoMongo.getOneElement(self.elementLabel.text())["xpath"])
            else:
                webElement = client.find_element(By.XPATH, self.manualInputXpathCombobox.text())
            if self.textInputLabel.isChecked():
                webElement.send_keys(self.object1Edit.toPlainText())
            else:
                webElement.clear()
                webElement.send_keys(self.object1Edit.toPlainText())
        except Exception as e:
            print(e)

    def handleQuestionBtnClicked(self):
        print("点击获取信息按钮")

    def handleConfirmBtnClicked(self):
        self.updateSettingData()
        self.accept()

    def handleCancelBtnClicked(self):
        self.close()

    def handleExecutionBtnClicked(self):
        print("点击执行按钮")
        self.executeStep()

    def updateSettingData(self):
        data = self.directive["data"]
        data["browser_type"] = self.browserTypeCombobox.currentIndex()
        data["element"] = self.elementLabel.text()
        data["continue"] = self.textInputLabel.isChecked()
        data["text"] = self.object1Edit.toPlainText()
        self.updateDirectiveData2DB(self.directive["_id"], data)

    def updateDirectiveData2DB(self, directive_id, data: dict):
        self.directiveDaoObj.updateDirective(directive_id, {"data": data})

    def getDirectiveSettingDataFromDB(self, directive_id):
        return self.directiveDaoObj.getOneDirective(directive_id)["data"]

    def getSettingData(self):
        data = self.getDirectiveSettingDataFromDB(self.directive["_id"])
        self.browserTypeCombobox.setCurrentIndex(data["browser_type"])
        self.elementLabel.setText(data["element"])
        self.textInputLabel.setChecked(data["continue"])
        self.object1Edit.setText(data["text"])
        self.directive["data"] = data

    def serialize(self):
        from collections import OrderedDict
        dict = OrderedDict([
            ('browser_type', self.browserTypeCombobox.currentText()),
            ('element', self.elementLabel.text()),
            ('manual', self.manualInputXpathCombobox.text()),
            ('continue', self.textInputLabel.isChecked()),
            ('text', self.object1Edit.toPlainText()),
            ('clickPositon', self.webLoadTimeOutPeriod4Combobox.currentText()),
            ('waitElementExist', self.executeAfterLoadTimesOut2Combobox.text()),
            ('executeAfterDelay', self.executeAfterLoadTimesOutCombobox.text())
        ])
        if (self.objectLabel.isChecked()):
            dict["choose"] = 0
        else:
            dict["choose"] = 1
        return dict

    def deserialize(self, data):
        self.browserTypeCombobox.addItem(data["browser_type"])
        self.browserTypeCombobox.setCurrentText(data["browser_type"])
        self.textInputLabel.setChecked(data["continue"])
        self.object1Edit.setText(data["text"])
        if data["choose"] == 0:
            self.objectLabel.setChecked(True)
            self.elementLabel.setText(data["element"])
        else:
            self.objectLabel1.setChecked(True)
            self.manualInputXpathCombobox.setText(data['manual'])
        self.webLoadTimeOutPeriod4Combobox.setCurrentText(data['clickPositon'])
        self.executeAfterLoadTimesOut2Combobox.setText(data['waitElementExist'])
        self.executeAfterLoadTimesOutCombobox.setText(data['executeAfterDelay'])
        self.accept()

