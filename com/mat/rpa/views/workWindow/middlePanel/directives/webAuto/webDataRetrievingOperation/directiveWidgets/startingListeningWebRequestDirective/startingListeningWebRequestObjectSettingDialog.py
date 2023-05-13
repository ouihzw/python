# -*- coding:utf-8 -*-
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from com.mat.rpa.dao.workDao.directiveDao import DirectiveDao
from com.mat.rpa.utils.webAutoSave import WebAutoSave
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowSettingDialog

class StartingListeningWebRequestObjectSettingDialog(flowSettingDialog.BasicFlowSettingDialog):
    def __init__(self, title, directive_id, id, parent=None):
        super().__init__(title, directive_id, id, parent)
        self.directiveDaoObj = DirectiveDao()
        self.webSave = WebAutoSave()
        self.changeImage(flowSettingDialog.BasicFlowSettingDialog.picPath + "startListen.png")
        #参照修改infolabel的提示信息
        self.setInfoLabelText("获取网址或标题匹配的已打开的网页，或者获取在当前浏览器中选中的网页")
        #下边按照需求布局指令输入控件、指令输出控件、高级和错误Tab
        self.screenWidth = 1920
        self.screenHeight = 1030
        self.setFixedSize(self.screenWidth * 0.46, self.screenHeight * 0.75)
        self.center()
        self.regularTabUI()
        self.errorHandlingTabUI()


    def regularTabUI(self):
        __font = QFont()
        __font.setPixelSize(20)
        __font.setFamily("Courier")

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

        self.sourceUrlPathLabel = QLabel("资源路径Url：")
        self.sourceUrlPathLabel.setFont(__font)
        self.directiveInputSettingLayout.addWidget(self.sourceUrlPathLabel, 1, 0, 1, 1, Qt.AlignRight)
        self.sourceUrlPathLineEdit = QLineEdit()
        self.sourceUrlPathLineEdit.setFont(__font)
        self.sourceUrlPathLineEdit.setMinimumSize(600, 50)
        self.directiveInputSettingLayout.addWidget(self.sourceUrlPathLineEdit, 1, 1, 1, 1, Qt.AlignCenter)
        self.sourceUrlFunctionBtn = flowSettingDialog.addFunctionButton(self.sourceUrlPathLineEdit, self)
        self.directiveInputSettingLayout.addWidget(self.sourceUrlFunctionBtn, 1, 1, 1, 1, Qt.AlignRight)
        self.sourceUrlTipLabel = flowSettingDialog.createTipLabel(u"资源路径Url",
                                                                  u"根据输入的资源Url，筛选网页监听结果\n（值为空则忽略该筛选条件）"
                                                                  )
        self.directiveInputSettingLayout.addWidget(self.sourceUrlTipLabel, 1, 2, 1, 1, Qt.AlignLeft)

        self.regexCheckBox = QCheckBox("根据通配符匹配")
        self.directiveInputSettingLayout.addWidget(self.regexCheckBox, 2, 1, 1, 1, Qt.AlignLeft)

        self.sourceTypeLabel = QLabel("筛选资源类型：")
        self.sourceTypeLabel.setFont(__font)
        self.directiveInputSettingLayout.addWidget(self.sourceTypeLabel, 3, 0, 1, 1, Qt.AlignRight)
        self.sourceTypeComboBox = QComboBox()
        self.sourceTypeComboBox.setFont(__font)
        self.sourceTypeComboBox.setMinimumSize(600, 50)
        self.sourceTypeComboBox.addItems(["全部", "Fetch/XHR", "JS", "CSS", "图片", "媒体", "字体", "文档", "WebSocket", "其他"])
        self.sourceTypeComboBox.setItemDelegate(QStyledItemDelegate())
        self.sourceTypeComboBox.setStyleSheet(
            "QComboBox QAbstractItemView{selection-background-color: #f0f0f0;selection-color: #000;} QComboBox QAbstractItemView::item{min-height: 50px;}")
        self.directiveInputSettingLayout.addWidget(self.sourceTypeComboBox, 3, 1, 1, 1, Qt.AlignCenter)


    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2 - 80)



    #实现确认和取消按钮点击事件
    def handleQuestionBtnClicked(self):
        print("点击获取信息按钮")

    def handleConfirmBtnClicked(self):
        self.accept()

    def handleCancelBtnClicked(self):
        self.reject()

    def executeStep(self):
        pass

    #def handleExecutionBtnClicked(self): 根据情况实现指令执行按钮事件
    #   print("点击执行按钮)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = StartingListeningWebRequestObjectSettingDialog("test", 1, 1)
    win.show()
    app.exec_()