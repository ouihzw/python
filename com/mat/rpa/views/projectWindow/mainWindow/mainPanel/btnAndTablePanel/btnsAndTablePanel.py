# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from com.mat.rpa.views.projectWindow.mainWindow.mainPanel.btnAndTablePanel import topPanel, appTablePanel
import sys

#RPA studio右边的应用按钮和表格面板
class BtnsAndTablePanel(QWidget):
    def __init__(self, parent=None):
        super(BtnsAndTablePanel, self).__init__(parent)
        self.parentPanel = parent
        self.entireLayout = QVBoxLayout()
        self.setLayout(self.entireLayout)
        self.entireLayout.setContentsMargins(0,0,0,0)
        self.entireLayout.setSpacing(0)
        self.topPanel = topPanel.TopBtnPanel(self)
        self.entireLayout.addWidget(self.topPanel)
        self.tablePanel = appTablePanel.AppTablePanel(self)
        self.entireLayout.addWidget(self.tablePanel)
        self.topPanel.editAppBtn.clicked.connect(self.editApp)
        self.topPanel.exportAppBtn.clicked.connect(self.tablePanel.exportApp)
        self.topPanel.importAppBtn.clicked.connect(self.tablePanel.importApp)

    def editApp(self):
        row = self.tablePanel.tableWidget.currentRow()
        if row >= 0:
            print("当前选中的表格是第", row, "行")
            widget = self.tablePanel.tableWidget.cellWidget(row, 3)
            if hasattr(widget, "appId"):
                self.tablePanel.openAppSignal.emit(widget.appId)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = BtnsAndTablePanel()
    win.show()
    sys.exit(app.exec_())
