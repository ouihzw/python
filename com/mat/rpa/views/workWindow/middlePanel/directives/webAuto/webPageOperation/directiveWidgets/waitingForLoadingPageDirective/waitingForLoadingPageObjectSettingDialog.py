# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from com.mat.rpa.utils import webAutoSave
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowSettingDialog
from com.mat.rpa.dao.workDao.directiveDao import DirectiveDao
class WaitingForLoadingPageObjectSettingDialog(flowSettingDialog.BasicFlowSettingDialog):
    def __init__(self, title, directive_id, id, parent=None):
        # 参照修改infolabel的提示信息
        super(WaitingForLoadingPageObjectSettingDialog, self).__init__(title, directive_id, id, parent)
        self.webSave = webAutoSave.WebAutoSave()
        self.setInfoLabelText(u"等待网页加载完成")
        self.changeImage(flowSettingDialog.BasicFlowSettingDialog.picPath + "openWebPageBig.png")
        self.screenWidth = 1920
        self.screenHeight = 1030
        self.setFixedSize(self.screenWidth * 0.48, self.screenHeight * 0.54)
        self.regularTabUI()
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
                                  "time_out": "20",
                                  "execute_error": 0,
                                  "log": True,
                                  "handle": 0,
                                  "retry_count": 1,
                                  "retry_interval": 1}
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

        self.loadTimeOutPeriodLabel = QLabel()
        self.loadTimeOutPeriodLabel.setFont(__font)
        self.loadTimeOutPeriodLabel.setText(u"加载超时时间:")
        self.directiveInputSettingLayout.addWidget(self.loadTimeOutPeriodLabel, 1, 0, 1, 1, Qt.AlignRight)
        self.webLoadTimeOutPeriodLineEdit = QLineEdit()
        self.webLoadTimeOutPeriodLineEdit.setFont(__font)
        self.webLoadTimeOutPeriodLineEdit.setMinimumSize(600, 50)
        self.directiveInputSettingLayout.addWidget(self.webLoadTimeOutPeriodLineEdit, 1, 1, 1, 1, Qt.AlignCenter)
        self.webLoadTimeOutPeriodFunctionBtn = flowSettingDialog.addFunctionButton(self.webLoadTimeOutPeriodLineEdit,
                                                                                   self)
        self.directiveInputSettingLayout.addWidget(self.webLoadTimeOutPeriodFunctionBtn, 1, 1, 1, 1, Qt.AlignRight)
        self.loadTimeOutPeriodTipLabel = flowSettingDialog.createTipLabel(u"加载超时时间", u"  等待网页加载完成的超时时间")
        self.directiveInputSettingLayout.addWidget(self.loadTimeOutPeriodTipLabel, 1, 2, 1, 1, Qt.AlignLeft)

        self.executeAfterLoadTimesOutLabel = QLabel()
        self.executeAfterLoadTimesOutLabel.setFont(__font)
        self.executeAfterLoadTimesOutLabel.setText(u"加载超时后执行:")
        self.directiveInputSettingLayout.addWidget(self.executeAfterLoadTimesOutLabel, 2, 0, 1, 1, Qt.AlignRight)
        self.executeAfterLoadTimesOutCombobox = QComboBox()
        self.executeAfterLoadTimesOutCombobox.setFont(__font)
        self.executeAfterLoadTimesOutCombobox.setMinimumSize(600, 50)
        self.executeAfterLoadTimesOutCombobox.setObjectName("executeAfterLoadTimesOutCombobox")
        self.executeAfterLoadTimesOutCombobox.addItems([u"执行\"错误\"处理", u"停止网页加载"])
        self.executeAfterLoadTimesOutCombobox.setItemDelegate(QStyledItemDelegate())
        self.executeAfterLoadTimesOutCombobox.setStyleSheet(
            "QComboBox QAbstractItemView{selection-background-color: #f0f0f0;selection-color: #000;} QComboBox QAbstractItemView::item{min-height: 50px;}")
        self.directiveInputSettingLayout.addWidget(self.executeAfterLoadTimesOutCombobox, 2, 1, 1, 1, Qt.AlignCenter)
        self.executeAfterLoadTimesOutTipLabel = flowSettingDialog.createTipLabel(u"加载超时后执行", u"  等待网页加载完成超时后希望执行的\n  操作")
        self.directiveInputSettingLayout.addWidget(self.executeAfterLoadTimesOutTipLabel, 2, 2, 1, 1, Qt.AlignLeft)

        self.directiveInputSettingLayout.setColumnStretch(0, 20)
        self.directiveInputSettingLayout.setColumnStretch(1, 70)
        self.directiveInputSettingLayout.setColumnStretch(2, 10)

        self.directiveOutputSettingLayout = QGridLayout()
        self.directiveOutputSettingLayout.setContentsMargins(10, 0, 0, 20)
        self.directiveOutputSettingLayout.setSpacing(10)
        self.directiveOutputSettingPanel.setLayout(self.directiveOutputSettingLayout)
        self.emptyLabel = QLabel()
        self.emptyLabel.setFont(__font)
        self.emptyLabel.setText(u"（当前指令不包含任何输出项）")
        self.emptyLabel.setStyleSheet("color:#838b8b;font-size:16px;font-family:Courier")
        self.emptyLabel.setAlignment(Qt.AlignCenter)
        self.directiveOutputSettingLayout.addWidget(self.emptyLabel, 0, 0, 1, 1, Qt.AlignCenter)

    def changeOpenWebPageObjectSettingDialogSize(self):
        if self.settingTabWidget.currentIndex()==0:
            self.setFixedSize(self.screenWidth * 0.48, self.screenHeight * 0.54)
        elif self.settingTabWidget.currentIndex()==1:
            if self.handleErrorWayCombobox.currentIndex() == 2:
                self.setFixedSize(self.screenWidth * 0.46, self.screenHeight * 0.37)
            else:
                self.setFixedSize(self.screenWidth * 0.46, self.screenHeight * 0.3)

    def executeStep(self):
        handle = self.webSave.getWebObjectHandle(self.webObjectCombobox.currentText())
        client = self.webSave.getWebObjectClient(self.webObjectCombobox.currentText())
        client.switch_to.window(handle)
        try:
            if self.webLoadTimeOutPeriodLineEdit.text() == "":
                timeout = 0
            else:
                timeout = int(self.webLoadTimeOutPeriodLineEdit.text())
            client.set_page_load_timeout(timeout)
            handles = client.window_handles
            client.switch_to.window(handles[-1])
        except Exception as e:
            if self.executeAfterLoadTimesOutCombobox.currentIndex()==1:
                client.execute_script('window.stop ? window.stop() : document.execCommand("Stop");')
            else:
                #应该执行错误处理
                print(e)

    def handleQuestionBtnClicked(self):
        print("点击使用说明按钮")

    def handleConfirmBtnClicked(self):
        self.accept()

    def handleCancelBtnClicked(self):
        self.reject()

    def handleExecutionBtnClicked(self):
        self.executeStep()

    def getSettingData(self):
        data = self.getDirectiveSettingDataFromDB(self.directive["_id"])
        self.webObjectCombobox.setCurrentText(data["web_object"])
        self.webLoadTimeOutPeriodLineEdit.setText(data["time_out"])
        self.executeAfterLoadTimesOutCombobox.setCurrentIndex(data["execute_error"])
        self.printErrorLogsCheckbox.setChecked(data["log"])
        self.handleErrorWayCombobox.setCurrentIndex(data["handle"])
        self.retryCountSpinbox.setValue(data["retry_count"])
        self.retryIntervalSpinbox.setValue(data["retry_interval"])
        self.directive["data"] = data

    def updateSettingData(self):
        data = self.directive["data"]
        data["web_object"] = self.webObjectCombobox.currentText()
        data["time_out"] = self.webLoadTimeOutPeriodLineEdit.text()
        data["execute_error"] = self.executeAfterLoadTimesOutCombobox.currentIndex()
        data["log"] = self.printErrorLogsCheckbox.isChecked()
        data["handle"] = self.handleErrorWayCombobox.currentIndex()
        data["retry_count"] = self.retryCountSpinbox.value()
        data["retry_interval"] = self.retryIntervalSpinbox.value()
        self.updateDirectiveData2DB(self.directive["_id"], self.directive["data"])
        self.updateSecondLineInfo()
    def updateDirectiveData2DB(self, directive_id, data: dict):
        self.directiveDaoObj.updateDirective(directive_id, {"data": data})

    def getDirectiveSettingDataFromDB(self, directive_id):
        return self.directiveDaoObj.getOneDirective(directive_id)["data"]