# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets, QtWebChannel
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineScript, QWebEnginePage
import os
from jinja2 import Template
from com.mat.rpa.views.workWindow.middlePanel.consolePanel.tabPanel import basicConsolePanel
import pyautogui
from com.mat.rpa.dao.elementDao import elementDao
import io
from com.mat.rpa.utils.variable import VariableManager
from com.mat.rpa.utils.globalConstants import GlobalConstants

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


class BasicFlowSettingDialog(QDialog):
    picPath = "./com/mat/rpa/views/workWindow/images/"

    def __init__(self, title, directive_id, id, parent=None):
        super(BasicFlowSettingDialog, self).__init__(parent)
        # 设置最小尺寸
        # self.setMinimumSize(1000,600)
        __font = QFont()
        __font.setPixelSize(20)
        __font.setFamily("黑体")
        __font.setBold(True)
        # 设置标题栏按钮
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        self.setWindowModality(Qt.WindowModal)
        # 设置标题
        self.setWindowTitle(title)
        # 设置布局
        self.entireLayout = QVBoxLayout()
        self.setLayout(self.entireLayout)
        self.entireLayout.setContentsMargins(20, 20, 20, 20)
        self.entireLayout.setSpacing(10)
        # 第一行布局
        self.firstLineLayout = QGridLayout()
        self.firstLineLayout.setContentsMargins(0, 0, 0, 0)
        self.firstLineLayout.setSpacing(5)
        self.imageLabel = QLabel()  # 默认没有设置图片，根据不同指令设置不同图片
        self.imageLabel.setPixmap(QPixmap(BasicFlowSettingDialog.picPath + "openWebPageBig.png"))
        self.firstLineLayout.addWidget(self.imageLabel, 0, 0, 2, 1, Qt.AlignLeft)
        self.titleLabel = QLabel()  # 填写标题
        self.titleLabel.setText(title)
        self.firstLineLayout.addWidget(self.titleLabel, 0, 1, 1, 1, Qt.AlignLeft)
        self.infoLabel = QLabel()  # 填写提示信息
        self.infoLabel.setText("111111111111111")
        self.infoLabel.setStyleSheet("color:#838b8b")
        self.firstLineLayout.addWidget(self.infoLabel, 1, 1, 1, 1, Qt.AlignLeft)
        self.questionBtn = QPushButton()
        self.questionBtn.setIcon(QIcon(QPixmap(BasicFlowSettingDialog.picPath + "question.png")))
        self.questionBtn.setText("使用说明")
        self.questionBtn.setStyleSheet("border:None; color:#4e6ef2;")
        self.questionBtn.clicked.connect(self.handleQuestionBtnClicked)
        self.firstLineLayout.addWidget(self.questionBtn, 0, 2, 1, 1, Qt.AlignRight)
        self.firstLineLayout.setColumnStretch(0, 2)  # 设置gridlayout拉伸时，第一列占拉伸比例2/100
        self.firstLineLayout.setColumnStretch(1, 90)  # 而第二列占90/100
        self.firstLineLayout.setColumnStretch(2, 8)  # 而第三列占8/100
        self.entireLayout.addLayout(self.firstLineLayout)
        # 第二行，tabWidget
        self.settingTabWidget = QTabWidget()
        self.regularTab = QWidget()
        self.regularTabLayout = QVBoxLayout()
        self.regularTab.setLayout(self.regularTabLayout)
        self.regularTabLayout.setContentsMargins(0, 20, 0, 0)
        self.regularTabLayout.setSpacing(10)
        ##第一条横线
        inputOfDirectiveLineLayout = QHBoxLayout()
        inputOfDirectiveLineLayout.setContentsMargins(10, 10, 10, 10)
        inputOfDirectiveLineLayout.setSpacing(0)
        inputOfDirectiveLine_firstShortLine = QFrame()
        inputOfDirectiveLine_firstShortLine.setFrameShape(QFrame.HLine)
        inputOfDirectiveLine_firstShortLine.setFrameShadow(QFrame.Sunken)
        inputOfDirectiveLine_firstShortLine.setObjectName("inputOfDirectiveLine_firstShortLine")
        inputOfDirectiveLineLayout.addWidget(inputOfDirectiveLine_firstShortLine, 1)
        inputOfDirectiveLine_info_label = QLabel()
        inputOfDirectiveLine_info_label.setText("指令输入")
        inputOfDirectiveLine_info_label.setFont(__font)
        inputOfDirectiveLineLayout.addWidget(inputOfDirectiveLine_info_label, 1)
        inputOfDirectiveLine_secondLongLine = QFrame()
        inputOfDirectiveLine_secondLongLine.setFrameShape(QFrame.HLine)
        inputOfDirectiveLine_secondLongLine.setFrameShadow(QFrame.Sunken)
        inputOfDirectiveLine_secondLongLine.setObjectName("inputOfDirectiveLine_secondLongLine")
        inputOfDirectiveLineLayout.addWidget(inputOfDirectiveLine_secondLongLine, 8)
        self.regularTabLayout.addLayout(inputOfDirectiveLineLayout)
        ##指令输入设置区域
        self.directiveInputSettingPanel = QWidget()
        self.regularTabLayout.addWidget(self.directiveInputSettingPanel)
        # ##指令输出线
        outputOfDirectiveLineLayout = QHBoxLayout()
        outputOfDirectiveLineLayout.setContentsMargins(10, 10, 10, 10)
        outputOfDirectiveLineLayout.setSpacing(0)
        outputOfDirectiveLine_firstShortLine = QFrame()
        outputOfDirectiveLine_firstShortLine.setFrameShape(QFrame.HLine)
        outputOfDirectiveLine_firstShortLine.setFrameShadow(QFrame.Sunken)
        outputOfDirectiveLine_firstShortLine.setObjectName("outputOfDirectiveLine_firstShortLine")
        outputOfDirectiveLineLayout.addWidget(outputOfDirectiveLine_firstShortLine, 1)
        outputOfDirectiveLine_info_label = QLabel()
        outputOfDirectiveLine_info_label.setText("指令输出")
        outputOfDirectiveLine_info_label.setFont(__font)
        outputOfDirectiveLineLayout.addWidget(outputOfDirectiveLine_info_label, 1)
        outputOfDirectiveLine_secondLongLine = QFrame()
        outputOfDirectiveLine_secondLongLine.setFrameShape(QFrame.HLine)
        outputOfDirectiveLine_secondLongLine.setFrameShadow(QFrame.Sunken)
        outputOfDirectiveLine_secondLongLine.setObjectName("outputOfDirectiveLine_secondLongLine")
        outputOfDirectiveLineLayout.addWidget(outputOfDirectiveLine_secondLongLine, 8)
        self.regularTabLayout.addLayout(outputOfDirectiveLineLayout)
        ##指令输出设置区域
        self.directiveOutputSettingPanel = QWidget()
        self.regularTabLayout.addWidget(self.directiveOutputSettingPanel)
        ##添加常规Tab
        self.settingTabWidget.addTab(self.regularTab, "常规")
        self.entireLayout.addWidget(self.settingTabWidget)
        # 第三行,按钮
        self.thirdLineLayout = QHBoxLayout()
        self.thirdLineLayout.setContentsMargins(0, 0, 0, 0)
        self.thirdLineLayout.setSpacing(5)
        self.executionButton = QPushButton()
        self.executionButton.setText("运行指令")
        self.executionButton.clicked.connect(self.handleExecutionBtnClicked)
        self.thirdLineLayout.addWidget(self.executionButton)
        self.thirdLineLayout.addStretch(1)
        self.confirmButton = QPushButton()
        self.confirmButton.setText("确定")
        self.confirmButton.setDefault(True)
        self.confirmButton.clicked.connect(self.handleConfirmBtnClicked)
        self.confirmButton.setObjectName("BasicFlowSettingDialog_confirmBtn")
        self.confirmButton.setStyleSheet('''
            #BasicFlowSettingDialog_confirmBtn {
                background-color: red
            }
        ''')
        self.thirdLineLayout.addWidget(self.confirmButton)
        self.cancelButton = QPushButton()
        self.cancelButton.setText("取消")
        self.cancelButton.clicked.connect(self.handleCancelBtnClicked)
        self.thirdLineLayout.addWidget(self.cancelButton)
        self.entireLayout.addLayout(self.thirdLineLayout)
        self.isFirstShow = True
        self.errorHandlingTab = None
        self.settingTabWidget.currentChanged.connect(self.changeTab)

    def errorHandlingTabUI(self):
        __font = QFont()
        __font.setPixelSize(20)
        __font.setFamily("Courier")
        self.errorHandlingTab = QWidget()
        self.settingTabWidget.addTab(self.errorHandlingTab, "错误处理")
        self.errorHandlingLayout = QGridLayout()
        self.errorHandlingTab.setLayout(self.errorHandlingLayout)
        self.errorHandlingLayout.setContentsMargins(20, 20, 30, 20)
        self.errorHandlingLayout.setSpacing(10)
        self.errorHandlingLayout.setVerticalSpacing(20)

        checkBoxHLayout = QHBoxLayout()
        self.printErrorLogsCheckbox = QCheckBox()
        self.printErrorLogsCheckbox.setText(u"打印错误日志")
        self.printErrorLogsCheckbox.setFont(__font)
        self.printErrorLogsCheckbox.setChecked(True)
        checkBoxHLayout.addWidget(self.printErrorLogsCheckbox)
        self.printErrorLogsTipLabel = createTipLabel(u"打印错误日志", u"当出现错误时打印错误日志到日志面板")
        checkBoxHLayout.addWidget(self.printErrorLogsTipLabel)
        self.errorHandlingLayout.addLayout(checkBoxHLayout, 0, 1, 1, 1, Qt.AlignLeft)
        self.handleErrorWayLabel = QLabel()
        self.handleErrorWayLabel.setFont(__font)
        self.handleErrorWayLabel.setText(u"处理方式:")
        self.errorHandlingLayout.addWidget(self.handleErrorWayLabel, 1, 0, 1, 1, Qt.AlignRight)
        self.handleErrorWayCombobox = QComboBox()
        self.handleErrorWayCombobox.setFont(__font)
        self.handleErrorWayCombobox.setMinimumSize(650, 50)
        self.handleErrorWayCombobox.addItems([u"终止流程", u"忽略异常并继续执行", u"重试此指令"])
        self.handleErrorWayCombobox.setItemDelegate(QStyledItemDelegate())
        self.handleErrorWayCombobox.setStyleSheet('''
            QComboBox QAbstractItemView {
                selection-background-color: #f0f0f0;
                selection-color: #000;
            }
            QComboBox QAbstractItemView::item {
                min-height: 50px;
            }''')
        self.handleErrorWayCombobox.currentIndexChanged.connect(self.changeErrorHandlingWidgets)
        self.errorHandlingLayout.addWidget(self.handleErrorWayCombobox, 1, 1, 1, 1, Qt.AlignCenter)
        self.handleErrorWayTipLabel = createTipLabel(u"选择错误处理方式",
                                                     u"选择错误处理方式，当出现错误时默\n认终止流程，也可以选择忽略错误或\n者重试当前指令")
        self.errorHandlingLayout.addWidget(self.handleErrorWayTipLabel, 1, 2, 1, 1, Qt.AlignLeft)
        if hasattr(self, "outputVariableNameLineEdit"):
            self.outputVariableNameLineEdit.editingFinished.connect(self.changeVariableName)
            self.onErrorOutputValueLabel = QLabel(text=u"设置异常情况下指令的输出值", font=__font)
            self.errorHandlingLayout.addWidget(self.onErrorOutputValueLabel, 2, 0, 1, 2, Qt.AlignLeft)
            variableOutputHLayout = QHBoxLayout()
            variableOutputHLayout.setSpacing(10)
            self.onErrorOutputVariableLabel = QLabel(text=self.outputVariableNameLineEdit.text() + ":", font=__font)
            variableOutputHLayout.addWidget(self.onErrorOutputVariableLabel)
            self.onErrorOutputVariableLineEdit = QLineEdit(font=__font)
            self.onErrorOutputVariableLineEdit.setMinimumHeight(50)
            variableOutputHLayout.addWidget(self.onErrorOutputVariableLineEdit, 1)
            self.errorHandlingLayout.addLayout(variableOutputHLayout, 3, 1, 1, 1)
            self.onErrorOutputValueLabel.hide()
            self.onErrorOutputVariableLineEdit.hide()
            self.onErrorOutputVariableLabel.hide()
        retryHLayout = QHBoxLayout()
        retryHLayout.setSpacing(10)
        self.retryCountLabel = QLabel(text=u"重试次数", font=__font)
        retryHLayout.addWidget(self.retryCountLabel)
        self.retryCountSpinbox = QSpinBox()
        self.retryCountSpinbox.setFont(__font)
        self.retryCountSpinbox.setMinimumSize(7, 40)
        self.retryCountSpinbox.setMinimum(1)
        self.retryCountSpinbox.setMaximum(100000000)
        self.retryCountSpinbox.setValue(1)
        retryHLayout.addWidget(self.retryCountSpinbox)
        retryHLayout.addSpacing(20)
        self.retryIntervalLabel = QLabel(text=u"重试间隔(秒)", font=__font)
        retryHLayout.addWidget(self.retryIntervalLabel)
        self.retryIntervalSpinbox = QSpinBox()
        self.retryIntervalSpinbox.setFont(__font)
        self.retryIntervalSpinbox.setMinimumSize(7, 40)
        self.retryIntervalSpinbox.setMinimum(1)
        self.retryIntervalSpinbox.setMaximum(100000000)
        self.retryIntervalSpinbox.setValue(1)
        retryHLayout.addWidget(self.retryIntervalSpinbox)
        self.errorHandlingLayout.addLayout(retryHLayout, 4, 1, 1, 1, Qt.AlignLeft)
        self.retryCountSpinbox.hide()
        self.retryCountLabel.hide()
        self.retryIntervalSpinbox.hide()
        self.retryIntervalLabel.hide()

    def getSettingData(self):
        pass

    def changeErrorHandlingWidgets(self):
        # 终止流程
        if self.handleErrorWayCombobox.currentIndex() == 0:
            if hasattr(self, "onErrorOutputVariableLineEdit"):
                self.onErrorOutputValueLabel.hide()
                self.onErrorOutputVariableLineEdit.hide()
                self.onErrorOutputVariableLabel.hide()
            self.retryCountSpinbox.hide()
            self.retryCountLabel.hide()
            self.retryIntervalSpinbox.hide()
            self.retryIntervalLabel.hide()
            self.setFixedHeight(310)
        # 忽略异常
        elif self.handleErrorWayCombobox.currentIndex() == 1:
            if hasattr(self, "onErrorOutputVariableLineEdit"):
                self.onErrorOutputValueLabel.show()
                self.onErrorOutputVariableLineEdit.show()
                self.onErrorOutputVariableLabel.show()
                self.setFixedHeight(450)
            else:
                self.setFixedHeight(310)
            self.retryCountSpinbox.hide()
            self.retryCountLabel.hide()
            self.retryIntervalSpinbox.hide()
            self.retryIntervalLabel.hide()
        # 重试
        else:
            self.setFixedHeight(370)
            if hasattr(self, "onErrorOutputVariableLineEdit"):
                self.onErrorOutputValueLabel.hide()
                self.onErrorOutputVariableLineEdit.hide()
                self.onErrorOutputVariableLabel.hide()
            self.retryCountSpinbox.show()
            self.retryCountLabel.show()
            self.retryIntervalSpinbox.show()
            self.retryIntervalLabel.show()

    # 切换页面状态，需要重写
    def changeTab(self):
        # 错误处理页面
        if self.settingTabWidget.currentWidget() == self.errorHandlingTab:
            self.changeErrorHandlingWidgets()
        elif self.settingTabWidget.currentWidget() == self.regularTab:
            self.setFixedHeight(self.defaultSize[1])

    # 改变错误处理的变量名
    def changeVariableName(self):
        try:
            self.onErrorOutputVariableLabel.setText(self.outputVariableNameLineEdit.text() + ":")
        except Exception:
            pass

    def showEvent(self, a0: QShowEvent) -> None:
        super().showEvent(a0)
        if self.isFirstShow:
            self.defaultSize = (self.width(), self.height())
            self.isFirstShow = False

    def handleQuestionBtnClicked(self):
        print("点击了使用说明按钮")

    def handleExecutionBtnClicked(self):
        print("点击了执行按钮")

    def handleConfirmBtnClicked(self):
        print("点击了确认按钮")

    def handleCancelBtnClicked(self):
        print("点击了取消按钮")

    def setInfoLabelText(self, infoText):
        self.infoLabel.setText(infoText)

    def changeImage(self, imagePath):
        self.imageLabel.setPixmap(QPixmap(imagePath))

    def executeStep(self):
        pass


