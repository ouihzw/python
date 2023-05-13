# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowSettingDialog

class ProcessingUploadDialogObjectSettingDialog(flowSettingDialog.BasicFlowSettingDialog):
    def __init__(self, title, parent=None):
        super(ProcessingUploadDialogObjectSettingDialog, self).__init__(title, parent)
        #参照修改infolabel的提示信息
        self.setInfoLabelText("获取网址或标题匹配的已打开的网页，或者获取在当前浏览器中选中的网页")
        #下边按照需求布局指令输入控件、指令输出控件、高级和错误Tab

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

