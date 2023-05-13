# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from com.mat.rpa.dao.workDao.directiveDao import DirectiveDao
from com.mat.rpa.utils import webSingleCase
from com.mat.rpa.utils import webAutoSave,gettingWebPageObjectList
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowSettingDialog

class GettingWebPageObjectListObjectSettingDialog(flowSettingDialog.BasicFlowSettingDialog):
    flowTextList = pyqtSignal(list)
    def __init__(self, title, directive_id, id, parent=None):
        super(GettingWebPageObjectListObjectSettingDialog, self).__init__(title, directive_id, id,parent)
        self.directiveDaoObj = DirectiveDao()
        self.webSave = webAutoSave.WebAutoSave()
        self.WebPageObjectListObj= gettingWebPageObjectList.GettingWebPageObjectList()
        self.setInfoLabelText(u"获取已打开的网页对象列表，以实现批量对每个网页相关自动化操作")
        self.changeImage(flowSettingDialog.BasicFlowSettingDialog.picPath + "openWebPageBig.png")
        self.screenWidth = 1920
        self.screenHeight = 1030
        self.setFixedSize(self.screenWidth * 0.48, self.screenHeight * 0.5)
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
        self.directive["data"] = {"browser_type": 0,
                                  "match_way": 0,
                                  "title": "",
                                  "url": "",
                                  "match_wildcard": False,
                                  "output": "web_page_list",
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
        self.directiveInputSettingLayout.setContentsMargins(90, 0, 20, 0)
        self.directiveInputSettingLayout.setSpacing(10)
        self.directiveInputSettingLayout.setVerticalSpacing(30)
        self.directiveInputSettingPanel.setLayout(self.directiveInputSettingLayout)
        self.browserTypeLabel = QLabel()
        self.browserTypeLabel.setFont(__font)
        self.browserTypeLabel.setText(u"浏览器类型:")
        self.directiveInputSettingLayout.addWidget(self.browserTypeLabel, 0, 0, 1, 1, Qt.AlignRight)
        self.browserTypeCombobox = QComboBox()
        self.browserTypeCombobox.setObjectName("browserTypeCombobox")
        self.browserTypeCombobox.setFont(__font)
        self.browserTypeCombobox.setMinimumSize(600, 50)
        self.browserTypeCombobox.addItems([u"内置Fire Fox浏览器", u"Google Chrome浏览器",
                                           u"MicroSoft Edge浏览器", u"Internet Explorer浏览器",
                                           u"360安全浏览器"])
        self.browserTypeCombobox.setItemDelegate(QStyledItemDelegate())
        self.browserTypeCombobox.setStyleSheet(
            "QComboBox QAbstractItemView{selection-background-color: #f0f0f0;selection-color: #000;} QComboBox QAbstractItemView::item{min-height: 50px;}")
        self.directiveInputSettingLayout.addWidget(self.browserTypeCombobox, 0, 1, 1, 2, Qt.AlignCenter)
        self.browserTypeTipLabel = flowSettingDialog.createTipLabel(u"浏览器类型",
                                                                    u"  选择浏览器类型，Google Chrome浏\n  览器、Microsoft Edge浏览器需要\n  安装插件才能实现自动化")
        self.directiveInputSettingLayout.addWidget(self.browserTypeTipLabel, 0, 3, 1, 1, Qt.AlignLeft)

        self.matchWayLabel = QLabel()
        self.matchWayLabel.setFont(__font)
        self.matchWayLabel.setText(u"匹配方式:")
        self.directiveInputSettingLayout.addWidget(self.matchWayLabel, 1, 0, 1, 1, Qt.AlignRight)
        self.matchWayCombobox = QComboBox()
        self.matchWayCombobox.setObjectName("matchWayCombobox")
        self.matchWayCombobox.setFont(__font)
        self.matchWayCombobox.setMinimumSize(600, 50)
        self.matchWayCombobox.addItems([u"匹配所有网页",u"根据标题匹配", u"根据网址匹配"])
        self.matchWayCombobox.currentIndexChanged.connect(self.changeRegularTab)
        self.matchWayCombobox.setItemDelegate(QStyledItemDelegate())
        self.matchWayCombobox.setStyleSheet(
            "QComboBox QAbstractItemView{selection-background-color: #f0f0f0;selection-color: #000;} QComboBox QAbstractItemView::item{min-height: 50px;}")
        self.directiveInputSettingLayout.addWidget(self.matchWayCombobox, 1, 1, 1, 2, Qt.AlignCenter)
        self.matchWayTipLabel = flowSettingDialog.createTipLabel(u"匹配方式", u"  选择获取已打开网页的匹配方式")
        self.directiveInputSettingLayout.addWidget(self.matchWayTipLabel, 1, 3, 1, 1, Qt.AlignLeft)

        self.titleLabel = QLabel()
        self.titleLabel.setFont(__font)
        self.titleLabel.setText(u"标题:")
        self.directiveInputSettingLayout.addWidget(self.titleLabel, 2, 0, 1, 1, Qt.AlignRight)
        self.titleLineEdit = QLineEdit()
        self.titleLineEdit.setFont(__font)
        self.titleLineEdit.setMinimumSize(600, 50)
        self.directiveInputSettingLayout.addWidget(self.titleLineEdit, 2, 1, 1, 2, Qt.AlignCenter)
        self.titleFunctionBtn = flowSettingDialog.addFunctionButton(self.titleLineEdit, self)
        self.directiveInputSettingLayout.addWidget(self.titleFunctionBtn, 2, 1, 1, 2, Qt.AlignRight)
        self.titleTipLabel = flowSettingDialog.createTipLabel(u"标题",
                                                              u"  填写要匹配的网页标题或地址，支持模\n  糊匹配，不填则匹配所有网页")
        self.directiveInputSettingLayout.addWidget(self.titleTipLabel, 2, 3, 1, 1, Qt.AlignLeft)
        self.titleLabel.hide()
        self.titleLineEdit.hide()
        self.titleFunctionBtn.hide()
        self.titleTipLabel.hide()

        self.webLabel = QLabel()
        self.webLabel.setFont(__font)
        self.webLabel.setText(u"网址:")
        self.directiveInputSettingLayout.addWidget(self.webLabel, 3, 0, 1, 1, Qt.AlignRight)
        self.webLineEdit = QLineEdit()
        self.webLineEdit.setFont(__font)
        self.webLineEdit.setMinimumSize(600, 50)
        self.directiveInputSettingLayout.addWidget(self.webLineEdit, 3, 1, 1, 2, Qt.AlignCenter)
        self.webFunctionBtn = flowSettingDialog.addFunctionButton(self.webLineEdit, self)
        self.directiveInputSettingLayout.addWidget(self.webFunctionBtn, 3, 1, 1, 2, Qt.AlignRight)
        self.webTipLabel = flowSettingDialog.createTipLabel(u"网址",
                                                            u"  输入要匹配的网址，支持模糊匹配")
        self.directiveInputSettingLayout.addWidget(self.webTipLabel, 3, 3, 1, 1, Qt.AlignLeft)
        self.webLabel.hide()
        self.webLineEdit.hide()
        self.webFunctionBtn.hide()
        self.webTipLabel.hide()

        self.matchByWildcardCheckbox = QCheckBox()
        self.matchByWildcardCheckbox.setText(u"根据通配符匹配")
        self.matchByWildcardCheckbox.setFont(__font)
        self.directiveInputSettingLayout.addWidget(self.matchByWildcardCheckbox, 4, 1, 1, 1, Qt.AlignCenter)
        self.matchByWildcardTipLabel = flowSettingDialog.createTipLabel(u"根据通配符匹配", u"  根据通配符匹配")
        self.directiveInputSettingLayout.addWidget(self.matchByWildcardTipLabel, 4, 2, 1, 1, Qt.AlignLeft)
        self.matchByWildcardCheckbox.hide()
        self.matchByWildcardTipLabel.hide()
        # 设置表格三列的比例
        self.directiveInputSettingLayout.setColumnStretch(0, 20)
        self.directiveInputSettingLayout.setColumnStretch(1, 15)
        self.directiveInputSettingLayout.setColumnStretch(2, 55)
        self.directiveInputSettingLayout.setColumnStretch(3, 10)

        self.directiveOutputSettingLayout = QGridLayout()
        self.directiveOutputSettingLayout.setContentsMargins(10, 0, 0, 20)
        self.directiveOutputSettingLayout.setSpacing(10)
        self.directiveOutputSettingPanel.setLayout(self.directiveOutputSettingLayout)

        self.saveWebPageObjectListLabel = QLabel()
        self.saveWebPageObjectListLabel.setFont(__font)
        self.saveWebPageObjectListLabel.setText(u"保存网页对象列表至:")
        self.directiveOutputSettingLayout.addWidget(self.saveWebPageObjectListLabel, 0, 0, 1, 1, Qt.AlignRight)
        self.outputVariableNameLineEdit = QLineEdit()
        self.outputVariableNameLineEdit.setFont(__font)
        self.outputVariableNameLineEdit.setMinimumSize(600, 50)
        self.outputVariableNameLineEdit.setText("web_page_list")
        self.directiveOutputSettingLayout.addWidget(self.outputVariableNameLineEdit, 0, 1, 1, 1, Qt.AlignCenter)
        self.saveWebPageObjectListFunctionBtn = flowSettingDialog.addFunctionButton(self.outputVariableNameLineEdit, self)
        self.directiveOutputSettingLayout.addWidget(self.saveWebPageObjectListFunctionBtn, 0, 1, 1, 1, Qt.AlignRight)
        self.saveWebPageObjectListTipLabel = flowSettingDialog.createTipLabel(u"保存网页对象列表至",
                                                                          u"  该变量保存的是网页对象列表，使用此\n  网页对象列表可以对每个网页进行自\n  动化操作")
        self.directiveOutputSettingLayout.addWidget(self.saveWebPageObjectListTipLabel, 0, 2, 1, 1, Qt.AlignLeft)
        self.directiveOutputSettingLayout.setColumnStretch(0, 20)  # 第一列占10/100
        self.directiveOutputSettingLayout.setColumnStretch(1, 70)  # 第二列占80/100
        self.directiveOutputSettingLayout.setColumnStretch(2, 10)  # 第三列占10/100

    def changeRegularTab(self):
        if self.matchWayCombobox.currentIndex() == 1:
            self.titleLabel.show()
            self.titleLineEdit.show()
            self.titleFunctionBtn.show()
            self.titleTipLabel.show()
            self.webLabel.hide()
            self.webLineEdit.hide()
            self.webFunctionBtn.hide()
            self.webTipLabel.hide()
            self.matchByWildcardCheckbox.show()
            self.matchByWildcardTipLabel.show()
        elif self.matchWayCombobox.currentIndex() == 2:
            self.titleLabel.hide()
            self.titleLineEdit.hide()
            self.titleFunctionBtn.hide()
            self.titleTipLabel.hide()
            self.webLabel.show()
            self.webLineEdit.show()
            self.webFunctionBtn.show()
            self.webTipLabel.show()
            self.matchByWildcardCheckbox.show()
            self.matchByWildcardTipLabel.show()
        elif self.matchWayCombobox.currentIndex() == 0:
            self.titleLabel.hide()
            self.titleLineEdit.hide()
            self.titleFunctionBtn.hide()
            self.titleTipLabel.hide()
            self.webLabel.hide()
            self.webLineEdit.hide()
            self.webFunctionBtn.hide()
            self.webTipLabel.hide()
            self.matchByWildcardCheckbox.hide()
            self.matchByWildcardTipLabel.hide()
        self.changeOpenWebPageObjectSettingDialogSize()

    def changeOpenWebPageObjectSettingDialogSize(self):
        if self.settingTabWidget.currentIndex() == 0:
            if self.matchWayCombobox.currentIndex() == 0:
                self.setFixedSize(self.screenWidth * 0.48, self.screenHeight * 0.5)
                self.center()
            else:
                self.setFixedSize(self.screenWidth * 0.48, self.screenHeight * 0.63)
                self.center()
        elif self.settingTabWidget.currentIndex() == 1:
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
                  (screen.height() - size.height()) / 2 - 80)

    def executeStep(self):
        try:
            browser = self.browserTypeCombobox.currentIndex()
            # Chrome
            if browser == 0:
                client = webSingleCase.WebSingleClass().getFirefoxClient()
            elif browser == 1:
                client = webSingleCase.WebSingleClass().getChromeClient()
            # Edge Chromium
            elif browser == 2:
                client = 1
            # 其他
            else:
                return
            self.webPageList=[]
            if self.matchWayCombobox.currentIndex()==0:
                self.webPageList=client.window_handles
            elif self.matchWayCombobox.currentIndex()==1:
                handles = client.window_handles
                handlesNumber=len(handles)
                if self.matchByWildcardCheckbox.isChecked():
                    for i in range(0,handlesNumber):
                        client.switch_to.window(handles[i])
                        if self.titleLineEdit.text() in client.title:
                            self.webPageList.append(client.current_window_handle)
                else:
                    for i in range(0,handlesNumber):
                        client.switch_to.window(handles[i])
                        if self.titleLineEdit.text() == client.title:
                            self.webPageList.append(client.current_window_handle)
            elif self.matchWayCombobox.currentIndex()==2:
                handles = client.window_handles
                handlesNumber=len(handles)
                if self.matchByWildcardCheckbox.isChecked():
                    for i in range(0,handlesNumber):
                        client.switch_to.window(handles[i])
                        if self.webLineEdit.text() in client.current_url:
                            self.webPageList.append(client.current_window_handle)
                else:
                    for i in range(0,handlesNumber):
                        client.switch_to.window(handles[i])
                        if self.webLineEdit.text() == client.current_url:
                            self.webPageList.append(client.current_window_handle)
            print(self.webPageList)
            handles = client.window_handles
            client.switch_to.window(handles[-1])
            self.WebPageObjectListObj.saveGettingWebPageObjectListObject(
                self.outputVariableNameLineEdit.text(),
                self.webPageList)
        except Exception as e:
            print(e)

    def handleQuestionBtnClicked(self):
        print("点击使用说明按钮")

    def handleConfirmBtnClicked(self):
        self.accept()

    def handleCancelBtnClicked(self):
        self.reject()

    def handleExecutionBtnClicked(self):
        self.executeStep()