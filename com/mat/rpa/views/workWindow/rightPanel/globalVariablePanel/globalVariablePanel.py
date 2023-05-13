# -*- coding:utf-8 -*-
import time

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtGui

from com.mat.rpa.dao.workDao.directiveDao import DirectiveDao
from com.mat.rpa.utils.variable import VariableManager
import sys


class GlobalVariablePanel(QWidget):
    picPath = "./com/mat/rpa/views/workWindow/rightPanel/images/"
    __instance = None
    _isFirstInit = True

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(GlobalVariablePanel, cls).__new__(cls)
        return cls.__instance


    def __init__(self, parent=None):
        cls = type(self)
        if cls._isFirstInit:
            super(GlobalVariablePanel, self).__init__(parent)
            self.variableDict={}
            self.parentPanel = parent
            self.variableManagerObj=VariableManager()
            self.directiveDaoObj = DirectiveDao()
            #设置全局布局管理器
            self.entireLayout = QVBoxLayout()
            self.entireLayout.setContentsMargins(0,0,0,0)
            self.entireLayout.setSpacing(0)
            self.setLayout(self.entireLayout)
            #添加topPanel
            self.topPanel = QWidget()
            self.topPanelLayout = QHBoxLayout()
            self.topPanelLayout.setContentsMargins(0,0,0,0)
            self.topPanelLayout.setSpacing(0)
            self.hintLabel = QLabel()
            self.hintLabel.setText("变量")
            self.topPanelLayout.addWidget(self.hintLabel)
            self.topPanelLayout.addStretch(1) #添加弹簧
            ##添加stackedWidget
            self.stackedWidget = QStackedWidget()
            self.stackedWidget.setContentsMargins(0,0,0,0)
            self.topPanelLayout.addWidget(self.stackedWidget)
            self.topPanel.setLayout(self.topPanelLayout)
            ###添加搜索按钮和添加变量按钮面板
            self.firstPanel = QWidget()
            self.firstPanelLayout = QHBoxLayout()
            self.firstPanel.setLayout(self.firstPanelLayout)
            self.firstPanelLayout.setContentsMargins(0,0,0,0)
            self.firstPanelLayout.setSpacing(0)
            self.firstPanelLayout.addStretch(1)
            self.searchLine = QLineEdit()
            self.firstPanelLayout.addWidget(self.searchLine)
            self.valueLabel = QLabel("value:  ")
            self.firstPanelLayout.addWidget(self.valueLabel)
            self.searchBtn = QPushButton()
            self.searchBtn.setIcon(QIcon(QPixmap(GlobalVariablePanel.picPath+"search.png")))
            self.firstPanelLayout.addWidget(self.searchBtn)
            self.addVariableBtn = QPushButton()
            self.addVariableBtn.setIcon(QIcon(QPixmap(GlobalVariablePanel.picPath+"addVariable.png")))
            self.firstPanelLayout.addWidget(self.addVariableBtn)
            self.deleteVariableBtn = QPushButton()
            self.deleteVariableBtn.setIcon(QIcon(QPixmap(GlobalVariablePanel.picPath + "delete.png")))
            self.firstPanelLayout.addWidget(self.deleteVariableBtn)



            self.stackedWidget.addWidget(self.firstPanel)
            self.stackedWidget.setCurrentIndex(0)
            ###添加搜索框面板
            self.secondPanel = QWidget()
            self.secondPanelLayout = QHBoxLayout()
            self.secondPanelLayout.setContentsMargins(0,0,0,0)
            self.secondPanelLayout.setSpacing(0)
            self.secondPanel.setLayout(self.secondPanelLayout)
            self.secondPanelLayout.addStretch(1)
            self.searchBox = QLineEdit()
            self.secondPanelLayout.addWidget(self.searchBox)
            self.closeSearchBtn = QPushButton()
            self.closeSearchBtn.setIcon(QIcon(QPixmap(GlobalVariablePanel.picPath+"closeSearch.png")))
            self.secondPanelLayout.addWidget(self.closeSearchBtn)
            self.stackedWidget.addWidget(self.secondPanel)
            self.entireLayout.addWidget(self.topPanel,0.5)
            #添加变量表格
            self.variableTableView = QTableView()
            self.variableTableView.horizontalHeader().setStretchLastSection(True)
            self.variableTableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.variableTableModel = QStandardItemModel()
            # 设置表格头
            self.tableTitle = ['变量名称', '类型', '值','flow_id']
            self.variableTableModel.setHorizontalHeaderLabels(self.tableTitle)
            # 表格设置模型
            self.variableTableView.setModel(self.variableTableModel)
            self.searchBtn.clicked.connect(lambda: self.searchVariable(self.searchLine))
            self.addVariableBtn.clicked.connect(self.addVariable)
            self.deleteVariableBtn.clicked.connect(lambda: self.deleteVariable(
                self.variableTableView, self.variableTableModel
            ))

            self.entireLayout.addWidget(self.variableTableView, 9.5)
            self.updateVariables()
            cls._isFirstInit = False

    def deleteVariable(self, view: QTableView, model: QStandardItemModel):
        vm = VariableManager()
        indexes = view.selectionModel().selection().indexes()
        try:
            vm.variableDaoObj.variable.delete_one({"name": self.variableTableModel.item(indexes[0].row(), 0).text()})
            model.removeRows(indexes[0].row(), 1)
        except Exception as e:
            print(e)

    def addVariable(self):
        directive = {"command": "",
                     "line_number": "",
                     "flow_title": "",
                     "data": {},
                     "comment": "",
                     "target": "",
                     "targets": [],
                     "value": ""
                     }
        directive["line_number"] = 1
        directive["command"] = "settingVariableDirective"
        directive["flow_id"] = "0"
        directive["data"] = {"type": 0,
                                  "value": "",
                                  "name": "variable",
                                  "log": True,
                                  "handle": 0,
                                  "on_error_output_value": "",
                                  "retry_count": 1,
                                  "retry_interval": 1}
        directive["_id"] = self.directiveDaoObj.insertDirective(directive)

    def searchVariable(self, searchLine: QLineEdit):
        value = self.getVariableByName(searchLine.text())
        self.valueLabel.setText(self.valueLabel.text()[0:8] + str(value))


    def insertItemToVariableTable(self, row, col, item):
        self.variableTableModel.setItem(row, col, item)

    def getVariableByName(self, name):
        r = 0
        c = 0
        find = 0

        while find == 0:
            try:
                item = self.variableTableModel.item(r, c)
                if item.text() == name:
                    find = 1
                    break
            except Exception as e:
                break
            r += 1

        if find:
            item = self.variableTableModel.item(r, 2)
            type = item.type()
            if type == 0:
                try:
                    value = eval(item.text())
                except Exception as e:
                    value = str(item.text())
            elif type == 1:
                value = int(item.text())
            elif type == 2:
                value = float(item.text())
            elif type == 3:
                value = eval(item.text())
            else:
                value = str(item.text())
            return value
        return None

    def updateVariables(self):
        m = 0
        for x in self.variableManagerObj.variableDaoObj.variable.find():
            self.insertItemToVariableTable(m, 0, QtGui.QStandardItem(x["name"]))
            if x["type"] == 0:
                self.insertItemToVariableTable(m, 1, QtGui.QStandardItem("任意类型"))
            elif x["type"] == 1:
                self.insertItemToVariableTable(m, 1, QtGui.QStandardItem("整数"))
            elif x["type"] == 2:
                self.insertItemToVariableTable(m, 1, QtGui.QStandardItem("浮点数"))
            elif x["type"] == 3:
                self.insertItemToVariableTable(m, 1, QtGui.QStandardItem("布尔型"))
            elif x["type"] == 4:
                self.insertItemToVariableTable(m, 1, QtGui.QStandardItem("字符型"))
            elif x["type"] == 5:
                self.insertItemToVariableTable(m, 1, QtGui.QStandardItem("字符串"))
            else:
                self.insertItemToVariableTable(m, 1, QtGui.QStandardItem("None"))
            self.insertItemToVariableTable(m, 2, QtGui.QStandardItem(x["value"]))
            self.insertItemToVariableTable(m, 3, QtGui.QStandardItem(str(x["flowId"])))
            # self.insertItemToVariableTable(m, 2, QtGui.QStandardItem(x["value"]))
            m = m + 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = GlobalVariablePanel()
    win.show()
    gvm = GlobalVariablePanel()
    print(gvm.variableTableModel.rowCount())

    app.exec_()