class createTipLabel(QLabel):
    picPath = "./com/mat/rpa/views/workWindow/images/"

    def __init__(self, tipTitle="", tipText="", parent=None):
        super(createTipLabel, self).__init__(parent)
        __font = QFont()
        __font.setPixelSize(20)
        __font.setFamily("Courier")
        self.setPixmap(QPixmap(BasicFlowSettingDialog.picPath + "blackInfo.png"))

        self.tip = QLabel()
        self.tip.setWindowFlags(Qt.ToolTip)
        # self.tip.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.tip.setStyleSheet("background-color:white")
        self.tipLabelLayout = QVBoxLayout()
        self.tip.setLayout(self.tipLabelLayout)
        self.tipLabelQuestionBtn = QPushButton()
        self.tipLabelLayout.addWidget(self.tipLabelQuestionBtn, 0, Qt.AlignLeft | Qt.AlignTop)
        self.tipLabelQuestionBtn.setIcon(
            QIcon(QPixmap(BasicFlowSettingDialog.picPath + "blueInfo.png")))
        self.tipLabelQuestionBtn.setText(tipTitle)
        self.tipLabelQuestionBtn.setFont(__font)
        self.tipLabelQuestionBtn.setStyleSheet("border:None;")
        self.tipLabelText = QLabel()
        self.tipLabelText.setText(tipText)
        self.tipLabelText.setStyleSheet("color:#838b8b;font-size:16px;font-family:Courier")
        self.tipLabelLayout.addWidget(self.tipLabelText)

    def enterEvent(self, e):
        rx = QCursor.pos().x() + 5
        ry = QCursor.pos().y()
        self.tip.move(rx, ry)
        self.tip.show()
        return super().enterEvent(e)

    def changeText(self, title, text):
        self.tipLabelQuestionBtn.setText(title)
        self.tipLabelText.setText(text)

    def leaveEvent(self, e):
        self.tip.hide()
        return super().enterEvent(e)


