# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from com.mat.rpa.utils import webAutoSave
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowSettingDialog

class RedirectingToNewWebPageObjectSettingDialog(flowSettingDialog.BasicFlowSettingDialog):
    def __init__(self, title,directive_id, id, parent=None):
        super(RedirectingToNewWebPageObjectSettingDialog, self).__init__(title, directive_id, id,parent)
        self.webSave = webAutoSave.WebAutoSave()
        self.setInfoLabelText(u"将Web浏览器跳转至新页面、后退、前进、或重新加载（刷新）当前页面")
        self.changeImage(flowSettingDialog.BasicFlowSettingDialog.picPath + "openWebPageBig.png")
        self.screenWidth = 1920
        self.screenHeight = 1030
        self.setFixedSize(self.screenWidth*0.46,self.screenHeight*0.52)
        self.regularTabUI()
        self.seniorTabUI()
        self.errorHandlingTabUI()
        self.settingTabWidget.currentChanged.connect(self.changeOpenWebPageObjectSettingDialogSize)

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
        self.directiveInputSettingLayout.addWidget(self.webObjectCombobox, 0, 1, 1, 2, Qt.AlignLeft)
        self.webObjectTipLabel = flowSettingDialog.createTipLabel(u"网页对象",
                                                                      u"  输入一个获取到的或者通过\"打开网\n  页\"创建的网页对象")
        self.directiveInputSettingLayout.addWidget(self.webObjectTipLabel, 0, 3, 1, 1, Qt.AlignLeft)

        self.webPageJumpMethodLabel = QLabel()
        self.webPageJumpMethodLabel.setFont(__font)
        self.webPageJumpMethodLabel.setText(u"跳转方式:")
        self.directiveInputSettingLayout.addWidget(self.webPageJumpMethodLabel, 1, 0, 1, 1, Qt.AlignRight)
        self.webPageJumpMethodCombobox = QComboBox()
        self.webPageJumpMethodCombobox.setObjectName("webPageJumpMethodCombobox")
        self.webPageJumpMethodCombobox.setFont(__font)
        self.webPageJumpMethodCombobox.setMinimumSize(600, 50)
        self.webPageJumpMethodCombobox.addItems([u"跳转至新页面",u"后退",u"前进",u"重新加载（刷新）"])
        self.webPageJumpMethodCombobox.currentIndexChanged.connect(self.changeRegularTab)
        self.webPageJumpMethodCombobox.setItemDelegate(QStyledItemDelegate())
        self.webPageJumpMethodCombobox.setStyleSheet(
            "QComboBox QAbstractItemView{selection-background-color: #f0f0f0;selection-color: #000;} QComboBox QAbstractItemView::item{min-height: 50px;}")
        self.directiveInputSettingLayout.addWidget(self.webPageJumpMethodCombobox, 1, 1, 1, 2, Qt.AlignCenter)
        self.webPageJumpMethodTipLabel = flowSettingDialog.createTipLabel(u"跳转方式",
                                                                  u"  选择一种跳转方式，可以是跳转至新页\n  面、后退、前进、或重新加载当前页面")
        self.directiveInputSettingLayout.addWidget(self.webPageJumpMethodTipLabel, 1, 3, 1, 1, Qt.AlignLeft)

        self.newUrlLabel = QLabel()
        self.newUrlLabel.setFont(__font)
        self.newUrlLabel.setText(u"新网址:")
        self.directiveInputSettingLayout.addWidget(self.newUrlLabel, 2, 0, 1, 1, Qt.AlignRight)
        self.newUrlLineEdit = QLineEdit()
        self.newUrlLineEdit.setFont(__font)
        self.newUrlLineEdit.setMinimumSize(600, 50)
        self.directiveInputSettingLayout.addWidget(self.newUrlLineEdit, 2, 1, 1, 2, Qt.AlignCenter)
        self.newUrlFunctionBtn = flowSettingDialog.addFunctionButton(self.newUrlLineEdit,self)
        self.directiveInputSettingLayout.addWidget(self.newUrlFunctionBtn, 2, 1, 1, 2, Qt.AlignRight)
        self.newUrlTipLabel = flowSettingDialog.createTipLabel(u"新网址",
                                                                  u"  填写要跳转到的目标网址")
        self.directiveInputSettingLayout.addWidget(self.newUrlTipLabel, 2, 3, 1, 1, Qt.AlignLeft)

        self.ignoreCacheCheckbox = QCheckBox()
        self.ignoreCacheCheckbox.setText(u"忽略缓存")
        self.ignoreCacheCheckbox.setFont(__font)
        self.directiveInputSettingLayout.addWidget(self.ignoreCacheCheckbox, 3, 1, 1, 1, Qt.AlignLeft)
        self.ignoreCacheTipLabel = flowSettingDialog.createTipLabel(u"忽略缓存",
                                                                    u"  重新加载时是否忽略浏览器缓存")
        self.directiveInputSettingLayout.addWidget(self.ignoreCacheTipLabel, 3, 2, 1, 1, Qt.AlignLeft)
        self.ignoreCacheCheckbox.hide()
        self.ignoreCacheTipLabel.hide()
        self.directiveInputSettingLayout.setColumnStretch(0, 20)
        self.directiveInputSettingLayout.setColumnStretch(1, 15)
        self.directiveInputSettingLayout.setColumnStretch(2, 55)
        self.directiveInputSettingLayout.setColumnStretch(3, 10)

        self.directiveOutputSettingLayout = QGridLayout()
        self.directiveOutputSettingLayout.setContentsMargins(10, 0, 0, 20)
        self.directiveOutputSettingLayout.setSpacing(10)
        self.directiveOutputSettingPanel.setLayout(self.directiveOutputSettingLayout)

        self.emptyLabel = QLabel()
        self.emptyLabel.setFont(__font)
        self.emptyLabel.setText(u"当前指令不包含任何输出项")
        self.emptyLabel.setStyleSheet("color:#838b8b;font-size:16px;font-family:Courier")
        self.emptyLabel.setAlignment(Qt.AlignCenter)
        self.directiveOutputSettingLayout.addWidget(self.emptyLabel, 0, 0, 1, 1, Qt.AlignCenter)

    def changeRegularTab(self):
        if self.webPageJumpMethodCombobox.currentIndex() == 0:
            self.newUrlLabel.show()
            self.newUrlLineEdit.show()
            self.newUrlFunctionBtn.show()
            self.newUrlTipLabel.show()
            self.ignoreCacheCheckbox.hide()
            self.ignoreCacheTipLabel.hide()
        elif self.webPageJumpMethodCombobox.currentIndex() == 3:
            self.newUrlLabel.hide()
            self.newUrlLineEdit.hide()
            self.newUrlFunctionBtn.hide()
            self.newUrlTipLabel.hide()
            self.ignoreCacheCheckbox.show()
            self.ignoreCacheTipLabel.show()
        else:
            self.newUrlLabel.hide()
            self.newUrlLineEdit.hide()
            self.newUrlFunctionBtn.hide()
            self.newUrlTipLabel.hide()
            self.ignoreCacheCheckbox.hide()
            self.ignoreCacheTipLabel.hide()
        self.changeOpenWebPageObjectSettingDialogSize()

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

        self.webLoadTimeOutPeriodLabel = QLabel()
        self.webLoadTimeOutPeriodLabel.setFont(__font)
        self.webLoadTimeOutPeriodLabel.setText(u"网页加载超时时间（秒）:")
        self.seniorTabLayout.addWidget(self.webLoadTimeOutPeriodLabel, 0, 0, 1, 1, Qt.AlignRight)
        self.webLoadTimeOutPeriodLineEdit = QLineEdit()
        self.webLoadTimeOutPeriodLineEdit.setFont(__font)
        self.webLoadTimeOutPeriodLineEdit.setMinimumSize(600, 50)
        self.seniorTabLayout.addWidget(self.webLoadTimeOutPeriodLineEdit, 0, 1, 1, 1, Qt.AlignCenter)
        self.webLoadTimeOutPeriodFunctionBtn = flowSettingDialog.addFunctionButton(self.webLoadTimeOutPeriodLineEdit,self)
        self.seniorTabLayout.addWidget(self.webLoadTimeOutPeriodFunctionBtn, 0, 1, 1, 1, Qt.AlignRight)
        self.webLoadTimeOutPeriodTipLabel = flowSettingDialog.createTipLabel(u"网页加载超时时间（秒）", u"  等待网页加载完成的超时时间")
        self.seniorTabLayout.addWidget(self.webLoadTimeOutPeriodTipLabel, 0, 2, 1, 1, Qt.AlignLeft)

    def changeOpenWebPageObjectSettingDialogSize(self):
        if self.settingTabWidget.currentIndex()==0:
            if self.webPageJumpMethodCombobox.currentIndex() == 0:
                self.setFixedSize(self.screenWidth*0.46,self.screenHeight*0.52)
            elif self.webPageJumpMethodCombobox.currentIndex() == 3:
                self.setFixedSize(self.screenWidth * 0.46, self.screenHeight * 0.55)
            else:
                self.setFixedSize(self.screenWidth * 0.46, self.screenHeight * 0.45)
        elif self.settingTabWidget.currentIndex()==1:
            self.setFixedSize(self.screenWidth * 0.50, self.screenHeight * 0.28)
        elif self.settingTabWidget.currentIndex()==2:
            if self.handleErrorWayCombobox.currentIndex() == 2:
                self.setFixedSize(self.screenWidth * 0.46, self.screenHeight * 0.37)
            else:
                self.setFixedSize(self.screenWidth * 0.46, self.screenHeight * 0.3)

    def executeStep(self):
        handle = self.webSave.getWebObjectHandle(self.webObjectCombobox.currentText())
        client = self.webSave.getWebObjectClient(self.webObjectCombobox.currentText())
        client.switch_to.window(handle)
        try:
            if self.webLoadTimeOutPeriodLineEdit.text() =="":
                timeout=0
            else:timeout=int(self.webLoadTimeOutPeriodLineEdit.text())
            client.set_page_load_timeout(timeout)
            if self.webPageJumpMethodCombobox.currentIndex()==0:
                client.get(self.newUrlLineEdit.text())
            elif self.webPageJumpMethodCombobox.currentIndex()==1:
                client.back()
            elif self.webPageJumpMethodCombobox.currentIndex() == 2:
                client.forward()
            elif self.webPageJumpMethodCombobox.currentIndex() == 3:
                client.refresh()
            handles = client.window_handles
            client.switch_to.window(handles[-1])
        except Exception as e:
            client.execute_script('window.stop ? window.stop() : document.execCommand("Stop");')
            print(e)

    def handleQuestionBtnClicked(self):
        print("点击使用说明按钮")

    def handleConfirmBtnClicked(self):
        self.accept()

    def handleCancelBtnClicked(self):
        self.reject()

    def handleExecutionBtnClicked(self):
        self.executeStep()

