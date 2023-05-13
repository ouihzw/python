# -*- coding:utf-8 -*-
import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class LeftPanel(QFrame):
    def __init__(self, parent=None):
        super(LeftPanel, self).__init__(parent)
        self.parentPanel = parent
        #创建布局管理器
        self.entireLayout = QVBoxLayout()
        self.entireLayout.setContentsMargins(5,5,5,5)
        self.entireLayout.setSpacing(5)
        self.setLayout(self.entireLayout)
        #添加创建按钮
        self.creationBtn = QPushButton()
        self.creationBtn.setStyleSheet('''QPushButton {
        background-color: #ff525b;
        font: 24px bold;
        }''')
        self.creationBtnMenu = QMenu()
        self.creationBtn.setMenu(self.creationBtnMenu)
        self.creationBtn.setFixedHeight(41)
        self.entireLayout.addWidget(self.creationBtn)
        #添加菜单树
        # 设置菜单树各列宽度
        desktop = QApplication.desktop()
        # 得到屏幕可显示尺寸
        rect = desktop.availableGeometry()
        screenWidth = rect.width()
        self.menuTreeWidth = screenWidth * 0.18
        self.menuTree = QTreeWidget()
        #设置行高
        self.menuTree.setStyleSheet(" QTreeView::item {height: 30px;};")
        __font = QFont()
        __font.setPixelSize(20)
        self.menuTree.setFont(__font)
        self.menuTree.setColumnCount(2) #设置两列
        self.menuTree.setHeaderHidden(True)
        self.menuTree.setColumnWidth(0, self.menuTreeWidth * 0.75)
        self.menuTree.setColumnWidth(1, self.menuTreeWidth * 0.25)
        self.entireLayout.addWidget(self.menuTree, 9)

    def setCreateBtnText(self, text):
        self.creationBtn.setText(text)

    def addActionToMenu(self, subAction):
        self.creationBtnMenu.addAction(subAction)

    def addSeparatorToMenu(self):
        self.creationBtnMenu.addSeparator()

    def getTreeNodeAtFirstLevel(self):
        return QTreeWidgetItem(self.menuTree)





if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = LeftPanel()
    win.show()
    sys.exit(app.exec_())


