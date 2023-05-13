# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from urllib.parse import urlparse
from com.mat.rpa.dao.workDao.directiveDao import DirectiveDao
from com.mat.rpa.utils import webAutoSave,webSingleCase
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowSettingDialog

class SettingWebCookieObjectSettingDialog(flowSettingDialog.BasicFlowSettingDialog):
    flowTextList = pyqtSignal(list)
    def __init__(self, title, directive_id, id, parent=None):
        super(SettingWebCookieObjectSettingDialog,self).__init__(title, directive_id, id,parent)
        self.directiveDaoObj = DirectiveDao()
        self.webSave = webAutoSave.WebAutoSave()
        self.setInfoLabelText(u"根据指定的cookie数据设置cookie,若存在等效cook...")
        self.changeImage(flowSettingDialog.BasicFlowSettingDialog.picPath + "openWebPageBig.png")
        self.screenWidth = 1920
        self.screenHeight = 1030
        self.setFixedSize(self.screenWidth * 0.50, self.screenHeight * 0.9)
        self.move(self.screenWidth * 0.26, self.screenHeight * 0.03)
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
        self.directive["data"] = {"setting_mode": 0,
                                  "web_object": "",
                                  "browser_type": 0,
                                  "cookie_url": "",
                                  "cookie_name": "",
                                  "cookie_value": "",
                                  "cookie_domain": "",
                                  "cookie_path": "",
                                  "https_only": False,
                                  "secure": False,
                                  "session_cookie": True,
                                  "cookie_expiration_date": "100",
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
        self.directiveInputSettingLayout.setContentsMargins(20, 0, 20, 20)
        self.directiveInputSettingLayout.setSpacing(10)
        self.directiveInputSettingLayout.setVerticalSpacing(30)
        self.directiveInputSettingPanel.setLayout(self.directiveInputSettingLayout)

        self.urlSettingModeLabel = QLabel()
        self.urlSettingModeLabel.setFont(__font)
        self.urlSettingModeLabel.setText(u"url设置方式:")
        self.directiveInputSettingLayout.addWidget(self.urlSettingModeLabel, 0, 0, 1, 1, Qt.AlignRight)
        self.urlSettingModeCombobox = QComboBox()
        self.urlSettingModeCombobox.setObjectName("urlSettingModeCombobox")
        self.urlSettingModeCombobox.setFont(__font)
        self.urlSettingModeCombobox.setMinimumSize(600, 50)
        self.urlSettingModeCombobox.addItems([u"根据网页对象", u"根据输入的url"])
        self.urlSettingModeCombobox.currentIndexChanged.connect(self.changeRegularTab)
        self.urlSettingModeCombobox.setItemDelegate(QStyledItemDelegate())
        self.urlSettingModeCombobox.setStyleSheet(
            "QComboBox QAbstractItemView{selection-background-color: #f0f0f0;selection-color: #000;} QComboBox QAbstractItemView::item{min-height: 50px;}")
        self.directiveInputSettingLayout.addWidget(self.urlSettingModeCombobox, 0, 1, 1, 4, Qt.AlignCenter)
        self.urlSettingModeTipLabel = flowSettingDialog.createTipLabel(u"url设置方式",
                                                                       u"  cookie url设置来源，可选择手动输\n  入，如果选择网页对象，则自动使用网\n  页url设置")
        self.directiveInputSettingLayout.addWidget(self.urlSettingModeTipLabel, 0, 5, 1, 1, Qt.AlignLeft)

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
        self.directiveInputSettingLayout.addWidget(self.webObjectCombobox, 1, 1, 1, 4, Qt.AlignLeft)
        self.webObjectTipLabel = flowSettingDialog.createTipLabel(u"网页对象",
                                                                  u"  输入一个获取到的或者通过\"打开网\n  页\"创建的网页对象")
        self.directiveInputSettingLayout.addWidget(self.webObjectTipLabel, 1, 5, 1, 1, Qt.AlignLeft)

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
        self.directiveInputSettingLayout.addWidget(self.browserTypeCombobox, 2, 1, 1, 4, Qt.AlignCenter)
        self.browserTypeTipLabel = flowSettingDialog.createTipLabel(u"浏览器类型",
                                                                    u"  设置指定浏览器类型cookie")
        self.directiveInputSettingLayout.addWidget(self.browserTypeTipLabel, 2, 5, 1, 1, Qt.AlignLeft)
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
        self.directiveInputSettingLayout.addWidget(self.cookieUrlLineEdit, 3, 1, 1, 4, Qt.AlignCenter)
        self.cookieUrlFunctionBtn = flowSettingDialog.addFunctionButton(self.cookieUrlLineEdit, self)
        self.directiveInputSettingLayout.addWidget(self.cookieUrlFunctionBtn, 3, 1, 1, 4, Qt.AlignRight)
        self.cookieUrlTipLabel = flowSettingDialog.createTipLabel(u"cookie url",
                                                                  u"  cookie url，与cookie设置相关联的\n  url,该值影响创建cookie的默认\  domain和path值")
        self.directiveInputSettingLayout.addWidget(self.cookieUrlTipLabel, 3, 5, 1, 1, Qt.AlignLeft)
        self.cookieUrlLabel.hide()
        self.cookieUrlLineEdit.hide()
        self.cookieUrlFunctionBtn.hide()
        self.cookieUrlTipLabel.hide()

        self.cookieNameLabel = QLabel()
        self.cookieNameLabel.setFont(__font)
        self.cookieNameLabel.setText(u"cookie name:")
        self.directiveInputSettingLayout.addWidget(self.cookieNameLabel, 4, 0, 1, 1, Qt.AlignRight)
        self.cookieNameLineEdit = QLineEdit()
        self.cookieNameLineEdit.setFont(__font)
        self.cookieNameLineEdit.setMinimumSize(600, 50)
        self.directiveInputSettingLayout.addWidget(self.cookieNameLineEdit, 4, 1, 1, 4, Qt.AlignCenter)
        self.cookieNameFunctionBtn = flowSettingDialog.addFunctionButton(self.cookieNameLineEdit,self)
        self.directiveInputSettingLayout.addWidget(self.cookieNameFunctionBtn, 4, 1, 1, 4, Qt.AlignRight)
        self.cookieNameTipLabel = flowSettingDialog.createTipLabel(u"cookie名称",
                                                                  u"  cookie名称，忽略则为空")
        self.directiveInputSettingLayout.addWidget(self.cookieNameTipLabel, 4, 5, 1, 1, Qt.AlignLeft)

        self.cookieValueLabel = QLabel()
        self.cookieValueLabel.setFont(__font)
        self.cookieValueLabel.setText(u"cookie value:")
        self.directiveInputSettingLayout.addWidget(self.cookieValueLabel, 5, 0, 1, 1, Qt.AlignRight)
        self.cookieValueTextEdit = QTextEdit()
        self.cookieValueTextEdit.setFont(__font)
        self.cookieValueTextEdit.setFixedSize(575, 50)
        self.directiveInputSettingLayout.addWidget(self.cookieValueTextEdit, 5, 1, 1, 4, Qt.AlignLeft)
        self.cookieValueFunctionBtn = flowSettingDialog.addFunctionButton(self.cookieValueTextEdit,self)
        self.directiveInputSettingLayout.addWidget(self.cookieValueFunctionBtn, 5, 1, 1, 4, Qt.AlignRight)
        self.cookieValueTipLabel = flowSettingDialog.createTipLabel(u"cookie值",
                                                                   u"  cookie值，忽略则为空")
        self.directiveInputSettingLayout.addWidget(self.cookieValueTipLabel, 5, 5, 1, 1, Qt.AlignLeft)

        self.cookieDomainLabel = QLabel()
        self.cookieDomainLabel.setFont(__font)
        self.cookieDomainLabel.setText(u"cookie domain:")
        self.directiveInputSettingLayout.addWidget(self.cookieDomainLabel, 6, 0, 1, 1, Qt.AlignRight)
        self.cookieDomainLineEdit = QLineEdit()
        self.cookieDomainLineEdit.setFont(__font)
        self.cookieDomainLineEdit.setMinimumSize(600, 50)
        self.directiveInputSettingLayout.addWidget(self.cookieDomainLineEdit, 6, 1, 1, 4, Qt.AlignCenter)
        self.cookieDomainFunctionBtn = flowSettingDialog.addFunctionButton(self.cookieDomainLineEdit,self)
        self.directiveInputSettingLayout.addWidget(self.cookieDomainFunctionBtn, 6, 1, 1, 4, Qt.AlignRight)
        self.cookieDomainTipLabel = flowSettingDialog.createTipLabel(u"cookie所在服务器域名",
                                                                    u"  cookie所在服务器域名，默认为url的\n  domain部分，忽略则该cookie为\n  host-only cookie")
        self.directiveInputSettingLayout.addWidget(self.cookieDomainTipLabel, 6, 5, 1, 1, Qt.AlignLeft)

        self.cookiePathLabel = QLabel()
        self.cookiePathLabel.setFont(__font)
        self.cookiePathLabel.setText(u"cookie path:")
        self.directiveInputSettingLayout.addWidget(self.cookiePathLabel, 7, 0, 1, 1, Qt.AlignRight)
        self.cookiePathLineEdit = QLineEdit()
        self.cookiePathLineEdit.setFont(__font)
        self.cookiePathLineEdit.setMinimumSize(600, 50)
        self.directiveInputSettingLayout.addWidget(self.cookiePathLineEdit, 7, 1, 1, 4, Qt.AlignCenter)
        self.cookiePathFunctionBtn = flowSettingDialog.addFunctionButton(self.cookiePathLineEdit,self)
        self.directiveInputSettingLayout.addWidget(self.cookiePathFunctionBtn, 7, 1, 1, 4, Qt.AlignRight)
        self.cookiePathTipLabel = flowSettingDialog.createTipLabel(u"cookie路径",
                                                                     u"  cookie路径，默认为url的path部\n  分，忽略则为空")
        self.directiveInputSettingLayout.addWidget(self.cookiePathTipLabel, 7, 5, 1, 1, Qt.AlignLeft)

        self.markedAsHttpOnlyCheckbox = QCheckBox()
        self.markedAsHttpOnlyCheckbox.setText(u"标记为HttpOnly")
        self.markedAsHttpOnlyCheckbox.setFont(__font)
        self.directiveInputSettingLayout.addWidget(self.markedAsHttpOnlyCheckbox, 8, 1, 1, 2, Qt.AlignLeft)
        self.markedAsHttpOnlyTipLabel = flowSettingDialog.createTipLabel(u"标记为HttpOnly", u"  设置该cookie是否被标记为\n  HttpOnly，默认为falise")
        self.directiveInputSettingLayout.addWidget(self.markedAsHttpOnlyTipLabel, 8, 3, 1, 1, Qt.AlignLeft)

        self.markedAsSecureCheckbox = QCheckBox()
        self.markedAsSecureCheckbox.setText(u"标记为Secure")
        self.markedAsSecureCheckbox.setFont(__font)
        self.directiveInputSettingLayout.addWidget(self.markedAsSecureCheckbox, 9, 1, 1, 1, Qt.AlignLeft)
        self.markedAsSecureTipLabel = flowSettingDialog.createTipLabel(u"标记为Secure",
                                                                         u"  设置该cookie是否被标记为\n  Secure，默认为falise")
        self.directiveInputSettingLayout.addWidget(self.markedAsSecureTipLabel, 9, 2, 1, 1, Qt.AlignLeft)

        self.setToSessionCookieCheckbox = QCheckBox()
        self.setToSessionCookieCheckbox.setText(u"设置为会话Cookie")
        self.setToSessionCookieCheckbox.setChecked(True)
        self.setToSessionCookieCheckbox.setFont(__font)
        self.setToSessionCookieCheckbox.stateChanged.connect(self.changeRegularTabButtom)
        self.directiveInputSettingLayout.addWidget(self.setToSessionCookieCheckbox, 10, 1, 1, 2, Qt.AlignLeft)
        self.setToSessionCookieTipLabel = flowSettingDialog.createTipLabel(u"设置为会话Cookie",
                                                                       u"  默认设置为会话Cookie,取消勾选则\n  设置为持久化cookie")
        self.directiveInputSettingLayout.addWidget(self.setToSessionCookieTipLabel, 10, 3, 1, 1, Qt.AlignLeft)

        self.cookieExpirationDateLabel = QLabel()
        self.cookieExpirationDateLabel.setFont(__font)
        self.cookieExpirationDateLabel.setText(u"cookie 有效期(秒):")
        self.directiveInputSettingLayout.addWidget(self.cookieExpirationDateLabel, 11, 0, 1, 1, Qt.AlignRight)
        self.cookieExpirationDateLineEdit = QLineEdit()
        self.cookieExpirationDateLineEdit.setFont(__font)
        self.cookieExpirationDateLineEdit.setMinimumSize(600, 50)
        self.directiveInputSettingLayout.addWidget(self.cookieExpirationDateLineEdit, 11, 1, 1, 4, Qt.AlignCenter)
        self.cookieExpirationDateFunctionBtn = flowSettingDialog.addFunctionButton(
            self.cookieExpirationDateLineEdit, self)
        self.directiveInputSettingLayout.addWidget(self.cookieExpirationDateFunctionBtn, 11, 1, 1, 4, Qt.AlignRight)
        self.cookieExpirationDateTipLabel = flowSettingDialog.createTipLabel(u"cookie 有效期(秒)",
                                                                             u"  持久化cookie需要设置有效期\n  （cookie生效到失效的时间间隔，单\n  位为秒），默认100s")
        self.directiveInputSettingLayout.addWidget(self.cookieExpirationDateTipLabel, 11, 5, 1, 1, Qt.AlignLeft)
        self.cookieExpirationDateLabel.hide()
        self.cookieExpirationDateLineEdit.hide()
        self.cookieExpirationDateFunctionBtn.hide()
        self.cookieExpirationDateTipLabel.hide()
        self.directiveInputSettingLayout.setColumnStretch(0, 20)
        self.directiveInputSettingLayout.setColumnStretch(1, 5)
        self.directiveInputSettingLayout.setColumnStretch(2, 2)
        self.directiveInputSettingLayout.setColumnStretch(3, 2)
        self.directiveInputSettingLayout.setColumnStretch(4, 61)
        self.directiveInputSettingLayout.setColumnStretch(5, 10)

        self.directiveOutputSettingLayout = QGridLayout()
        self.directiveOutputSettingLayout.setContentsMargins(0, 0, 0, 0)
        self.directiveOutputSettingLayout.setSpacing(0)
        self.directiveOutputSettingPanel.setLayout(self.directiveOutputSettingLayout)

        self.emptyLabel = QLabel()
        self.emptyLabel.setFont(__font)
        self.emptyLabel.setText(u"（当前指令不包含任何输出项）")
        self.emptyLabel.setStyleSheet("color:#838b8b;font-size:16px;font-family:Courier")
        self.emptyLabel.setAlignment(Qt.AlignCenter)
        self.emptyLabel.setFixedHeight(20)
        self.directiveOutputSettingLayout.addWidget(self.emptyLabel, 0, 0, 1, 1, Qt.AlignCenter)

    def changeRegularTab(self):
        if self.urlSettingModeCombobox.currentIndex() == 0:
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
        else:
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

    def changeRegularTabButtom(self):
        if self.setToSessionCookieCheckbox.isChecked():
            self.cookieExpirationDateLabel.hide()
            self.cookieExpirationDateLineEdit.hide()
            self.cookieExpirationDateFunctionBtn.hide()
            self.cookieExpirationDateTipLabel.hide()
        else:
            self.cookieExpirationDateLabel.show()
            self.cookieExpirationDateLineEdit.show()
            self.cookieExpirationDateFunctionBtn.show()
            self.cookieExpirationDateTipLabel.show()
        self.changeOpenWebPageObjectSettingDialogSize()


    def changeOpenWebPageObjectSettingDialogSize(self):
        if self.settingTabWidget.currentIndex() == 0:
            if self.setToSessionCookieCheckbox.isChecked():
                self.setFixedSize(self.screenWidth * 0.50, self.screenHeight * 0.90)
            else:
                if self.urlSettingModeCombobox.currentIndex()==0:
                    self.setFixedSize(self.screenWidth * 0.50, self.screenHeight * 0.91)
                else:
                    self.setFixedSize(self.screenWidth * 0.50, self.screenHeight * 0.93)
            self.move(self.screenWidth * 0.26, self.screenHeight * 0.01)
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

        #url对象时在不输入domain的时候获取默认的domain
    def get_urlDomain(self):
        return urlparse(self.cookieUrlLineEdit.text()).netloc

    def executeStep(self):
        try:
            #使用网页对象
            if self.urlSettingModeCombobox.currentIndex()==0:
                handle = self.webSave.getWebObjectHandle(self.webObjectCombobox .currentText())
                client = self.webSave.getWebObjectClient(self.webObjectCombobox .currentText())
                client.switch_to.window(handle)
            elif self.urlSettingModeCombobox.currentIndex()==1:
                #选择浏览器类型
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
            cookies={'name':self.cookieNameLineEdit.text(),'value':self.cookieValueTextEdit.toPlainText().replace('\n', ''),
                     'domain':self.cookieDomainLineEdit.text(),'path':self.cookiePathLineEdit.text(),
                     'httpOnly':self.markedAsHttpOnlyCheckbox.isChecked(),'secure':self.markedAsSecureCheckbox.isChecked()}
            if cookies['domain'] == '':
                cookies['domain'] = self.get_urlDomain()
            if self.setToSessionCookieCheckbox.isChecked():
                cookies=cookies
            else:
                cookies={'name':self.cookieNameLineEdit.text(),'value':self.cookieValueTextEdit.toPlainText().replace('\n', ''),
                     'domain':self.cookieDomainLineEdit.text(),'path':self.cookiePathLineEdit.text(),
                     'httpOnly':self.markedAsHttpOnlyCheckbox.isChecked(),'secure':self.markedAsSecureCheckbox.isChecked(),'expiry':int(self.cookieExpirationDateLineEdit.text())}
            client.add_cookie(cookie_dict=cookies)
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
