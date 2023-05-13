# -*- coding:utf-8 -*-
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from com.mat.rpa.views.workWindow.leftPanel.directiveTree import directiveTree
#本文件只是定义了按键的行为功能，但是按键上的文字等特征没有被设计，顾引用directiveTree

class LeftPanel(QFrame):
    picPath = "./com/mat/rpa/views/workWindow/images/"
    def __init__(self, parent=None):
        super(LeftPanel, self).__init__(parent)
        #设置布局
        self.parentPanel = parent
        self.entireLayout = QVBoxLayout()
        self.setLayout(self.entireLayout)
        self.entireLayout.setContentsMargins(0,0,0,0)
        self.entireLayout.setSpacing(0)
        #设置topPanel，安装一个label，一个展开/收起按钮
        self.topPanel = QWidget()
        self.entireLayout.addWidget(self.topPanel)
        self.topPanelLayout = QHBoxLayout()
        self.topPanel.setLayout(self.topPanelLayout)
        self.topPanelLayout.setContentsMargins(0,0,0,0)
        self.topPanelLayout.setSpacing(0)
        self.directiHintLabel = QLabel()
        self.directiHintLabel.setText("指令")
        self.topPanelLayout.addWidget(self.directiHintLabel)
        self.topPanelLayout.addStretch(1)
        self.expandBtn = QPushButton()
        self.expandBtn.clicked.connect(self.handleExpandingBtnClick)
        self.expandingTree = False
        self.expandBtn.setIcon(QIcon(QPixmap(LeftPanel.picPath+"foldup.png")))
        self.topPanelLayout.addWidget(self.expandBtn)
        #安装指令树
        self.directiveTree = directiveTree.DirectiveTree()
        self.entireLayout.addWidget(self.directiveTree)



    def handleExpandingBtnClick(self):
        if self.expandingTree: #假如现在树是展开的，就收起树，并改图片
            self.expandingTree = False
            self.expandBtn.setIcon(QIcon(QPixmap(LeftPanel.picPath + "foldup.png")))
            #收起树
        else:
            self.expandingTree = True
            self.expandBtn.setIcon(QIcon(QPixmap(LeftPanel.picPath + "folddown.png")))
            #打开树



if __name__ == '__main__':
    app = QApplication(sys.argv)
    fms = LeftPanel()
    fms.show()
    sys.exit(app.exec_())



