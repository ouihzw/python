# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from com.mat.rpa.dao.elementDao import elementDao
from com.mat.rpa.utils import webAutoSave,webPageInfo
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowSettingDialog

from com.mat.rpa.dao.workDao.directiveDao import DirectiveDao

import html2text
import re
class GettingWebPageInfoObjectSettingDialog(flowSettingDialog.BasicFlowSettingDialog):
    flowTextList = pyqtSignal(list)
    def __init__(self, title, directive_id, id, parent=None):
        super().__init__(title, directive_id, id, parent)
        self.directiveDaoObj = DirectiveDao()
        self.webSave = webAutoSave.WebAutoSave()
        self.elementDaoMongo = elementDao.ElementDao()
        self.webPageInfoObject = webPageInfo.WebPageInfo()
        self.setInfoLabelText(u"获取网页对话框内容")
        self.changeImage(flowSettingDialog.BasicFlowSettingDialog.picPath + "openWebPageBig.png")
        self.screenWidth = 1920
        self.screenHeight = 1030
        self.setFixedSize(self.screenWidth * 0.46, self.screenHeight * 0.49)
        self.center()
        self.regularTabUI()
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
                                  "operation": 0,
                                  "output": "web_page_attribute",
                                  "log": True,
                                  "handle": 0,
                                  "on_error_output_value": "",
                                  "retry_count": 1,
                                  "retry_interval": 1}

    '''
    operationCombobox:操作选项
    '''
    def regularTabUI(self):
        __font = QFont()
        __font.setPixelSize(20)
        __font.setFamily("Courier")
        self.directiveInputSettingLayout = QGridLayout()
        self.directiveInputSettingLayout.setContentsMargins(70, 0, 20, 0)
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
        self.directiveInputSettingLayout.addWidget(self.webObjectCombobox, 0, 1, 1, 1, Qt.AlignLeft)
        self.webObjectTipLabel = flowSettingDialog.createTipLabel(u"网页对象",
                                                                  u"  输入一个获取到的或者通过\"打开网\n  页\"创建的网页对象")
        self.directiveInputSettingLayout.addWidget(self.webObjectTipLabel, 0, 2, 1, 1, Qt.AlignLeft)

        self.operationLabel = QLabel()
        self.operationLabel.setFont(__font)
        self.operationLabel.setText(u"操作:")
        self.directiveInputSettingLayout.addWidget(self.operationLabel, 1, 0, 1, 1, Qt.AlignRight)
        self.operationCombobox = QComboBox()
        self.operationCombobox.setObjectName("operationCombobox")
        self.operationCombobox.setFont(__font)
        self.operationCombobox.setMinimumSize(600, 50)
        self.operationCombobox.addItems(
            [u"获取网址", u"获取网页标题",u"获取网页源代码","获取网页文本内容"])
        self.operationCombobox.setItemDelegate(QStyledItemDelegate())
        self.operationCombobox.setStyleSheet(
            "QComboBox QAbstractItemView{selection-background-color: #f0f0f0;selection-color: #000;} QComboBox QAbstractItemView::item{min-height: 50px;}")
        self.directiveInputSettingLayout.addWidget(self.operationCombobox, 1, 1, 1, 1, Qt.AlignCenter)
        self.operationTipLabel = flowSettingDialog.createTipLabel(u"操作",
                                                                       u"  选择要获取的网页信息")
        self.directiveInputSettingLayout.addWidget(self.operationTipLabel, 1, 2, 1, 1, Qt.AlignLeft)
        self.directiveInputSettingLayout.setColumnStretch(0, 20)
        self.directiveInputSettingLayout.setColumnStretch(1, 70)
        self.directiveInputSettingLayout.setColumnStretch(2, 10)

        self.directiveOutputSettingLayout = QGridLayout()
        self.directiveOutputSettingLayout.setContentsMargins(10, 0, 0, 20)
        self.directiveOutputSettingLayout.setSpacing(10)
        self.directiveOutputSettingPanel.setLayout(self.directiveOutputSettingLayout)
        self.webPageInfoLabel = QLabel()
        self.webPageInfoLabel.setFont(__font)
        self.webPageInfoLabel.setText(u"存储网页信息至:")
        self.directiveOutputSettingLayout.addWidget(self.webPageInfoLabel, 0, 0, 1, 1, Qt.AlignRight)
        self.outputVariableNameLineEdit = QLineEdit()
        self.outputVariableNameLineEdit.setFont(__font)
        self.outputVariableNameLineEdit.setMinimumSize(600, 50)
        self.outputVariableNameLineEdit.setText("web_page_attribute")
        self.directiveOutputSettingLayout.addWidget(self.outputVariableNameLineEdit, 0, 1, 1, 1, Qt.AlignCenter)
        self.webPageInfoFunctionBtn = flowSettingDialog.addFunctionButton(self.outputVariableNameLineEdit, self)
        self.directiveOutputSettingLayout.addWidget(self.webPageInfoFunctionBtn, 0, 1, 1, 1, Qt.AlignRight)
        self.webPageInfoTipLabel = flowSettingDialog.createTipLabel(
            u"存储网页信息至",
            u"  指定一个变量名称，该变量用于存储获\n  取导的网页信息")
        self.directiveOutputSettingLayout.addWidget(self.webPageInfoTipLabel, 0, 2, 1, 1, Qt.AlignLeft)
        self.directiveOutputSettingLayout.setColumnStretch(0, 20)  # 第一列占10/100
        self.directiveOutputSettingLayout.setColumnStretch(1, 70)  # 第二列占80/100
        self.directiveOutputSettingLayout.setColumnStretch(2, 10)  # 第三列占10/100


    def changeOpenWebPageObjectSettingDialogSize(self):
        if self.settingTabWidget.currentIndex() == 0:
           self.setFixedSize(self.screenWidth * 0.46, self.screenHeight * 0.49)
           self.center()
        elif self.settingTabWidget.currentIndex()==1:
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
                  (screen.height() - size.height()) / 2-80)

    def get_AllText(self,client):
        h = html2text.HTML2Text()
        h.ignore_links = True
        html = client.page_source
        text = h.handle(html)
        return text


    def executeStep(self):
        try:
            handle = self.webSave.getWebObjectHandle(self.webObjectCombobox.currentText())
            client = self.webSave.getWebObjectClient(self.webObjectCombobox.currentText())
            client.switch_to.window(handle)
            if self.operationCombobox.currentIndex() == 0:
                self.webPageInfo = client.current_url
            elif self.operationCombobox.currentIndex() == 1:
                self.webPageInfo = client.title
            elif self.operationCombobox.currentIndex() == 2:
                self.webPageInfo = client.page_source
            elif self.operationCombobox.currentIndex() == 3:
                self.webPageInfo = self.get_AllText(client)
            self.webPageInfoObject.saveWebPageInfoObject(self.outputVariableNameLineEdit.text(),self.webPageInfo)
            handles = client.window_handles
            print(self.webPageInfo)
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
        self.operationCombobox.setCurrentIndex(data["operation"])
        self.outputVariableNameLineEdit.setText(data["output"])
        self.printErrorLogsCheckbox.setChecked(data["log"])
        self.handleErrorWayCombobox.setCurrentIndex(data["handle"])
        self.onErrorOutputVariableLineEdit.setText(data["on_error_output_value"])
        self.retryCountSpinbox.setValue(data["retry_count"])
        self.retryIntervalSpinbox.setValue(data["retry_interval"])
        self.directive["data"] = data

    def updateSettingData(self):
        data = self.directive["data"]
        data["web_object"] = self.webObjectCombobox.currentText()
        data["operation"] = self.operationCombobox.currentIndex()
        data["output"] = self.outputVariableNameLineEdit.text()
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