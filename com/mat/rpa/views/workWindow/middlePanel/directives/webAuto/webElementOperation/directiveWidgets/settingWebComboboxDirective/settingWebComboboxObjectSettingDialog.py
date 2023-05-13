# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowSettingDialog
from com.mat.rpa.utils import webAutoSave
from com.mat.rpa.dao.elementDao import elementDao
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from com.mat.rpa.dao.workDao.directiveDao import DirectiveDao
class SettingWebComboboxObjectSettingDialog(flowSettingDialog.BasicFlowSettingDialog):
    flowTextList = pyqtSignal(list)

    def __init__(self, title, directive_id, id, parent=None):
        super().__init__(title, directive_id, id, parent)
        self.directiveDaoObj = DirectiveDao()
        self.webSave = webAutoSave.WebAutoSave()
        self.elementDaoMongo = elementDao.ElementDao()
        self.setInfoLabelText(u"设置网页中下拉框的选择项")
        __font = QFont()
        __font.setPixelSize(20)
        __font.setFamily("Courier")
        self.screenWidth = 1920
        self.screenHeight = 1030
        self.setFixedSize(self.screenWidth * 0.46, self.screenHeight * 0.8)
        self.center()
        self.changeImage(flowSettingDialog.BasicFlowSettingDialog.picPath + "openWebPageBig.png")
        self.seniorTab = QWidget()
        self.settingTabWidget.addTab(self.seniorTab, u"\u9ad8\u7ea7")
        self.errorHandingTab = QWidget()
        self.settingTabWidget.addTab(self.errorHandingTab, u"\u9519\u8bef\u5904\u7406")
        self.regularTabUI()
        self.seniorTabUI()
        self.errorHandingTabUI()
        self.settingTabWidget.currentChanged.connect(self.changeOpenWebPageObjectSettingDialogSize)

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
                                  "object": 0,
                                  "element": "",
                                  "value": ""}

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

        self.objectLabel = QLabel()
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

        self.object1Label = QLabel()
        self.object1Label.setFont(__font)
        self.object1Label.setText("选择方式:")
        self.directiveInputSettingLayout.addWidget(self.object1Label, 2, 0, 1, 1, Qt.AlignRight)
        self.objectComboBox = QComboBox()
        self.objectComboBox.setObjectName("objectComboBox")
        self.objectComboBox.setFont(__font)
        self.objectComboBox.setMinimumSize(600, 50)
        self.objectComboBox.addItems(["按选项内容选择", "按选项位置选择"])
        self.objectComboBox.currentIndexChanged.connect(self.changeRegularTabUI)
        self.objectComboBox.setItemDelegate(QStyledItemDelegate())
        self.objectComboBox.setStyleSheet(
            "QComboBox QAbstractItemView{selection-background-color: #f0f0f0;selection-color: #000;} QComboBox QAbstractItemView::item{min-height: 50px;}")
        self.directiveInputSettingLayout.addWidget(self.objectComboBox, 2, 1, 1, 2, Qt.AlignLeft)
        self.TipLabel = flowSettingDialog.createTipLabel("操作",
                                                         "  选择要对复选框进行的操作")
        self.directiveInputSettingLayout.addWidget(self.TipLabel, 2, 3, 1, 1, Qt.AlignLeft)

        self.selectValueLabel = QLabel()
        self.selectValueLabel.setFont(__font)
        self.selectValueLabel.setText("选择值:")
        self.directiveInputSettingLayout.addWidget(self.selectValueLabel, 3, 0, 1, 1, Qt.AlignRight)
        self.selectValueLineEdit = QLineEdit()
        self.selectValueLineEdit.setFont(__font)
        self.selectValueLineEdit.setMinimumSize(600, 50)
        self.directiveInputSettingLayout.addWidget(self.selectValueLineEdit, 3, 1, 1, 2, Qt.AlignCenter)
        self.selectValueFunctionBtn = flowSettingDialog.addFunctionButton(self.selectValueLineEdit, self)
        self.directiveInputSettingLayout.addWidget(self.selectValueFunctionBtn, 3, 1, 1, 2, Qt.AlignRight)
        self.selectValueTipLabel = flowSettingDialog.createTipLabel("选择值", "  输入选项内容或者选项位置")
        self.directiveInputSettingLayout.addWidget(self.selectValueTipLabel, 3, 3, 1, 1, Qt.AlignLeft)

        self.selectLabel = QLabel()
        self.selectLabel.setFont(__font)
        self.selectLabel.setText("匹配模式:")
        self.directiveInputSettingLayout.addWidget(self.selectLabel, 4, 0, 1, 1, Qt.AlignRight)
        self.selectComboBox = QComboBox()
        self.selectComboBox.setObjectName("objectComboBox")
        self.selectComboBox.setFont(__font)
        self.selectComboBox.addItems(["模糊匹配", "精准匹配", "正则匹配"])
        self.selectComboBox.setCurrentIndex(1)
        self.selectComboBox.setMinimumSize(600, 50)
        self.selectComboBox.setItemDelegate(QStyledItemDelegate())
        self.selectComboBox.setStyleSheet(
            "QComboBox QAbstractItemView{selection-background-color: #f0f0f0;selection-color: #000;} QComboBox QAbstractItemView::item{min-height: 50px;}")
        self.directiveInputSettingLayout.addWidget(self.selectComboBox, 4, 1, 1, 2, Qt.AlignLeft)
        self.selectTipLabel = flowSettingDialog.createTipLabel("匹配模式",
                                                               "  选项内容的匹配模式，默认是模糊匹配")
        self.directiveInputSettingLayout.addWidget(self.selectTipLabel, 4, 3, 1, 1, Qt.AlignLeft)

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

    def changeRegularTabUI(self):
        __font = QFont()
        __font.setPixelSize(20)
        __font.setFamily("Courier")
        if self.objectComboBox.currentIndex() == 0:
            self.selectComboBox.show()
            self.selectLabel.show()
            self.selectTipLabel.show()
        else:
            self.selectComboBox.hide()
            self.selectLabel.hide()
            self.selectTipLabel.hide()

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

        self.executeAfterLoadTimesOutLabel = QLabel()
        self.executeAfterLoadTimesOutLabel.setFont(__font)
        self.executeAfterLoadTimesOutLabel.setText("延迟时间(s):")
        self.seniorTabLayout.addWidget(self.executeAfterLoadTimesOutLabel, 0, 0, 1, 1, Qt.AlignRight)
        self.executeAfterLoadTimesOutCombobox = QLineEdit()
        self.executeAfterLoadTimesOutCombobox.setFont(__font)
        self.executeAfterLoadTimesOutCombobox.setMinimumSize(600, 50)
        self.executeAfterLoadTimesOutCombobox.setObjectName("executeAfterLoadTimesOutCombobox")
        self.executeAfterLoadTimesOutCombobox.setText("1")
        self.seniorTabLayout.addWidget(self.executeAfterLoadTimesOutCombobox, 0, 1, 1, 3, Qt.AlignCenter)
        self.executeAfterLoadTimesOutTipLabel = flowSettingDialog.createTipLabel("执行后延迟(s)", "  执行指令完成后的等待时间")
        self.seniorTabLayout.addWidget(self.executeAfterLoadTimesOutTipLabel, 0, 4, 1, 1, Qt.AlignLeft)

        self.executeAfterLoadTimesOut2Label = QLabel()
        self.executeAfterLoadTimesOut2Label.setFont(__font)
        self.executeAfterLoadTimesOut2Label.setText("等待元素存在(s):")
        self.seniorTabLayout.addWidget(self.executeAfterLoadTimesOut2Label, 1, 0, 1, 1, Qt.AlignRight)
        self.executeAfterLoadTimesOut2Combobox = QLineEdit()
        self.executeAfterLoadTimesOut2Combobox.setFont(__font)
        self.executeAfterLoadTimesOut2Combobox.setMinimumSize(600, 50)
        self.executeAfterLoadTimesOut2Combobox.setObjectName("executeAfterLoadTimesOutCombobox")
        self.executeAfterLoadTimesOut2Combobox.setText("20")
        self.seniorTabLayout.addWidget(self.executeAfterLoadTimesOut2Combobox, 1, 1, 1, 3, Qt.AlignCenter)
        self.executeAfterLoadTimesOutTip2Label = flowSettingDialog.createTipLabel("等待元素存在(s)", "  等待目标元素存在的超时时间")
        self.seniorTabLayout.addWidget(self.executeAfterLoadTimesOutTip2Label, 1, 4, 1, 1, Qt.AlignLeft)

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
            self.setFixedSize(self.screenWidth * 0.46, self.screenHeight * 0.8)
            self.center()
        elif self.settingTabWidget.currentIndex() == 1:
            self.setFixedSize(self.screenWidth * 0.50, self.screenHeight * 0.5)
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
            handle = self.webSave.getWebObjectHandle(self.browserTypeCombobox.currentText())
            client = self.webSave.getWebObjectClient(self.browserTypeCombobox.currentText())
            client.switch_to.window(handle)
            webElement = client.find_element(By.XPATH,
                                             self.elementDaoMongo.getOneElement(self.elementLabel.text())["xpath"])
            if self.objectComboBox.currentIndex() == 0:
                if self.selectComboBox.currentIndex() == 1:
                    Select(webElement).select_by_visible_text(self.selectValueLineEdit.text())
            else:
                Select(webElement).select_by_index(int(self.selectValueLineEdit.text()) - 1)
        except Exception as e:
            print(e)

    # 实现确认和取消按钮点击事件
    def handleQuestionBtnClicked(self):
        print("点击使用说明按钮")

    def handleConfirmBtnClicked(self):
        self.updateSettingData()
        self.accept()

    def handleCancelBtnClicked(self):
        self.reject()

    def handleExecutionBtnClicked(self):
        self.executeStep()

    def updateDirectiveData2DB(self, directive_id, data: dict):
        self.directiveDaoObj.updateDirective(directive_id, {"data": data})

    def getDirectiveSettingDataFromDB(self, directive_id):
        return self.directiveDaoObj.getOneDirective(directive_id)["data"]


    def getSettingData(self):
        data = self.getDirectiveSettingDataFromDB(self.directive["_id"])
        self.browserTypeCombobox.setCurrentIndex(data["browser_type"])
        self.objectComboBox.setCurrentIndex(data["object"])
        self.elementLabel.setText(data["element"])
        self.selectValueLineEdit.setText(data["value"])
        self.directive["data"] = data

    def updateSettingData(self):
        data = self.directive["data"]
        data["browser_type"] = self.browserTypeCombobox.currentIndex()
        data["object"] = self.objectComboBox.currentIndex()
        data["element"] = self.elementLabel.text()
        data["value"] = self.selectValueLineEdit.text()
        self.updateDirectiveData2DB(self.directive["_id"], data)
