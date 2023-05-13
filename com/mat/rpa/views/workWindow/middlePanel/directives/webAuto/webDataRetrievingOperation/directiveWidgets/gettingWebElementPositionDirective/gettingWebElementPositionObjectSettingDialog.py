# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowSettingDialog
from com.mat.rpa.utils import webAutoSave,webElementPosition
from com.mat.rpa.dao.elementDao import elementDao
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from com.mat.rpa.dao.workDao.directiveDao import DirectiveDao
class GettingWebElementPositionObjectSettingDialog(flowSettingDialog.BasicFlowSettingDialog):
    def __init__(self, title, directive_id, id, parent=None):
        super().__init__(title, directive_id, id, parent)
        self.setInfoLabelText(u"获取元素相对于屏幕或浏览器客户区域左上角的位置信息")
        self.changeImage(flowSettingDialog.BasicFlowSettingDialog.picPath + "openWebPageBig.png")
        self.webSave = webAutoSave.WebAutoSave()
        self.webElementPositionObject = webElementPosition.WebElementPosition()
        self.elementDaoMongo = elementDao.ElementDao()
        self.screenWidth = 1920
        self.screenHeight = 1030
        self.setFixedSize(self.screenWidth * 0.46, self.screenHeight * 0.59)
        self.center()
        self.regularTabUI()
        self.seniorTabUI()
        self.errorHandlingTabUI()
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
        self.directive["data"] = {"web_object": "",
                                  "element": "",
                                  "relatively": 0,
                                  "output": "bound",
                                  "switch_dpi": True,
                                  "time_out": "20",
                                  "log": True,
                                  "handle": 0,
                                  "on_error_output_value": "",
                                  "retry_count": 1,
                                  "retry_interval": 1}
    def regularTabUI(self):
        __font = QFont()
        __font.setPixelSize(20)
        __font.setFamily("Courier")
        # 布局指令输入面板
        self.directiveInputSettingLayout = QGridLayout()
        self.directiveInputSettingLayout.setContentsMargins(50, 0, 0, 0)
        self.directiveInputSettingLayout.setSpacing(10)
        self.directiveInputSettingLayout.setVerticalSpacing(30)
        self.directiveInputSettingPanel.setLayout(self.directiveInputSettingLayout)
        self.webObjectLabel = QLabel()
        self.webObjectLabel.setFont(__font)
        self.webObjectLabel.setText(u"网页对象:")
        self.directiveInputSettingLayout.addWidget(self.webObjectLabel, 0, 0, 1, 1, Qt.AlignRight)
        self.webObjectCombobox = QComboBox()
        self.webObjectCombobox.setObjectName("webObjectCombobox")
        self.webObjectCombobox.setEditable(False)  # 设置不可以编辑
        for i in range(len(self.webSave.getWebObjectName())):
            self.webObjectCombobox.addItem(self.webSave.getWebObjectName()[i])
        self.webObjectCombobox.setFont(__font)
        self.webObjectCombobox.setMinimumSize(600, 50)
        self.webObjectCombobox.setItemDelegate(QStyledItemDelegate())
        self.webObjectCombobox.setStyleSheet(
            "QComboBox QAbstractItemView{selection-background-color: #f0f0f0;selection-color: #000;} QComboBox QAbstractItemView::item{min-height: 50px;}")
        self.directiveInputSettingLayout.addWidget(self.webObjectCombobox, 0, 1, 1, 2, Qt.AlignLeft)
        self.webObjectTipLabel = flowSettingDialog.createTipLabel(u"网页对象",
                                                                  u"  输入一个获取到的或者通过\"打开网\n  页\"创建的网页对象")
        self.directiveInputSettingLayout.addWidget(self.webObjectTipLabel, 0, 3, 1, 1, Qt.AlignLeft)

        self.objectLabel = QLabel()
        self.objectLabel.setFont(__font)
        self.objectLabel.setText(u"操作目标:")
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
        self.matchWayTipLabel = flowSettingDialog.createTipLabel(u"操作目标",
                                                                 u"  选择要操作的网页元素")
        self.directiveInputSettingLayout.addWidget(self.matchWayTipLabel, 1, 3, 1, 1, Qt.AlignLeft)

        self.relativelyLabel = QLabel()
        self.relativelyLabel.setFont(__font)
        self.relativelyLabel.setText(u"相对于:")
        self.directiveInputSettingLayout.addWidget(self.relativelyLabel, 2, 0, 1, 1, Qt.AlignRight)
        self.relativelyCombobox = QComboBox()
        self.relativelyCombobox.setObjectName("relativelyCombobox")
        self.relativelyCombobox.setFont(__font)
        self.relativelyCombobox.setMinimumSize(600, 50)
        self.relativelyCombobox.addItems([u"屏幕左上角", u"浏览器页面左上角"])
        self.relativelyCombobox.setItemDelegate(QStyledItemDelegate())
        self.relativelyCombobox.setStyleSheet(
            "QComboBox QAbstractItemView{selection-background-color: #f0f0f0;selection-color: #000;} QComboBox QAbstractItemView::item{min-height: 50px;}")
        self.directiveInputSettingLayout.addWidget(self.relativelyCombobox, 2, 1, 1, 2, Qt.AlignCenter)
        self.relativelyTipLabel = flowSettingDialog.createTipLabel(u"相对于",
                                                                  u"  在整个屏幕中的位置还是在浏览器客户\n  区域中的位置")
        self.directiveInputSettingLayout.addWidget(self.relativelyTipLabel, 2, 3, 1, 1, Qt.AlignLeft)
        self.directiveInputSettingLayout.setColumnStretch(0, 20)
        self.directiveInputSettingLayout.setColumnStretch(1, 57)
        self.directiveInputSettingLayout.setColumnStretch(2, 13)
        self.directiveInputSettingLayout.setColumnStretch(3, 10)

        self.directiveOutputSettingLayout = QGridLayout()
        self.directiveOutputSettingLayout.setContentsMargins(10, 0, 0, 20)
        self.directiveOutputSettingLayout.setSpacing(10)
        self.directiveOutputSettingPanel.setLayout(self.directiveOutputSettingLayout)

        self.saveElementPositionInfoLabel = QLabel()
        self.saveElementPositionInfoLabel.setFont(__font)
        self.saveElementPositionInfoLabel.setText(u"保存位置信息至:")
        self.directiveOutputSettingLayout.addWidget(self.saveElementPositionInfoLabel, 0, 0, 1, 1, Qt.AlignRight)
        self.outputVariableNameLineEdit = QLineEdit()
        self.outputVariableNameLineEdit.setFont(__font)
        self.outputVariableNameLineEdit.setMinimumSize(600, 50)
        self.outputVariableNameLineEdit.setText("bound")
        self.directiveOutputSettingLayout.addWidget(self.outputVariableNameLineEdit, 0, 1, 1, 1, Qt.AlignCenter)
        self.saveElementPositionInfoFunctionBtn = flowSettingDialog.addFunctionButton(self.outputVariableNameLineEdit,
                                                                              self)
        self.directiveOutputSettingLayout.addWidget(self.saveElementPositionInfoFunctionBtn, 0, 1, 1, 1, Qt.AlignRight)
        self.saveElementPositionInfoTipLabel = flowSettingDialog.createTipLabel(u"保存位置信息至",
                                                                        u"  输入一个名称来保存元素位置信息")
        self.directiveOutputSettingLayout.addWidget(self.saveElementPositionInfoTipLabel, 0, 2, 1, 1, Qt.AlignLeft)
        self.directiveOutputSettingLayout.setColumnStretch(0, 20)  # 第一列占10/100
        self.directiveOutputSettingLayout.setColumnStretch(1, 70)  # 第二列占80/100
        self.directiveOutputSettingLayout.setColumnStretch(2, 10)  # 第三列占10/100

    def seniorTabUI(self):
        __font = QFont()
        __font.setPixelSize(20)
        __font.setFamily("Courier")
        self.seniorTab = QWidget()
        self.settingTabWidget.addTab(self.seniorTab, u"高级")
        self.seniorTabLayout = QGridLayout()
        self.seniorTab.setLayout(self.seniorTabLayout)
        self.seniorTabLayout.setContentsMargins(10, 20, 20, 20)
        self.seniorTabLayout.setSpacing(10)
        self.seniorTabLayout.setVerticalSpacing(20)
        self.seniorTabLayout.setColumnStretch(0, 20)
        self.seniorTabLayout.setColumnStretch(1, 20)
        self.seniorTabLayout.setColumnStretch(2, 50)
        self.seniorTabLayout.setColumnStretch(3,10)

        self.switchToDpiCheckbox = QCheckBox()
        self.switchToDpiCheckbox.setText(u"转为dpi为96对应值")
        self.switchToDpiCheckbox.setFont(__font)
        self.seniorTabLayout.addWidget(self.switchToDpiCheckbox, 0, 1, 1, 1, Qt.AlignLeft)
        self.switchToDpiTipLabel = flowSettingDialog.createTipLabel(u"转为dpi为96对应值",
            u"  是否需要将边框属性转换成与设备无关\n  的单位（每个单位1/96英寸）")
        self.seniorTabLayout.addWidget(self.switchToDpiTipLabel, 0, 2, 1, 1,Qt.AlignLeft)

        self.waitElementExistLabel = QLabel()
        self.waitElementExistLabel.setFont(__font)
        self.waitElementExistLabel.setText(u"等待元素存在(s):")
        self.seniorTabLayout.addWidget(self.waitElementExistLabel, 1, 0, 1, 1, Qt.AlignRight)
        self.waitElementExistLineEdit = QLineEdit()
        self.waitElementExistLineEdit.setFont(__font)
        self.waitElementExistLineEdit.setMinimumSize(600, 50)
        self.waitElementExistLineEdit.setText("20")
        self.seniorTabLayout.addWidget(self.waitElementExistLineEdit, 1, 1, 1, 2, Qt.AlignCenter)
        self.waitElementExistFunctionBtn = flowSettingDialog.addFunctionButton(self.waitElementExistLineEdit, self)
        self.seniorTabLayout.addWidget(self.waitElementExistFunctionBtn, 1, 1, 1, 2, Qt.AlignRight)
        self.waitElementExistTipLabel = flowSettingDialog.createTipLabel(u"等待元素存在(s)",u"  等待元素存在的超时时间")
        self.seniorTabLayout.addWidget(self.waitElementExistTipLabel, 1, 3, 1, 1, Qt.AlignLeft)

    def changeOpenWebPageObjectSettingDialogSize(self):
        if self.settingTabWidget.currentIndex() == 0:
            self.setFixedSize(self.screenWidth * 0.46, self.screenHeight * 0.59)
            self.center()
        elif self.settingTabWidget.currentIndex() == 1:
            self.setFixedSize(self.screenWidth * 0.47, self.screenHeight * 0.32)
            self.center()
        elif self.settingTabWidget.currentIndex() == 2:
            if self.handleErrorWayCombobox.currentIndex() == 0:
                self.setFixedSize(self.screenWidth * 0.46, self.screenHeight * 0.3)
                self.center()
            elif self.handleErrorWayCombobox.currentIndex() == 1:
                self.setFixedSize(self.screenWidth * 0.46, self.screenHeight * 0.42)
                self.center()
            else:
                self.setFixedSize(self.screenWidth * 0.46, self.screenHeight * 0.37)
                self.center()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2 - 100)

    def executeStep(self):
        try:
            handle = self.webSave.getWebObjectHandle(self.webObjectCombobox.currentText())
            client = self.webSave.getWebObjectClient(self.webObjectCombobox.currentText())
            client.switch_to.window(handle)
            WebDriverWait(client, int(self.waitElementExistLineEdit.text())).until(lambda p: p.find_element(By.XPATH,
                                                                                                            self.elementDaoMongo.getOneElement(
                                                                                                                self.elementLabel.text())[
                                                                                                                "xpath"]).is_displayed())
            webElement = client.find_element(By.XPATH,
                                             self.elementDaoMongo.getOneElement(self.elementLabel.text())["xpath"])
            if self.relativelyCombobox.currentIndex() == 0:
                elementAbscissa= webElement.location["x"] +client.get_window_position()["x"]
                elementOrdinate= webElement.location["y"] + client.get_window_position()["y"]
                webElementPosition= {'x':elementAbscissa, 'y': elementOrdinate}
            elif self.relativelyCombobox.currentIndex() == 1:
                webElementPosition = webElement.location
            self.webElementPositionObject.saveWebElementPositionObject(self.outputVariableNameLineEdit.text(), webElementPosition)
            handles = client.window_handles
            client.switch_to.window(handles[-1])
            print(webElementPosition)
        except Exception as e:
            print(e)

    def handleQuestionBtnClicked(self):
        print("点击使用说明按钮")

    def handleConfirmBtnClicked(self):
        self.updateSettingData()
        self.accept()

    def handleCancelBtnClicked(self):
        self.reject()

    def handleExecutionBtnClicked(self):
        self.executeStep()

    def getSettingData(self):
        data = self.getDirectiveSettingDataFromDB(self.directive["_id"])
        self.webObjectCombobox.setCurrentText(data["web_object"])
        self.elementLabel.setText(data["element"])
        self.relativelyCombobox.setCurrentIndex(data["relatively"])
        self.outputVariableNameLineEdit.setText(data["output"])
        self.switchToDpiCheckbox.setChecked(data["switch_dpi"])
        self.waitElementExistLineEdit.setText(data["time_out"])
        self.printErrorLogsCheckbox.setChecked(data["log"])
        self.handleErrorWayCombobox.setCurrentIndex(data["handle"])
        self.onErrorOutputVariableLineEdit.setText(data["on_error_output_value"])
        self.retryCountSpinbox.setValue(data["retry_count"])
        self.retryIntervalSpinbox.setValue(data["retry_interval"])
        self.directive["data"] = data

    def updateSettingData(self):
        data = self.directive["data"]
        data["web_object"] = self.webObjectCombobox.currentText()
        data["element"] = self.elementLabel.text()
        data["relatively"] = self.relativelyCombobox.currentIndex()
        data["output"] = self.outputVariableNameLineEdit.text()
        data["switch_dpi"]=self.switchToDpiCheckbox.isChecked()
        data["time_out"] = self.waitElementExistLineEdit.text()
        data["log"] = self.printErrorLogsCheckbox.isChecked()
        data["handle"] = self.handleErrorWayCombobox.currentIndex()
        data["on_error_output_value"] = self.onErrorOutputVariableLineEdit.text()
        data["retry_count"] = self.retryCountSpinbox.value()
        data["retry_interval"] = self.retryIntervalSpinbox.value()
        self.updateDirectiveData2DB(self.directive["_id"], data)

    def updateDirectiveData2DB(self, directive_id, data: dict):
        self.directiveDaoObj.updateDirective(directive_id, {"data": data})

    def getDirectiveSettingDataFromDB(self, directive_id):
        return self.directiveDaoObj.getOneDirective(directive_id)["data"]