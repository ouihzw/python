# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from . import flowModuleTree

styleSheet = """
QPushButton {
    border-style: none;
    border-width: 0px;
    border-radius: 4px;
    height: 26px;
    width: 26px;
    margin: 1px 1px 3px 1px;
    qproperty-iconSize: 18px;
}
QPushButton:hover {
    background-color: #e0e0e0;
}
QPushButton:pressed {
    padding: 2px 0 0 1px;
    background-color: #d0d0d0;
}
QTreeWidget::item {
    height: 28px;
}
"""


class FlowModulePanel(QWidget):
    picPath = "./com/mat/rpa/views/workWindow/rightPanel/images/"
    def __init__(self, parent=None):
        super(FlowModulePanel, self).__init__(parent)
        #设置布局管理器
        self.entireLayout = QVBoxLayout()
        self.setLayout(self.entireLayout)
        self.entireLayout.setContentsMargins(0,0,0,0)
        self.entireLayout.setSpacing(0)
        #安装topPanel
        self.topPanel = QWidget()
        self.entireLayout.addWidget(self.topPanel, 0.5)
        self.topPanelLayout = QHBoxLayout()
        self.topPanel.setLayout(self.topPanelLayout)
        self.topPanelLayout.setContentsMargins(0,0,0,0)
        self.topPanelLayout.setSpacing(0)
        ##安装提示label
        self.hintLabel = QLabel()
        font = QFont()
        font.setFamily("Microsoft YaHei")
        self.hintLabel.setFont(font)
        self.hintLabel.setText("流程")
        self.topPanelLayout.addWidget(self.hintLabel)
        self.topPanelLayout.addStretch(1)
        ##安装StackedWidget
        self.stackedWidget = QStackedWidget()
        self.stackedWidget.setMaximumHeight(100)
        self.stackedWidget.setContentsMargins(0,0,0,0)
        self.topPanelLayout.addWidget(self.stackedWidget)
        ###安装按钮panel,并且都右对齐
        self.btnPanel = QWidget()
        self.btnPanelLayout = QHBoxLayout()
        self.btnPanel.setLayout(self.btnPanelLayout)
        self.btnPanelLayout.setContentsMargins(0,0,0,0)
        self.btnPanelLayout.setSpacing(0)
        self.btnPanelLayout.addStretch(1)
        self.addNewFlowBtn = QPushButton()
        self.addNewFlowBtn.setText("sousuo")
        self.btnPanelLayout.addWidget(self.addNewFlowBtn)
        self.addPythonModuleBtn = QPushButton()
        self.addPythonModuleBtn.setIcon(QIcon(QPixmap(FlowModulePanel.picPath+"newPython.png")))
        self.btnPanelLayout.addWidget(self.addPythonModuleBtn)
        self.searchBtn = QPushButton()
        self.searchBtn.setIcon(QIcon(QPixmap(FlowModulePanel.picPath + "search.png")))
        self.btnPanelLayout.addWidget(self.searchBtn)
        self.ellipsisBtn = QPushButton()
        self.ellipsisBtn.setIcon(QIcon(QPixmap(FlowModulePanel.picPath + "horizontalEllipsis.png")))
        self.ellipsisBtn.clicked.connect(self.showMenu)
        self.btnPanelLayout.addWidget(self.ellipsisBtn)
        self.folddingBtn = QPushButton()
        self.folddingBtn.setIcon(QIcon(QPixmap(FlowModulePanel.picPath + "doubleRightArrow.png")))
        # self.btnPanelLayout.addWidget(self.folddingBtn)
        self.stackedWidget.addWidget(self.btnPanel)
        self.stackedWidget.setCurrentIndex(0)
        #另一个搜索框面板
        self.searchBoxPanel = QWidget()
        self.searchBoxPanelLayout = QHBoxLayout()
        self.searchBoxPanel.setLayout(self.searchBoxPanelLayout)
        self.searchBoxPanelLayout.setContentsMargins(0,0,0,0)
        self.searchBoxPanelLayout.setSpacing(0)
        self.searchBox = QLineEdit()
        self.searchCloseBtn = QPushButton()
        self.searchCloseBtn.setIcon(QIcon(QPixmap(FlowModulePanel.picPath + "closeSearch.png")))
        self.searchBoxPanelLayout.addWidget(self.searchBox)
        self.searchBoxPanelLayout.addWidget(self.searchCloseBtn)
        self.stackedWidget.addWidget(self.searchBoxPanel)
        #添加流程树
        self.flowTree = flowModuleTree.FlowModuleTree(self)
        self.entireLayout.addWidget(self.flowTree,9.5)
        self.setStyleSheet(styleSheet)
        # 绑定信号，切换搜索框面板
        self.searchBtn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.searchCloseBtn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.addNewFlowBtn.clicked.connect(lambda: self.flowTree.openEditor(self.flowTree.addSubFlow()))

    def showMenu(self):
        menu = DetailMenu(self)
        sender = self.sender()
        pos = sender.mapToGlobal(QPoint(0, 0))
        menu.popup(QPoint(pos.x(), pos.y() + sender.height()))


menuStyleSheet = """
QMenu {
    background-color: #fff;
    padding: 2px;
    margin: 4px;
    font-size: 12px;
    border-radius: 5px;
    border-color: #aaa;
    border-width: 1px;
    border-style: solid;
}
QMenu::item {
    padding: 5px;
    margin: 1px;
    border-radius: 4px;
    min-width: 130px;
    color: #333;
}
QMenu::item:default {
    color: red;
}
QMenu::item:selected {
    background-color: #e0e0e0;
}
QMenu::icon {
    padding-left: 10px;
}
"""


class DetailMenu(QMenu):
    picPath = "./com/mat/rpa/views/workWindow/rightPanel/images/"

    def __init__(self, parent=None):
        try:
            super().__init__(parent)
            self.importFlow = QAction(QIcon(self.picPath + "import.png"), u"导入Flow文件", self)
            self.importFlow.setShortcut(Qt.ALT + Qt.Key_Enter)
            self.importFlow.triggered.connect(parent.flowTree.importSubFlow)
            self.setStyleSheet(menuStyleSheet)
            self.addActions([self.importFlow])
            # 透明背景
            self.setAttribute(Qt.WA_TranslucentBackground)
            # 无边框，去除阴影
            self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
            # 加阴影
            shadow = QGraphicsDropShadowEffect()
            shadow.setOffset(0, 0)
            shadow.setBlurRadius(6)
            shadow.setColor(QColor(70, 70, 70))
            self.setGraphicsEffect(shadow)
        except Exception as e:
            print(e)