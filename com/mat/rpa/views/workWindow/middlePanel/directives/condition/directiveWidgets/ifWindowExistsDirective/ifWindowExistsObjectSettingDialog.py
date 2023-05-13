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
class IfWindowExistsObjectSettingDialog(flowSettingDialog.BasicFlowSettingDialog):
    isFirstInit = True
    normalHeight = 0
    def __init__(self, title, parent=None):
        super().__init__(title, parent)
        __font = QFont()
        __font.setPixelSize(20)
        __font.setFamily("Courier")
        # 改变图片
        self.changeImage(flowSettingDialog.BasicFlowSettingDialog.picPath + "ifContainBig.png")
        self.infoLabel.setText(u"检测指定窗口是否存在")
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
        getWindowMethodLabel = QLabel(text=u"获取窗口方式:", font=__font)
        self.directiveInputSettingLayout.addWidget(getWindowMethodLabel, 0, 0, 1, 1, Qt.AlignRight)
        self.getWindowMethodComboBox = QComboBox(font=__font)
        self.getWindowMethodComboBox.setMinimumSize(650, 50)
        self.getWindowMethodComboBox.setItemDelegate(QStyledItemDelegate())
        self.getWindowMethodComboBox.setStyleSheet(comboBoxStyleSheet)
        self.getWindowMethodComboBox.addItems([u"窗口对象", u"捕获窗口元素", u"窗口标题或类型名", u"窗口句柄"])
        self.directiveInputSettingLayout.addWidget(self.getWindowMethodComboBox, 0, 1, 1, 1, Qt.AlignCenter)
        getWindowMethodTipLabel = flowSettingDialog.createTipLabel(u"获取窗口方式", u"选择获取窗口的方式")
        self.directiveInputSettingLayout.addWidget(getWindowMethodTipLabel, 0, 2, 1, 1, Qt.AlignLeft)
        self.secondLabel = QLabel(text=u"窗口对象:", font=__font)
        self.directiveInputSettingLayout.addWidget(self.secondLabel, 1, 0, 1, 1, Qt.AlignRight)
        objectHLayout = QHBoxLayout()
        objectHLayout.setContentsMargins(0, 0, 0, 0)
        objectHLayout.setSpacing(10)
        self.directiveInputSettingLayout.addLayout(objectHLayout, 1, 1, 1, 1, Qt.AlignCenter)
        # 窗口对象
        self.windowObjectComboBox = QComboBox(font=__font)
        self.windowObjectComboBox.setMinimumSize(650, 50)
        objectHLayout.addWidget(self.windowObjectComboBox)
        # 捕获窗口元素
        self.elementLineEdit = QLineEdit(placeholderText=u"(未选择元素)", font=__font, readOnly=True)
        self.clearAction = QAction(icon=QIcon(flowSettingDialog.BasicFlowSettingDialog.picPath + "clear.png"))
        self.clearAction.triggered.connect(self.clearElement)
        self.elementLineEdit.addAction(self.clearAction, QLineEdit.TrailingPosition)
        self.elementLineEdit.setMinimumHeight(50)
        objectHLayout.addWidget(self.elementLineEdit, 11)
        self.elementBtn = QPushButton(text=u"去元素库选择", font=__font, clicked=self.openElementLib)
        self.elementBtn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        objectHLayout.addWidget(self.elementBtn, 3)
        self.elementLineEdit.hide()
        self.elementBtn.hide()
        # 窗口标题
        self.windowTitleComboBox = QComboBox(font=__font, editable=True)
        self.windowTitleComboBox.setMinimumSize(650, 50)
        objectHLayout.addWidget(self.windowTitleComboBox)
        self.windowTitleComboBox.hide()
        windowTitleCheckBoxVLayout = QVBoxLayout()
        windowTitleCheckBoxVLayout.setContentsMargins(0, 0, 0, 0)
        windowTitleCheckBoxVLayout.setSpacing(10)
        self.directiveInputSettingLayout.addLayout(windowTitleCheckBoxVLayout, 2, 1, 1, 1, Qt.AlignCenter)
        checkBoxHLayoutA = QHBoxLayout()
        checkBoxHLayoutA.setContentsMargins(0, 0, 0, 0)
        windowTitleCheckBoxVLayout.addLayout(checkBoxHLayoutA)
        self.addWindowType = QCheckBox(text=u"添加窗口类型", font=__font)
        self.addWindowType.setMinimumHeight(40)
        checkBoxHLayoutA.addWidget(self.addWindowType, alignment=Qt.AlignLeft)
        self.addWindowTypeTipLabel = flowSettingDialog.createTipLabel(u"添加窗口类型", u"添加窗口类型")
        checkBoxHLayoutA.addWidget(self.addWindowTypeTipLabel, alignment=Qt.AlignLeft)
        checkBoxHLayoutA.addStretch(1)
        self.addWindowType.hide()
        self.addWindowTypeTipLabel.hide()
        checkBoxHLayoutB = QHBoxLayout()
        checkBoxHLayoutB.setContentsMargins(0, 0, 0, 0)
        windowTitleCheckBoxVLayout.addLayout(checkBoxHLayoutB)
        self.wildCard = QCheckBox(text=u"根据通配符匹配", font=__font)
        self.wildCard.setMinimumHeight(40)
        checkBoxHLayoutB.addWidget(self.wildCard, alignment=Qt.AlignLeft)
        self.wildCardTipLabel = flowSettingDialog.createTipLabel(u"根据通配符匹配", u"根据通配符匹配，*代表任意\n多个字符，?代表单个字符")
        checkBoxHLayoutB.addWidget(self.wildCardTipLabel, alignment=Qt.AlignLeft)
        checkBoxHLayoutB.addStretch(1)
        self.wildCard.hide()
        self.wildCardTipLabel.hide()
        # 窗口句柄
        self.windowHandleLineEdit = QLineEdit(font=__font)
        self.windowHandleLineEdit.setMinimumSize(650, 50)
        objectHLayout.addWidget(self.windowHandleLineEdit)
        self.windowHandleLineEdit.hide()
        self.secondTipLabel = flowSettingDialog.createTipLabel(u"窗口对象", u"输入一个获取到的窗口对象")
        self.directiveInputSettingLayout.addWidget(self.secondTipLabel, 1, 2, 1, 1, Qt.AlignLeft)
        existLabel = QLabel(text=u"窗口是否:", font=__font)
        self.directiveInputSettingLayout.addWidget(existLabel, 3, 0, 1, 1, Qt.AlignRight)
        self.existComboBox = QComboBox(font=__font)
        self.existComboBox.setMinimumSize(650, 50)
        self.existComboBox.setItemDelegate(QStyledItemDelegate())
        self.existComboBox.setStyleSheet(comboBoxStyleSheet)
        self.existComboBox.addItems([u"存在", u"不存在"])
        self.directiveInputSettingLayout.addWidget(self.existComboBox, 3, 1, 1, 1, Qt.AlignCenter)
        existTipLabel = flowSettingDialog.createTipLabel(u"窗口是否", u"选择需要判断的窗口存在或不存在")
        self.directiveInputSettingLayout.addWidget(existTipLabel, 3, 2, 1, 1, Qt.AlignLeft)
        self.directiveInputSettingLayout.setColumnStretch(0, 10)  # 第一列占10/100
        self.directiveInputSettingLayout.setColumnStretch(1, 80)  # 第二列占80/100
        self.directiveInputSettingLayout.setColumnStretch(2, 10)  # 第三列占10/100
        hLayout = QHBoxLayout(self.directiveOutputSettingPanel)
        self.directiveOutputSettingPanel.setLayout(hLayout)
        nothingLabel = QLabel(text=u"(当前指令不包含任何输出项)", font=__font)
        hLayout.addWidget(nothingLabel, 1, Qt.AlignCenter)
        hLayout.setContentsMargins(0, 10, 0, 30)
        self.getWindowMethodComboBox.currentIndexChanged.connect(self.changeMode)

    def showEvent(self, a0: QShowEvent) -> None:
        super().showEvent(a0)
        if self.isFirstInit:
            self.isFirstInit = False
            self.normalHeight = self.height()
            self.setFixedSize(self.width(), self.normalHeight)

    def changeMode(self, idx: int):
        # 设置隐藏
        self.windowObjectComboBox.hide()
        self.elementLineEdit.hide()
        self.elementBtn.hide()
        self.windowTitleComboBox.hide()
        self.addWindowType.hide()
        self.addWindowTypeTipLabel.hide()
        self.wildCard.hide()
        self.wildCardTipLabel.hide()
        self.windowHandleLineEdit.hide()
        # 窗口对象
        if idx == 0:
            # 设置文本
            self.secondLabel.setText(u"窗口对象:")
            self.secondTipLabel.tipLabelQuestionBtn.setText(u"窗口对象")
            self.secondTipLabel.tipLabelText.setText(u"输入一个获取到的窗口对象")
            # 设置显示
            self.windowObjectComboBox.show()
        # 窗口元素
        elif idx == 1:
            # 设置文本
            self.secondLabel.setText(u"操作目标:")
            self.secondTipLabel.tipLabelQuestionBtn.setText(u"操作目标")
            self.secondTipLabel.tipLabelText.setText(u"从元素库中选择一个录制好的\n窗口元素")
            # 设置显示
            self.elementLineEdit.show()
            self.elementBtn.show()
        # 窗口标题
        elif idx == 2:
            # 设置文本
            self.secondLabel.setText(u"窗口标题:")
            self.secondTipLabel.tipLabelQuestionBtn.setText(u"窗口标题")
            self.secondTipLabel.tipLabelText.setText(u"选择或输入窗口标题")
            # 设置显示
            self.windowTitleComboBox.show()
            self.addWindowType.show()
            self.addWindowTypeTipLabel.show()
            self.wildCard.show()
            self.wildCardTipLabel.show()
        # 窗口句柄
        else:
            # 设置文本
            self.secondLabel.setText(u"窗口实例句柄:")
            self.secondTipLabel.tipLabelQuestionBtn.setText(u"窗口实例句柄")
            self.secondTipLabel.tipLabelText.setText(u"输入已知的窗口句柄")
            # 设置显示
            self.windowHandleLineEdit.show()
        # 设置窗口高度
        if idx == 2:
            self.setFixedHeight(self.normalHeight + 140)
        else:
            self.setFixedHeight(self.normalHeight)

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
