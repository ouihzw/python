# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowSettingDialog
from com.mat.rpa.utils.sizeCalc import screenPercentage
comboBoxStyleSheet = """
QComboBox QAbstractItemView {
    selection-background-color: #f0f0f0;
    selection-color: #000;
}
QComboBox QAbstractItemView::item {
    min-height: 50px;
}
"""
class ElseIfObjectSettingDialog(flowSettingDialog.BasicFlowSettingDialog):

    def __init__(self, title, parent=None):
        super().__init__(title, parent)
        __font = QFont()
        __font.setPixelSize(20)
        __font.setFamily("Courier")
        # 改变图片
        self.changeImage(flowSettingDialog.BasicFlowSettingDialog.picPath + "elseIfBig.png")
        self.infoLabel.setText("条件分支判断")
        self.regularTabUI()

    def regularTabUI(self):
        __font = QFont()
        __font.setPixelSize(20)
        __font.setFamily("Courier")
        self.directiveInputSettingLayout = QGridLayout()
        self.directiveInputSettingLayout.setContentsMargins(20, 0, 20, 0)
        self.directiveInputSettingLayout.setSpacing(10)
        self.directiveInputSettingLayout.setVerticalSpacing(30)
        self.directiveInputSettingPanel.setLayout(self.directiveInputSettingLayout)
        objectOneLabel = QLabel(text="对象1:", font=__font)
        self.directiveInputSettingLayout.addWidget(objectOneLabel, 0,0,1,1, Qt.AlignRight)
        self.objectOneComboBox = QComboBox(font=__font, editable=True)
        self.objectOneComboBox.setMinimumSize(650, 50)
        self.objectOneComboBox.setItemDelegate(QStyledItemDelegate())
        self.objectOneComboBox.setStyleSheet(comboBoxStyleSheet)
        self.directiveInputSettingLayout.addWidget(self.objectOneComboBox, 0,1,1,1, Qt.AlignCenter)
        objectOneTipLabel = flowSettingDialog.createTipLabel("对象1", "输入前面指令创建的变量、文本\n或数字，与对象2进行比较")
        self.directiveInputSettingLayout.addWidget(objectOneTipLabel, 0,2,1,1, Qt.AlignLeft)
        relationLabel = QLabel(text="关系:", font=__font)
        self.directiveInputSettingLayout.addWidget(relationLabel, 1,0,1,1, Qt.AlignRight)
        self.relationComboBox = QComboBox(font=__font)
        self.relationComboBox.setMinimumSize(650, 50)
        self.relationComboBox.setItemDelegate(QStyledItemDelegate())
        self.relationComboBox.setStyleSheet(comboBoxStyleSheet)
        self.relationComboBox.addItems(["等于", "不等于", "大于", "大于等于", "小于", "小于等于", "包含", "不包含",
                                        "等于True", "等于False", "等于None", "不等于None", "是空字符串",
                                        "不是空字符串", "以对象2开头", "不以对象2开头", "以对象2结束", "不以对象2结束"])
        self.directiveInputSettingLayout.addWidget(self.relationComboBox, 1,1,1,1, Qt.AlignCenter)
        relationTipLabel = flowSettingDialog.createTipLabel("关系", "选择对象1和对象2的比较方式")
        self.directiveInputSettingLayout.addWidget(relationTipLabel, 1,2,1,1, Qt.AlignLeft)
        objectTwoLabel = QLabel(text="对象2:", font=__font)
        self.directiveInputSettingLayout.addWidget(objectTwoLabel, 2,0,1,1, Qt.AlignRight)
        self.objectTwoComboBox = QComboBox(font=__font, editable=True)
        self.objectTwoComboBox.setMinimumSize(650, 50)
        self.objectTwoComboBox.setItemDelegate(QStyledItemDelegate())
        self.objectTwoComboBox.setStyleSheet(comboBoxStyleSheet)
        self.directiveInputSettingLayout.addWidget(self.objectTwoComboBox, 2,1,1,1, Qt.AlignCenter)
        objectTwoTipLabel = flowSettingDialog.createTipLabel("对象2", "输入前面指令创建的变量、文本\n或数字，与对象1进行比较")
        self.directiveInputSettingLayout.addWidget(objectTwoTipLabel, 2,2,1,1, Qt.AlignLeft)

        hLayout = QHBoxLayout(self.directiveOutputSettingPanel)
        self.directiveOutputSettingPanel.setLayout(hLayout)
        nothingLabel = QLabel(text="(当前指令不包含任何输出项)", font=__font)
        hLayout.addWidget(nothingLabel, 1, Qt.AlignCenter)
        hLayout.setContentsMargins(0,10,0,30)

    def showEvent(self, a0: QShowEvent) -> None:
        super().showEvent(a0)
        self.setFixedSize(self.width(), self.height())

    #实现确认和取消按钮点击事件D
    def handleQuestionBtnClicked(self):
        print("点击执行命令按钮")

    def handleConfirmBtnClicked(self):
        print("点击确定按钮")
        self.accept()

    def handleCancelBtnClicked(self):
        print("点击取消按钮")
        self.reject()
