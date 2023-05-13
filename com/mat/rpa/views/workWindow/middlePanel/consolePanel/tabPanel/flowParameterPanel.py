from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from com.mat.rpa.views.workWindow.middlePanel.consolePanel.tabPanel import basicConsolePanel
import sys

class FlowParameterPanel(basicConsolePanel.BasicConsolePanel):
    picPath = "./com/mat/rpa/views/workWindow/middlePanel/consolePanel/tabPanel/images/"
    picLastPath = "./com/mat/rpa/views/workWindow/middlePanel/consolePanel/images/"
    def __init__(self, parent=None):
        super(FlowParameterPanel, self).__init__(parent)
        self.hintLabel.setText("流程参数")
        self.searchBtn=QPushButton()
        self.searchBtn.setIcon(QIcon(QPixmap(FlowParameterPanel.picPath + "search.png")))
        self.searchBtn.clicked.connect(self.searchBoxPanelUp)
        self.btnPanelLayout.addWidget(self.searchBtn)
        self.addVariableBtn = QPushButton()
        self.addVariableBtn.setIcon(QIcon(QPixmap(FlowParameterPanel.picPath + "addVariable.png")))
        self.addVariableBtn.clicked.connect(self.addRow)
        self.btnPanelLayout.addWidget(self.addVariableBtn)
        #流程参数表格
        self.flowParameterPanelTable = QTableWidget()
        self.centerPanelLayout.addWidget(self.flowParameterPanelTable,0,0,2,2)
        self.flowParameterPanelTable.setColumnCount(5)
        self.flowParameterPanelTable.setHorizontalHeaderLabels(["参数名称", "参数方向", "参数类型","默认值","描述"])
        desktop = QApplication.desktop()
        rect = desktop.availableGeometry()
        screenWidth = rect.width()
        self.tableWidth = screenWidth * 0.54
        self.flowParameterPanelTable.setColumnWidth(0, self.tableWidth*0.15)
        self.flowParameterPanelTable.setColumnWidth(1, self.tableWidth*0.1)
        self.flowParameterPanelTable.setColumnWidth(2,self.tableWidth*0.1)
        self.flowParameterPanelTable.setColumnWidth(3, self.tableWidth*0.4)
        self.flowParameterPanelTable.horizontalHeader().setStretchLastSection(True)
        self.flowParameterPanelTable.setContextMenuPolicy(Qt.CustomContextMenu)
        ##搜索参数
        self.searchBtn_2.clicked.connect(self.parameterSearching)
        self.closeSearchBtn.clicked.connect(self.btnPanelUp)
        ##右键删除某一行
        self.flowParameterPanelTable.customContextMenuRequested.connect(self.deletFlowParameterPanelTable)

        ##表格插入数据
    def addRow(self):
        i=0
        row=self.flowParameterPanelTable.rowCount()
        self.flowParameterPanelTable.insertRow(row)
        self.flowParameterPanelTable.setItem(row,0,QTableWidgetItem("parameter"+str(row)))
        self.parameterDirectionCombobox=QComboBox()
        self.parameterDirectionCombobox.addItems((["输入","输出"]))
        self.flowParameterPanelTable.setCellWidget(row,1,self.parameterDirectionCombobox)
        self.parameterTypesCombobox=QComboBox()
        self.parameterTypesCombobox.addItems((["字符串","整数","小数","布尔值","文件路径"]))
        self.parameterTypesCombobox.currentIndexChanged.connect(self.settingDefaults)
        self.flowParameterPanelTable.setCellWidget(row,2,self.parameterTypesCombobox)

    def settingDefaults(self):
        row_num = -1
        row = self.flowParameterPanelTable.rowCount()
        currentIndex=self.parameterDirectionCombobox.currentIndex()
        for i in self.flowParameterPanelTable.selectionModel().selection().indexes():
            row_num=i.row()
        if row_num<row:
           if currentIndex==1:
            self.flowParameterPanelTable.setItem(row_num, 3, QTableWidgetItem(str(0)))
           else:
               pass


    def searchBoxPanelUp(self):
        self.stackedWidget.setCurrentIndex(1)
        self.folddingBtn.setIcon(QIcon(QPixmap(FlowParameterPanel.picLastPath + "folddown.png")))

    #搜索
    def parameterSearching(self):
        text = self.searchBox.text()
        row = self.flowParameterPanelTable.rowCount()
        if (text==""):
          for i in range(0,row-1):
             self.flowParameterPanelTable.setRowHidden(i,False)
        else:
            items = self.flowParameterPanelTable.findItems(text, Qt.MatchExactly)
            for i in range(0,row-1):
                self.flowParameterPanelTable.setRowHidden(i,True)
            if items!="":
                for i in range(0,row-1):
                    self.flowParameterPanelTable.setRowHidden(items[i].row(),False)
                    print( items[i].row())
    #删除
    def deletFlowParameterPanelTable(self,pos):
        row_num=-1
        row = self.flowParameterPanelTable.rowCount()
        for i in self.flowParameterPanelTable.selectionModel().selection().indexes():
            row_num=i.row()
        if row_num<row:
            menu=QMenu()
            findReferences=menu.addAction("查找引用")
            delete=menu.addAction("删除")
            action=menu.exec_(self.flowParameterPanelTable.mapToGlobal(pos))
            if action==delete:
                self.flowParameterPanelTable.removeRow(row_num)
            else:
                return

    def btnPanelUp(self):
        self.stackedWidget.setCurrentIndex(0)
        row = self.flowParameterPanelTable.rowCount()
        for i in range (0,row):
             self.flowParameterPanelTable.setRowHidden(i, False)
        else:
            pass


if __name__=='__main__':
     app=QApplication(sys.argv)
     fms=FlowParameterPanel()
     fms.show()
     sys.exit(app.exec())
