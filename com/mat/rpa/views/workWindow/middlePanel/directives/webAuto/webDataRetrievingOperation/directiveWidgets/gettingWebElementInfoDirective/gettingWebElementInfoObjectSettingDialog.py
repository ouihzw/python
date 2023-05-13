# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowSettingDialog
from com.mat.rpa.utils import webAutoSave,webElementInfo
from com.mat.rpa.dao.elementDao import elementDao
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from com.mat.rpa.dao.workDao.directiveDao import DirectiveDao

class GettingWebElementInfoObjectSettingDialog(flowSettingDialog.BasicFlowSettingDialog):
    flowTextList = pyqtSignal(list)
    def __init__(self, title, directive_id, id, parent=None):
        super().__init__(title, directive_id, id, parent)
        self.directiveDaoObj = DirectiveDao()
        self.webSave = webAutoSave.WebAutoSave()
        self.elementDaoMongo = elementDao.ElementDao()
        self.setInfoLabelText(u"获取网页中的元素的文本内容、源代码、属性值等信息")
        self.changeImage(flowSettingDialog.BasicFlowSettingDialog.picPath + "openWebPageBig.png")
        self.webElement = webElementInfo.WebElementInfo()
        self.screenWidth = 1920
        self.screenHeight = 1030
        self.setFixedSize(self.screenWidth * 0.47, self.screenHeight * 0.59)
        self.center()
        self.regularTabUI()
        self.seniorTabUI()
        self.errorHandlingTabUI()
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
        self.directive["data"] = {"web_object": "",
                                  "element": "",
                                  "operation": 0,
                                  "intelligent_identification": False,
                                  "propert_name": "",
                                  "output": "web_element_attribute",
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
        self.directiveInputSettingLayout.setContentsMargins(10, 0, 0, 0)
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

        self.operationLabel = QLabel()
        self.operationLabel.setFont(__font)
        self.operationLabel.setText(u"操作:")
        self.directiveInputSettingLayout.addWidget(self.operationLabel, 2, 0, 1, 1, Qt.AlignRight)
        self.operationCombobox = QComboBox()
        self.operationCombobox.setObjectName("operationCombobox")
        self.operationCombobox.setFont(__font)
        self.operationCombobox.setMinimumSize(600, 50)
        self.operationCombobox.addItems([u"获取元素文本内容", u"获取元素源代码",u"获取元素值", u"获取网页链接地址",u"获取元素属性"])
        self.operationCombobox.setItemDelegate(QStyledItemDelegate())
        self.operationCombobox.setStyleSheet(
            "QComboBox QAbstractItemView{selection-background-color: #f0f0f0;selection-color: #000;} QComboBox QAbstractItemView::item{min-height: 50px;}")
        self.operationCombobox.currentIndexChanged.connect(self.changeRegularTab)
        self.directiveInputSettingLayout.addWidget(self.operationCombobox, 2, 1, 1, 2, Qt.AlignCenter)
        self.operationTipLabel = flowSettingDialog.createTipLabel(u"操作",
                                                                  u"  选择要获取的网页元素信息")
        self.directiveInputSettingLayout.addWidget(self.operationTipLabel, 2, 3, 1, 1, Qt.AlignLeft)

        self.intelligentIdentificationCheckbox=QCheckBox()
        self.intelligentIdentificationCheckbox.setText(u"智能识别并补充地址前缀（http://或https://）")
        self.intelligentIdentificationCheckbox.setFont(__font)
        self.directiveInputSettingLayout.addWidget(self.intelligentIdentificationCheckbox, 3, 1, 1, 1, Qt.AlignLeft)
        self.intelligentIdentificationCheckboxTipLabel = flowSettingDialog.createTipLabel(u"智能识别并补充地址前缀\n（http://或https://）",
                                                                                          u"  智能识别并补充地址前缀（http://或\n  https://）")
        self.directiveInputSettingLayout.addWidget(self.intelligentIdentificationCheckboxTipLabel, 3, 2, 1, 1, Qt.AlignLeft)
        self.intelligentIdentificationCheckbox.hide()
        self.intelligentIdentificationCheckboxTipLabel.hide()

        self.propertyNameLabel=QLabel()
        self.propertyNameLabel.setFont(__font)
        self.propertyNameLabel.setText(u"属性名称:")
        self.directiveInputSettingLayout.addWidget(self.propertyNameLabel, 4, 0, 1, 1, Qt.AlignRight)
        self.propertyNameLineEdit = QLineEdit()
        self.propertyNameLineEdit.setFont(__font)
        self.propertyNameLineEdit.setMinimumSize(600, 50)
        self.directiveInputSettingLayout.addWidget(self.propertyNameLineEdit, 4, 1, 1, 2, Qt.AlignCenter)
        self.propertyNameFunctionBtn = flowSettingDialog.addFunctionButton(self.propertyNameLineEdit,self)
        self.directiveInputSettingLayout.addWidget(self.propertyNameFunctionBtn, 4, 1, 1, 2, Qt.AlignRight)
        self.propertyNameTipLabel = flowSettingDialog.createTipLabel(u"属性名称",
                                                                              u"  填写要获取的网页元素的属性名称")
        self.directiveInputSettingLayout.addWidget(self.propertyNameTipLabel, 4, 3, 1, 1, Qt.AlignLeft)
        self.propertyNameLabel.hide()
        self.propertyNameLineEdit.hide()
        self.propertyNameFunctionBtn.hide()
        self.propertyNameTipLabel.hide()
        self.directiveInputSettingLayout.setColumnStretch(0, 20)
        self.directiveInputSettingLayout.setColumnStretch(1, 57)
        self.directiveInputSettingLayout.setColumnStretch(2, 13)
        self.directiveInputSettingLayout.setColumnStretch(3, 10)

        self.directiveOutputSettingLayout = QGridLayout()
        self.directiveOutputSettingLayout.setContentsMargins(10, 0, 0, 20)
        self.directiveOutputSettingLayout.setSpacing(10)
        self.directiveOutputSettingPanel.setLayout(self.directiveOutputSettingLayout)

        self.saveElementInfoLabel = QLabel()
        self.saveElementInfoLabel.setFont(__font)
        self.saveElementInfoLabel.setText(u"保存元素信息至")
        self.directiveOutputSettingLayout.addWidget(self.saveElementInfoLabel, 0, 0, 1, 1, Qt.AlignRight)
        self.outputVariableNameLineEdit = QLineEdit()
        self.outputVariableNameLineEdit.setFont(__font)
        self.outputVariableNameLineEdit.setMinimumSize(600, 50)
        self.outputVariableNameLineEdit.setText("web_element_attribute")
        self.directiveOutputSettingLayout.addWidget(self.outputVariableNameLineEdit, 0, 1, 1, 1, Qt.AlignCenter)
        self.saveElementInfoFunctionBtn = flowSettingDialog.addFunctionButton(self.outputVariableNameLineEdit,
                                                                                    self)
        self.directiveOutputSettingLayout.addWidget(self.saveElementInfoFunctionBtn, 0, 1, 1, 1, Qt.AlignRight)
        self.saveElementInfoTipLabel = flowSettingDialog.createTipLabel(u"保存元素信息至",
                                                                              u"  指定一个变量名称，该变量用于保存获\n  取到的网页元素信息")
        self.directiveOutputSettingLayout.addWidget(self.saveElementInfoTipLabel, 0, 2, 1, 1, Qt.AlignLeft)
        self.directiveOutputSettingLayout.setColumnStretch(0, 20)  # 第一列占10/100
        self.directiveOutputSettingLayout.setColumnStretch(1, 70)  # 第二列占80/100
        self.directiveOutputSettingLayout.setColumnStretch(2, 10)  # 第三列占10/100

    def changeRegularTab(self):
        if self.operationCombobox.currentIndex()==3:
            self.intelligentIdentificationCheckbox.show()
            self.intelligentIdentificationCheckboxTipLabel.show()
            self.propertyNameLabel.hide()
            self.propertyNameLineEdit.hide()
            self.propertyNameFunctionBtn.hide()
            self.propertyNameTipLabel.hide()
            self.setFixedSize(self.screenWidth * 0.47, self.screenHeight * 0.65)
            self.center()
        elif self.operationCombobox.currentIndex()==4:
            self.intelligentIdentificationCheckbox.hide()
            self.intelligentIdentificationCheckboxTipLabel.hide()
            self.propertyNameLabel.show()
            self.propertyNameLineEdit.show()
            self.propertyNameFunctionBtn.show()
            self.propertyNameTipLabel.show()
            self.setFixedSize(self.screenWidth * 0.47, self.screenHeight * 0.67)
            self.center()
        else:
            self.intelligentIdentificationCheckbox.hide()
            self.intelligentIdentificationCheckboxTipLabel.hide()
            self.propertyNameLabel.hide()
            self.propertyNameLineEdit.hide()
            self.propertyNameFunctionBtn.hide()
            self.propertyNameTipLabel.hide()
            self.setFixedSize(self.screenWidth * 0.47, self.screenHeight * 0.59)
            self.center()

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
        self.seniorTabLayout.setColumnStretch(1, 70)
        self.seniorTabLayout.setColumnStretch(2, 10)

        self.waitElementExistLabel = QLabel()
        self.waitElementExistLabel.setFont(__font)
        self.waitElementExistLabel.setText(u"等待元素存在(s):")
        self.seniorTabLayout.addWidget(self.waitElementExistLabel, 0, 0, 1, 1, Qt.AlignRight)
        self.waitElementExistLineEdit = QLineEdit()
        self.waitElementExistLineEdit.setFont(__font)
        self.waitElementExistLineEdit.setMinimumSize(600, 50)
        self.waitElementExistLineEdit.setText("20")
        self.seniorTabLayout.addWidget(self.waitElementExistLineEdit, 0, 1, 1, 1, Qt.AlignCenter)
        self.waitElementExistFunctionBtn = flowSettingDialog.addFunctionButton(self.waitElementExistLineEdit, self)
        self.seniorTabLayout.addWidget(self.waitElementExistFunctionBtn, 0, 1, 1, 1, Qt.AlignRight)
        self.waitElementExistTipLabel = flowSettingDialog.createTipLabel(u"等待元素存在(s)",u"  等待元素存在的超时时间")
        self.seniorTabLayout.addWidget(self.waitElementExistTipLabel, 0, 2, 1, 1, Qt.AlignLeft)

    def changeOpenWebPageObjectSettingDialogSize(self):
        if self.settingTabWidget.currentIndex() == 0:
            if self.operationCombobox.currentIndex()==3 :
                self.setFixedSize(self.screenWidth * 0.47, self.screenHeight * 0.67)
                self.center()
            elif self.operationCombobox.currentIndex()==4:
                self.setFixedSize(self.screenWidth * 0.47, self.screenHeight * 0.65)
                self.center()
            else:
                self.setFixedSize(self.screenWidth * 0.47, self.screenHeight * 0.59)
                self.center()
        elif self.settingTabWidget.currentIndex()==1:
            self.setFixedSize(self.screenWidth * 0.47, self.screenHeight * 0.3)
            self.center()
        elif self.settingTabWidget.currentIndex()==2:
            if self.handleErrorWayCombobox.currentIndex()==0:
                self.setFixedSize(self.screenWidth * 0.46, self.screenHeight * 0.3)
                self.center()
            elif self.handleErrorWayCombobox.currentIndex() == 1:
                self.setFixedSize(self.screenWidth * 0.46, self.screenHeight * 0.42)
                self.center()
            else:
                self.setFixedSize(self.screenWidth * 0.46, self.screenHeight *  0.37)
                self.center()
    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2-100)

    #实现确认和取消按钮点击事件
    def executeStep(self):
        try:
            handle = self.webSave.getWebObjectHandle(self.webObjectCombobox.currentText())
            client = self.webSave.getWebObjectClient(self.webObjectCombobox.currentText())
            client.switch_to.window(handle)
            WebDriverWait(client, int(self.waitElementExistLineEdit.text())).until(lambda p: p.find_element(By.XPATH,self.elementDaoMongo.getOneElement(self.elementLabel.text())["xpath"]).is_displayed())
            webElement = client.find_element(By.XPATH,self.elementDaoMongo.getOneElement(self.elementLabel.text())["xpath"])
            if self.operationCombobox.currentIndex()==0:
                webElementInfo=webElement.text
            elif self.operationCombobox.currentIndex()==1:
                webElementInfo=webElement.get_property("outerHTML")
            elif self.operationCombobox.currentIndex()==2:
                webElementInfo = webElement.get_attribute("value")
            elif self.operationCombobox.currentIndex()==3:
                webElementInfo = webElement.get_attribute("herf")
            elif self.operationCombobox.currentIndex()==4:
                webElementInfo = webElement.get_attribute(self.propertyNameLineEdit.text())
            print("webElementInfo",webElementInfo)
            self.webElement.saveWebElementInfoObject(self.outputVariableNameLineEdit.text(),webElementInfo)
            handles = client.window_handles
            client.switch_to.window(handles[-1])
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
        self.operationCombobox.setCurrentIndex(data["operation"])
        self.intelligentIdentificationCheckbox.setChecked(data["intelligent_identification"])
        self.propertyNameLineEdit.setText(data["propert_name"])
        self.outputVariableNameLineEdit.setText(data["output"])
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
        data["operation"] = self.operationCombobox.currentIndex()
        data["intelligent_identification"] = self.intelligentIdentificationCheckbox.isChecked()
        data["propert_name"] = self.propertyNameLineEdit.text()
        data["output"] = self.outputVariableNameLineEdit.text()
        data["time_out"] = self.waitElementExistLineEdit.text()
        data["log"] = self.printErrorLogsCheckbox.isChecked()
        data["handle"] = self.handleErrorWayCombobox.currentIndex()
        data["on_error_output_value"] = self.onErrorOutputVariableLineEdit.text()
        data["retry_count"] = self.retryCountSpinbox.value()
        data["retry_interval"] = self.retryIntervalSpinbox.value()
        self.updateDirectiveData2DB(self.directive["_id"],data)

    def updateDirectiveData2DB(self, directive_id, data: dict):
        self.directiveDaoObj.updateDirective(directive_id, {"data": data})

    def getDirectiveSettingDataFromDB(self, directive_id):
        return self.directiveDaoObj.getOneDirective(directive_id)["data"]