listStyleSheet = """
QListView::item {
    height: 35px;
    padding: 0px;
}
QListView::item QLabel {
    height: 30px;
    font-size: 14px;
    padding: 0 15px;
}
QListView::item QLabel:hover {
    background-color: #EEE;
}
"""


class functionPanel(QWidget):
    picPath = "./com/mat/rpa/views/workWindow/images/"
    __instance = None  # 单例模式
    _isFirstInit = True  # 判断首次构造的标记

    def __new__(cls, targetWidget, plainTextMode, parent=None):
        if not cls.__instance:
            cls.__instance = super(functionPanel, cls).__new__(cls, targetWidget, plainTextMode, parent)
        return cls.__instance

    def __init__(self, targetWidget, plainTextMode, parent=None):
        # 获取type类
        cls = type(self)
        # 判断类的构造函数是否初次执行
        if cls._isFirstInit:
            super(functionPanel, self).__init__(parent)
            __font = QFont()
            __font.setPixelSize(20)
            __font.setFamily("Courier")
            self.setWindowFlags(Qt.Popup)
            self.setStyleSheet("background-color:white")
            self.functionPanelLayout = QVBoxLayout()
            self.setLayout(self.functionPanelLayout)
            self.functionPanelLayout.setContentsMargins(0, 0, 0, 0)
            self.functionPanelLayout.setSpacing(0)
            self.topPanel = QWidget()
            self.topPanel.setStyleSheet("background-color:#F5F5F5")
            self.functionPanelLayout.addWidget(self.topPanel)
            self.topPanelLayout = QHBoxLayout()
            self.topPanelLayout.setContentsMargins(10, 10, 10, 10)
            self.topPanelLayout.setSpacing(0)
            self.topPanel.setLayout(self.topPanelLayout)
            self.searchLineEdit = QLineEdit()
            self.searchLineEdit.setFont(__font)
            self.searchLineEdit.setStyleSheet("background-color:white")
            self.topPanelLayout.addWidget(self.searchLineEdit)
            self.searchBtn = QPushButton()
            self.searchBtn.setMinimumSize(50, 50)
            self.searchBtn.setIcon(
                QIcon(QPixmap(BasicFlowSettingDialog.picPath + "search.png")))
            self.searchBtn.setStyleSheet("background-color:white")
            self.searchBtn.setIconSize(QSize(32, 32))
            self.topPanelLayout.addWidget(self.searchBtn)
            self.variableList = QListWidget()
            self.variableList.setStyleSheet(listStyleSheet)
            self.promptLabel = QLabel()
            self.promptLabel.setText("(当前无可用的变量)")
            self.promptLabel.setFont(__font)
            self.promptLabel.setStyleSheet(
                "color:#808080;font-size:16px;font-family:Courier;border-radius:2px;border: 1px solid DarkGray")
            self.promptLabel.setAlignment(Qt.AlignCenter)
            self.functionPanelLayout.addWidget(self.promptLabel)
            self.functionPanelLayout.addWidget(self.variableList)
            self.variableList.hide()
            self.functionPanelLayout.setStretch(0, 1)
            self.functionPanelLayout.setStretch(0, 3)
            cls._isFirstInit = False
        self.targetWidget = targetWidget
        width = self.targetWidget.size().width()
        self.plainTextMode = plainTextMode
        self.setFixedSize(width, 300)
        self.searchLineEdit.setMinimumSize(width - 20, 50)
        self.topPanel.setFixedSize(width, 70)

    def setVariables(self, vDict: dict = None):
        if vDict:
            self.variableList.show()
            self.promptLabel.hide()
            self.variableList.clear()
            for item in vDict:
                widgetItem = QListWidgetItem(self.variableList, 0)
                self.variableList.addItem(widgetItem)
                # 使用重写的QLabel控件替换列表项
                label = VariableLabel(item)
                label.clicked.connect(self.selectVariable)
                label.setText(item + '&emsp;<span style="color: #0f7af4; background-color: #e0f0ff">&nbsp;' +
                              GlobalConstants.variableDataType[vDict[item]] + "&nbsp;</span>")
                self.variableList.setItemWidget(widgetItem, label)
        else:
            self.variableList.hide()
            self.promptLabel.show()

    def selectVariable(self, name):
        if self.plainTextMode:
            self.targetWidget.setText(self.targetWidget.text() + "${" + name + "}")
        else:
            self.targetWidget.setText(self.targetWidget.text() + name)
        self.hide()


