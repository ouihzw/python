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
class IfFolderExistsObjectSettingDialog(flowSettingDialog.BasicFlowSettingDialog):

    def __init__(self, title, parent=None):
        super().__init__(title, parent)
        __font = QFont()
        __font.setPixelSize(20)
        __font.setFamily("Courier")
        # 改变图片
        self.changeImage(flowSettingDialog.BasicFlowSettingDialog.picPath + "ifFolderExistsBig.png")
        self.infoLabel.setText(u"判断文件夹是否存在")
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
        folderPathLabel = QLabel(text=u"文件夹路径:", font=__font)
        self.directiveInputSettingLayout.addWidget(folderPathLabel, 0,0,1,1, Qt.AlignRight)
        # 文件夹路径输入框和预览文件夹按钮的水平布局
        folderPathHLayout = QHBoxLayout()
        folderPathHLayout.setContentsMargins(0, 0, 0, 0)
        folderPathHLayout.setSpacing(0)
        self.folderPathLineEdit = QLineEdit(font=__font)
        self.folderPathLineEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.folderPathLineEdit.setMinimumHeight(50)
        folderPathHLayout.addWidget(self.folderPathLineEdit)
        self.selectFolderBtn = QPushButton(text=u"预览...", font=__font, clicked=self.selectFolder)
        self.selectFolderBtn.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        folderPathHLayout.addWidget(self.selectFolderBtn)
        self.directiveInputSettingLayout.addLayout(folderPathHLayout, 0,1,1,1, Qt.AlignCenter)
        folderPathTipLabel = flowSettingDialog.createTipLabel(u"文件夹路径", u"输入或选择文件夹路径")
        self.directiveInputSettingLayout.addWidget(folderPathTipLabel, 0,2,1,1, Qt.AlignLeft)
        folderExistsLabel = QLabel(text=u"文件夹是否:", font=__font)
        self.directiveInputSettingLayout.addWidget(folderExistsLabel, 1,0,1,1, Qt.AlignRight)
        self.folderExistsComboBox = QComboBox(font=__font, minimumSize=QSize(650, 50))
        self.folderExistsComboBox.setItemDelegate(QStyledItemDelegate())
        self.folderExistsComboBox.setStyleSheet(comboBoxStyleSheet)
        self.folderExistsComboBox.addItems([u"存在", u"不存在"])
        self.directiveInputSettingLayout.addWidget(self.folderExistsComboBox, 1, 1, 1, 1, Qt.AlignCenter)
        folderExistsTipLabel = flowSettingDialog.createTipLabel(u"文件夹是否", u"选择预期的文件夹是否存在")
        self.directiveInputSettingLayout.addWidget(folderExistsTipLabel, 1,2,1,1, Qt.AlignLeft)
        # 指令输出
        hLayout = QHBoxLayout(self.directiveOutputSettingPanel)
        self.directiveOutputSettingPanel.setLayout(hLayout)
        nothingLabel = QLabel(text=u"(当前指令不包含任何输出项)", font=__font)
        hLayout.addWidget(nothingLabel, 1, Qt.AlignCenter)
        hLayout.setContentsMargins(0,30,0,50)

    # 选择文件
    def selectFolder(self):
        directory = QFileDialog.getExistingDirectory(self, u"选择文件夹", "")
        self.folderPathLineEdit.setText(directory)

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
