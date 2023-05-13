import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from com.mat.rpa.views.workWindow.middlePanel.consolePanel.tabPanel import basicConsolePanel

class DataTablePanel(basicConsolePanel.BasicConsolePanel):
    picPath = "./com/mat/rpa/views/workWindow/middlePanel/consolePanel/tabPanel/images/"
    def __init__(self, parent=None):
        super(DataTablePanel, self).__init__(parent)
        self.hintLabel.setText("数据表格")
        self.importBtn = QPushButton()
        self.importBtn.setIcon(
            QIcon(QPixmap(DataTablePanel.picPath+"import.png")))
        self.btnPanelLayout.addWidget(self.importBtn)

        self.exportingBtnMenu = QMenu()
        self.dataExportingAction = QAction("导出数据表格", self.exportingBtnMenu)
        self.exportingBtnMenu.addAction(self.dataExportingAction)
        self.dataExportingWithHeaderAction = QAction("导出表格（带表头）", self.exportingBtnMenu)
        self.exportingBtnMenu.addAction(self.dataExportingWithHeaderAction)
        self.exportBtn = QToolButton()
        self.exportBtn.setIcon(QIcon(QPixmap(DataTablePanel.picPath + "export.png")))
        self.exportBtn.setMenu(self.exportingBtnMenu)
        self.exportBtn.setPopupMode(QToolButton.InstantPopup)
        self.btnPanelLayout.addWidget(self.exportBtn)

        self.deleteBtnMenu=QMenu()
        self.selectedContentDeletingAction = QAction("删除选中内容", self.deleteBtnMenu)
        self.deleteBtnMenu.addAction(self.selectedContentDeletingAction)
        self.everythingClearingAction = QAction("清空全部内容", self.deleteBtnMenu)
        self.deleteBtnMenu.addAction(self.everythingClearingAction)
        self.deleteBtn = QToolButton()
        self.deleteBtn.setIcon(QIcon(QPixmap(DataTablePanel.picPath + "delete.png")))
        self.deleteBtn.setMenu(self.deleteBtnMenu)
        self.deleteBtn.setPopupMode(QToolButton.InstantPopup)
        self.btnPanelLayout.addWidget(self.deleteBtn)

        self.dataTable = QTableWidget()
        self.centerPanelLayout.addWidget(self.dataTable,0,0,2,2)
        self.dataTable.setRowCount(50)
        self.dataTable.setColumnCount(8)
        self.dataTable.setShowGrid(True)
        self.dataTable.setHorizontalHeaderLabels(["A", "B", "C","D","E","F","G","H"])
        self.dataTable.horizontalHeader().setStretchLastSection(QHeaderView.Stretch)
        self.dataTable.horizontalHeader().setStretchLastSection(True)

if __name__=='__main__':
    app=QApplication(sys.argv)
    fms=DataTablePanel()
    fms.show()
    sys.exit(app.exec_())