# -*- coding:utf-8 -*-
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from com.mat.rpa.dao.workDao.directiveDao import DirectiveDao
from com.mat.rpa.utils import webAutoSave
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowSettingDialog

class GettingWebRequestResultObjectSettingDialog(flowSettingDialog.BasicFlowSettingDialog):
    def __init__(self, title, directive_id, id, parent=None):
        super().__init__(title, directive_id, id, parent)
        self.directiveDaoObj = DirectiveDao()
        self.webSave = webAutoSave.WebAutoSave()
        self.changeImage(flowSettingDialog.BasicFlowSettingDialog.picPath + "getRequestResult.png")
        self.screenWidth = 2520
        self.screenHeight = 830
        self.setFixedSize(self.screenWidth * 0.46, self.screenHeight * 0.75)
        self.center()
        #参照修改infolabel的提示信息
        self.setInfoLabelText("获取网址或标题匹配的已打开的网页，或者获取在当前浏览器中选中的网页")
        #下边按照需求布局指令输入控件、指令输出控件、高级和错误Tab

        #根据需求实现执行指令的显示和点击事件
        #self.executionButton.setVisible(False)  #假如不需要显示就取消注释
        self.regularTabUI()
        self.errorHandlingTabUI()


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
        self.webObjectCombobox.setMinimumSize(500, 50)
        self.webObjectCombobox.setItemDelegate(QStyledItemDelegate())
        self.webObjectCombobox.setStyleSheet(
            "QComboBox QAbstractItemView{selection-background-color: #f0f0f0;selection-color: #000;} QComboBox QAbstractItemView::item{min-height: 50px;}")
        self.directiveInputSettingLayout.addWidget(self.webObjectCombobox, 0, 1, 1, 1, Qt.AlignCenter)
        self.webObjectTipLabel = flowSettingDialog.createTipLabel(u"网页对象",
                                                                  u"  输入一个获取到的或者通过\"打开网\n  页\"创建的网页对象")
        self.directiveInputSettingLayout.addWidget(self.webObjectTipLabel, 0, 2, 1, 1, Qt.AlignLeft)

        self.directiveOutputSettingLayout = QHBoxLayout()
        self.directiveOutputSettingPanel.setLayout(self.directiveOutputSettingLayout)

        self.saveResultListLabel = QLabel("保存网页监听结果列表至：")
        self.saveResultListLabel.setFont(__font)
        self.directiveOutputSettingLayout.addWidget(self.saveResultListLabel)
        self.saveResultListLineEdit = QLineEdit()
        self.saveResultListLineEdit.setFont(__font)
        self.saveResultListLineEdit.setMinimumSize(500, 50)
        self.saveResultListLineEdit.setText("response_body_list")
        self.saveResultListLineEdit.setFixedWidth(550)
        self.directiveOutputSettingLayout.addWidget(self.saveResultListLineEdit)
        self.saveResultFunctionBtn = flowSettingDialog.addFunctionButton(self.saveResultListLineEdit, self)
        self.directiveOutputSettingLayout.addWidget(self.saveResultFunctionBtn)


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

    #def handleExecutionBtnClicked(self): 根据情况实现指令执行按钮事件
    #   print("点击执行按钮)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = GettingWebRequestResultObjectSettingDialog("test", 1, 1)
    win.show()
    app.exec_()