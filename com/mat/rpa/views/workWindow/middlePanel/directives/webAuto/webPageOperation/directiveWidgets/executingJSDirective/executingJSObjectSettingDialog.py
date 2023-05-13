# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import re

from com.mat.rpa.dao.workDao.directiveDao import DirectiveDao
from com.mat.rpa.utils import webAutoSave,executingJSObject
from com.mat.rpa.dao.elementDao import elementDao
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowSettingDialog

class ExecutingJSObjectSettingDialog(flowSettingDialog.BasicFlowSettingDialog):
    flowTextList = pyqtSignal(list)
    def __init__(self, title, directive_id, id, parent=None):
        super().__init__(title, directive_id, id,parent)
        self.directiveDaoObj = DirectiveDao()
        self.webSave = webAutoSave.WebAutoSave()
        #不清楚有啥用
        self.elementDaoMongo = elementDao.ElementDao()
        self.executingJSObject = executingJSObject.ExecutingJS()
        self.setInfoLabelText(u"在指定的网页中执行一段Javascript脚本")
        self.changeImage(flowSettingDialog.BasicFlowSettingDialog.picPath + "openWebPageBig.png")
        self.screenWidth = 1920
        self.screenHeight = 1030
        self.setFixedSize(self.screenWidth * 0.485, self.screenHeight * 0.8)
        self.move(self.screenWidth * 0.26, self.screenHeight * 0.03)
        self.regularTabUI()
        self.seniorTabUI()
        self.errorHandlingTabUI()
        self.settingTabWidget.currentChanged.connect(self.changeOpenWebPageObjectSettingDialogSize)
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
        self.directive["data"] = {"web_object": "",
                                  "element_name": "",
                                  "parameter": "",
                                  "javascript": "function(element, input){\n  //在此处编写您的Javascript代码\n  //element表示选择的操作目标(HTML元素)\n  //input表示输入的参数(字符串)\n\n  return null;\n}",
                                  "output": "web_js_result",
                                  "time_out_period": "20",
                                  "log": True,
                                  "handle": 0,
                                  "on_error_output_value": "",
                                  "retry_count": 1,
                                  "retry_interval": 1}
        self.infoFormat = u"在网页%s中的元素%s上执行Javascript，将执行结果保存到%s"

    def regularTabUI(self):
        """
        webObjectLabel:网页对象
        webObjectCombobox:网页对象的选择框
        webObjectTipLabel:网页对象的!提示
        objectLabel:操作目标
        elementLabel:操作目标输入框
        pointoutButton:去元素库选择
        matchWayTipLabel:同样是提示
        parameterLineEdit:参数输入框
        javascriptFunctionTextEdit：js函数输入框
        """
        __font = QFont()
        __font.setPixelSize(20)
        __font.setFamily("Courier")
        # 布局指令输入面板
        self.directiveInputSettingLayout = QGridLayout()
        self.directiveInputSettingLayout.setContentsMargins(70, 0, 20, 0)
        self.directiveInputSettingLayout.setSpacing(10)
        self.directiveInputSettingLayout.setVerticalSpacing(30)
        self.directiveInputSettingPanel.setLayout(self.directiveInputSettingLayout)
        self.webObjectLabel = QLabel()
        self.webObjectLabel.setFont(__font)
        self.webObjectLabel.setText(u"网页对象:")
        self.directiveInputSettingLayout.addWidget(self.webObjectLabel, 0, 0, 1, 1, Qt.AlignRight)
        self.webObjectCombobox = QComboBox()
        self.webObjectCombobox.setObjectName("webObjectCombobox")
        self.webObjectCombobox.setEditable(False)  # 设置不可以编辑
        for i in range(len(self.webSave.getWebObjectName())):
            self.webObjectCombobox.addItem(self.webSave.getWebObjectName()[i])
        self.webObjectCombobox.setFont(__font)
        self.webObjectCombobox.setMinimumSize(600, 50)
        self.webObjectCombobox.setItemDelegate(QStyledItemDelegate())
        self.webObjectCombobox.setStyleSheet(
            "QComboBox QAbstractItemView{selection-background-color: #f0f0f0;selection-color: #000;} QComboBox QAbstractItemView::item{min-height: 50px;}")
        self.directiveInputSettingLayout.addWidget(self.webObjectCombobox, 0, 1, 1, 4, Qt.AlignLeft)
        self.webObjectTipLabel = flowSettingDialog.createTipLabel(u"网页对象",
                                                                  u"  输入一个获取到的或者通过\"打开网\n  页\"创建的网页对象")
        self.directiveInputSettingLayout.addWidget(self.webObjectTipLabel, 0, 5, 1, 1, Qt.AlignLeft)

        self.objectLabel = QLabel()
        self.objectLabel.setFont(__font)
        self.objectLabel.setText(u"操作目标:")
        self.directiveInputSettingLayout.addWidget(self.objectLabel, 1, 0, 1, 1, Qt.AlignRight)
        self.elementLayout = QHBoxLayout()
        self.elementLayout.setContentsMargins(0, 0, 0, 0)
        self.elementLayout.setSpacing(10)
        self.elementLabel = QLineEdit()
        self.elementLabel.setEnabled(False)  # 设置不可以编辑
        self.elementLabel.setFont(__font)
        self.elementLabel.setMinimumSize(390, 50)
        self.elementLayout.addWidget(self.elementLabel, 5)
        self.pointoutButton = flowSettingDialog.readElementFunctionButton(self.elementLabel, self)
        self.elementLayout.addWidget(self.pointoutButton, 1)
        self.directiveInputSettingLayout.addLayout(self.elementLayout, 1, 1, 1, 4, Qt.AlignLeft)
        self.matchWayTipLabel = flowSettingDialog.createTipLabel(u"操作目标",
                                                                 u"  选择要操作的网页元素")
        self.directiveInputSettingLayout.addWidget(self.matchWayTipLabel, 1, 5, 1, 1, Qt.AlignLeft)

        self.parameterLabel= QLabel()
        self.parameterLabel.setFont(__font)
        self.parameterLabel.setText(u"参数:")
        self.directiveInputSettingLayout.addWidget(self.parameterLabel, 4, 0, 1, 1, Qt.AlignRight)
        self.parameterLineEdit = QLineEdit()
        self.parameterLineEdit.setFont(__font)
        self.parameterLineEdit.setMinimumSize(600, 50)
        self.parameterLineEdit.setPlaceholderText("填写要传入到Javascript脚本中的参数")
        self.directiveInputSettingLayout.addWidget(self.parameterLineEdit, 4, 1, 1, 4, Qt.AlignCenter)
        self.parameterFunctionBtn = flowSettingDialog.addFunctionButton(self.parameterLineEdit, self)
        self.directiveInputSettingLayout.addWidget(self.parameterFunctionBtn, 4, 1, 1, 4, Qt.AlignRight)
        self.parameterTipLabel = flowSettingDialog.createTipLabel(u"参数",
                                                                  u"  填写要传入到Javascript脚本中的参\n  数")
        self.directiveInputSettingLayout.addWidget(self.parameterTipLabel, 4, 5, 1, 1, Qt.AlignLeft)

        self.javascriptFunctionLabel = QLabel()
        self.javascriptFunctionLabel.setFont(__font)
        self.javascriptFunctionLabel.setText(u"javascript:")
        self.directiveInputSettingLayout.addWidget(self.javascriptFunctionLabel, 5, 0, 1, 1, Qt.AlignLeft)
        self.javascriptFunctionTextEdit=QTextEdit()
        self.javascriptFunctionTextEdit.setFont(__font)
        self.javascriptFunctionTextEdit.setFixedSize(550,200)
        self.javascriptFunctionTextEdit.setPlainText(
"""function (element, input) {
    // 在此处编写您的Javascript代码
    // element表示选择的操作目标(HTML元素)
    // input表示输入的参数(字符串)
    
    return null;
}
""")
        self.javascriptFunctionTextEdit.setStyleSheet("border-radius:2px;border: 1px solid DarkGray")
        self.directiveInputSettingLayout.addWidget(self.javascriptFunctionTextEdit,5,1,3,3,Qt.AlignLeft)
        self.javascriptFunctionFunctionBtn = flowSettingDialog.addFunctionButton(self.javascriptFunctionTextEdit, self)
        self.directiveInputSettingLayout.addWidget(self.javascriptFunctionFunctionBtn, 5, 3, 1, 2, Qt.AlignRight)
        self.javascriptFunctionTipLabel = flowSettingDialog.createTipLabel(u"javascript",
                                                                  u"  编写一段用于执行的javascript脚本")
        self.directiveInputSettingLayout.addWidget(self.javascriptFunctionTipLabel, 5, 5, 1, 1, Qt.AlignLeft)

        self.directiveInputSettingLayout.setColumnStretch(0, 20)
        self.directiveInputSettingLayout.setColumnStretch(1, 50)
        self.directiveInputSettingLayout.setColumnStretch(2, 5)
        self.directiveInputSettingLayout.setColumnStretch(3,13)
        self.directiveInputSettingLayout.setColumnStretch(4,2)
        self.directiveInputSettingLayout.setColumnStretch(5, 10)




    def seniorTabUI(self):
        __font = QFont()
        __font.setPixelSize(20)
        __font.setFamily("Courier")
        self.seniorTab = QWidget()
        self.settingTabWidget.addTab(self.seniorTab, u"高级")
        self.seniorTabLayout = QGridLayout()
        self.seniorTab.setLayout(self.seniorTabLayout)
        self.seniorTabLayout.setContentsMargins(10, 20, 20, 20)
        self.seniorTabLayout.setSpacing(10)
        self.seniorTabLayout.setVerticalSpacing(20)
        self.seniorTabLayout.setColumnStretch(0, 20)
        self.seniorTabLayout.setColumnStretch(1, 70)
        self.seniorTabLayout.setColumnStretch(2, 10)

        self.waitForElementAppearLabel = QLabel()
        self.waitForElementAppearLabel.setFont(__font)
        self.waitForElementAppearLabel.setText(u"等待元素存在(s):")
        self.seniorTabLayout.addWidget(self.waitForElementAppearLabel, 0, 0, 1, 1, Qt.AlignRight)
        self.waitForElementAppearLineEdit = QLineEdit()
        self.waitForElementAppearLineEdit.setFont(__font)
        self.waitForElementAppearLineEdit.setMinimumSize(600, 50)
        self.waitForElementAppearLineEdit.setText("20")
        self.seniorTabLayout.addWidget(self.waitForElementAppearLineEdit, 0, 1, 1, 1, Qt.AlignCenter)
        self.waitForElementAppearFunctionBtn = flowSettingDialog.addFunctionButton(self.waitForElementAppearLineEdit,
                                                                                   self)
        self.seniorTabLayout.addWidget(self.waitForElementAppearFunctionBtn, 0, 1, 1, 1, Qt.AlignRight)
        self.waitForElementAppearTipLabel = flowSettingDialog.createTipLabel(u"等待元素存在(s)", u"  等待元素存在的超时时间")
        self.seniorTabLayout.addWidget(self.waitForElementAppearTipLabel, 0, 2, 1, 1, Qt.AlignLeft)

    def changeOpenWebPageObjectSettingDialogSize(self):
        if self.settingTabWidget.currentIndex()==0:
            self.setFixedSize(self.screenWidth * 0.485, self.screenHeight * 0.8)
            self.move(self.screenWidth * 0.26, self.screenHeight * 0.05)
        elif self.settingTabWidget.currentIndex()==1:
            self.setFixedSize(self.screenWidth * 0.47, self.screenHeight * 0.28)
            self.center()
        elif self.settingTabWidget.currentIndex()==2:
            if self.handleErrorWayCombobox.currentIndex()==0:
                self.setFixedSize(self.screenWidth * 0.46, self.screenHeight * 0.3)
            elif self.handleErrorWayCombobox.currentIndex() == 1:
                self.setFixedSize(self.screenWidth * 0.46, self.screenHeight * 0.42)
            else:
                self.setFixedSize(self.screenWidth * 0.46, self.screenHeight *  0.37)
            self.center()

    def center(self):
        self.screen = QDesktopWidget().screenGeometry()
        self.size = self.geometry()
        self.move((self.screen.width() - self.size.width()) / 2,
                  (self.screen.height() - self.height()) / 2 - 80)

    def executeStep(self):
        try:
            handle = self.webSave.getWebObjectHandle(self.webObjectCombobox.currentText())
            client = self.webSave.getWebObjectClient(self.webObjectCombobox.currentText())
            client.switch_to.window(handle)
            if self.waitForElementAppearLineEdit.text() =="":
                timeout=0
            else:
                timeout=int(self.waitForElementAppearLineEdit.text())
            webElement = ""
            # elementLabel操作目标
            if self.elementLabel.text() != "":
                WebDriverWait(client,timeout ).until(lambda p: p.find_element(By.XPATH, self.elementDaoMongo.getOneElement(self.elementLabel.text())["xpath"]).is_displayed())
                webElement = client.find_element(By.XPATH,self.elementDaoMongo.getOneElement(self.elementLabel.text())["xpath"])
            script = self.javascriptFunctionTextEdit.toPlainText()
            script = script.lstrip()
            script = script.rstrip()
            script = script.replace("\n", "")
            index = script.find("{")
            functionHeader = script[:index]
            functionHeader = functionHeader.replace(" ","")
            scriptBody = script[index + 1:-1]
            if functionHeader.find("()") != -1:
                elementName = None
                inputName = None
            elif functionHeader.find(",)") != -1:
                reElement = r'function\((.*?),'
                elementName = re.findall(reElement, functionHeader)[0].replace(" ", "")
                inputName = None
            elif functionHeader.find(",") == -1:
                reElement = r'function\((.*?)\)'
                elementName = re.findall(reElement, functionHeader)[0].replace(" ", "")
                inputName = None
            else:
                reElement = r'function\((.*?),'
                reInput = r',(.*?)\)'
                elementName = re.findall(reElement, functionHeader)[0].replace(" ", "")
                inputName = re.findall(reInput, functionHeader)[0].replace(" ", "")
            if inputName is not None and elementName is not None:
                scriptBody = scriptBody.replace(elementName, "arguments[0]")
                scriptBody = scriptBody.replace(inputName, "arguments[1]")
                scriptBody = self.executeStep_removeAnnotation(scriptBody)
                self.executeJSResult=client.execute_script(scriptBody,webElement,self.parameterLineEdit.text())
            elif elementName is not None:
                scriptBody = scriptBody.replace(elementName, "arguments[0]")
                scriptBody = self.executeStep_removeAnnotation(scriptBody)
                self.executeJSResult=client.execute_script(scriptBody, webElement)
            else:
                scriptBody = self.executeStep_removeAnnotation(scriptBody)
                self.executeJSResult = client.execute_script(scriptBody)
            self.executingJSObject.saveExecutingJSObject(self.outputVariableNameLineEdit.text(),self.executeJSResult)
            print(client.execute_script(scriptBody, webElement))
            handles = client.window_handles
            client.switch_to.window(handles[-1])
        except Exception as e:
            print(e)

    # 移去中文注释保证js代码正常运行
    def executeStep_removeAnnotation(self,text):
        scriptBodyText = text
        text1 = "// 在此处编写您的Javascript代码"
        text2 = "// element表示选择的操作目标(HTML元素)"
        text3 = "// input表示输入的参数(字符串)"
        scriptBodyText = scriptBodyText.replace(text1,"")
        scriptBodyText = scriptBodyText.replace(text2,"")
        scriptBodyText = scriptBodyText.replace(text3,"")
        return scriptBodyText

    #实现确认和取消按钮点击事件
    def handleQuestionBtnClicked(self):
        print("点击使用说明按钮")

    def handleConfirmBtnClicked(self):
        self.accept()

    def handleCancelBtnClicked(self):
        self.reject()

    def handleExecutionBtnClicked(self):
        self.executeStep()