# 重写QLabel，点击发射clicked信号，保存变量名
class VariableLabel(QLabel):
    clicked = pyqtSignal(str)

    def __init__(self, name, parent=None):
        self.variableName = name
        super().__init__(parent)

    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:
        self.clicked.emit(self.variableName)


class addFunctionButton(QPushButton):
    picPath = "./com/mat/rpa/views/workWindow/images/"

    def __init__(self, targetWidget: QWidget, settingDialog: BasicFlowSettingDialog, plainTextMode=True, parent=None):
        super(addFunctionButton, self).__init__(parent)
        self.flowStepWidget = settingDialog.parent()
        self.setMinimumSize(50, 50)
        self.setIcon(
            QIcon(QPixmap(BasicFlowSettingDialog.picPath + "function.png")))
        self.setIconSize(QSize(32, 32))
        self.clicked.connect(self.openFunctionPanel)
        self.targetWidget = targetWidget
        self.plainTextMode = plainTextMode

    def openFunctionPanel(self):
        self.functionPanel = functionPanel(self.targetWidget, self.plainTextMode)
        self.functionPanel.setVariables(
            VariableManager().getVariableDictByLineNumber(self.flowStepWidget.parent().id,
                                                          self.flowStepWidget.directive["line_number"]))
        self.functionPanel.show()
        position = self.pos()
        parentPosition = self.parent().mapToGlobal(QPoint(0, 0))
        self.functionPanel.move(self.targetWidget.x() + parentPosition.x(),
                                position.y() + parentPosition.y() + 50)


