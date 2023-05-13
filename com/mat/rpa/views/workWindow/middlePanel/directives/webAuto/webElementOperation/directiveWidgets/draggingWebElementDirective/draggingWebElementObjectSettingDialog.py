# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowSettingDialog
from com.mat.rpa.utils import webAutoSave
from com.mat.rpa.dao.elementDao import elementDao
from selenium.webdriver.common.by import By
import time
import pyautogui
from selenium.webdriver.common.action_chains import ActionChains
from com.mat.rpa.dao.workDao.directiveDao import DirectiveDao
class DraggingWebElementObjectSettingDialog(flowSettingDialog.BasicFlowSettingDialog):
    flowTextList = pyqtSignal(list)
    def __init__(self, title, directive_id, id, parent=None):
        super().__init__(title, directive_id, id, parent)
        self.directiveDaoObj = DirectiveDao()
        self.webSave = webAutoSave.WebAutoSave()
        self.elementDaoMongo = elementDao.ElementDao()
        self.setInfoLabelText("在指定的网页中将元素拖拽到指定位置")
        __font = QFont()
        __font.setPixelSize(20)
        __font.setFamily("Courier")
        self.screenWidth = 1920
        self.screenHeight = 1030
        self.setFixedSize(self.screenWidth * 0.46, self.screenHeight * 0.8)
        self.center()
        # 改变图片
        self.changeImage(flowSettingDialog.BasicFlowSettingDialog.picPath + "openWebPageBig.png")
        self.seniorTab = QWidget()
        self.settingTabWidget.addTab(self.seniorTab, u"\u9ad8\u7ea7")
        self.errorHandingTab = QWidget()
        self.settingTabWidget.addTab(self.errorHandingTab, u"\u9519\u8bef\u5904\u7406")
        self.regularTabUI()
        self.seniorTabUI()
        self.errorHandingTabUI()
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

    def regularTabUI(self):
        __font = QFont()
        __font.setPixelSize(20)
        __font.setFamily("Courier")
        # 布局指令输入面板
        self.directiveInputSettingLayout = QGridLayout()
        self.directiveInputSettingLayout.setContentsMargins(50, 0, 20, 0)
        self.directiveInputSettingLayout.setSpacing(10)
        self.directiveInputSettingLayout.setVerticalSpacing(30)
        self.directiveInputSettingPanel.setLayout(self.directiveInputSettingLayout)

        self.browserTypeLabel = QLabel()
        self.browserTypeLabel.setFont(__font)
        self.browserTypeLabel.setText(u"\u7f51\u9875\u5bf9\u8c61\u003a")
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
        self.directiveInputSettingLayout.addWidget(self.browserTypeCombobox, 0, 1, 1, 2, Qt.AlignLeft)
        self.browserTypeTipLabel = flowSettingDialog.createTipLabel("\u7f51\u9875\u5bf9\u8c61",
                                                                    "  \u8f93\u5165\u4e00\u4e2a\u83b7\u53d6\u5230\u7684\u6216\u8005\u901a\u8fc7\u201c\u6253\u5f00\u7f51\n  \u9875\u201d\u521b\u5efa\u7684\u7f51\u9875\u5bf9\u8c61")
        self.directiveInputSettingLayout.addWidget(self.browserTypeTipLabel, 0, 3, 1, 1, Qt.AlignLeft)

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
        self.elementLabel.setMinimumSize(390, 50)
        self.elementLayout.addWidget(self.elementLabel, 5)
        self.pointoutButton = flowSettingDialog.readElementFunctionButton(self.elementLabel, self)
        self.elementLayout.addWidget(self.pointoutButton, 1)
        self.directiveInputSettingLayout.addLayout(self.elementLayout, 1, 1, 1, 2, Qt.AlignLeft)
        self.matchWayTipLabel = flowSettingDialog.createTipLabel("\u64cd\u4f5c\u76ee\u6807",
                                                                 "  \u9009\u62e9\u8981\u64cd\u4f5c\u7684\u7f51\u9875\u5143\u7d20")
        self.directiveInputSettingLayout.addWidget(self.matchWayTipLabel, 1, 3, 1, 1, Qt.AlignLeft)

        self.dragTypeLabel = QLabel()
        self.dragTypeLabel.setFont(__font)
        self.dragTypeLabel.setText("拖拽方式:")
        self.directiveInputSettingLayout.addWidget(self.dragTypeLabel, 2, 0, 1, 1, Qt.AlignRight)
        self.dragCombobox = QComboBox()
        self.dragCombobox.setObjectName("dragCombobox")
        self.dragCombobox.setFont(__font)
        self.dragCombobox.setMinimumSize(600, 50)
        self.dragCombobox.addItems(["拖拽至目标点", "拖拽至目标元素上"])
        self.dragCombobox.setItemDelegate(QStyledItemDelegate())
        self.dragCombobox.setStyleSheet(
            "QComboBox QAbstractItemView{selection-background-color: #f0f0f0;selection-color: #000;} QComboBox QAbstractItemView::item{min-height: 50px;}")
        self.dragCombobox.currentIndexChanged.connect(self.changeRegularWidgets)
        self.directiveInputSettingLayout.addWidget(self.dragCombobox, 2, 1, 1, 2, Qt.AlignCenter)
        self.dragTypeTipLabel = flowSettingDialog.createTipLabel("拖拽方式", " ")
        self.directiveInputSettingLayout.addWidget(self.dragTypeTipLabel, 2, 3, 1, 1, Qt.AlignLeft)

        self.dragXLabel = QLabel()
        self.dragXLabel.setFont(__font)
        self.dragXLabel.setText("X:")
        self.directiveInputSettingLayout.addWidget(self.dragXLabel, 3, 0, 1, 1, Qt.AlignRight)
        self.dragXLineEdit = QLineEdit()
        self.dragXLineEdit.setFont(__font)
        self.dragXLineEdit.setMinimumSize(600, 50)
        self.directiveInputSettingLayout.addWidget(self.dragXLineEdit, 3, 1, 1, 2, Qt.AlignCenter)
        self.dragXFunctionBtn = flowSettingDialog.addFunctionButton(self.dragXLineEdit, self)
        self.directiveInputSettingLayout.addWidget(self.dragXFunctionBtn, 3, 1, 1, 2, Qt.AlignRight)
        self.dragXTipLabel = flowSettingDialog.createTipLabel("X", "鼠标移动到的目标位置的横坐标")
        self.directiveInputSettingLayout.addWidget(self.dragXTipLabel, 3, 3, 1, 1, Qt.AlignLeft)

        self.dragYLabel = QLabel()
        self.dragYLabel.setFont(__font)
        self.dragYLabel.setText("Y:")
        self.directiveInputSettingLayout.addWidget(self.dragYLabel, 4, 0, 1, 1, Qt.AlignRight)
        self.dragYLineEdit = QLineEdit()
        self.dragYLineEdit.setFont(__font)
        self.dragYLineEdit.setMinimumSize(600, 50)
        self.directiveInputSettingLayout.addWidget(self.dragYLineEdit, 4, 1, 1, 2, Qt.AlignCenter)
        self.dragYFunctionBtn = flowSettingDialog.addFunctionButton(self.dragYLineEdit, self)
        self.directiveInputSettingLayout.addWidget(self.dragYFunctionBtn, 4, 1, 1, 2, Qt.AlignRight)
        self.dragYTipLabel = flowSettingDialog.createTipLabel("Y", "鼠标移动到的目标位置的纵坐标")
        self.directiveInputSettingLayout.addWidget(self.dragYTipLabel, 4, 3, 1, 1, Qt.AlignLeft)

        self.mousePosLabel = QLabel()
        self.mousePosLabel.setFont(__font)
        self.thread = WorkThread()
        self.thread.start()
        self.thread.trigger.connect(self.posShow)
        self.directiveInputSettingLayout.addWidget(self.mousePosLabel, 5, 0, 1, 3, Qt.AlignRight)

        # 设置表格三列的比例
        self.directiveInputSettingLayout.setColumnStretch(0, 20)
        self.directiveInputSettingLayout.setColumnStretch(1, 15)
        self.directiveInputSettingLayout.setColumnStretch(2, 55)
        self.directiveInputSettingLayout.setColumnStretch(3, 10)

        outputHLayout = QHBoxLayout(self.directiveOutputSettingPanel)
        self.directiveOutputSettingPanel.setLayout(outputHLayout)
        nothingOutputLabel = QLabel(text="(当前指令不包含任何输出项)", font=__font)
        outputHLayout.addWidget(nothingOutputLabel, 1, Qt.AlignCenter)
        outputHLayout.setContentsMargins(0, 20, 0, 40)

    def changeRegularWidgets(self):
        __font = QFont()
        __font.setPixelSize(20)
        __font.setFamily("Courier")
        if self.dragCombobox.currentIndex() == 1:
            self.dragXLabel.hide()
            self.dragXLineEdit.hide()
            self.dragXFunctionBtn.hide()
            self.dragXTipLabel.hide()
            self.dragYLabel.hide()
            self.dragYLineEdit.hide()
            self.dragYFunctionBtn.hide()
            self.dragYTipLabel.hide()
            self.mousePosLabel.hide()
            self.object2Label = QLabel()
            self.object2Label.setFont(__font)
            self.object2Label.setText("\u64cd\u4f5c\u76ee\u6807\u003a")
            self.directiveInputSettingLayout.addWidget(self.object2Label, 3, 0, 1, 1, Qt.AlignRight)
            self.element2Layout = QHBoxLayout()
            self.element2Layout.setSpacing(10)
            self.element2Label = QLineEdit()
            self.element2Label.setObjectName("object2Label")
            self.element2Label.setEnabled(False)  # 设置不可以编辑
            self.element2Label.setFont(__font)
            self.element2Label.setMinimumSize(390, 50)
            self.element2Layout.addWidget(self.element2Label, 5)
            self.pointout2Button = flowSettingDialog.readElementFunctionButton(self.element2Label, self)
            self.element2Layout.addWidget(self.pointout2Button, 1)
            self.directiveInputSettingLayout.addLayout(self.element2Layout, 3, 1, 1, 2, Qt.AlignLeft)
            self.matchWay2TipLabel = flowSettingDialog.createTipLabel("\u64cd\u4f5c\u76ee\u6807",
                                                                      "  \u9009\u62e9\u8981\u64cd\u4f5c\u7684\u7f51\u9875\u5143\u7d20")
            self.directiveInputSettingLayout.addWidget(self.matchWay2TipLabel, 3, 3, 1, 1, Qt.AlignLeft)
        else:
            self.object2Label.hide()
            self.element2Label.hide()
            self.pointout2Button.hide()
            self.matchWay2TipLabel.hide()
            self.dragXLabel = QLabel()
            self.dragXLabel.setFont(__font)
            self.dragXLabel.setText("X:")
            self.directiveInputSettingLayout.addWidget(self.dragXLabel, 3, 0, 1, 1, Qt.AlignRight)
            self.dragXLineEdit = QLineEdit()
            self.dragXLineEdit.setFont(__font)
            self.dragXLineEdit.setMinimumSize(600, 50)
            self.directiveInputSettingLayout.addWidget(self.dragXLineEdit, 3, 1, 1, 2, Qt.AlignCenter)
            self.dragXFunctionBtn = flowSettingDialog.addFunctionButton(self.dragXLineEdit, self)
            self.directiveInputSettingLayout.addWidget(self.dragXFunctionBtn, 3, 1, 1, 2, Qt.AlignRight)
            self.dragXTipLabel = flowSettingDialog.createTipLabel("X", "鼠标移动到的目标位置的横坐标")
            self.directiveInputSettingLayout.addWidget(self.dragXTipLabel, 3, 3, 1, 1, Qt.AlignLeft)

            self.dragYLabel = QLabel()
            self.dragYLabel.setFont(__font)
            self.dragYLabel.setText("Y:")
            self.directiveInputSettingLayout.addWidget(self.dragYLabel, 4, 0, 1, 1, Qt.AlignRight)
            self.dragYLineEdit = QLineEdit()
            self.dragYLineEdit.setFont(__font)
            self.dragYLineEdit.setMinimumSize(600, 50)
            self.directiveInputSettingLayout.addWidget(self.dragYLineEdit, 4, 1, 1, 2, Qt.AlignCenter)
            self.dragYFunctionBtn = flowSettingDialog.addFunctionButton(self.dragYLineEdit, self)
            self.directiveInputSettingLayout.addWidget(self.dragYFunctionBtn, 4, 1, 1, 2, Qt.AlignRight)
            self.dragYTipLabel = flowSettingDialog.createTipLabel("Y", "鼠标移动到的目标位置的纵坐标")
            self.directiveInputSettingLayout.addWidget(self.dragYTipLabel, 4, 3, 1, 1, Qt.AlignLeft)

            self.mousePosLabel = QLabel()
            self.mousePosLabel.setFont(__font)
            self.thread = WorkThread()
            self.thread.start()
            self.thread.trigger.connect(self.posShow)
            self.directiveInputSettingLayout.addWidget(self.mousePosLabel, 5, 0, 1, 3, Qt.AlignRight)


    def seniorTabUI(self):
        __font = QFont()
        __font.setPixelSize(20)
        __font.setFamily("Courier")
        self.seniorTabLayout = QGridLayout()
        self.seniorTab.setLayout(self.seniorTabLayout)
        self.seniorTabLayout.setContentsMargins(10, 20, 20, 20)
        self.seniorTabLayout.setSpacing(10)
        self.seniorTabLayout.setVerticalSpacing(20)
        self.seniorTabLayout.setColumnStretch(0, 20)
        self.seniorTabLayout.setColumnStretch(1, 15)
        self.seniorTabLayout.setColumnStretch(2, 55)
        self.seniorTabLayout.setColumnStretch(3, 10)

        self.delayTimeLabel = QLabel()
        self.delayTimeLabel.setText("延迟时间(s):")
        self.seniorTabLayout.addWidget(self.delayTimeLabel, 0, 0, 1, 1, Qt.AlignRight)
        self.delayTimeLineEdit = QLineEdit()
        self.delayTimeLineEdit.setFont(__font)
        self.delayTimeLineEdit.setMinimumSize(590, 50)
        self.seniorTabLayout.addWidget(self.delayTimeLineEdit, 0, 1, 1, 2, Qt.AlignCenter)
        self.delayTimeFunctionBtn = flowSettingDialog.addFunctionButton(self.delayTimeLineEdit, self)
        self.seniorTabLayout.addWidget(self.delayTimeFunctionBtn, 0, 1, 1, 2, Qt.AlignRight)
        self.delayTimeTipLabel = flowSettingDialog.createTipLabel("延迟时间(s)",  "  执行指令完成后的等待时间")
        self.seniorTabLayout.addWidget(self.delayTimeTipLabel, 0, 3, 1, 1, Qt.AlignLeft)

        self.pressPosLabel = QLabel()
        self.pressPosLabel.setFont(__font)
        self.pressPosLabel.setText("鼠标按下位置:")
        self.seniorTabLayout.addWidget(self.pressPosLabel, 1, 0, 1, 1, Qt.AlignRight)
        self.pressPosCombobox = QComboBox()
        self.pressPosCombobox.setFont(__font)
        self.pressPosCombobox.setMinimumSize(600, 50)
        self.pressPosCombobox.addItems(["中心点", "随机位置", "自定义"])
        self.pressPosCombobox.setItemDelegate(QStyledItemDelegate())
        self.pressPosCombobox.setStyleSheet(
            "QComboBox QAbstractItemView{selection-background-color: #f0f0f0;selection-color: #000;} QComboBox QAbstractItemView::item{min-height: 50px;}")
        self.seniorTabLayout.addWidget(self.pressPosCombobox, 1, 1, 1, 2, Qt.AlignCenter)
        self.pressPosTipLabel = flowSettingDialog.createTipLabel("鼠标按下位置锚点", "  支持鼠标在拖拽元素中心位置、随机\n  位置（在元素矩形范围内）、自定义位置\n  处按下")
        self.seniorTabLayout.addWidget(self.pressPosTipLabel, 1, 3, 1, 1, Qt.AlignLeft)

        self.dropPosLabel = QLabel()
        self.dropPosLabel.setFont(__font)
        self.dropPosLabel.setText("鼠标释放位置:")
        self.seniorTabLayout.addWidget(self.dropPosLabel, 2, 0, 1, 1, Qt.AlignRight)
        self.dropPosCombobox = QComboBox()
        self.dropPosCombobox.setFont(__font)
        self.dropPosCombobox.setMinimumSize(600, 50)
        self.dropPosCombobox.addItems(["中心点", "随机位置", "自定义"])
        self.dropPosCombobox.setItemDelegate(QStyledItemDelegate())
        self.dropPosCombobox.setStyleSheet(
            "QComboBox QAbstractItemView{selection-background-color: #f0f0f0;selection-color: #000;} QComboBox QAbstractItemView::item{min-height: 50px;}")
        self.seniorTabLayout.addWidget(self.dropPosCombobox, 2, 1, 1, 2, Qt.AlignCenter)
        self.dropPosTipLabel = flowSettingDialog.createTipLabel("鼠标释放位置锚点",
                                                                 "  支持鼠标在拖拽至元素中心位置、\n  随机位置（在元素矩形范围内）、自定义\n  位置释放")
        self.seniorTabLayout.addWidget(self.dropPosTipLabel, 2, 3, 1, 1, Qt.AlignLeft)

        self.waitTimeLabel = QLabel()
        self.waitTimeLabel.setText("等待元素存在(s):")
        self.seniorTabLayout.addWidget(self.waitTimeLabel, 3, 0, 1, 1)
        self.waitTimeLineEdit = QLineEdit()
        self.waitTimeLineEdit.setFont(__font)
        self.waitTimeLineEdit.setMinimumSize(590, 50)
        self.seniorTabLayout.addWidget(self.waitTimeLineEdit, 3, 1, 1, 2, Qt.AlignCenter)
        self.waitTimeFunctionBtn = flowSettingDialog.addFunctionButton(self.waitTimeLineEdit, self)
        self.seniorTabLayout.addWidget(self.waitTimeFunctionBtn, 3, 1, 1, 2, Qt.AlignRight)
        self.waitTimeTipLabel = flowSettingDialog.createTipLabel("等待元素存在(s)", "  等待目标元素存在的超时时间")
        self.seniorTabLayout.addWidget(self.waitTimeTipLabel, 3, 3, 1, 1, Qt.AlignLeft)

    def posShow(self, posList):
        self.posX = str(posList[0])
        self.posY = str(posList[1])
        self.mousePosLabel.setText('当前鼠标位置(相对于屏幕左上角): X= ' + self.posX + ' Y= ' + self.posY
                                   + '    按Ctrl+Alt输入坐标')  # 打印坐标
        return posList

    def keyPressEvent(self, event):
        modifiers = event.modifiers()
        if modifiers == Qt.ControlModifier|Qt.AltModifier:
            self.dragXLineEdit.setText(self.posX)
            self.dragYLineEdit.setText(self.posY)

    def errorHandingTabUI(self):
        __font = QFont()
        __font.setPixelSize(20)
        __font.setFamily("Courier")
        self.errorHandingLayout = QGridLayout()
        self.errorHandingTab.setLayout(self.errorHandingLayout)
        self.errorHandingLayout.setContentsMargins(10, 20, 0, 20)
        self.errorHandingLayout.setSpacing(10)
        self.errorHandingLayout.setVerticalSpacing(20)
        self.errorHandingLayout.setColumnStretch(0, 20)
        self.errorHandingLayout.setColumnStretch(1, 7)
        self.errorHandingLayout.setColumnStretch(2, 7)
        self.errorHandingLayout.setColumnStretch(3, 3)
        self.errorHandingLayout.setColumnStretch(4, 10)
        self.errorHandingLayout.setColumnStretch(5, 10)
        self.errorHandingLayout.setColumnStretch(6, 31)
        self.errorHandingLayout.setColumnStretch(7, 10)

        self.printErrorLogsCheckbox = QCheckBox()
        self.printErrorLogsCheckbox.setText("打印错误日志")
        self.printErrorLogsCheckbox.setFont(__font)
        self.printErrorLogsCheckbox.setChecked(True)
        self.errorHandingLayout.addWidget(self.printErrorLogsCheckbox, 0, 1, 1, 2, Qt.AlignLeft)
        self.printErrorLogsTipLabel = flowSettingDialog.createTipLabel("打印错误日志", "  当出现错误时打印错误日志到日志面\n  版")
        self.errorHandingLayout.addWidget(self.printErrorLogsTipLabel, 0, 3, 1, 1, Qt.AlignLeft)

        self.handleErrorWayLabel = QLabel()
        self.handleErrorWayLabel.setFont(__font)
        self.handleErrorWayLabel.setText("处理方式")
        self.errorHandingLayout.addWidget(self.handleErrorWayLabel, 1, 0, 1, 1, Qt.AlignRight)
        self.handleErrorWayCombobox = QComboBox()
        self.handleErrorWayCombobox.setFont(__font)
        self.handleErrorWayCombobox.setMinimumSize(600, 50)
        self.handleErrorWayCombobox.setObjectName("handleErrorWayCombobox")
        self.handleErrorWayCombobox.addItems(["终止流程", "忽略异常并继续执行", "重试此指令"])
        self.handleErrorWayCombobox.setItemDelegate(QStyledItemDelegate())
        self.handleErrorWayCombobox.setStyleSheet(
            "QComboBox QAbstractItemView{selection-background-color: #f0f0f0;selection-color: #000;} QComboBox QAbstractItemView::item{min-height: 50px;}")
        self.handleErrorWayCombobox.currentIndexChanged.connect(self.changeErrorHandingTab)
        self.errorHandingLayout.addWidget(self.handleErrorWayCombobox, 1, 1, 1, 6, Qt.AlignCenter)
        self.handleErrorWayTipLabel = flowSettingDialog.createTipLabel("选择错误处理方式",
                                                                       "  选择错误处理方式，当出现错误时默\n  认终止流程，也可以选择忽略错误或\n  者重试当前指令")
        self.errorHandingLayout.addWidget(self.handleErrorWayTipLabel, 1, 7, 1, 1, Qt.AlignLeft)

    def changeErrorHandingTab(self):
        __font = QFont()
        __font.setPixelSize(20)
        __font.setFamily("Courier")
        if self.handleErrorWayCombobox.currentIndex() == 0:
            i = 8
            while i > 4:
                item = self.errorHandingLayout.itemAt(i)
                i -= 1
                if item:
                    self.errorHandingLayout.removeItem(item)
                    item.widget().deleteLater()
            self.setFixedSize(self.screenWidth * 0.44, self.screenHeight * 0.3)
        elif self.handleErrorWayCombobox.currentIndex() == 1:
            i = 8
            while i > 4:
                item = self.errorHandingLayout.itemAt(i)
                i -= 1
                if item:
                    self.errorHandingLayout.removeItem(item)
                    item.widget().deleteLater()
            self.blankLabel = QLabel()
            self.blankLabel.setMaximumHeight(0)
            self.errorHandingLayout.addWidget(self.blankLabel, 2, 0, 1, 1, Qt.AlignRight)
            self.outputValueOfInstructionLabel = QLabel()
            self.outputValueOfInstructionLabel.setFont(__font)
            self.outputValueOfInstructionLabel.setText("设置异常情况下指令的输出值")
            self.outputValueOfInstructionLabel.setStyleSheet("color:#808080;")
            self.errorHandingLayout.addWidget(self.outputValueOfInstructionLabel, 3, 1, 1, 7, Qt.AlignLeft)
            self.webPageFunctionLabel = QLabel()
            self.webPageFunctionLabel.setFont(__font)
            self.webPageFunctionLabel.setText("web_page:")
            self.errorHandingLayout.addWidget(self.webPageFunctionLabel, 4, 1, 1, 2, Qt.AlignRight)
            self.webPageFunctionCombobox = QComboBox()
            self.webPageFunctionCombobox.setFont(__font)
            self.webPageFunctionCombobox.setMinimumSize(400, 50)
            self.webPageFunctionCombobox.setEditable(True)  # 设置可以编辑
            self.errorHandingLayout.addWidget(self.webPageFunctionCombobox, 4, 3, 1, 4, Qt.AlignLeft)
            self.setFixedSize(self.screenWidth * 0.44, self.screenHeight * 0.42)
        elif self.handleErrorWayCombobox.currentIndex() == 2:
            i = 8
            while i > 4:
                item = self.errorHandingLayout.itemAt(i)
                i -= 1
                if item:
                    self.errorHandingLayout.removeItem(item)
                    item.widget().deleteLater()
            self.retryCountLabel = QLabel()
            self.retryCountLabel.setFont(__font)
            self.retryCountLabel.setText("重试次数")
            self.errorHandingLayout.addWidget(self.retryCountLabel, 2, 1, 1, 1, Qt.AlignLeft)
            self.retryCountSpinbox = QSpinBox()
            self.retryCountSpinbox.setFont(__font)
            self.retryCountSpinbox.setMinimumSize(7, 50)
            self.retryCountSpinbox.setMinimum(1)
            self.retryCountSpinbox.setMaximum(100000000)
            self.retryCountSpinbox.setValue(3)
            self.errorHandingLayout.addWidget(self.retryCountSpinbox, 2, 2, 1, 1, Qt.AlignLeft)
            self.retryIntervalLabel = QLabel()
            self.retryIntervalLabel.setFont(__font)
            self.retryIntervalLabel.setText("重试间隔(秒)")
            self.errorHandingLayout.addWidget(self.retryIntervalLabel, 2, 4, 1, 1, Qt.AlignCenter)
            self.retryIntervalSpinbox = QSpinBox()
            self.retryIntervalSpinbox.setFont(__font)
            self.retryIntervalSpinbox.setMinimumSize(7, 50)
            self.retryIntervalSpinbox.setMinimum(1)
            self.retryIntervalSpinbox.setMaximum(100000000)
            self.retryIntervalSpinbox.setValue(3)
            self.errorHandingLayout.addWidget(self.retryIntervalSpinbox, 2, 5, 1, 1, Qt.AlignLeft)
            self.setFixedSize(self.screenWidth * 0.44, self.screenHeight * 0.37)

    def changeOpenWebPageObjectSettingDialogSize(self):
        if self.settingTabWidget.currentIndex() == 0:
            self.setFixedSize(self.screenWidth * 0.46, self.screenHeight * 0.8)
            self.center()
        elif self.settingTabWidget.currentIndex() == 1:
            self.setFixedSize(self.screenWidth * 0.45, self.screenHeight * 0.5)
            self.center()
        elif self.settingTabWidget.currentIndex() == 2:
            if self.handleErrorWayCombobox.currentIndex() == 0:
                self.setFixedSize(self.screenWidth * 0.44, self.screenHeight * 0.3)
            elif self.handleErrorWayCombobox.currentIndex() == 1:
                self.setFixedSize(self.screenWidth * 0.44, self.screenHeight * 0.42)
            else:
                self.setFixedSize(self.screenWidth * 0.44, self.screenHeight * 0.37)
            self.center()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2 - 80)

    def executeStep(self):
        handle = self.webSave.getWebObjectHandle(self.browserTypeCombobox.currentText())
        client = self.webSave.getWebObjectClient(self.browserTypeCombobox.currentText())
        client.maximize_window()
        client.switch_to.window(handle)
        if self.dragCombobox.currentIndex() == 0:
            webElement = client.find_element(By.XPATH,
                                             self.elementDaoMongo.getOneElement(self.elementLabel.text())["xpath"])
            x = self.dragXLineEdit.text()
            y = self.dragYLineEdit.text()
            time.sleep(2)
            ActionChains(client).drag_and_drop_by_offset(webElement, x, y).perform()
        else:
            webElement1 = client.find_element(By.XPATH,
                                              self.elementDaoMongo.getOneElement(self.elementLabel.text())["xpath"])
            webElement2 = client.find_element(By.XPATH,
                                              self.elementDaoMongo.getOneElement(self.element2Label.text())["xpath"])
            ActionChains(client).drag_and_drop(webElement1, webElement2).perform()

    #实现确认和取消按钮点击事件
    def handleQuestionBtnClicked(self):
        print("点击获取信息按钮")

    def handleConfirmBtnClicked(self):
        self.accept()

    def handleCancelBtnClicked(self):
        self.close()

    def handleExecutionBtnClicked(self):
        self.executeStep()

class WorkThread(QThread):
    trigger = pyqtSignal(list)
    def __init__(self, parent=None):
        super(WorkThread, self).__init__(parent)
        self.working = True
    def __del__(self):
        self.working = False
        self.wait()
    def run(self):
        while self.working:
            x, y = pyautogui.position()  # 返回鼠标的坐标
            posList = [x, y]
            self.trigger.emit(posList)
            time.sleep(0.1)  # 每0.1s打印一次
