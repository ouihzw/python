# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowSettingDialog
from com.mat.rpa.utils import webAutoSave
from com.mat.rpa.dao.elementDao import elementDao
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from com.mat.rpa.dao.workDao.directiveDao import DirectiveDao
class WaitingForWebElementObjectSettingDialog(flowSettingDialog.BasicFlowSettingDialog):
    flowTextList = pyqtSignal(list)

    def __init__(self, title, directive_id, id, parent=None):
        super().__init__(title, directive_id, id, parent)
        self.directiveDaoObj = DirectiveDao()
        self.webSave = webAutoSave.WebAutoSave()
        self.elementDaoMongo = elementDao.ElementDao()
        self.setInfoLabelText("等待网页中元素出现或消失，再执行接下来的流程")
        __font = QFont()
        __font.setPixelSize(20)
        __font.setFamily("Courier")
        self.screenWidth = 1920
        self.screenHeight = 1030
        self.setFixedSize(self.screenWidth * 0.46, self.screenHeight * 0.7)
        self.center()
        self.changeImage(flowSettingDialog.BasicFlowSettingDialog.picPath + "openWebPageBig.png")
        self.errorHandingTab = QWidget()
        self.settingTabWidget.addTab(self.errorHandingTab, u"\u9519\u8bef\u5904\u7406")
        self.regularTabUI()
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
                                  "element": "",
                                  "method": 0,
                                  "value": ""}
    def regularTabUI(self):
        __font = QFont()
        __font.setPixelSize(20)
        __font.setFamily("Courier")
        # 布局指令输入面板
        self.directiveInputSettingLayout = QGridLayout()
        self.directiveInputSettingLayout.setContentsMargins(20, 0, 20, 0)
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

        self.waitTypeLabel = QLabel()
        self.waitTypeLabel.setFont(__font)
        self.waitTypeLabel.setText(u"等待状态")
        self.directiveInputSettingLayout.addWidget(self.waitTypeLabel, 3, 0, 1, 1, Qt.AlignRight)
        self.waitTypeCombobox = QComboBox()
        self.waitTypeCombobox.setObjectName("waitTypeCombobox")
        self.waitTypeCombobox.addItems(["等待元素出现", "等待元素消失"])
        self.waitTypeCombobox.setFont(__font)
        self.waitTypeCombobox.setMinimumSize(600, 50)
        self.waitTypeCombobox.setItemDelegate(QStyledItemDelegate())
        self.waitTypeCombobox.setStyleSheet(
            "QComboBox QAbstractItemView{selection-background-color: #f0f0f0;selection-color: #000;} QComboBox QAbstractItemView::item{min-height: 50px;}")
        self.directiveInputSettingLayout.addWidget(self.waitTypeCombobox, 3, 1, 1, 2, Qt.AlignLeft)
        self.waitTypeTipLabel = flowSettingDialog.createTipLabel(u"等待状态",
                                                                 u"  选择等待状态")
        self.directiveInputSettingLayout.addWidget(self.waitTypeTipLabel, 3, 3, 1, 1, Qt.AlignLeft)

        self.waitLayout = QHBoxLayout()
        self.waitCheckbox = QCheckBox()
        self.waitCheckbox.setText("设置超时时间")
        self.waitCheckbox.setFont(__font)
        self.waitCheckbox.setChecked(True)
        self.waitCheckbox.stateChanged.connect(self.changeRegularTabUI)
        self.waitLayout.addWidget(self.waitCheckbox)
        self.waitTipLabel = flowSettingDialog.createTipLabel(u"设置超时时间", u"  设置等待超时时间，超时后流程将自\n  动往下继续执行")
        self.waitLayout.addWidget(self.waitTipLabel)
        self.waitLayout.addStretch(1)
        self.directiveInputSettingLayout.addLayout(self.waitLayout, 4, 1, 1, 1, Qt.AlignLeft)

        self.waitTimeLabel = QLabel()
        self.waitTimeLabel.setFont(__font)
        self.waitTimeLabel.setText("超时时间(s):")
        self.directiveInputSettingLayout.addWidget(self.waitTimeLabel, 5, 0, 1, 1, Qt.AlignRight)
        self.waitTimeLineEdit = QLineEdit()
        self.waitTimeLineEdit.setFont(__font)
        self.waitTimeLineEdit.setMinimumSize(590, 50)
        self.waitTimeLineEdit.setText("20")
        self.directiveInputSettingLayout.addWidget(self.waitTimeLineEdit, 5, 1, 1, 2, Qt.AlignCenter)
        self.waitTimeFunctionBtn = flowSettingDialog.addFunctionButton(self.waitTimeLineEdit, self)
        self.directiveInputSettingLayout.addWidget(self.waitTimeFunctionBtn, 5, 1, 1, 2, Qt.AlignRight)
        self.waitTimeTipLabel = flowSettingDialog.createTipLabel(u"超时时间(s)", u"  设置最大等待时间")
        self.directiveInputSettingLayout.addWidget(self.waitTimeTipLabel, 5, 3, 1, 1, Qt.AlignLeft)

        # 设置表格三列的比例
        self.directiveInputSettingLayout.setColumnStretch(0, 20)
        self.directiveInputSettingLayout.setColumnStretch(1, 15)
        self.directiveInputSettingLayout.setColumnStretch(2, 55)
        self.directiveInputSettingLayout.setColumnStretch(3, 10)

        self.outputHLayout = QGridLayout()
        self.outputHLayout.setContentsMargins(50, 0, 20, 0)
        self.outputHLayout.setSpacing(10)
        self.outputHLayout.setVerticalSpacing(30)
        self.directiveOutputSettingPanel.setLayout(self.outputHLayout)
        self.waitResultLabel = QLabel(text="等待结果:", font=__font)
        self.outputHLayout.addWidget(self.waitResultLabel, 0, 0, 1, 1, Qt.AlignRight)
        self.waitResultLineEdit = QLineEdit()
        self.waitResultLineEdit.setFont(__font)
        self.waitResultLineEdit.setMinimumSize(600, 50)
        self.waitResultLineEdit.setText("web_wait_result")
        self.outputHLayout.addWidget(self.waitResultLineEdit, 0, 1, 1, 2, Qt.AlignCenter)
        self.waitResultFunctionBtn = flowSettingDialog.addFunctionButton(self.waitResultLineEdit, self)
        self.outputHLayout.addWidget(self.waitResultFunctionBtn, 0, 1, 1, 2, Qt.AlignRight)
        self.waitResultTipLabel = flowSettingDialog.createTipLabel(u"等待结果", u"  如果为True则等待成功，否则等待超时")
        self.outputHLayout.addWidget(self.waitResultTipLabel, 0, 3, 1, 1, Qt.AlignLeft)
        self.outputHLayout.setColumnStretch(0, 25)
        self.outputHLayout.setColumnStretch(1, 15)
        self.outputHLayout.setColumnStretch(2, 55)
        self.outputHLayout.setColumnStretch(3, 5)

    def selectCapturedElement(self):
        self.manualInputXpathCombobox.setEnabled(False)
        self.pointoutButton.setEnabled(True)

    def selectManualInputXpath(self):
        self.manualInputXpathCombobox.setEnabled(True)
        self.pointoutButton.setEnabled(False)

    def changeRegularTabUI(self):
        if self.waitCheckbox.isChecked() is True:
            self.waitTimeLabel.show()
            self.waitTimeLineEdit.show()
            self.waitTimeFunctionBtn.show()
            self.waitTimeTipLabel.show()
            self.outputHLayout.setColumnStretch(0, 25)
            self.outputHLayout.setColumnStretch(1, 15)
            self.outputHLayout.setColumnStretch(2, 55)
            self.outputHLayout.setColumnStretch(3, 5)
        else:
            self.waitTimeLabel.hide()
            self.waitTimeLineEdit.hide()
            self.waitTimeFunctionBtn.hide()
            self.waitTimeTipLabel.hide()
            self.outputHLayout.setColumnStretch(0, 20)
            self.outputHLayout.setColumnStretch(1, 15)
            self.outputHLayout.setColumnStretch(2, 55)
            self.outputHLayout.setColumnStretch(3, 10)

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
            self.webPageFunctionLabel.setText(self.waitResultLineEdit.text())
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
            self.setFixedSize(self.screenWidth * 0.46, self.screenHeight * 0.7)
            self.center()
        elif self.settingTabWidget.currentIndex() == 1:
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

    def printResult(self, result):
        print(result)

    def executeStep(self):
        try:
            handle = self.webSave.getWebObjectHandle(self.browserTypeCombobox.currentText())
            client = self.webSave.getWebObjectClient(self.browserTypeCombobox.currentText())
            client.maximize_window()
            client.switch_to.window(handle)
            if self.objectLabel.isChecked():
                webElement = client.find_element(By.XPATH, self.elementDaoMongo.getOneElement(self.elementLabel.text())["xpath"])
            else:
                webElement = client.find_element(By.XPATH, self.manualInputXpathCombobox.text())
            if self.waitTypeCombobox.currentIndex() == 0:
                if self.waitCheckbox.isChecked() is True:
                    waitResult = WebDriverWait(client, self.waitTimeLineEdit.text(), poll_frequency=0.1).until(
                        EC.visibility_of(webElement), message="failed")
                    print(waitResult)
                    if waitResult != 'Message: failed':
                        web_wait_result = True
                    else:
                        web_wait_result = False
                else:
                    while 1:
                        result = webElement.is_displayed()
                        if result is True:
                            print(result)
                            web_wait_result = True
                            break
                        time.sleep(0.5)
            elif self.waitTypeCombobox.currentIndex() == 1:
                if self.waitCheckbox.isChecked() is True:
                    waitResult = WebDriverWait(client, self.waitTimeLineEdit.text(), poll_frequency=0.1).until(
                        EC.invisibility_of_element(webElement), message="failed")
                    print(waitResult)
                    if waitResult != 'Message: failed':
                        web_wait_result = True
                    else:
                        web_wait_result = False
                else:
                    while 1:
                        result = webElement.is_displayed()
                        if result is False:
                            print(result)
                            web_wait_result = True
                            break
                        time.sleep(0.5)
            print(web_wait_result)
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
        self.elementLabel.setText(data["element"])
        self.waitTypeCombobox.setCurrentIndex(data["method"])
        self.waitTimeLineEdit.setText(data["value"])
        self.directive["data"] = data

    def updateSettingData(self):
        data = self.directive["data"]
        data["browser_type"] = self.browserTypeCombobox.currentIndex()
        data["element"] = self.elementLabel.text()
        data["method"] = self.waitTypeCombobox.currentIndex()
        data["value"] = self.waitTimeLineEdit.text()
        self.updateDirectiveData2DB(self.directive["_id"], data)

