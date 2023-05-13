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
class IfFileExistsObjectSettingDialog(flowSettingDialog.BasicFlowSettingDialog):

    def __init__(self, title, parent=None):
        super().__init__(title, parent)
        __font = QFont()
        __font.setPixelSize(20)
        __font.setFamily("Courier")
        # 改变图片
        self.changeImage(flowSettingDialog.BasicFlowSettingDialog.picPath + "ifFileExistsBig.png")
        self.infoLabel.setText(u"判断文件是否存在")
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
        filePathLabel = QLabel(text=u"文件路径:", font=__font)
        self.directiveInputSettingLayout.addWidget(filePathLabel, 0,0,1,1, Qt.AlignRight)
        # 文件路径输入框和选择文件按钮的水平布局
        filePathHLayout = QHBoxLayout()
        filePathHLayout.setContentsMargins(0, 0, 0, 0)
        filePathHLayout.setSpacing(0)
        self.filePathLineEdit = QLineEdit(font=__font)
        self.filePathLineEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.filePathLineEdit.setMinimumHeight(50)
        filePathHLayout.addWidget(self.filePathLineEdit)
        self.selectFileBtn = QPushButton(text=u"选择文件...", font=__font, clicked=self.selectFile)
        self.selectFileBtn.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        filePathHLayout.addWidget(self.selectFileBtn)
        self.directiveInputSettingLayout.addLayout(filePathHLayout, 0,1,1,1, Qt.AlignCenter)
        filePathTipLabel = flowSettingDialog.createTipLabel(u"文件路径", u"输入或选择文件路径")
        self.directiveInputSettingLayout.addWidget(filePathTipLabel, 0,2,1,1, Qt.AlignLeft)
        fileExistsLabel = QLabel(text=u"文件是否:", font=__font)
        self.directiveInputSettingLayout.addWidget(fileExistsLabel, 1,0,1,1, Qt.AlignRight)
        self.fileExistsComboBox = QComboBox(font=__font, minimumSize=QSize(650,50))
        self.fileExistsComboBox.setItemDelegate(QStyledItemDelegate())
        self.fileExistsComboBox.setStyleSheet(comboBoxStyleSheet)
        self.fileExistsComboBox.addItems([u"存在", u"不存在"])
        self.directiveInputSettingLayout.addWidget(self.fileExistsComboBox, 1, 1, 1, 1, Qt.AlignCenter)
        fileExistsTipLabel = flowSettingDialog.createTipLabel(u"文件是否", u"选择预期的文件是否存在")
        self.directiveInputSettingLayout.addWidget(fileExistsTipLabel, 1,2,1,1, Qt.AlignLeft)
        # 指令输出
        hLayout = QHBoxLayout(self.directiveOutputSettingPanel)
        self.directiveOutputSettingPanel.setLayout(hLayout)
        nothingLabel = QLabel(text=u"(当前指令不包含任何输出项)", font=__font)
        hLayout.addWidget(nothingLabel, 1, Qt.AlignCenter)
        hLayout.setContentsMargins(0,30,0,50)

    # 选择文件
    def selectFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, u"选择文件", "", u"所有文件(*)")
        self.filePathLineEdit.setText(fileName)

    def showEvent(self, a0: QShowEvent) -> None:
        super().showEvent(a0)
        self.setFixedSize(self.width(), self.height())

    #实现确认和取消按钮点击事件
    def handleQuestionBtnClicked(self):
        print("点击执行命令按钮")

    def handleConfirmBtnClicked(self):
        print("点击确定按钮")
        self.accept()

    def handleCancelBtnClicked(self):
        print("点击取消按钮")
        self.reject()
