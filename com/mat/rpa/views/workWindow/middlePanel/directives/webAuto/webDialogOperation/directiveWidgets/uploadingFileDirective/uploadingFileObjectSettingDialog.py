# -*- coding:utf-8 -*-
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowSettingDialog
from com.mat.rpa.dao.workDao.directiveDao import DirectiveDao
from com.mat.rpa.dao.elementDao import elementDao
from com.mat.rpa.utils import webAutoSave
import datetime,os,win32clipboard as clip,tkinter as tk,win32con
from tkinter import filedialog


class UploadingFileObjectSettingDialog(flowSettingDialog.BasicFlowSettingDialog):
    def __init__(self, title, directive_id, id, parent=None):
        super().__init__(title, directive_id, id, parent)
        self.directiveDaoObj = DirectiveDao()
        self.webSave = webAutoSave.WebAutoSave()
        self.elementDaoMongo = elementDao.ElementDao()
        #参照修改infolabel的提示信息
        self.setInfoLabelText("自动完成点击上传按钮、在文件选择对话框中输入待上传文件等系列操作")
        #下边按照需求布局指令输入控件、指令输出控件、高级和错误Tab
        self.screenWidth = 1920
        self.screenHeight = 1030
        self.setFixedSize(self.screenWidth * 0.46, self.screenHeight * 0.63)
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
                                  "screenshot_area": 0,
                                  "element_name": "",
                                  "save_location": False,
                                  "save_location_name": "",
                                  "name": True,
                                  "custom_name": "",
                                  "name_way": True,
                                  "output": "screenshot_save_file_name",
                                  "time_out_period": "20",
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
        self.directiveInputSettingLayout.addWidget(self.objectLabel, 2, 0, 1, 1, Qt.AlignRight)
        self.elementLayout = QHBoxLayout()
        self.elementLayout.setContentsMargins(0, 0, 0, 0)
        self.elementLayout.setSpacing(10)
        self.elementLabel = QLineEdit()
        self.elementLabel.setEnabled(False)  # 设置不可以编辑
        self.elementLabel.setFont(__font)
        self.elementLabel.setMinimumSize(390, 50)
        self.elementLayout.addWidget(self.elementLabel, 5)
        self.pointoutButton = flowSettingDialog.readElementFunctionButton(self.elementLabel, self)
        self.elementLayout.addWidget(self.pointoutButton, 1)
        self.directiveInputSettingLayout.addLayout(self.elementLayout, 2, 1, 1, 2, Qt.AlignLeft)
        self.matchWayTipLabel = flowSettingDialog.createTipLabel(u"操作目标",
                                                                 u"  选择要操作的网页元素")
        self.directiveInputSettingLayout.addWidget(self.matchWayTipLabel, 2, 3, 1, 1, Qt.AlignLeft)

        self.folderToSaveLabel = QLabel()
        self.folderToSaveLabel.setFont(__font)
        self.folderToSaveLabel.setText(u"上传文件路径:")
        self.directiveInputSettingLayout.addWidget(self.folderToSaveLabel, 4, 0, 1, 1, Qt.AlignRight)
        # 文件路径输入框和选择文件按钮的水平布局
        filePathHLayout = QHBoxLayout()
        filePathHLayout.setContentsMargins(0, 0, 0, 0)
        filePathHLayout.setSpacing(0)
        self.filePathLineEdit = QLineEdit(font=__font)
        self.filePathLineEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.filePathLineEdit.setFixedHeight(50)
        filePathHLayout.addWidget(self.filePathLineEdit)
        self.selectFileBtn = QPushButton(text=u"预览...", font=__font, clicked=self.selectFile)
        self.selectFileBtn.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.selectFileBtn.setFixedHeight(50)
        filePathHLayout.addWidget(self.selectFileBtn)
        self.selectFileFunctionBtn = flowSettingDialog.addFunctionButton(
            self.filePathLineEdit, self)
        self.selectFileFunctionBtn.setFixedHeight(50)
        filePathHLayout.addWidget(self.selectFileFunctionBtn)
        self.directiveInputSettingLayout.addLayout(filePathHLayout, 4, 1, 1, 2, Qt.AlignCenter)
        self.folderToSaveTipLabel = flowSettingDialog.createTipLabel(u"保存文件夹",
                                                                     u"  截图保存的文件夹")
        self.directiveInputSettingLayout.addWidget(self.folderToSaveTipLabel, 4, 3, 1, 1, Qt.AlignLeft)

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

        self.waitForElementAppearLabel = QLabel()
        self.waitForElementAppearLabel.setFont(__font)
        self.waitForElementAppearLabel.setText(u"等待元素存在(s):")
        self.seniorTabLayout.addWidget(self.waitForElementAppearLabel, 0, 0, 1, 1, Qt.AlignRight)
        self.waitForElementAppearLineEdit = QLineEdit()
        self.waitForElementAppearLineEdit.setFont(__font)
        self.waitForElementAppearLineEdit.setMinimumSize(600, 50)
        self.waitForElementAppearLineEdit.setText("20")
        self.seniorTabLayout.addWidget(self.waitForElementAppearLineEdit, 0, 1, 1, 1, Qt.AlignCenter)
        self.waitForElementAppearFunctionBtn = flowSettingDialog.addFunctionButton(
            self.waitForElementAppearLineEdit, self)
        self.seniorTabLayout.addWidget(self.waitForElementAppearFunctionBtn, 0, 1, 1, 1, Qt.AlignRight)
        self.waitForElementAppearTipLabel = flowSettingDialog.createTipLabel(u"等待元素存在(s)",
                                                                             u"  设置网页截图的超时时间")
        self.seniorTabLayout.addWidget(self.waitForElementAppearTipLabel, 0, 2, 1, 1, Qt.AlignLeft)

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2 - 80)

    def changeOpenWebPageObjectSettingDialogSize(self):
        if self.settingTabWidget.currentIndex() == 0:
            self.setFixedSize(self.screenWidth * 0.46, self.screenHeight * 0.5)
            self.center()
        elif self.settingTabWidget.currentIndex() == 1:
            self.setFixedSize(self.screenWidth * 0.47, self.screenHeight * 0.27)
            self.center()
        elif self.settingTabWidget.currentIndex() == 2:
            if self.handleErrorWayCombobox.currentIndex() == 0:
                self.setFixedSize(self.screenWidth * 0.44, self.screenHeight * 0.3)
            elif self.handleErrorWayCombobox.currentIndex() == 1:
                self.setFixedSize(self.screenWidth * 0.44, self.screenHeight * 0.42)
            else:
                self.setFixedSize(self.screenWidth * 0.44, self.screenHeight * 0.37)
            self.center()

    def selectFile(self):
        root = tk.Tk()
        root.withdraw()
        Filepath = filedialog.askopenfilename()
        self.filePathLineEdit.setText(Filepath)
        #根据需求实现执行指令的显示和点击事件
        #self.executionButton.setVisible(False)  #假如不需要显示就取消注释

    #实现确认和取消按钮点击事件
    def handleQuestionBtnClicked(self):
        print("点击获取信息按钮")

    def handleConfirmBtnClicked(self):
        print("点击确认按钮")

    def handleCancelBtnClicked(self):
        print("点击取消按钮")

    #def handleExecutionBtnClicked(self): 根据情况实现指令执行按钮事件
    #   print("点击执行按钮)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = UploadingFileObjectSettingDialog("下载文件",1,1)
    win.show()
    sys.exit(app.exec_())

