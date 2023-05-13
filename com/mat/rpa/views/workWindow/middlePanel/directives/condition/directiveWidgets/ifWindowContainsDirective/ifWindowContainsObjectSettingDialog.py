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
class IfWindowContainsObjectSettingDialog(flowSettingDialog.BasicFlowSettingDialog):

    def __init__(self, title, parent=None):
        super().__init__(title, parent)
        __font = QFont()
        __font.setPixelSize(20)
        __font.setFamily("Courier")
        # 改变图片
        self.changeImage(flowSettingDialog.BasicFlowSettingDialog.picPath + "ifContainBig.png")
        self.infoLabel.setText(u"检测指定的元素是否包含在指定窗口中")
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
        windowObjectLabel = QLabel(text=u"窗口对象:", font=__font)
        self.directiveInputSettingLayout.addWidget(windowObjectLabel, 0,0,1,1, Qt.AlignRight)
        self.windowObjectComboBox = QComboBox(font=__font)
        self.windowObjectComboBox.setMinimumSize(650, 50)
        self.windowObjectComboBox.setItemDelegate(QStyledItemDelegate())
        self.windowObjectComboBox.setStyleSheet(comboBoxStyleSheet)
        self.windowObjectComboBox.addItem(u"根据操作目标自动匹配")
        self.directiveInputSettingLayout.addWidget(self.windowObjectComboBox, 0, 1, 1, 1, Qt.AlignCenter)
        windowObjectTipLabel = flowSettingDialog.createTipLabel(u"窗口对象", u"选择一个窗口对象")
        self.directiveInputSettingLayout.addWidget(windowObjectTipLabel, 0,2,1,1, Qt.AlignLeft)
        detectLabel = QLabel(text=u"检测窗口是否:", font=__font)
        self.directiveInputSettingLayout.addWidget(detectLabel, 1,0,1,1, Qt.AlignRight)
        self.detectComboBox = QComboBox(font=__font)
        self.detectComboBox.setMinimumSize(650, 50)
        self.detectComboBox.setItemDelegate(QStyledItemDelegate())
        self.detectComboBox.setStyleSheet(comboBoxStyleSheet)
        self.detectComboBox.addItems([u"包含元素", u"不包含元素"])
        self.directiveInputSettingLayout.addWidget(self.detectComboBox, 1, 1, 1, 1, Qt.AlignCenter)
        detectTipLabel = flowSettingDialog.createTipLabel(u"检测窗口是否", u"检测窗口是否存在某个元素")
        self.directiveInputSettingLayout.addWidget(detectTipLabel, 1,2,1,1, Qt.AlignLeft)
        elementLabel = QLabel(text=u"操作目标:", font=__font)
        self.directiveInputSettingLayout.addWidget(elementLabel, 2, 0, 1, 1, Qt.AlignRight)
        self.elementLayout = QHBoxLayout()
        self.elementLayout.setSpacing(10)
        self.elementLayout.setContentsMargins(0, 0, 0, 0)
        self.elementLineEdit = QLineEdit(text=u"(未选择元素)", font=__font, readOnly=True)
        self.clearAction = QAction(icon=QIcon(flowSettingDialog.BasicFlowSettingDialog.picPath + "clear.png"))
        self.clearAction.triggered.connect(self.clearElement)
        self.elementLineEdit.addAction(self.clearAction, QLineEdit.TrailingPosition)
        self.elementLineEdit.setMinimumHeight(50)
        self.elementLayout.addWidget(self.elementLineEdit, 11)
        self.elementBtn = QPushButton(text=u"去元素库选择", font=__font, clicked=self.openElementLib)
        self.elementBtn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.elementLayout.addWidget(self.elementBtn, 3)
        self.textArea = QPlainTextEdit(font=__font)
        self.elementLayout.addWidget(self.textArea)
        self.textArea.hide()
        self.directiveInputSettingLayout.addLayout(self.elementLayout, 2, 1, 1, 1, Qt.AlignCenter)
        elementTipLabel = flowSettingDialog.createTipLabel(u"操作目标", u"选择要操作的桌面软件元素")
        self.directiveInputSettingLayout.addWidget(elementTipLabel, 2,2,1,1, Qt.AlignLeft)

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

    def openElementLib(self):
        pass

    # 清除元素
    def clearElement(self):
        self.elementLineEdit.setText("")

    #实现确认和取消按钮点击事件
    def handleQuestionBtnClicked(self):
        print("点击执行命令按钮")

    def handleConfirmBtnClicked(self):
        print("点击确定按钮")
        self.accept()

    def handleCancelBtnClicked(self):
        print("点击取消按钮")
        self.reject()