class elementfunctionPanel(basicConsolePanel.BasicConsolePanel):
    picPath = "./com/mat/rpa/views/workWindow/middlePanel/consolePanel/tabPanel/images/"

    def __init__(self, targetWidget, parent=None):
        super(elementfunctionPanel, self).__init__(parent)
        self.elementDaoMongo = elementDao.ElementDao()
        __font = QFont()
        __font.setPixelSize(20)
        __font.setFamily("Courier")
        self.setWindowFlags(Qt.Popup)
        self.setFixedSize(1000, 300)
        self.hintLabel.setText("元素库")
        self.newElementCaptureBtnMenu = QMenu()
        # 创建标准模式捕获行为
        self.standardModeCaptureAction = QAction(QIcon(QPixmap(elementfunctionPanel.picPath + "plusSign.png")),
                                                 "标准模式捕获",
                                                 self.newElementCaptureBtnMenu)
        self.newElementCaptureBtnMenu.addAction(self.standardModeCaptureAction)
        # 创建深度模式捕获行为
        self.deepModeCaptureAction = QAction(QIcon(QPixmap(elementfunctionPanel.picPath + "deepModeCapture.png")),
                                             "深度模式捕获",
                                             self.newElementCaptureBtnMenu)
        self.newElementCaptureBtnMenu.addAction(self.deepModeCaptureAction)
        # 创建CV智能模式捕获行为
        self.IntelligentModeCaptureAction = QAction(
            QIcon(QPixmap(elementfunctionPanel.picPath + "intelligentPatternCapture.png")), "CV智能模式捕获",
            self.newElementCaptureBtnMenu)
        self.newElementCaptureBtnMenu.addAction(self.IntelligentModeCaptureAction)
        # 创建QToolButoon
        self.newElementCaptureBtn = QToolButton()
        self.newElementCaptureBtn.setText("捕获新元素")
        self.newElementCaptureBtn.setIcon(QIcon(QPixmap(elementfunctionPanel.picPath + "plusSign.png")))
        self.newElementCaptureBtn.setMenu(self.newElementCaptureBtnMenu)
        self.newElementCaptureBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.newElementCaptureBtn.setPopupMode(QToolButton.MenuButtonPopup)
        # self.newElementCaptureBtn.clicked.connect(self.captureNewElement)
        self.centerPanelLayout.addWidget(self.newElementCaptureBtn, 0, 1)

        self.elementShowWin = QTableWidget()
        self.centerPanelLayout.addWidget(self.elementShowWin, 1, 1)

        self.newElementWindow = QTreeWidget()
        self.newElementWindow.setColumnCount(1)
        self.newElementWindow.setHeaderHidden(True)
        self.newElementWindow.itemDoubleClicked.connect(self.mouseDoubieClickEvent)
        self.centerPanelLayout.addWidget(self.newElementWindow, 0, 0, 2, 1)
        for i in self.elementDaoMongo.findAllElement():
            self.root = QTreeWidgetItem(self.newElementWindow)
            self.child = QTreeWidgetItem(self.root)
            self.root.setText(0, i["title"])
            self.child.setText(0, i["name"])
        self.newElementWindow.expandAll()
        self.targetWidget = targetWidget

    def mouseDoubieClickEvent(self):
        item = self.newElementWindow.currentItem()
        if item is not None:
            self.targetWidget.setText(item.text(0))
            self.hide()


class readElementFunctionButton(QPushButton):
    def __init__(self, targetWidget: QWidget, settingDialog: BasicFlowSettingDialog, parent=None):
        super(readElementFunctionButton, self).__init__(parent)
        self.flowStepWidget = settingDialog.parent()
        self.setMinimumSize(200, 50)
        self.setText("去元素库选择")
        self.clicked.connect(self.openFunctionPanel)
        self.targetWidget = targetWidget

    def openFunctionPanel(self):
        self.functionPanel = elementfunctionPanel(self.targetWidget)
        self.functionPanel.show()
        self.position = self.pos()
        self.parentPosition = self.parent().mapToGlobal(QPoint(0, 0))
        self.functionPanel.move(self.position.x() + self.parentPosition.x(),
                                self.position.y() + self.parentPosition.y() + 50)
