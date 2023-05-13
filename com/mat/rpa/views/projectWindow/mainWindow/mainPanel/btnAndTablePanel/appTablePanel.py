# -*- coding:utf-8 -*-
import datetime
import json
import os
import traceback

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from com.mat.rpa.dao.projectAppDao import myAppDao
from bson import ObjectId

from com.mat.rpa.dao.workDao.directiveDao import DirectiveDao
from com.mat.rpa.dao.workDao.workDao import WorkDao


class DisplayLabel(QLabel):
    #设置类属性，所有对象共享，不用重复创建
    __font = QFont()
    __font.setFamily("Microsoft YaHei")
    __font.setPixelSize(17)
    # __font.setBold(True)
    __metrics = QFontMetrics(__font)

    def __init__(self, parent=None):
        super(DisplayLabel, self).__init__(parent)
        self.setMaximumHeight(40)

    def setAutoWidthText(self, text):
        self.setFont(DisplayLabel.__font)
        self.setText(text)
        self.setMaximumWidth(DisplayLabel.__metrics.boundingRect(text).size().width()*1.4+18)

class AppTablePanel(QWidget):
    picPath = "./com/mat/rpa/views/projectWindow/mainWindow/mainPanel/btnAndTablePanel/images/"
    openAppSignal = pyqtSignal(ObjectId)
    statusText = [u"编辑中", u"已完成", u"正在运行", u"临时"]

    def __init__(self, parent=None):
        super(AppTablePanel, self).__init__(parent)
        self.parentPanel = parent
        #数据模型
        self.model = None
        #数据表
        self.tableView = None
        #总页数文本
        self.totalPageLabel = None
        #当前页文本
        self.currentPageLabel = None
        #转到页输入框
        self.switchPageLineEdit = None
        #前一页按钮
        self.prevButton = None
        #后一页按钮
        self.nextButton = None
        #转到页按钮
        self.switchPageButton = None
        #当前页
        self.currentPage = 0
        #总页数
        self.totalPage = 0
        #总记录数
        self.totalRecordCount = 0
        #每页显示记录数
        self.pageRecordCount = 10
        self.myAppDaoObj = myAppDao.MyAppDao(self)
        self.initUI()

    def refreshTable(self):
        # 设置当前页
        self.currentPage = 1
        # 得到总记录数
        self.updateStatus(self.myAppDaoObj.queryTotalRecordCount())
        # 查询第0页记录
        result = self.myAppDaoObj.queryLimitedAppsIntoTable((self.currentPage-1)*self.pageRecordCount,
                                                            self.pageRecordCount)
        self.insertAppRecordIntoTableWidget(result)
        # #插入一条记录
        # self.myAppDao.insertIntoOneRecord(("应用程序3", "2021-12-31", 1))
        # self.myAppDao.delRecordByAppName("应用程序3")

    def initUI(self):
        # 创建窗口
        self.createWindow()
        #设置表格
        self.setTableView()
        self.updateStatus(0)
        self.refreshTable()
        # 信号槽连接
        self.prevButton.clicked.connect(self.onPrevButtonClick)
        self.nextButton.clicked.connect(self.onNextButtonClick)
        self.switchPageButton.clicked.connect(self.onSwitchPageButtonClick)

    def createWindow(self):
        #操作布局
        __font = QFont()
        __font.setFamily("Microsoft YaHei")
        __font.setPixelSize(14)
        operatorLayout= QHBoxLayout()
        operatorLayout.setContentsMargins(0,5,5,0)
        operatorLayout.setSpacing(5)
        self.prevButton = QPushButton(text=u"前一页", font=__font)
        self.nextButton = QPushButton(text=u"后一页", font=__font)
        self.switchPageButton = QPushButton(text=u"Go", font=__font)
        self.switchPageButton.setFixedWidth(30)
        self.switchPageLineEdit = QLineEdit(font=__font)
        self.switchPageLineEdit.setAlignment(Qt.AlignCenter)
        self.switchPageLineEdit.setValidator(QIntValidator())
        self.switchPageLineEdit.setFixedWidth(30)
        switchPage = QLabel(text=u"转到第", font=__font)
        page = QLabel(text=u"页", font=__font)
        operatorLayout.addWidget(self.prevButton)
        operatorLayout.addWidget(self.nextButton)
        operatorLayout.addSpacing(15)
        operatorLayout.addWidget(switchPage)
        operatorLayout.addWidget(self.switchPageLineEdit)
        operatorLayout.addWidget(page)
        operatorLayout.addWidget(self.switchPageButton)
        operatorLayout.addStretch(1)
        #设置表格属性
        self.tableWidget = QTableWidget()
        self.totalPageLabel = DisplayLabel()
        self.currentPageLabel = DisplayLabel()
        self.totalRecordLabel = DisplayLabel()
        operatorLayout.addWidget(self.totalPageLabel)
        operatorLayout.addWidget(self.currentPageLabel)
        operatorLayout.addWidget(self.totalRecordLabel)
        #创建分页控件的主窗口
        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(5,0,5,5)
        mainLayout.setSpacing(0)
        mainLayout.addWidget(self.tableWidget)
        mainLayout.addLayout(operatorLayout)
        self.setLayout(mainLayout)

    def resizeEvent(self, a0: QResizeEvent) -> None:
        super().resizeEvent(a0)
        width = a0.size().width() - 11
        self.tableWidget.setColumnWidth(0, width*0.5)
        self.tableWidget.setColumnWidth(1, width*0.2)
        self.tableWidget.setColumnWidth(2, width*0.1)
        self.tableWidget.setColumnWidth(3, width*0.2)

    def setTableView(self):
        #设置表格头
        self.title = ['应用名称', '更新时间', '状态', '']
        # 创建模型
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(self.title)
        headerView = self.tableWidget.horizontalHeader()
        headerView.setDefaultAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        #设置表格各列宽度
        desktop = QApplication.desktop()
        # 得到屏幕可显示尺寸
        rect = desktop.availableGeometry()
        screenWidth = rect.width()
        self.tableWidth = screenWidth*0.78
        self.tableWidget.setColumnWidth(0, self.tableWidth*0.5)
        self.tableWidget.setColumnWidth(1, self.tableWidth*0.2)
        self.tableWidget.setColumnWidth(2, self.tableWidth*0.1)
        self.tableWidget.setColumnWidth(3, self.tableWidth*0.2)
        self.tableWidget.verticalHeader().setVisible(False)
        # 设置各行高度
        self.tableWidget.verticalHeader().setDefaultSectionSize(60)
        #去除表格线
        self.tableWidget.setShowGrid(False)
        # self.tableWidget.setFocusPolicy(Qt.NoFocus)
        # 设置表格样式
        self.tableWidget.setStyleSheet('''
        QTableView::item {
            padding: 5;
            border-bottom: 1px solid #CCC;
        }
        QTableView::item:selected {
            background-color: #FAF0F0;
            color: black;
        }
        QTableWidget {
            outline: none;
        }
        QHeaderView::section {
            color: #444;
            font-size: 14px;
            padding: 5px;
            border-style: none;
            background-color: #e5e5e5
        }
        ''')
        self.tableWidget.cellDoubleClicked.connect(self.openApp)

    # 打开应用
    def openApp(self, row, _):
        print("点击的App应用row是:", row, ", appid是：", self.tableWidget.cellWidget(row, 3).appId)
        self.openAppSignal.emit(self.tableWidget.cellWidget(row, 3).appId)

    # 刷新状态
    def updateStatus(self, totalRecordCount=None):
        szCurrentText = ("当前第%d页" % self.currentPage)
        self.currentPageLabel.setAutoWidthText(szCurrentText)
        if totalRecordCount:
            self.setTotalRecordLabel(totalRecordCount)
        self.getPageCount()
        self.setTotalPageLabel()
        self.switchPageLineEdit.setText(str(self.currentPage))
        # 设置按钮是否可用
        if self.currentPage == 1:
            self.prevButton.setEnabled(False)
        else:
            self.prevButton.setEnabled(True)
        if self.currentPage == self.totalPage:
            self.nextButton.setEnabled(False)
        else:
            self.nextButton.setEnabled(True)

    def addBtnToTableCell(self, row, appId):
        btnPanel = QWidget()
        btnPanel.appId = appId
        btnPanelLayout = QHBoxLayout()
        btnPanel.setLayout(btnPanelLayout)
        btnPanelLayout.setContentsMargins(0,0,0,0)
        btnPanelLayout.setSpacing(5)
        runBtn = QPushButton()
        runBtn.setIcon(QIcon(QPixmap(AppTablePanel.picPath + "runBtn.png")))
        btnPanelLayout.addWidget(runBtn)
        editBtn = QPushButton()
        editBtn.setIcon(QIcon(QPixmap(AppTablePanel.picPath + "editBtn.png")))
        editBtn.clicked.connect(lambda: self.openAppSignal.emit(appId))
        btnPanelLayout.addWidget(editBtn)
        infoBtn = QPushButton()
        infoBtn.setIcon(QIcon(QPixmap(AppTablePanel.picPath + "infoBtn.png")))
        btnPanelLayout.addWidget(infoBtn)
        deleteBtn = QPushButton()
        deleteBtn.setIcon(QIcon(QPixmap(AppTablePanel.picPath + "deleteBtn.png")))
        btnPanelLayout.addWidget(deleteBtn)
        deleteBtn.clicked.connect(lambda: self.deleteApp(appId))
        ellipsisBtn = QPushButton()
        ellipsisBtn.setIcon(QIcon(QPixmap(AppTablePanel.picPath + "ellipsisBtn.png")))
        btnPanelLayout.addWidget(ellipsisBtn)
        btnPanel.setStyleSheet("""
        QPushButton {
            border-style: none;
            border-radius: 4px;
            height: 24px;
        }
        QPushButton:hover {
            background-color: #e0e0e0;
        }
        QPushButton:pressed {
            background-color: #d0d0d0;
        }
        """)
        self.tableWidget.setCellWidget(row, 3, btnPanel)

    def insertAppRecordIntoTableWidget(self, resultList: list):
        self.tableWidget.setRowCount(len(resultList))
        idx = 0
        for item in resultList:
            nameItem = QTableWidgetItem(item["name"])
            font = QFont()
            font.setPixelSize(18)
            nameItem.setFont(font)
            self.tableWidget.setItem(idx, 0, nameItem)
            fontS = QFont()
            fontS.setPixelSize(14)
            if "update_time" in item.keys():
                timeItem = QTableWidgetItem(item["update_time"].strftime("%Y-%m-%d  %H:%M:%S"))
            else:
                timeItem = QTableWidgetItem("")
            timeItem.setFont(fontS)
            timeItem.setForeground(QColor(92, 92, 92))
            self.tableWidget.setItem(idx, 1, timeItem)
            statusItem = QTableWidgetItem(self.statusText[int(item["status"])])
            statusItem.setFont(fontS)
            statusItem.setForeground(QColor(92, 92, 92))
            self.tableWidget.setItem(idx, 2, statusItem)
            self.addBtnToTableCell(idx, item["_id"])
            idx += 1
        self.tableWidget.update()

    # 得到页数
    def getPageCount(self):
        print(self.totalRecordCount, self.pageRecordCount)
        self.totalPage = (self.totalRecordCount - 1) // self.pageRecordCount + 1

    # 设置总数页文本
    def setTotalPageLabel(self):
        szPageCountText = ("共%d页" % self.totalPage)
        self.totalPageLabel.setAutoWidthText(szPageCountText)

    # 设置总记录数
    def setTotalRecordLabel(self, totalRecordCount):
        self.totalRecordCount = totalRecordCount
        szTotalRecordText = ("共%d条" % self.totalRecordCount)
        self.totalRecordLabel.setAutoWidthText(szTotalRecordText)

    #前一页按钮对应的槽函数
    def onPrevButtonClick(self):
        self.currentPage = 1 \
            if self.currentPage<1 else self.currentPage-1
        limitIndex = (self.currentPage-1)*self.pageRecordCount
        result = self.myAppDaoObj.queryLimitedAppsIntoTable(limitIndex, self.pageRecordCount)
        self.insertAppRecordIntoTableWidget(result)
        self.updateStatus()

    #后一页按钮对应的槽函数
    def onNextButtonClick(self):
        self.currentPage = self.totalPage \
            if self.currentPage>self.totalPage else self.currentPage+1
        limitIndex = (self.currentPage-1)*self.pageRecordCount
        result = self.myAppDaoObj.queryLimitedAppsIntoTable(limitIndex, self.pageRecordCount)
        self.insertAppRecordIntoTableWidget(result)
        self.updateStatus()

    # 转到页按钮按下
    def onSwitchPageButtonClick(self):
        # 得到输入字符串
        szText = self.switchPageLineEdit.text()
        if szText == '':
            QMessageBox.information(self,
                            "提示", "请输入跳转页面")
            return
        # 得到页数
        pageIndex = int(szText)
        # 判断是否有指定页
        if pageIndex > self.totalPage or pageIndex < 1:
            QMessageBox.information(self,
                    "提示", "没有指定的页面，请重新输入")
            return
        # 设置当前页
        self.currentPage = pageIndex
        # 得到查询起始行号
        limitIndex = (pageIndex - 1) * self.pageRecordCount
        # 记录查询
        result = self.myAppDaoObj.queryLimitedAppsIntoTable(limitIndex, self.pageRecordCount)
        self.insertAppRecordIntoTableWidget(result)
        # 刷新状态
        self.updateStatus()

    # 删除App
    def deleteApp(self, appId):
        messageBox = QMessageBox(QMessageBox.Question, u"删除应用",
                                 u"确定要删除此应用吗？",
                                 QMessageBox.Yes | QMessageBox.Cancel)
        yesBtn = messageBox.button(QMessageBox.Yes)
        yesBtn.setText(u"确认")
        yesBtn.setStyleSheet("background-color: red; color: white;")
        messageBox.button(QMessageBox.Cancel).setText(u"取消")
        messageBox.setStyleSheet("QMessageBox {background-color: white}")
        messageBox.setContentsMargins(6, 8, 6, 4)
        reply = messageBox.exec()
        if reply == QMessageBox.Yes:
            self.myAppDaoObj.deleteApp(appId)
            self.refreshTable()

    # 导出App
    def exportApp(self):
        try:
            row = self.tableWidget.currentRow()
            if row < 0:
                # 未选中行
                return
            widget = self.tableWidget.cellWidget(row, 3)
            if not hasattr(widget, "appId"):
                return
            appInfo = WorkDao().loadApp(widget.appId)
            if appInfo["status"] == -1:
                # 当前APP为临时APP
                return
            if hasattr(appInfo, "export_path"):
                exportPath = appInfo["export_path"]
            else:
                # 没有设置导出路径
                exportPath = ""
            # 路径选择
            exportPath = QFileDialog.getExistingDirectory(self, u"确认导出路径", exportPath)
            if exportPath == "":
                # 取消选择
                return
            exportPath = exportPath + "/" + appInfo["name"]
            if not os.path.exists(exportPath):
                os.mkdir(exportPath)
            with open(exportPath + "/" + appInfo["name"] + ".app", "w", encoding="utf-8") as appFile:
                appInfo["_id"] = str(appInfo["_id"])
                appInfo["update_time"] = str(appInfo["update_time"])
                for item in appInfo["flow"]:
                    item["id"] = str(item["id"])
                del appInfo["export_path"]
                json.dump(appInfo, appFile, indent=2, ensure_ascii=False)
            del appInfo
            flows = WorkDao().getFlows(widget.appId)
            for flowDict in flows:
                fileName = exportPath + "/" + flowDict["flow_name"]
                flowId = flowDict["id"]
                # 写入Flow文件信息
                with open(fileName, 'w', encoding="utf-8") as flow:
                    flowDict["id"] = str(flowId)
                    flowDict["name"] = flowDict["flow_name"]
                    del flowDict["flow_name"]
                    flowDict["app_id"] = str(widget.appId)
                    json.dump(flowDict, flow, indent=2, ensure_ascii=False)
                # 删掉最后的大括号换行符，填写directives:
                with open(fileName, 'ab') as flow:
                    flow.seek(-3, 2)
                    flow.truncate()
                    flow.write(b',\n  "directives": [')
                # 导出数据库中的指令
                with open(fileName, 'a', encoding="utf-8") as flow:
                    first = True
                    for directive in DirectiveDao().getAllDirectives(flowId):
                        if first:
                            first = False
                        else:
                            flow.write(", ")
                        directive["_id"] = str(directive["_id"])
                        del directive["flow_id"]
                        text = json.dumps(directive, indent=2, ensure_ascii=False)
                        text = text.split('\n')
                        indented = text[0]
                        for line in text[1:]:
                            indented += "\n  " + line
                        flow.write(indented)
                    flow.write("]\n}")
        except Exception:
            traceback.print_exc()

    # 导入App
    def importApp(self):
        try:
            fileName, _ = QFileDialog.getOpenFileName(self, u"导入App", "", u"App工程文件 (*.app)")
            if fileName == "":
                # 用户取消
                return
            appPath = fileName.rsplit('/', 1)[0]
            if not os.path.exists(appPath + u"/主流程.flow"):
                # 不存在主流程 todo 提示
                return
            flowIdSet = set()
            workDaoObj = WorkDao()
            directiveDaoObj = DirectiveDao()
            # 导入App信息
            with open(fileName, "r", encoding="utf-8") as appFile:
                appInfo = json.load(appFile)
                del appInfo["_id"]
                for item in appInfo["flow"]:
                    flowIdSet.add(item["id"])
                del appInfo["flow"]
                appInfo["update_time"] = datetime.datetime.strptime(appInfo["update_time"], "%Y-%m-%d %H:%M:%S.%f")
                appId = workDaoObj.importNewApp(appInfo)
            # 查找同一目录下的Flow文件
            for file in os.listdir(appPath):
                if not file.endswith(".flow"):
                    # 不是Flow文件
                    continue
                # 读取Flow文件
                with open(appPath + "/" + file, "r", encoding="utf-8") as flow:
                    flowDict = json.load(flow)
                    if flowDict["id"] not in flowIdSet:
                        # 不是此App的Flow文件
                        continue
                    flowId = workDaoObj.importFlow(appId, {"flow_name": flowDict["name"], "type": flowDict["type"]})
                    for directive in flowDict["directives"]:
                        # 导入指令
                        del directive["_id"]
                        directive["flow_id"] = flowId
                        directiveDaoObj.insertDirective(directive)
            self.refreshTable()
        except Exception:
            traceback.print_exc()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 创建窗口
    example = AppTablePanel()
    # 显示窗口
    example.show()
    sys.exit(app.exec_())