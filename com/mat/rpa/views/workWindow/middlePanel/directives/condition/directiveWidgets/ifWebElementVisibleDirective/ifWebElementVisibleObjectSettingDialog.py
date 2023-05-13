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
class IfWebElementVisibleObjectSettingDialog(flowSettingDialog.BasicFlowSettingDialog):

    def __init__(self, title, parent=None):
        super().__init__(title, parent)
        __font = QFont()
        __font.setPixelSize(20)
        __font.setFamily("Courier")
        # 改变图片
        self.changeImage(flowSettingDialog.BasicFlowSettingDialog.picPath + "ifContainBig.png")
        self.infoLabel.setText(u"检测指定的元素在网页中是否可见")
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
        webPageObjectLabel = QLabel(text=u"网页对象:", font=__font)
        self.directiveInputSettingLayout.addWidget(webPageObjectLabel, 0,0,1,1, Qt.AlignRight)
        self.webPageObjectComboBox = QComboBox(font=__font)
        self.webPageObjectComboBox.setMinimumSize(650, 50)
        self.webPageObjectComboBox.setItemDelegate(QStyledItemDelegate())
        self.webPageObjectComboBox.setStyleSheet(comboBoxStyleSheet)
        self.directiveInputSettingLayout.addWidget(self.webPageObjectComboBox, 0, 1, 1, 1, Qt.AlignCenter)
        webPageObjectTipLabel = flowSettingDialog.createTipLabel(u"网页对象", u"输入一个获取到的或者通过“打开\n网页”创建的对象")
        self.directiveInputSettingLayout.addWidget(webPageObjectTipLabel, 0,2,1,1, Qt.AlignLeft)
        detectLabel = QLabel(text=u"检测网页是否:", font=__font)
        self.directiveInputSettingLayout.addWidget(detectLabel, 1,0,1,1, Qt.AlignRight)
        self.detectComboBox = QComboBox(font=__font)
        self.detectComboBox.setMinimumSize(650, 50)
        self.detectComboBox.setItemDelegate(QStyledItemDelegate())
        self.detectComboBox.setStyleSheet(comboBoxStyleSheet)
        self.detectComboBox.addItems([u"可见", u"不可见"])
        self.directiveInputSettingLayout.addWidget(self.detectComboBox, 1, 1, 1, 1, Qt.AlignCenter)
        detectTipLabel = flowSettingDialog.createTipLabel(u"检测网页是否", u"指定你想要检测的内容类型，检测\n元素可见或不可见")
        self.directiveInputSettingLayout.addWidget(detectTipLabel, 1,2,1,1, Qt.AlignLeft)
        self.thirdLabel = QLabel(text=u"操作目标:", font=__font)
        self.directiveInputSettingLayout.addWidget(self.thirdLabel, 2,0,1,1, Qt.AlignRight)
        self.targetLayout = QHBoxLayout()
        self.targetLayout.setSpacing(10)
        self.targetLayout.setContentsMargins(0, 0, 0, 0)
        self.elementLineEdit = QLineEdit(placeholderText=u"(未选择元素)", font=__font, readOnly=True)
        self.clearAction = QAction(icon=QIcon(flowSettingDialog.BasicFlowSettingDialog.picPath + "clear.png"))
        self.clearAction.triggered.connect(self.clearElement)
        self.elementLineEdit.addAction(self.clearAction, QLineEdit.TrailingPosition)
        self.elementLineEdit.setMinimumHeight(50)
        self.targetLayout.addWidget(self.elementLineEdit, 11)
        self.elementBtn = QPushButton(text=u"去元素库选择", font=__font, clicked=self.openElementLib)
        self.elementBtn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.targetLayout.addWidget(self.elementBtn, 3)
        self.directiveInputSettingLayout.addLayout(self.targetLayout, 2, 1, 1, 1, Qt.AlignCenter)
        targetTipLabel = flowSettingDialog.createTipLabel(u"操作目标", u"选择要操作的网页元素")
        self.directiveInputSettingLayout.addWidget(targetTipLabel, 2,2,1,1, Qt.AlignLeft)

        self.directiveInputSettingLayout.setColumnStretch(0, 10) #第一列占10/100
        self.directiveInputSettingLayout.setColumnStretch(1, 80)  # 第二列占80/100
        self.directiveInputSettingLayout.setColumnStretch(2, 10)  # 第三列占10/100

        hLayout = QHBoxLayout(self.directiveOutputSettingPanel)
        self.directiveOutputSettingPanel.setLayout(hLayout)
        nothingLabel = QLabel(text=u"(当前指令不包含任何输出项)", font=__font)
        hLayout.addWidget(nothingLabel, 1, Qt.AlignCenter)
        hLayout.setContentsMargins(0,10,0,30)

    def showEvent(self, a0: QShowEvent) -> None:
        super().showEvent(a0)
        self.setFixedSize(self.width(), self.height())

    # 打开元素库
    def openElementLib(self):
        pass

    # 清除元素
    def clearElement(self):
        self.elementLineEdit.setText("")

    # 实现确认和取消按钮点击事件
    def handleQuestionBtnClicked(self):
        print("点击执行命令按钮")

    def handleConfirmBtnClicked(self):
        print("点击确定按钮")
        self.accept()

    def handleCancelBtnClicked(self):
        print("点击取消按钮")
        self.reject()
