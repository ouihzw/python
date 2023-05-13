# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from com.mat.rpa.utils import webAutoSave
from com.mat.rpa.dao.elementDao import elementDao
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowSettingDialog
from com.mat.rpa.dao.workDao.directiveDao import DirectiveDao
class GettingWebElementObjectSettingDialog(flowSettingDialog.BasicFlowSettingDialog):
    def __init__(self, title, directive_id, id, parent=None):
        super().__init__(title, directive_id, id, parent)
        self.directiveDaoObj = DirectiveDao()
        #参照修改infolabel的提示信息
        self.webSave = webAutoSave.WebAutoSave()
        self.elementDaoMongo = elementDao.ElementDao()
        self.setInfoLabelText("可通过捕获、CSS、XPath三种方式定位网页上的一个元素")
        self.changeImage(flowSettingDialog.BasicFlowSettingDialog.picPath + "setVariableBig.png")
        self.regularTabUI()
        self.seniorTabUI()

        self.errorHandlingTabUI()

        self.settingTabWidget.currentChanged.connect(self.changeTabs)

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

        #下边按照需求布局指令输入控件、指令输出控件、高级和错误Tab
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

        self.locateMethodLabel = QLabel()
        self.locateMethodLabel.setFont(__font)
        self.locateMethodLabel.setText("定位方式:")
        self.directiveInputSettingLayout.addWidget(self.locateMethodLabel, 1, 0, 1, 1, Qt.AlignRight)
        self.locateMethodCombobox = QComboBox()
        self.locateMethodCombobox.setObjectName("browserTypeCombobox")
        self.locateMethodCombobox.setFont(__font)
        self.locateMethodCombobox.setMinimumSize(600, 50)
        self.locateMethodCombobox.addItems(["默认方式", "CSS选择器",
                                           "XPath"])
        self.locateMethodCombobox.setItemDelegate(QStyledItemDelegate())
        self.locateMethodCombobox.setStyleSheet(
            "QComboBox QAbstractItemView{selection-background-color: #f0f0f0;selection-color: #000;} QComboBox QAbstractItemView::item{min-height: 50px;}")
        self.directiveInputSettingLayout.addWidget(self.locateMethodCombobox, 1, 1, 1, 3, Qt.AlignCenter)
        self.locateMethodTipLabel = flowSettingDialog.createTipLabel("定位方式",
                                                                  "  指定一种元素的定位方式")
        self.directiveInputSettingLayout.addWidget(self.locateMethodTipLabel, 1, 4, 1, 1, Qt.AlignLeft)
        # 布局操作目标
        self.objectLabel = QLabel()
        self.objectLabel.setFont(__font)
        self.objectLabel.setText("\u64cd\u4f5c\u76ee\u6807\u003a")
        self.directiveInputSettingLayout.addWidget(self.objectLabel, 2, 0, 1, 1, Qt.AlignRight)
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
        self.directiveInputSettingLayout.addLayout(self.elementLayout, 2, 1, 1, 3, Qt.AlignCenter)
        self.matchWayTipLabel = flowSettingDialog.createTipLabel("操作目标",
                                                                 " 选择要操作的网页元素,若存在相似元素,则会默认选择第一个可见元素。")
        self.directiveInputSettingLayout.addWidget(self.matchWayTipLabel, 2, 4, 1, 1, Qt.AlignLeft)

        self.tinyLayout = QLayout
        self.releventFatherElementCheckbox = QCheckBox()
        self.releventFatherElementCheckbox.setText("关联父元素")
        self.releventFatherElementCheckbox.setFont(__font)
        self.releventFatherElementCheckbox.setChecked(False)
        self.releventFatherElementCheckbox.stateChanged.connect(self.changeRegularTabUI)
        self.directiveInputSettingLayout.addWidget(self.releventFatherElementCheckbox, 3, 1, 1, 1, Qt.AlignCenter)
        self.releventFatherElementTipLabel = flowSettingDialog.createTipLabel("关联父元素", "  是否关联父元素")
        self.directiveInputSettingLayout.addWidget(self.releventFatherElementTipLabel, 3, 2, 1, 1, Qt.AlignLeft)


        self.fatherElementLabel = QLabel()
        self.fatherElementLabel.setFont(__font)
        self.fatherElementLabel.setText("父元素:")
        self.directiveInputSettingLayout.addWidget(self.fatherElementLabel, 4, 0, 1, 1, Qt.AlignLeft)
        self.fatherElementCombobox = QComboBox()
        self.fatherElementCombobox.setFont(__font)
        self.fatherElementCombobox.setMinimumSize(600, 50)
        self.fatherElementCombobox.setEditable(True)  # 设置可以编辑
        self.directiveInputSettingLayout.addWidget(self.fatherElementCombobox, 4, 1, 1, 3, Qt.AlignLeft)
        self.fatherElementTipLabel = flowSettingDialog.createTipLabel("父元素",
                                                                          "  在指定的父元素内查找目标元素")
        self.directiveInputSettingLayout.addWidget(self.fatherElementTipLabel, 4, 4, 1, 1, Qt.AlignLeft)

        self.directiveInputSettingLayout.setColumnStretch(0, 25)
        self.directiveInputSettingLayout.setColumnStretch(1, 15)
        self.directiveInputSettingLayout.setColumnStretch(2, 50)
        self.directiveInputSettingLayout.setColumnStretch(3, 10)



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


        self.fatherElementLabel.hide()
        self.fatherElementCombobox.hide()
        self.fatherElementTipLabel.hide()

        self.directiveOutputSettingLayout.setColumnStretch(0, 25)
        self.directiveOutputSettingLayout.setColumnStretch(1, 15)
        self.directiveOutputSettingLayout.setColumnStretch(2, 50)
        self.directiveOutputSettingLayout.setColumnStretch(3, 10)

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

    def changeRegularTabUI(self):
        if self.releventFatherElementCheckbox.isChecked() is True:
            self.fatherElementLabel.show()
            self.fatherElementCombobox.show()
            self.fatherElementTipLabel.show()


        else:
            self.fatherElementLabel.hide()
            self.fatherElementCombobox.hide()
            self.fatherElementTipLabel.hide()



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
            self.setFixedHeight(self.defaultSize[1])
            self.setFixedWidth(900)
        elif self.settingTabWidget.currentWidget() == self.seniorTab:
            self.setFixedHeight(300)
    #根据需求实现执行指令的显示和点击事件
    #self.executionButton.setVisible(False)  #假如不需要显示就取消注释

    #实现确认和取消按钮点击事件
    def handleQuestionBtnClicked(self):
        print("点击获取信息按钮")

    def handleConfirmBtnClicked(self):
        self.updateSettingData()
        self.accept()

    def handleCancelBtnClicked(self):
        self.reject()

    def handleExecutionBtnClicked(self):
        self.executeStep()

    def updateDirectiveData2DB(self, directive_id, data: dict):
        self.directiveDaoObj.updateDirective(directive_id, {"data": data})

    def getDirectiveSettingDataFromDB(self, directive_id):
        return self.directiveDaoObj.getOneDirective(directive_id)["data"]

    def getSettingData(self):
        data = self.getDirectiveSettingDataFromDB(self.directive["_id"])
        self.browserTypeCombobox.setCurrentIndex(data["browser_type"])
        self.elementLabel.setText(data["element"])
        self.releventFatherElementCheckbox.setChecked(data["value"])
        self.directive["data"] = data

    def updateSettingData(self):
        data = self.directive["data"]
        data["browser_type"] = self.browserTypeCombobox.currentIndex()
        data["element"] = self.elementLabel.text()
        data["value"] = self.releventFatherElementCheckbox.isChecked()
        self.updateDirectiveData2DB(self.directive["_id"], data)
    #def handleExecutionBtnClicked(self): 根据情况实现指令执行按钮事件
    #   print("点击执行按钮)

