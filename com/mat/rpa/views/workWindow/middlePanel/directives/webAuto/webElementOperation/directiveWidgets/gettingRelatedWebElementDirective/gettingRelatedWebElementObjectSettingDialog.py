# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from com.mat.rpa.utils import webAutoSave
from com.mat.rpa.dao.elementDao import elementDao
from com.mat.rpa.dao.workDao.directiveDao import DirectiveDao
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowSettingDialog
from selenium.webdriver.common.by import By

class GettingRelatedWebElementObjectSettingDialog(flowSettingDialog.BasicFlowSettingDialog):
    def __init__(self, title, directive_id, id, parent=None):
        super().__init__(title, directive_id, id, parent)
        self.directiveDaoObj = DirectiveDao()
        #参照修改infolabel的提示信息
        self.webSave = webAutoSave.WebAutoSave()
        self.elementDaoMongo = elementDao.ElementDao()
        self.setInfoLabelText("在指定的网页中获取元素的关联元素（父元素、子元素、相邻元素）")
        #下边按照需求布局指令输入控件、指令输出控件、高级和错误Tab
        self.regularTabUI()
        self.seniorTabUI()

        self.errorHandlingTabUI()

        self.settingTabWidget.currentChanged.connect(self.changeTabs)
        #根据需求实现执行指令的显示和点击事件
        #self.executionButton.setVisible(False)  #假如不需要显示就取消注释
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
                                  "element": "",
                                  "value": False}

    def regularTabUI(self):
        __font = QFont()
        __font.setPixelSize(20)
        __font.setFamily("Courier")
        self.directiveInputSettingLayout = QGridLayout()
        self.directiveInputSettingLayout.setContentsMargins(50, 0, 20, 0)
        self.directiveInputSettingLayout.setSpacing(10)
        self.directiveInputSettingLayout.setVerticalSpacing(30)
        self.directiveInputSettingPanel.setLayout(self.directiveInputSettingLayout)

        self.browserTypeLabel = QLabel()
        self.browserTypeLabel.setFont(__font)
        self.browserTypeLabel.setText("网页对象:")
        self.directiveInputSettingLayout.addWidget(self.browserTypeLabel, 0, 0, 1, 1, Qt.AlignRight)
        self.browserTypeCombobox = QComboBox()
        self.browserTypeCombobox.setObjectName("browserTypeCombobox")
        self.browserTypeCombobox.setEditable(False)  # 设置不可以编辑
        for i in range(len(self.webSave.getWebObjectName())):
            self.browserTypeCombobox.addItem(self.webSave.getWebObjectName()[i])
        self.browserTypeCombobox.setFont(__font)
        self.browserTypeCombobox.setMinimumSize(600, 50)
        self.browserTypeCombobox.setItemDelegate(QStyledItemDelegate())
        self.browserTypeCombobox.setStyleSheet(
            "QComboBox QAbstractItemView{selection-background-color: #f0f0f0;selection-color: #000;} QComboBox QAbstractItemView::item{min-height: 50px;}")
        self.directiveInputSettingLayout.addWidget(self.browserTypeCombobox, 0, 1, 1, 3, Qt.AlignCenter)
        self.browserTypeTipLabel = flowSettingDialog.createTipLabel("网页对象",
                                                                    "  输入一个获取到的或者通过""打开网页""创建的网页对象")
        self.directiveInputSettingLayout.addWidget(self.browserTypeTipLabel, 0, 4, 1, 1, Qt.AlignLeft)

        # 布局操作目标
        self.objectLabel = QLabel()
        self.objectLabel.setFont(__font)
        self.objectLabel.setText("\u64cd\u4f5c\u76ee\u6807\u003a")
        self.directiveInputSettingLayout.addWidget(self.objectLabel, 1, 0, 1, 1, Qt.AlignRight)
        self.elementLayout = QHBoxLayout()
        self.elementLayout.setSpacing(10)
        self.elementLabel = QLineEdit()
        self.elementLabel.setObjectName("objectLabel")
        self.elementLabel.setEnabled(False)  # 设置不可以编辑
        self.elementLabel.setFont(__font)
        self.elementLabel.setText("(未选择元素)")
        self.elementLabel.setMinimumSize(390, 50)

        self.elementLayout.addWidget(self.elementLabel, 5)
        self.pointoutButton = flowSettingDialog.readElementFunctionButton(self.elementLabel, self)
        self.elementLayout.addWidget(self.pointoutButton, 1)
        self.directiveInputSettingLayout.addLayout(self.elementLayout, 1, 1, 1, 3, Qt.AlignCenter)
        self.matchWayTipLabel = flowSettingDialog.createTipLabel("操作目标",
                                                                 " 选择要操作的网页元素,若存在相似元素,则会默认选择第一个可见元素。")
        self.directiveInputSettingLayout.addWidget(self.matchWayTipLabel, 1, 4, 1, 1, Qt.AlignLeft)

        self.relatedTypeLabel = QLabel()
        self.relatedTypeLabel.setFont(__font)
        self.relatedTypeLabel.setText("关联方式:")
        self.directiveInputSettingLayout.addWidget(self.relatedTypeLabel, 2, 0, 1, 1, Qt.AlignRight)
        self.relatedTypeCombobox = QComboBox()
        self.relatedTypeCombobox.setObjectName("relatedTypeCombobox")
        self.relatedTypeCombobox.setEditable(False)  # 设置不可以编辑
        self.relatedTypeCombobox.addItems(["父元素","子元素","相邻元素"])
        self.relatedTypeCombobox.setFont(__font)
        self.relatedTypeCombobox.setMinimumSize(600, 50)
        self.relatedTypeCombobox.currentIndexChanged.connect(self.relatedTypeComboboxChangedUI)
        self.relatedTypeCombobox.setItemDelegate(QStyledItemDelegate())
        self.relatedTypeCombobox.setStyleSheet(
            "QComboBox QAbstractItemView{selection-background-color: #f0f0f0;selection-color: #000;} QComboBox QAbstractItemView::item{min-height: 50px;}")
        self.directiveInputSettingLayout.addWidget(self.relatedTypeCombobox, 2, 1, 1, 3, Qt.AlignCenter)
        self.relatedTypeTipLabel = flowSettingDialog.createTipLabel("关联方式",
                                                                    "  ")
        self.directiveInputSettingLayout.addWidget(self.relatedTypeTipLabel, 2, 4, 1, 1, Qt.AlignLeft)

        self.getChildMathodLabel = QLabel()
        self.getChildMathodLabel.setFont(__font)
        self.getChildMathodLabel.setText("子元素获取方式:")
        self.directiveInputSettingLayout.addWidget(self.getChildMathodLabel, 3, 0, 1, 1, Qt.AlignRight)
        self.getChildMathodCombobox = QComboBox()
        self.getChildMathodCombobox.setObjectName("getChildMathodCombobox")
        self.getChildMathodCombobox.setEditable(False)  # 设置不可以编辑
        self.getChildMathodCombobox.addItems(["所有子元素", "指定位置的子元素"])
        self.getChildMathodCombobox.setFont(__font)
        self.getChildMathodCombobox.setMinimumSize(600, 50)
        self.getChildMathodCombobox.currentIndexChanged.connect(self.getChildMathodComboboxChangedUI)
        self.getChildMathodCombobox.setItemDelegate(QStyledItemDelegate())
        self.getChildMathodCombobox.setStyleSheet(
            "QComboBox QAbstractItemView{selection-background-color: #f0f0f0;selection-color: #000;} QComboBox QAbstractItemView::item{min-height: 50px;}")
        self.directiveInputSettingLayout.addWidget(self.getChildMathodCombobox, 3, 1, 1, 3, Qt.AlignCenter)
        self.getChildMathodTipLabel = flowSettingDialog.createTipLabel("子元素获取方式",
                                                                    "指定子元素获取方式")
        self.directiveInputSettingLayout.addWidget(self.getChildMathodTipLabel, 3, 4, 1, 1, Qt.AlignLeft)

        self.whichNeighbourLabel = QLabel()
        self.whichNeighbourLabel.setFont(__font)
        self.whichNeighbourLabel.setText("相邻方向:")
        self.directiveInputSettingLayout.addWidget(self.whichNeighbourLabel, 3, 0, 1, 1, Qt.AlignRight)
        self.whichNeighbourCombobox = QComboBox()
        self.whichNeighbourCombobox.setObjectName("whichNeighbourCombobox")
        self.whichNeighbourCombobox.setEditable(False)  # 设置不可以编辑
        self.whichNeighbourCombobox.addItems(["上一个相邻元素", "下一个相邻元素"])
        self.whichNeighbourCombobox.setFont(__font)
        self.whichNeighbourCombobox.setMinimumSize(600, 50)
        self.whichNeighbourCombobox.setItemDelegate(QStyledItemDelegate())
        self.whichNeighbourCombobox.setStyleSheet(
            "QComboBox QAbstractItemView{selection-background-color: #f0f0f0;selection-color: #000;} QComboBox QAbstractItemView::item{min-height: 50px;}")
        self.directiveInputSettingLayout.addWidget(self.whichNeighbourCombobox, 3, 1, 1, 3, Qt.AlignCenter)
        self.whichNeighbourTipLabel = flowSettingDialog.createTipLabel("相邻方向",
                                                                       " ")
        self.directiveInputSettingLayout.addWidget(self.whichNeighbourTipLabel, 3, 4, 1, 1, Qt.AlignLeft)

        self.ChildPositionLabel = QLabel()
        self.ChildPositionLabel.setFont(__font)
        self.ChildPositionLabel.setText("子元素位置:")
        self.directiveInputSettingLayout.addWidget(self.ChildPositionLabel, 4, 0, 1, 1, Qt.AlignRight)
        self.ChildPositionEdit = QLineEdit()
        self.ChildPositionEdit.setText("0")
        self.ChildPositionEdit.setFont(__font)
        self.ChildPositionEdit.setMinimumSize(600, 50)
        self.directiveInputSettingLayout.addWidget(self.ChildPositionEdit, 4, 1, 1, 1, Qt.AlignCenter)
        self.ChildPositionBtn = flowSettingDialog.addFunctionButton(self.ChildPositionEdit, self)
        self.directiveInputSettingLayout.addWidget(self.ChildPositionBtn, 4, 1, 1, 1, Qt.AlignRight)
        self.ChildPositionTipLabel = flowSettingDialog.createTipLabel("子元素位置",
                                                                       "在父元素中的索引位置，从0开始计数")
        self.directiveInputSettingLayout.addWidget(self.ChildPositionTipLabel, 4, 4, 1, 1, Qt.AlignLeft)



        # 输出保存元素对象
        self.directiveOutputSettingLayout = QGridLayout()
        self.directiveOutputSettingLayout.setContentsMargins(50, 0, 20, 20)
        self.directiveOutputSettingLayout.setSpacing(10)
        self.directiveOutputSettingLayout.setVerticalSpacing(30)
        self.directiveOutputSettingPanel.setLayout(self.directiveOutputSettingLayout)

        self.saveElementObjectLabel = QLabel()
        self.saveElementObjectLabel.setFont(__font)
        self.saveElementObjectLabel.setText("保存元素对象至:")
        self.directiveOutputSettingLayout.addWidget(self.saveElementObjectLabel, 0, 0, 1, 1, Qt.AlignLeft)
        self.saveElementObjectCombobox = QComboBox()
        self.saveElementObjectCombobox.setFont(__font)
        self.saveElementObjectCombobox.setMinimumSize(600, 50)
        self.saveElementObjectCombobox.setEditable(True)  # 设置可以编辑
        self.directiveOutputSettingLayout.addWidget(self.saveElementObjectCombobox, 0, 1, 1, 3, Qt.AlignLeft)
        self.saveElementObjectTipLabel = flowSettingDialog.createTipLabel("保存元素对象至",
                                                                          "  指定一个变量名称,该变量用于保存获\n  取到的元素对象")

        self.directiveOutputSettingLayout.addWidget(self.saveElementObjectTipLabel, 0, 4, 1, 1, Qt.AlignLeft)

        self.getChildMathodLabel.hide()
        self.getChildMathodCombobox.hide()
        self.getChildMathodTipLabel.hide()
        self.whichNeighbourLabel.hide()
        self.whichNeighbourCombobox.hide()
        self.whichNeighbourTipLabel.hide()
        self.ChildPositionLabel.hide()
        self.ChildPositionEdit.hide()
        self.ChildPositionBtn.hide()
        self.ChildPositionTipLabel.hide()

        self.directiveOutputSettingLayout.setColumnStretch(0, 25)
        self.directiveOutputSettingLayout.setColumnStretch(1, 15)
        self.directiveOutputSettingLayout.setColumnStretch(2, 50)
        self.directiveOutputSettingLayout.setColumnStretch(3, 10)

    def relatedTypeComboboxChangedUI(self):
        if self.relatedTypeCombobox.currentIndex() == 1:
            self.getChildMathodLabel.show()
            self.getChildMathodCombobox.show()
            self.getChildMathodTipLabel.show()
            self.whichNeighbourLabel.hide()
            self.whichNeighbourCombobox.hide()
            self.whichNeighbourTipLabel.hide()

        elif self.relatedTypeCombobox.currentIndex() == 2:
            self.whichNeighbourLabel.show()
            self.whichNeighbourCombobox.show()
            self.whichNeighbourTipLabel.show()
            self.getChildMathodLabel.hide()
            self.getChildMathodCombobox.hide()
            self.getChildMathodTipLabel.hide()
        else:
            self.getChildMathodLabel.hide()
            self.getChildMathodCombobox.hide()
            self.getChildMathodTipLabel.hide()
            self.whichNeighbourLabel.hide()
            self.whichNeighbourCombobox.hide()
            self.whichNeighbourTipLabel.hide()
            self.ChildPositionLabel.hide()
            self.ChildPositionEdit.hide()
            self.ChildPositionBtn.hide()
            self.ChildPositionTipLabel.hide()

    def getChildMathodComboboxChangedUI(self):
        if  self.getChildMathodCombobox.currentIndex()==1:
            self.ChildPositionLabel.show()
            self.ChildPositionEdit.show()
            self.ChildPositionBtn.show()
            self.ChildPositionTipLabel.show()
        else:
            self.ChildPositionLabel.hide()
            self.ChildPositionEdit.hide()
            self.ChildPositionBtn.hide()
            self.ChildPositionTipLabel.hide()




    def seniorTabUI(self):
        __font = QFont()
        __font.setPixelSize(20)
        __font.setFamily("Courier")
        self.seniorTab = QWidget()
        self.settingTabWidget.addTab(self.seniorTab, "高级")
        self.seniorTabLayout = QGridLayout()
        self.seniorTab.setLayout(self.seniorTabLayout)
        self.seniorTabLayout.setContentsMargins(10, 10, 10, 10)
        self.seniorTabLayout.setSpacing(10)
        self.seniorTabLayout.setVerticalSpacing(30)
        self.executeAfterLoadTimesOut2Label = QLabel()
        self.executeAfterLoadTimesOut2Label.setFont(__font)
        self.executeAfterLoadTimesOut2Label.setText("等待元素存在(s):")
        self.seniorTabLayout.addWidget(self.executeAfterLoadTimesOut2Label, 0, 0, 1, 1, Qt.AlignRight)
        self.executeAfterLoadTimesOut2Combobox = QLineEdit()
        self.executeAfterLoadTimesOut2Combobox.setFont(__font)
        self.executeAfterLoadTimesOut2Combobox.setMinimumSize(600, 50)
        self.executeAfterLoadTimesOut2Combobox.setObjectName("executeAfterLoadTimesOutCombobox")
        self.executeAfterLoadTimesOut2Combobox.setText("20")
        self.seniorTabLayout.addWidget(self.executeAfterLoadTimesOut2Combobox, 0, 1, 1, 3, Qt.AlignCenter)
        self.executeAfterLoadTimesOutTip2Label = flowSettingDialog.createTipLabel("等待元素存在(s)", "  等待目标元素存在的超时时间")
        self.seniorTabLayout.addWidget(self.executeAfterLoadTimesOutTip2Label, 0, 4, 1, 1, Qt.AlignLeft)


    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2 - 80)

    def changeTabs(self):
        # 错误处理页面
        if self.settingTabWidget.currentWidget() == self.errorHandlingTab:
            self.changeErrorHandlingWidgets()
        elif self.settingTabWidget.currentWidget() == self.regularTab:
            self.setFixedHeight(700)
            self.setFixedWidth(900)
        elif self.settingTabWidget.currentWidget() == self.seniorTab:
            self.setFixedHeight(300)

    def executeStep(self):
        try:
            handle = self.webSave.getWebObjectHandle(self.browserTypeCombobox.currentText())
            client = self.webSave.getWebObjectClient(self.browserTypeCombobox.currentText())
            client.switch_to.window(handle)
            webElement = client.find_element(By.XPATH,
                                             self.elementDaoMongo.getOneElement(self.elementLabel.text())["xpath"])
            if self.relatedTypeCombobox.currentIndex() == 0:
                new_xpath=self.elementDaoMongo.getOneElement(self.elementLabel.text())["xpath"]+'/..'
                fatherWebElement=client.find_element(By.XPATH,new_xpath)
                self.elementDict = {"name": self.saveElementObjectCombobox.currentText(), "xpath": new_xpath, "url": client.current_url,
                                    "title": client.title,
                                    "image": " ", "x": fatherWebElement.location['x'], "y": fatherWebElement.location['y'],
                                    "w": fatherWebElement.size['width'],
                                    "h": fatherWebElement.size['height']}
                print(self.elementDict)
                self.elementDaoMongo.insertNewElement(self.elementDict)

            elif self.relatedTypeCombobox.currentIndex() == 1:
                if self.getChildMathodCombobox.currentIndex() == 1:
                    positon=self.ChildPositionEdit.text()
                    new_xpath=self.elementDaoMongo.getOneElement(self.elementLabel.text())["xpath"] + '/*[%s]'%(positon)
                    childWebElement = client.find_element(By.XPATH, new_xpath)
                    self.elementDict = {"name": self.saveElementObjectCombobox.currentText(), "xpath": new_xpath,
                                        "url": client.current_url,
                                        "title": client.title,
                                        "image": " ", "x": childWebElement.location['x'],
                                        "y": childWebElement.location['y'],
                                        "w": childWebElement.size['width'],
                                        "h": childWebElement.size['height']}
                    print(self.elementDict)
                    self.elementDaoMongo.insertNewElement(self.elementDict)
                else:
                    new_xpath=self.elementDaoMongo.getOneElement(self.elementLabel.text())["xpath"]+'/*'
                    childWebElements=client.find_element(By.XPATH,new_xpath)
                    for element in childWebElements:
                        i=1
                        self.elementDict = {"name": self.saveElementObjectCombobox.currentText()+'%d'%(i),
                                            "xpath": new_xpath+'[%d]'%(i),
                                            "url": client.current_url,
                                            "title": client.title,
                                            "image": " ", "x": element.location['x'],
                                            "y": element.location['y'],
                                            "w": element.size['width'],
                                            "h": element.size['height']}
                        print(self.elementDict)
                        self.elementDaoMongo.insertNewElement(self.elementDict)
                        i+=1
            elif self.relatedTypeCombobox.currentIndex() == 2:
                if self.whichNeighbourCombobox.currentIndex()==0:
                    new_xpath=self.elementDaoMongo.getOneElement(self.elementLabel.text())["xpath"]+'/preceding-sibling::*'
                    last_neighbourWebElement=client.find_element(By.XPATH,new_xpath)
                    self.elementDict = {"name": self.saveElementObjectCombobox.currentText(), "xpath": new_xpath,
                                        "url": client.current_url,
                                        "title": client.title,
                                        "image": " ", "x": last_neighbourWebElement.location['x'],
                                        "y": last_neighbourWebElement.location['y'],
                                        "w": last_neighbourWebElement.size['width'],
                                        "h": last_neighbourWebElement.size['height']}
                    print(self.elementDict)
                    self.elementDaoMongo.insertNewElement(self.elementDict)
                if self.whichNeighbourCombobox.currentIndex()==1:
                    new_xpath= self.elementDaoMongo.getOneElement(self.elementLabel.text())["xpath"]+'/following::*'
                    next_neighbourWebElement=client.find_element(By.XPATH,new_xpath)
                    self.elementDict = {"name": self.saveElementObjectCombobox.currentText(), "xpath": new_xpath,
                                        "url": client.current_url,
                                        "title": client.title,
                                        "image": " ", "x": next_neighbourWebElement.location['x'],
                                        "y": next_neighbourWebElement.location['y'],
                                        "w": next_neighbourWebElement.size['width'],
                                        "h": next_neighbourWebElement.size['height']}
                    print(self.elementDict)
                    self.elementDaoMongo.insertNewElement(self.elementDict)
        except Exception as e:
            print(e)

    # 根据需求实现执行指令的显示和点击事件
    # self.executionButton.setVisible(False)  #假如不需要显示就取消注释
    #实现确认和取消按钮点击事件
    # 实现确认和取消按钮点击事件
    def handleQuestionBtnClicked(self):
        print("点击获取信息按钮")

    def handleConfirmBtnClicked(self):
        #self.updateSettingData()
        self.accept()

    def handleCancelBtnClicked(self):
        self.reject()

    def handleExecutionBtnClicked(self):
        self.executeStep()

    # def updateDirectiveData2DB(self, directive_id, data: dict):
    #     self.directiveDaoObj.updateDirective(directive_id, {"data": data})
    #
    # def getDirectiveSettingDataFromDB(self, directive_id):
    #     return self.directiveDaoObj.getOneDirective(directive_id)["data"]
    #
    # def getSettingData(self):
    #     data = self.getDirectiveSettingDataFromDB(self.directive["_id"])
    #     self.browserTypeCombobox.setCurrentIndex(data["browser_type"])
    #     self.elementLabel.setText(data["element"])
    #     self.releventFatherElementCheckbox.setChecked(data["value"])
    #     self.directive["data"] = data
    #
    # def updateSettingData(self):
    #     data = self.directive["data"]
    #     data["browser_type"] = self.browserTypeCombobox.currentIndex()
    #     data["element"] = self.elementLabel.text()
    #     data["value"] = self.releventFatherElementCheckbox.isChecked()
    #     self.updateDirectiveData2DB(self.directive["_id"], data)
    # # def handleExecutionBtnClicked(self): 根据情况实现指令执行按钮事件
    # #   print("点击执行按钮)

    def serialize(self):
        from collections import OrderedDict
        return OrderedDict([
            ('browser_type', self.browserTypeCombobox.currentIndex()),
            ('element', self.elementLabel.text()),
            ('relatedMathod', self.relatedTypeCombobox.currentIndex()),
            ('getchild', self.getChildMathodCombobox.currentIndex()),
            ('childposition', self.ChildPositionLabel.text()),
            ('neighbor', self.whichNeighbourCombobox.currentIndex()),
            ('save', self.saveElementObjectCombobox.currentText()),
        ])

    def deserialize(self, data):
        self.browserTypeCombobox.setCurrentIndex(data["browser_type"])
        self.elementLabel.setText(data["element"])
        self.relatedTypeCombobox.setCurrentIndex(data["relatedMathod"])
        self.getChildMathodCombobox.setCurrentIndex(data["getchild"])
        self.ChildPositionLabel.setText(data["childposition"])
        self.whichNeighbourCombobox.setCurrentIndex(data["neighbor"])
        self.saveElementObjectCombobox.setCurrentText(data["save"])
        self.data = data
        self.accept()

