# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys


styleSheet = """
QPushButton {
    border-width: 0;
    border-style: none;
    border-radius: 4px;
    height: 34px;
    width: 65px;
    font-size: 13px;
    color: #333;
}
QPushButton:hover {
    background-color: #e0e0e0;
}
QPushButton:pressed {
    background-color: #d0d0d0;
}
QPushButton:icon {
    padding-right: 5px;
}
#searchBtn {
    width: 32px;
}
"""


class TopBtnPanel(QWidget):
    # picPath = "./images/"
    picPath = "./com/mat/rpa/views/projectWindow/mainWindow/mainPanel/btnAndTablePanel/images/"
    def __init__(self, parent=None):
        super(TopBtnPanel, self).__init__(parent)
        self.parentPanel = parent
        self.topPanelLayout = QHBoxLayout()
        font = QFont()
        font.setFamily("Microsoft YaHei")
        self.setFont(font)
        self.setLayout(self.topPanelLayout)
        self.runAppBtn = QPushButton()
        self.runAppBtn.setIcon(QIcon(QPixmap(TopBtnPanel.picPath + "runBtn.png")))
        self.runAppBtn.setText(" 运行")
        self.runAppBtn.clicked.connect(self.handleRunAppBtnClicked)
        self.topPanelLayout.addWidget(self.runAppBtn)
        self.editAppBtn = QPushButton()
        self.editAppBtn.setIcon(QIcon(QPixmap(TopBtnPanel.picPath + "editBtn.png")))
        self.editAppBtn.setText(" 编辑")
        self.topPanelLayout.addWidget(self.editAppBtn)
        self.exportAppBtn = QPushButton()
        self.exportAppBtn.setIcon(QIcon(QPixmap(TopBtnPanel.picPath + "exportBtn.png")))
        self.exportAppBtn.setText(" 导出")
        self.topPanelLayout.addWidget(self.exportAppBtn)
        self.importAppBtn = QPushButton()
        self.importAppBtn.setIcon(QIcon(QPixmap(TopBtnPanel.picPath + "importBtn.png")))
        self.importAppBtn.setText(" 导入")
        self.topPanelLayout.addWidget(self.importAppBtn)
        self.publishAppBtn = QPushButton()
        self.publishAppBtn.setIcon(QIcon(QPixmap(TopBtnPanel.picPath + "publishBtn.png")))
        self.publishAppBtn.setText(" 发布")
        self.topPanelLayout.addWidget(self.publishAppBtn)
        self.topPanelLayout.addStretch(1)
        self.searchPanel = QFrame()
        self.searchPanelLayout = QHBoxLayout()
        self.searchPanel.setLayout(self.searchPanelLayout)
        self.searchPanelLayout.setContentsMargins(0, 0, 0, 0)
        self.searchPanelLayout.setSpacing(0)
        self.searchBox = QLineEdit()
        self.searchBox.setFixedHeight(33)
        self.searchBox.setMinimumWidth(260)
        self.searchBox.setPlaceholderText("查询应用名称")
        # self.searchBox.setStyleSheet("QLineEdit {border:None;}")
        self.searchPanelLayout.addWidget(self.searchBox)
        self.searchBtn = QPushButton()
        self.searchBtn.setObjectName("searchBtn")
        self.searchBtn.setIcon(QIcon(QPixmap(TopBtnPanel.picPath + "searchBtn.png")))
        self.searchPanelLayout.addWidget(self.searchBtn)
        self.topPanelLayout.addWidget(self.searchPanel)
        self.setStyleSheet(styleSheet)

    def handleRunAppBtnClicked(self):
        print("运行应用")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = TopBtnPanel()
    win.show()
    sys.exit(app.exec_())