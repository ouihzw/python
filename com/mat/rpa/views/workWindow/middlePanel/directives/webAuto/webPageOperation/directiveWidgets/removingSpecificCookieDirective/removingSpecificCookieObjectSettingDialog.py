# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from com.mat.rpa.utils import webAutoSave
from com.mat.rpa.utils import webSingleCase
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowSettingDialog

class RemovingSpecificCookieObjectSettingDialog(flowSettingDialog.BasicFlowSettingDialog):
    def __init__(self, title, directive_id, id, parent=None):
        super(RemovingSpecificCookieObjectSettingDialog, self).__init__(title, directive_id, id,parent)
        self.webSave = webAutoSave.WebAutoSave()
        self.setInfoLabelText(u"移除通过cookie url、cookie name指定的co...")
        self.changeImage(flowSettingDialog.BasicFlowSettingDialog.picPath + "openWebPageBig.png")
        self.screenWidth = 1920
        self.screenHeight = 1030
        self.setFixedSize(self.screenWidth * 0.47, self.screenHeight * 0.54)
        self.center()
        self.regularTabUI()
        self.errorHandlingTabUI()
        self.settingTabWidget.currentChanged.connect(self.changeOpenWebPageObjectSettingDialogSize)

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

        self.urlSpecificationMethodLabel = QLabel()
        self.urlSpecificationMethodLabel.setFont(__font)
        self.urlSpecificationMethodLabel.setText(u"url指定方式:")
        self.directiveInputSettingLayout.addWidget(self.urlSpecificationMethodLabel, 0, 0, 1, 1, Qt.AlignRight)
        self.urlSpecificationMethodCombobox = QComboBox()
        self.urlSpecificationMethodCombobox.setObjectName("urlSpecificationMethodCombobox")
        self.urlSpecificationMethodCombobox.setFont(__font)
        self.urlSpecificationMethodCombobox.setMinimumSize(600, 50)
        self.urlSpecificationMethodCombobox.addItems([u"根据网页对象", u"根据输入的url"])
        self.urlSpecificationMethodCombobox.currentIndexChanged.connect(self.changeRegularTab)
        self.urlSpecificationMethodCombobox.setItemDelegate(QStyledItemDelegate())
        self.urlSpecificationMethodCombobox.setStyleSheet(
            "QComboBox QAbstractItemView{selection-background-color: #f0f0f0;selection-color: #000;} QComboBox QAbstractItemView::item{min-height: 50px;}")
        self.directiveInputSettingLayout.addWidget(self.urlSpecificationMethodCombobox, 0, 1, 1, 1, Qt.AlignCenter)
        self.urlSpecificationMethodTipLabel = flowSettingDialog.createTipLabel(u"url指定方式",
                                                                       u"  用来指定cookie的url来源，可选择\n  手动输入，如果选择网页对象，则自动\n  使用网页url指定")
        self.directiveInputSettingLayout.addWidget(self.urlSpecificationMethodTipLabel, 0, 2, 1, 1, Qt.AlignLeft)

        self.webObjectLabel = QLabel()
        self.webObjectLabel.setFont(__font)
        self.webObjectLabel.setText(u"网页对象:")
        self.directiveInputSettingLayout.addWidget(self.webObjectLabel, 1, 0, 1, 1, Qt.AlignRight)
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
        self.directiveInputSettingLayout.addWidget(self.webObjectCombobox, 1, 1, 1, 1, Qt.AlignLeft)
        self.webObjectTipLabel = flowSettingDialog.createTipLabel(u"网页对象",
                                                                  u"  输入一个获取到的或者通过\"打开网\n  页\"创建的网页对象")
        self.directiveInputSettingLayout.addWidget(self.webObjectTipLabel, 1, 2, 1, 1, Qt.AlignLeft)

        self.browserTypeLabel = QLabel()
        self.browserTypeLabel.setFont(__font)
        self.browserTypeLabel.setText(u"浏览器类型:")
        self.directiveInputSettingLayout.addWidget(self.browserTypeLabel, 2, 0, 1, 1, Qt.AlignRight)
        self.browserTypeCombobox = QComboBox()
        self.browserTypeCombobox.setObjectName("browserTypeCombobox")
        self.browserTypeCombobox.setFont(__font)
        self.browserTypeCombobox.setMinimumSize(600, 50)
        self.browserTypeCombobox.addItems([u"内置Fire Fox浏览器", u"Google Chrome浏览器",
                                           u"MicroSoft Edge浏览器", u"Internet Explorer浏览器"])
        self.browserTypeCombobox.setItemDelegate(QStyledItemDelegate())
        self.browserTypeCombobox.setStyleSheet(
            "QComboBox QAbstractItemView{selection-background-color: #f0f0f0;selection-color: #000;} QComboBox QAbstractItemView::item{min-height: 50px;}")
        self.directiveInputSettingLayout.addWidget(self.browserTypeCombobox, 2, 1, 1, 1, Qt.AlignCenter)
        self.browserTypeTipLabel = flowSettingDialog.createTipLabel(u"浏览器类型",
                                                                    u"  获取指定类型浏览器cookie")
        self.directiveInputSettingLayout.addWidget(self.browserTypeTipLabel, 2, 2, 1, 1, Qt.AlignLeft)
        self.browserTypeLabel.hide()
        self.browserTypeCombobox.hide()
        self.browserTypeTipLabel.hide()

        self.cookieUrlLabel = QLabel()
        self.cookieUrlLabel.setFont(__font)
        self.cookieUrlLabel.setText(u"cookie url:")
        self.directiveInputSettingLayout.addWidget(self.cookieUrlLabel, 3, 0, 1, 1, Qt.AlignRight)
        self.cookieUrlLineEdit = QLineEdit()
        self.cookieUrlLineEdit.setFont(__font)
        self.cookieUrlLineEdit.setMinimumSize(600, 50)
        self.directiveInputSettingLayout.addWidget(self.cookieUrlLineEdit, 3, 1, 1, 1, Qt.AlignCenter)
        self.cookieUrlFunctionBtn = flowSettingDialog.addFunctionButton(self.cookieUrlLineEdit, self)
        self.directiveInputSettingLayout.addWidget(self.cookieUrlFunctionBtn, 3, 1, 1, 1, Qt.AlignRight)
        self.cookieUrlTipLabel = flowSettingDialog.createTipLabel(u"cookie url",
                                                                  u"  cookie url，将被移除的cookie url")
        self.directiveInputSettingLayout.addWidget(self.cookieUrlTipLabel, 3, 2, 1, 1, Qt.AlignLeft)
        self.cookieUrlLabel.hide()
        self.cookieUrlLineEdit.hide()
        self.cookieUrlFunctionBtn.hide()
        self.cookieUrlTipLabel.hide()

        self.cookieNameLabel = QLabel()
        self.cookieNameLabel.setFont(__font)
        self.cookieNameLabel.setText(u"cookie名称:")
        self.directiveInputSettingLayout.addWidget(self.cookieNameLabel, 4, 0, 1, 1, Qt.AlignRight)
        self.cookieNameLineEdit = QLineEdit()
        self.cookieNameLineEdit.setFont(__font)
        self.cookieNameLineEdit.setMinimumSize(600, 50)
        self.directiveInputSettingLayout.addWidget(self.cookieNameLineEdit, 4, 1, 1, 1, Qt.AlignCenter)
        self.cookieNameFunctionBtn = flowSettingDialog.addFunctionButton(self.cookieNameLineEdit, self)
        self.directiveInputSettingLayout.addWidget(self.cookieNameFunctionBtn, 4, 1, 1, 1, Qt.AlignRight)
        self.cookieNameTipLabel = flowSettingDialog.createTipLabel(u"cookie名称",
                                                                   u"  将被移除的cookie名称")
        self.directiveInputSettingLayout.addWidget(self.cookieNameTipLabel, 4, 2, 1, 1, Qt.AlignLeft)
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

    def changeRegularTab(self):
        if self.urlSpecificationMethodCombobox.currentIndex() == 0:
            self.webObjectLabel.show()
            self.webObjectCombobox.show()
            self.webObjectTipLabel.show()
            self.browserTypeLabel.hide()
            self.browserTypeCombobox.hide()
            self.browserTypeTipLabel.hide()
            self.cookieUrlLabel.hide()
            self.cookieUrlLineEdit.hide()
            self.cookieUrlFunctionBtn.hide()
            self.cookieUrlTipLabel.hide()
        elif self.urlSpecificationMethodCombobox.currentIndex() == 1:
            self.webObjectLabel.hide()
            self.webObjectCombobox.hide()
            self.webObjectTipLabel.hide()
            self.browserTypeLabel.show()
            self.browserTypeCombobox.show()
            self.browserTypeTipLabel.show()
            self.cookieUrlLabel.show()
            self.cookieUrlLineEdit.show()
            self.cookieUrlFunctionBtn.show()
            self.cookieUrlTipLabel.show()
        self.changeOpenWebPageObjectSettingDialogSize()

    def changeOpenWebPageObjectSettingDialogSize(self):
        if self.settingTabWidget.currentIndex() == 0:
            if self.urlSpecificationMethodCombobox.currentIndex() == 0:
                self.setFixedSize(self.screenWidth * 0.47, self.screenHeight * 0.54)
                self.center()
            else:
                self.setFixedSize(self.screenWidth * 0.47, self.screenHeight * 0.61)
                self.center()
        elif self.settingTabWidget.currentIndex() == 1:
            if self.handleErrorWayCombobox.currentIndex() == 2:
                self.setFixedSize(self.screenWidth * 0.46, self.screenHeight * 0.37)
                self.center()
            else:
                self.setFixedSize(self.screenWidth * 0.46, self.screenHeight * 0.3)
                self.center()
    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2 - 80)

    def executeStep(self):
        try:
            if self.urlSpecificationMethodCombobox.currentIndex() == 0:
                handle = self.webSave.getWebObjectHandle(self.webObjectCombobox.currentText())
                client = self.webSave.getWebObjectClient(self.webObjectCombobox.currentText())
                client.switch_to.window(handle)
            elif self.urlSpecificationMethodCombobox.currentIndex() == 1:
                browser = self.browserTypeCombobox.currentIndex()
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
                js = "window.open('" + self.cookieUrlLineEdit.text() + "')"
                client.execute_script(js)
                handles = client.window_handles
                client.switch_to.window(handles[-1])
            client.delete_cookie(self.cookieNameLineEdit.text())
            handles = client.window_handles
            client.switch_to.window(handles[-1])
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

