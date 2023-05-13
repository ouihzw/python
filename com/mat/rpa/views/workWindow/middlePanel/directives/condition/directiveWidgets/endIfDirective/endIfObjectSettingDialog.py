# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowSettingDialog
from com.mat.rpa.utils.sizeCalc import screenPercentage

class EndIfObjectSettingDialog(flowSettingDialog.BasicFlowSettingDialog):
    def __init__(self, title, parent=None):
        super().__init__(title, parent)
        w, h = screenPercentage(0.45, 0.4)
        self.setFixedWidth(w)
        __font = QFont()
        __font.setPixelSize(20)
        __font.setFamily("Courier")
        # 改变图片
        self.changeImage(flowSettingDialog.BasicFlowSettingDialog.picPath + "endIfBig.png")
        self.infoLabel.setText("条件判断结束标记")
        self.regularTabUI()

    def regularTabUI(self):
        __font = QFont()
        __font.setPixelSize(20)
        __font.setFamily("Courier")
        inputHLayout = QHBoxLayout(self.directiveInputSettingPanel)
        self.directiveInputSettingPanel.setLayout(inputHLayout)
        nothingInputLabel = QLabel(text="(当前指令不包含任何输入项)", font=__font)
        inputHLayout.addWidget(nothingInputLabel, 1, Qt.AlignCenter)
        inputHLayout.setContentsMargins(0, 15, 0, 10)
        outputHLayout = QHBoxLayout(self.directiveOutputSettingPanel)
        self.directiveOutputSettingPanel.setLayout(outputHLayout)
        nothingOutputLabel = QLabel(text="(当前指令不包含任何输出项)", font=__font)
        outputHLayout.addWidget(nothingOutputLabel, 1, Qt.AlignCenter)
        outputHLayout.setContentsMargins(0, 20, 0, 40)

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
