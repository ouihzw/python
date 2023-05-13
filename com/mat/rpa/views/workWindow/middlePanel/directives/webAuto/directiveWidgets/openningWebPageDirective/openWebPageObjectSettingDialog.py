# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
from com.mat.rpa.utils import webSingleCase
from com.mat.rpa.utils import webAutoSave
from com.mat.rpa.utils.variable import replacePlainTextVariable
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowSettingDialog
from com.mat.rpa.dao.workDao.directiveDao import DirectiveDao
from com.mat.rpa.views.workWindow.rightPanel.globalVariablePanel import globalVariablePanel


class OpenWebPageObjectSettingDialog(flowSettingDialog.BasicFlowSettingDialog):
    flowTextList = pyqtSignal(list)
    def __init__(self, title, directive_id, id, parent=None):
        super().__init__(title, directive_id, id,parent)
        self.directiveDaoObj = DirectiveDao()
        self.webSave = webAutoSave.WebAutoSave()
        self.setInfoLabelText(u"使用指定浏览器打开网页，以实现网页自动化")
        #改变图片
        self.changeImage(flowSettingDialog.BasicFlowSettingDialog.picPath + "openWebPageBig.png")
        self.regularTabUI()
        self.seniorTabUI()
        self.errorHandlingTabUI()
        self.settingTabWidget.currentChanged.connect(self.changeTab)
        self.directive = {"command": "",
                          "line_number": "",
                          "flow_title": "",
                          "data": {},
                          "comment": "",
                          "target": "",
                          "targets": [],
                          "value": ""
                          }
        self.directive["_id"] = directive_id
        self.directive["data"] = {"browser_type": 0,
                                  "url": "",
                                  "output": "web_page",
                                  "wait": True,
                                  "time_out_period": 15,
                                  "on_time_out": 0,
                                  "cli_parameter": "",
                                  "exe_path": "",
                                  "log": True,
                                  "handle": 0,
                                  "on_error_output_value": "",
                                  "retry_count": 1,
                                  "retry_interval": 1}
        self.infoFormat = u"在%s中新建标签页%s，将网页对象保存到%s，网页加载超时后执行%s操作"


    def regularTabUI(self):
        __font = QFont()
        __font.setPixelSize(20)
        __font.setFamily("Courier")
        #布局指令输入面板
        self.directiveInputSettingLayout = QGridLayout()
        self.directiveInputSettingLayout.setContentsMargins(50,0,20,0)
        self.directiveInputSettingLayout.setSpacing(10)
        self.directiveInputSettingLayout.setVerticalSpacing(30)
        self.directiveInputSettingPanel.setLayout(self.directiveInputSettingLayout)
        self.browserTypeLabel = QLabel()
        self.browserTypeLabel.setFont(__font)
        self.browserTypeLabel.setText("浏览器类型:")
        self.directiveInputSettingLayout.addWidget(self.browserTypeLabel, 0,0,1,1,Qt.AlignRight)
        self.browserTypeCombobox = QComboBox()
        self.browserTypeCombobox.setObjectName("browserTypeCombobox")
        self.browserTypeCombobox.setFont(__font)
        self.browserTypeCombobox.setMinimumSize(600,50)
        self.browserTypeCombobox.addItems(["内置Firefox浏览器", "Google Chrome浏览器",
                                           "MicroSoft Edge浏览器", "Internet Explorer浏览器",
                                           "360安全浏览器"])
        self.browserTypeCombobox.setItemDelegate(QStyledItemDelegate())
        self.browserTypeCombobox.setStyleSheet("QComboBox QAbstractItemView{selection-background-color: #f0f0f0;selection-color: #000;} QComboBox QAbstractItemView::item{min-height: 50px;}")
        self.directiveInputSettingLayout.addWidget(self.browserTypeCombobox, 0, 1, 1, 1, Qt.AlignCenter)
        self.browserTypeTipLabel = flowSettingDialog.createTipLabel("浏览器类型","  选择浏览器类型，Google Chrome浏\n  览器、Microsoft Edge浏览器需要\n  安装插件才能实现自动化。另外，\n  如Chrome、Edge或IE安装路径非\n  默认系统盘，需要在\"高级\"选项中设置\n  安装路径")
        self.directiveInputSettingLayout.addWidget(self.browserTypeTipLabel, 0, 2, 1, 1, Qt.AlignLeft)

        self.webUrlLabel = QLabel()
        self.webUrlLabel.setFont(__font)
        self.webUrlLabel.setText("网址:")
        self.directiveInputSettingLayout.addWidget(self.webUrlLabel, 1, 0, 1, 1, Qt.AlignRight)
        self.webUrlLineEdit= QLineEdit()
        self.webUrlLineEdit.setPlaceholderText(u"形如http(s)://www.baidu.com")
        self.webUrlLineEdit.setFont(__font)
        self.webUrlLineEdit.setMinimumSize(600, 50)
        self.directiveInputSettingLayout.addWidget(self.webUrlLineEdit, 1, 1, 1, 1, Qt.AlignCenter)
        self.webUrlFunctionBtn=flowSettingDialog.addFunctionButton(self.webUrlLineEdit, self)
        self.directiveInputSettingLayout.addWidget(self.webUrlFunctionBtn, 1, 1, 1, 1, Qt.AlignRight)
        self.webUrlTipLabel = flowSettingDialog.createTipLabel("网址","  输入需要打开的网址，如\nhttps://www.baidu.com")
        self.directiveInputSettingLayout.addWidget(self.webUrlTipLabel, 1, 2, 1, 1, Qt.AlignLeft)

        self.directiveOutputSettingLayout = QHBoxLayout()
        self.directiveOutputSettingLayout.setSpacing(0)
        self.directiveOutputSettingLayout.setContentsMargins(10, 0, 30, 25)
        self.directiveOutputSettingPanel.setLayout(self.directiveOutputSettingLayout)

        self.saveWebPageObjectLabel = QLabel()
        self.saveWebPageObjectLabel.setFont(__font)
        self.saveWebPageObjectLabel.setText("保存网页对象至:")
        self.directiveOutputSettingLayout.addWidget(self.saveWebPageObjectLabel)
        self.directiveOutputSettingLayout.addSpacing(10)
        self.outputVariableNameLineEdit = QLineEdit()
        self.outputVariableNameLineEdit.setFont(__font)
        self.outputVariableNameLineEdit.setMinimumHeight(50)
        self.outputVariableNameLineEdit.setText("web_page")
        self.directiveOutputSettingLayout.addWidget(self.outputVariableNameLineEdit, 1)
        self.saveWebPageObjectFunctionBtn = flowSettingDialog.addFunctionButton(self.outputVariableNameLineEdit, self)
        self.directiveOutputSettingLayout.addWidget(self.saveWebPageObjectFunctionBtn)
        self.directiveOutputSettingLayout.addSpacing(10)
        self.saveWebPageObjectTipLabel = flowSettingDialog.createTipLabel("保存网页对象至","  该变量保存的是网页对象，使用此网页\n  对象可以对网页进行自动化操作")
        self.directiveOutputSettingLayout.addWidget(self.saveWebPageObjectTipLabel)

    def seniorTabUI(self):
        __font = QFont()
        __font.setPixelSize(20)
        __font.setFamily("Courier")
        self.seniorTab = QWidget()
        self.settingTabWidget.addTab(self.seniorTab, "高级")
        self.seniorTabLayout = QGridLayout()
        self.seniorTab.setLayout(self.seniorTabLayout)
        self.seniorTabLayout.setContentsMargins(10, 30, 30, 30)
        self.seniorTabLayout.setSpacing(10)
        self.seniorTabLayout.setVerticalSpacing(30)

        waitWebPageLoadHLayout = QHBoxLayout()
        self.waitWebLoadCheckbox = QCheckBox()
        self.waitWebLoadCheckbox.setText("等待网页加载完成")
        self.waitWebLoadCheckbox.setFont(__font)
        self.waitWebLoadCheckbox.setChecked(True)
        waitWebPageLoadHLayout.addWidget(self.waitWebLoadCheckbox)
        self.waitWebLoadTipLabel = flowSettingDialog.createTipLabel("等待网页加载完成","  是否等待网页加载完成")
        waitWebPageLoadHLayout.addWidget(self.waitWebLoadTipLabel)
        waitWebPageLoadHLayout.addStretch(1)
        self.seniorTabLayout.addLayout(waitWebPageLoadHLayout, 0, 1, 1, 1, Qt.AlignLeft)

        self.loadTimeOutPeriodLabel = QLabel()
        self.loadTimeOutPeriodLabel.setFont(__font)
        self.loadTimeOutPeriodLabel.setText("加载超时时间:")
        self.seniorTabLayout.addWidget(self.loadTimeOutPeriodLabel, 1, 0, 1, 1,Qt.AlignRight)
        self.loadTimeOutPeriodLineEdit = QLineEdit()
        self.loadTimeOutPeriodLineEdit.setFont(__font)
        self.loadTimeOutPeriodLineEdit.setMinimumSize(600, 50)
        self.seniorTabLayout.addWidget(self.loadTimeOutPeriodLineEdit, 1, 1, 1, 1, Qt.AlignCenter)
        self.loadTimeOutPeriodFunctionBtn = flowSettingDialog.addFunctionButton(self.loadTimeOutPeriodLineEdit, self)
        self.seniorTabLayout.addWidget(self.loadTimeOutPeriodFunctionBtn, 1, 1, 1, 1, Qt.AlignRight)
        self.loadTimeOutPeriodTipLabel = flowSettingDialog.createTipLabel("加载超时时间","  等待网页加载完成的超时时间")
        self.seniorTabLayout.addWidget(self.loadTimeOutPeriodTipLabel, 1, 2, 1, 1,Qt.AlignLeft)

        self.executeAfterLoadTimesOutLabel = QLabel()
        self.executeAfterLoadTimesOutLabel.setFont(__font)
        self.executeAfterLoadTimesOutLabel.setText("加载超时后执行:")
        self.seniorTabLayout.addWidget(self.executeAfterLoadTimesOutLabel, 2, 0, 1, 1,Qt.AlignRight)
        self.executeAfterLoadTimesOutCombobox = QComboBox()
        self.executeAfterLoadTimesOutCombobox.setFont(__font)
        self.executeAfterLoadTimesOutCombobox.setMinimumSize(600, 50)
        self.executeAfterLoadTimesOutCombobox.addItems(["执行\"错误\"处理", "停止网页加载"])
        self.executeAfterLoadTimesOutCombobox.setItemDelegate(QStyledItemDelegate())
        self.executeAfterLoadTimesOutCombobox.setStyleSheet(
            "QComboBox QAbstractItemView{selection-background-color: #f0f0f0;selection-color: #000;} QComboBox QAbstractItemView::item{min-height: 50px;}")
        self.seniorTabLayout.addWidget(self.executeAfterLoadTimesOutCombobox, 2, 1, 1, 1,Qt.AlignCenter)
        self.executeAfterLoadTimesOutTipLabel = flowSettingDialog.createTipLabel("加载超时后执行","  等待网页加载完成超时后希望执行的\n  操作")
        self.seniorTabLayout.addWidget(self.executeAfterLoadTimesOutTipLabel, 2, 2, 1, 1,Qt.AlignLeft)

        self.executeFilePathLabel = QLabel()
        self.executeFilePathLabel.setFont(__font)
        self.executeFilePathLabel.setText(u"执行文件路径:")
        self.seniorTabLayout.addWidget(self.executeFilePathLabel, 3, 0, 1, 1, Qt.AlignRight)
        # 文件路径输入框和选择文件按钮的水平布局
        filePathHLayout = QHBoxLayout()
        filePathHLayout.setContentsMargins(0, 0, 0, 0)
        filePathHLayout.setSpacing(0)
        self.filePathLineEdit = QLineEdit(font=__font)
        self.filePathLineEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.filePathLineEdit.setMinimumHeight(50)
        filePathHLayout.addWidget(self.filePathLineEdit)
        self.selectFileBtn = QPushButton(text=u"选择文件...", font=__font, clicked=self.selectFile)
        self.selectFileBtn.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        filePathHLayout.addWidget(self.selectFileBtn)
        self.seniorTabLayout.addLayout(filePathHLayout, 3, 1, 1, 1, Qt.AlignCenter)
        self.executeFilePathTipLabel = flowSettingDialog.createTipLabel(u"Chrome执行文件路径",
                                                                        u"  我们会在默认根目录C:\Program Files\n  (x86)\Google\Chrome\Application\n  \下启动chrome.exe,也可以在这里手\n  动配置chrome.exe文件路径")
        self.seniorTabLayout.addWidget(self.executeFilePathTipLabel, 3, 2, 1, 1, Qt.AlignLeft)

        self.commandLineParameterLabel = QLabel()
        self.commandLineParameterLabel.setFont(__font)
        self.commandLineParameterLabel.setText("命令行参数:")
        self.seniorTabLayout.addWidget(self.commandLineParameterLabel, 4, 0, 1, 1,Qt.AlignRight)
        self.commandLineParameterLineEdit = QLineEdit()
        self.commandLineParameterLineEdit.setFont(__font)
        self.commandLineParameterLineEdit.setMinimumSize(600, 50)
        self.seniorTabLayout.addWidget(self.commandLineParameterLineEdit, 4, 1, 1, 1, Qt.AlignCenter)
        self.commandLineParameterTipLabel = flowSettingDialog.createTipLabel("命令行参数","  命令行参数，必须是目标浏览器支持的\n  命令行，可空")
        self.seniorTabLayout.addWidget(self.commandLineParameterTipLabel, 4, 2, 1, 1,Qt.AlignLeft)

    def changeSeniorWidgets(self):
        if self.browserTypeCombobox.currentIndex() == 0:
            self.executeFilePathLabel.hide()
            self.filePathLineEdit.hide()
            self.selectFileBtn.hide()
            self.executeFilePathTipLabel.hide()
            self.setFixedHeight(470)
        else:
            if self.browserTypeCombobox.currentIndex() == 1:
                tipLabelTitle = u"Chrome执行文件路径"
                tipLabelText = u"  我们会在默认根目录C:\Program Files\n  (x86)\Google\Chrome\Application\n  \下启动chrome.exe,也可以在这里手\n  动配置chrome.exe文件路径"
            elif self.browserTypeCombobox.currentIndex() == 2:
                tipLabelTitle = u"Edge执行文件路径"
                tipLabelText = u"  我们会在默认根目录C:\Program Files\n  (x86)\Microsoft\Edge\Application\n  \下启动msedge.exe,也可以在这里\n  手动配置msedge.exe文件路径"
            elif self.browserTypeCombobox.currentIndex() == 3:
                tipLabelTitle = u"IE执行文件路径"
                tipLabelText = u"  我们会在默认根目录C:\Program Files\n  \Internet Explorer\..下启动 \n  iexplore.exe,也可以在这里手动配置\n  iexplore.exe文件路径"
            else:
                tipLabelTitle = u"360执行文件路径"
                tipLabelText = u"  我们会在默认根目录下启动360se.exe，\n  也可以在这里手动配置360se.exe文\n  件路径"
            self.filePathLineEdit.setPlaceholderText(tipLabelTitle)
            self.executeFilePathTipLabel.tipLabelQuestionBtn.setText(tipLabelTitle)
            self.executeFilePathTipLabel.tipLabelText.setText(tipLabelText)
            self.executeFilePathLabel.show()
            self.filePathLineEdit.show()
            self.selectFileBtn.show()
            self.executeFilePathTipLabel.show()
            self.setFixedHeight(550)

    def changeTab(self):
        try:
            super().changeTab()
            if self.settingTabWidget.currentWidget() == self.seniorTab:
                self.changeSeniorWidgets()
        except Exception as e:
            print(e)

    # 选择文件
    def selectFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, u"选择文件", "", u"可执行文件 (*.exe)")
        self.filePathLineEdit.setText(fileName)

    def showEvent(self, a0: QShowEvent) -> None:
        if self.isFirstShow:
            self.setFixedHeight(550)
        super().showEvent(a0)
        self.setFixedSize(self.width(), self.height())

    def executeStep(self):
        try:
            browser = self.browserTypeCombobox.currentIndex()
            # Chrome
            if browser == 0:
                client = webSingleCase.WebSingleClass().getFirefoxClient()
            elif browser == 1:
                client = webSingleCase.WebSingleClass().getChromeClient()
            # Edge Chromium
            elif browser == 2:
                client = 1
            # 360
            elif browser == 4:
                if self.filePathLineEdit.text() != None:
                    client = webSingleCase.WebSingleClass().get360Client()
                else:
                    return
            # 其他
            else:
                return
            gvm = globalVariablePanel.GlobalVariablePanel()
            url = replacePlainTextVariable(self.webUrlLineEdit.text(), id)
            if url[0] == '$':
                url = gvm.getVariableByName(url[1:])
            if client.current_url == "about:blank" or client.current_url == "data:,":
                client.get(url)
            else:
                js = "window.open('" + url + "')"
                client.execute_script(js)
            handles = client.window_handles
            client.switch_to.window(handles[-1])
            handle = client.current_window_handle
            self.webSave.webObjectSave(self.outputVariableNameLineEdit.text(), handle, client)
        except Exception as e:
            print(e)

    # 实现确认和取消按钮点击事件
    def handleQuestionBtnClicked(self):
        print("点击使用说明按钮")
    #保存按钮
    def handleConfirmBtnClicked(self):
        self.webSave.webObjectSave(self.outputVariableNameLineEdit.text(), None, None)
        self.updateSettingData()
        self.accept()

    #取消按钮
    def handleCancelBtnClicked(self):
        self.reject()

    #运行按钮
    def handleExecutionBtnClicked(self):
        self.executeStep()

    def updateSettingData(self):
        data = self.directive["data"]
        data["browser_type"] = self.browserTypeCombobox.currentIndex()
        data["url"] = self.webUrlLineEdit.text()
        data["output"] = self.outputVariableNameLineEdit.text()
        data["wait"] = self.waitWebLoadCheckbox.isChecked()
        data["time_out_period"] = self.loadTimeOutPeriodLineEdit.text()
        data["on_time_out"] = self.executeAfterLoadTimesOutCombobox.currentIndex()
        data["cli_parameter"] = self.commandLineParameterLineEdit.text()
        data["exe_path"] = self.filePathLineEdit.text()
        data["log"] = self.printErrorLogsCheckbox.isChecked()
        data["handle"] = self.handleErrorWayCombobox.currentIndex()
        data["on_error_output_value"] = self.onErrorOutputVariableLineEdit.text()
        data["retry_count"] = self.retryCountSpinbox.value()
        data["retry_interval"] = self.retryIntervalSpinbox.value()
        self.updateDirectiveData2DB(self.directive["_id"], data)

    def updateDirectiveData2DB(self, directive_id, data: dict):
        self.directiveDaoObj.updateDirective(directive_id, {"data": data})

    def getDirectiveSettingDataFromDB(self, directive_id):
        return self.directiveDaoObj.getOneDirective(directive_id)["data"]

    def getSettingData(self):
        data = self.getDirectiveSettingDataFromDB(self.directive["_id"])
        self.browserTypeCombobox.setCurrentIndex(data["browser_type"])
        self.webUrlLineEdit.setText(data["url"])
        self.outputVariableNameLineEdit.setText(data["output"])
        self.waitWebLoadCheckbox.setChecked(data["wait"])
        self.loadTimeOutPeriodLineEdit.setText(str(data["time_out_period"]))
        self.executeAfterLoadTimesOutCombobox.setCurrentIndex(data["on_time_out"])
        self.commandLineParameterLineEdit.setText(data["cli_parameter"])
        self.filePathLineEdit.setText(data["exe_path"])
        self.printErrorLogsCheckbox.setChecked(data["log"])
        self.handleErrorWayCombobox.setCurrentIndex(data["handle"])
        self.onErrorOutputVariableLineEdit.setText(data["on_error_output_value"])
        self.retryCountSpinbox.setValue(data["retry_count"])
        self.retryIntervalSpinbox.setValue(data["retry_interval"])
        self.directive["data"] = data

    def serialize(self):
        from collections import OrderedDict
        return OrderedDict([
            ('browser_type',self.browserTypeCombobox.currentIndex()),
            ('url', self.webUrlLineEdit.text()),
            ('output', self.outputVariableNameLineEdit.text()),
            ('wait', self.waitWebLoadCheckbox.isChecked()),
            ('time_out_period', self.loadTimeOutPeriodLineEdit.text()),
            ('on_time_out', self.executeAfterLoadTimesOutCombobox.currentIndex()),
            ('cli_parameter', self.commandLineParameterLineEdit.text()),
            ('exe_path', self.filePathLineEdit.text()),
            ('log', self.printErrorLogsCheckbox.isChecked()),
            ('handle', self.handleErrorWayCombobox.currentIndex()),
            ('on_error_output_value', self.onErrorOutputVariableLineEdit.text()),
            ('retry_count', self.retryCountSpinbox.value()),
            ('retry_interval', self.retryIntervalSpinbox.value())
        ])

    def deserialize(self,data):
        self.browserTypeCombobox.setCurrentIndex(data["browser_type"])
        self.webUrlLineEdit.setText(data["url"])
        self.outputVariableNameLineEdit.setText(data["output"])
        self.waitWebLoadCheckbox.setChecked(data["wait"])
        self.loadTimeOutPeriodLineEdit.setText(str(data["time_out_period"]))
        self.executeAfterLoadTimesOutCombobox.setCurrentIndex(data["on_time_out"])
        self.commandLineParameterLineEdit.setText(data["cli_parameter"])
        self.filePathLineEdit.setText(data["exe_path"])
        self.printErrorLogsCheckbox.setChecked(data["log"])
        self.handleErrorWayCombobox.setCurrentIndex(data["handle"])
        self.onErrorOutputVariableLineEdit.setText(data["on_error_output_value"])
        self.retryCountSpinbox.setValue(data["retry_count"])
        self.retryIntervalSpinbox.setValue(data["retry_interval"])
        self.data = data
        self.accept()