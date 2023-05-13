# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from . import flowStepWidget
from com.mat.rpa.views.workWindow.middlePanel.directives import directiveWidgetFactory
from com.mat.rpa.dao.workDao.directiveDao import DirectiveDao
from com.mat.rpa.utils.variable import VariableManager
from com.mat.rpa.utils.action import ActionManager
import math
from copy import deepcopy


class InnerWidget(QWidget):
    lineNumberSignal = pyqtSignal(float, int, int) #传递宽度、起始行号、变动值
    __font = QFont()
    __font.setPixelSize(20)
    __font.setBold(True)
    __metrics = QFontMetrics(__font)

    def __init__(self, flowMode, parent=None):
        super(InnerWidget,self).__init__(parent)
        self.setStyleSheet("background-color:white;")
        self.setAcceptDrops(True)
        # self.stretchy_spacer_thing = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.stretchy_spacer_thing = QWidget()
        self.stretchy_spacer_thing.setMinimumSize(600,100)
        self.parentPanel = parent
        self.flowMode = flowMode #设置是PC流程应用还是手机流程应用
        self.indexingTreeWidget = None #流程索引树
        self.innerWidgetLayout = QVBoxLayout()
        self.innerWidgetLayout.setContentsMargins(0,0,0,0)
        self.innerWidgetLayout.setSpacing(0) #设置放入layout的控件之间空间为1
        self.setLayout(self.innerWidgetLayout)
        self.lastFlowWidget = None
        self.directiveWidgetFactory = directiveWidgetFactory.DirectiveWidgetFactory()
        # 流程指令数据访问对象
        self.directiveDaoObj = DirectiveDao()
        # 流程编辑区域所对应的flow文件的id
        self.id = None
        # 变量管理器
        self.variableManager = VariableManager()
        # 操作管理器
        self.actionManager = ActionManager()
        # 选择的指令控件
        self.selected = 0

    # 由各指令控件调用，将指令对象插入数据库
    def insertDirective2DB(self, directive: dict):
        directive["flow_id"] = self.id
        directive["_id"] = self.directiveDaoObj.insertDirective(directive)

    # 将指令设置数据更新到数据库，id为指令字典中的_id
    def updateDirectiveData2DB(self, directive_id, data: dict):
        self.directiveDaoObj.updateDirective(directive_id, {"data": data})

    # 从数据库中读取指令设置
    def getDirectiveSettingDataFromDB(self, directive_id):
        return self.directiveDaoObj.getOneDirective(directive_id)["data"]

    # 直接设置行号
    def setLineNumber(self, directive_id, lineNumber):
        self.directiveDaoObj.updateDirective(directive_id, {"line_number": lineNumber})

    # 删除指定指令
    def deleteDirectiveDataFromDB(self, directive_id):
        self.directiveDaoObj.deleteOneDirective(directive_id)

    # 撤销
    def undo(self):
        try:
            action = self.actionManager.undo(self.id)
            if action[0] == 2:
                widget = self.getWidgetAt(action[1] - 1)
                widget.directive["data"] = action[3]
                self.updateDirectiveData2DB(widget.directive["_id"], widget.directive["data"])
                widget.updateSecondLineInfo()
            elif action[0] == 3:
                print(action[1], action[2])
                if action[1] > action[2]:
                    self._moveWidget(action[2], action[1] + 1, 1)  # todo indentLevel
                else:
                    self._moveWidget(action[2] - 1, action[1], 1)
            elif action[0] == 0:
                widget = self.getWidgetAt(action[1] - 1)
                self._removeWidget(action[1], widget)
            elif action[0] == 1:
                directive = action[3]
                widget = self.directiveWidgetFactory.createDirectiveWidget(directive["command"],
                                                                           action[1],
                                                                           1,  # todo indentLevel
                                                                           directive["flow_title"],
                                                                           self.lineNumberSignal,
                                                                           self)
                widget.directive["data"] = directive["data"]
                widget.directive["comment"] = directive["comment"]
                widget.directive["target"] = directive["target"]
                widget.directive["targets"] = directive["targets"]
                widget.directive["value"] = directive["value"]
                self._insertWidget(action[1] - 1, widget)
        except Exception as e:
            print(e)

    # 重做
    def redo(self):
        try:
            action = self.actionManager.redo(self.id)
            if action[0] == 2:
                widget = self.getWidgetAt(action[1] - 1)
                widget.directive["data"] = action[2]
                self.updateDirectiveData2DB(widget.directive["_id"], widget.directive["data"])
                widget.updateSecondLineInfo()
            elif action[0] == 3:
                self._moveWidget(action[1], action[2], 1)  # todo indentLevel
            elif action[0] == 0:
                directive = action[2]
                widget = self.directiveWidgetFactory.createDirectiveWidget(directive["command"],
                                                                           action[1],
                                                                           1,  # todo indentLevel
                                                                           directive["flow_title"],
                                                                           self.lineNumberSignal,
                                                                           self)
                widget.directive["data"] = directive["data"]
                widget.directive["comment"] = directive["comment"]
                widget.directive["target"] = directive["target"]
                widget.directive["targets"] = directive["targets"]
                widget.directive["value"] = directive["value"]
                self._insertWidget(action[1] - 1, widget)
            elif action[0] == 1:
                widget = self.getWidgetAt(action[1] - 1)
                self._removeWidget(action[1], widget)
        except Exception as e:
            print(e)

    # 按序号获取控件
    def getWidgetAt(self, index):
        return self.innerWidgetLayout.itemAt(index).widget()

    def setIndexingTreeWidget(self, indexingTreeWidget):
        self.indexingTreeWidget = indexingTreeWidget

    def setFlowMode(self, flowMode):
        self.flowMode = flowMode

    def separateTreeNodeInfo(self, infoText):
        infoList = infoText.strip().split("|")
        return infoList

    def dragEnterEvent(self, e):
        if e.mimeData().hasText():
            objectName = e.mimeData().objectName()
            if (objectName == "leaf") or (objectName == "flowStepWidget"):
                if self.lastFlowWidget is not None:
                    self.lastFlowWidget.showBottomBorder()
                e.accept()
            else:
                e.ignore()
        else:
            e.ignore()

    def dragLeaveEvent(self, e):
        if self.lastFlowWidget != None:
            self.lastFlowWidget.hideBottomBorder()

    def deleteWidget(self, lineNumber: int):
        widget = self.getWidgetAt(lineNumber - 1)
        # 删除操作进入撤销栈
        oldDirective = widget.directive
        self.actionManager.insertUndoAction(self.id, 1, oldDirective["line_number"], None, oldDirective)
        self._removeWidget(lineNumber, widget)

    def _removeWidget(self, lineNumber: int, widget):
        self.selected = 0
        if widget == self.lastFlowWidget:
            if lineNumber != 1:
                self.lastFlowWidget = self.getWidgetAt(lineNumber - 2)
            else:
                self.lastFlowWidget = None
        # 从布局管理器中移除
        self.innerWidgetLayout.removeWidget(widget)
        self.deleteDirectiveDataFromDB(widget.directive["_id"])
        widget.deleteLater()
        # 当前控件总数量（删除后的）
        currentWidgetCount = self.innerWidgetLayout.count() - 1
        if currentWidgetCount > 0:
            digiNumber = math.floor(math.log10(currentWidgetCount)) + 1
            # 以最宽的“4”为基准计算宽度
            lineNumberWidth = InnerWidget.__metrics.boundingRect("4" * digiNumber).size().width() * 1.4 + 10
            self.lineNumberSignal.emit(lineNumberWidth, lineNumber, -1)
            self.directiveDaoObj.updateLineNumber(self.id, lineNumber, -1)

    # 移动控件，接口
    def moveWidget(self, widgetIndex: int, targetIndex: int, indentLevel: int):
        print(widgetIndex, targetIndex)
        self.actionManager.insertUndoAction(self.id, 3, widgetIndex, targetIndex)
        self._moveWidget(widgetIndex, targetIndex, indentLevel)

    # 移动控件，内部方法
    def _moveWidget(self, widgetIndex: int, targetIndex: int, indentLevel: int):
        widget = self.getWidgetAt(widgetIndex)
        # 插入位置之后的行号+1，删除位置之后的-1
        self.lineNumberSignal.emit(widget.lineNumberLabel.lineNumberWidth, targetIndex + 1, 1)
        self.lineNumberSignal.emit(widget.lineNumberLabel.lineNumberWidth, widgetIndex + 2, -1)
        # 对数据库也进行同等操作
        self.directiveDaoObj.updateLineNumber(self.id, targetIndex + 1, 1)
        self.directiveDaoObj.updateLineNumber(self.id, widgetIndex + 2, -1)
        # 如果插入位置在控件位置之后，插入时其实是将控件先删去再插入的，所以插入位置要-1
        if widgetIndex < targetIndex:
            targetIndex -= 1
        self.innerWidgetLayout.insertWidget(targetIndex, widget)
        # 更改缩进
        widget.setIndentLevel(indentLevel)
        # 如果挪动的是最后一个控件
        if widgetIndex + 2 == self.innerWidgetLayout.count():
            self.lastFlowWidget = self.getWidgetAt(widgetIndex)
        # 如果插入位置在最后
        if targetIndex + 2 == self.innerWidgetLayout.count():
            self.lastFlowWidget = widget
            x = self.parentPanel.vScrollBar.maximum()
            self.parentPanel.vScrollBar.setSliderPosition(x)
        # 设置新行号
        widget.setLineNumber(targetIndex + 1)

    def insertWidget(self, idx, mimeDataText, indentLevel, directive: dict = None):
        if directive:
            flowPanelWidget = self.directiveWidgetFactory.createDirectiveWidget(directive["command"],
                                                                                idx + 1,
                                                                                indentLevel,
                                                                                directive["flow_title"],
                                                                                self.lineNumberSignal,
                                                                                self)
            flowPanelWidget.directive["data"] = deepcopy(directive["data"])
            flowPanelWidget.directive["comment"] = directive["comment"]
            flowPanelWidget.directive["target"] = directive["target"]
            flowPanelWidget.directive["targets"] = directive["targets"].copy()
            flowPanelWidget.directive["value"] = directive["value"]
            flowPanelWidget.updateSecondLineInfo()
        else:
            # 解析拖拽的命令信息
            infoList = self.separateTreeNodeInfo(mimeDataText)
            # 创建新控件，将其插入对应位置
            flowPanelWidget = self.directiveWidgetFactory.createDirectiveWidget(infoList[1],
                                                                                idx + 1,
                                                                                indentLevel, infoList[2],
                                                                                self.lineNumberSignal,
                                                                                self)
        if flowPanelWidget:
            self._insertAction(flowPanelWidget)
            self._insertWidget(idx, flowPanelWidget)

    # 插入指令，内部方法
    def _insertWidget(self, idx: int, flowPanelWidget):
        # 当前控件总数量（包括新的）
        currentWidgetCount = self.innerWidgetLayout.count()
        digiNumber = math.floor(math.log10(currentWidgetCount)) + 1
        # 以最宽的“4”为基准计算宽度
        lineNumberWidth = InnerWidget.__metrics.boundingRect("4" * digiNumber).size().width() * 1.4 + 10
        print(lineNumberWidth)
        # 行号顺移一位，更新行号宽度
        self.lineNumberSignal.emit(lineNumberWidth, idx + 1, 1)
        # 插入数据库
        self.insertDirective2DB(flowPanelWidget.directive)
        flowPanelWidget.setErrorLabelVisible(False)
        flowPanelWidget.setCodePuckerVisible(False)
        # 插入
        self.innerWidgetLayout.insertWidget(idx, flowPanelWidget)
        # 若插入的是最后一个，则更新最后一个控件
        if currentWidgetCount == idx + 1:
            self.lastFlowWidget = flowPanelWidget
            x = self.parentPanel.vScrollBar.maximum()
            self.parentPanel.vScrollBar.setSliderPosition(x)
        # 把新控件的行号改回来
        flowPanelWidget.setLineNumber(idx + 1)

    def dropWidget(self, widget):
        # 首先删除最后边的占位控件
        self.innerWidgetLayout.removeWidget(self.stretchy_spacer_thing)
        # 添加控件
        self.innerWidgetLayout.addWidget(widget)
        # 在最后添加占位控件
        self.innerWidgetLayout.addWidget(self.stretchy_spacer_thing, 1)#占据所有空白空间

    def dropEvent(self, e):
        try:
            if self.lastFlowWidget is not None:
                self.lastFlowWidget.hideBottomBorder()
            currentIndex = self.innerWidgetLayout.count()
            if currentIndex == 0:#起始布局管理器中没有放占位控件，所以控件数为0，而起始序号为1
                currentIndex = 1
            mimeData = e.mimeData()
            if mimeData.objectName() == "flowStepWidget":
                self.moveWidget(int(mimeData.text()), currentIndex - 1, 1)
                return
            infoList = self.separateTreeNodeInfo(mimeData.text())
            flowPanelWidget = self.directiveWidgetFactory.createDirectiveWidget(infoList[1],
                                                                                currentIndex, 1,
                                                                                infoList[2],
                                                                                self.lineNumberSignal,
                                                                                self)
            if flowPanelWidget: #假如成功创建控件,再添加
                self._insertAction(flowPanelWidget)
                print("lineNumber Width is:", flowPanelWidget.lineNumberLabel.lineNumberWidth)
                if currentIndex != 1:
                    lastDigitNumber = math.floor(math.log10(currentIndex-1))+1
                    currentDigitNumber = math.floor(math.log10(currentIndex))+1
                    if currentDigitNumber > lastDigitNumber:#位数多了一位
                        self.lineNumberSignal.emit(flowPanelWidget.lineNumberLabel.lineNumberWidth, None, 0)

                flowPanelWidget.setErrorLabelVisible(False)
                flowPanelWidget.setCodePuckerVisible(False)
                self.insertDirective2DB(flowPanelWidget.directive)
                self.dropWidget(flowPanelWidget)
                self.lastFlowWidget = flowPanelWidget #更新最后一个流程控件
                # 当添加一条流程步骤时，垂直滚动条自动向下移动，能跟随显示最后一条
                #pyqt5这里可能有个bug：先滚动再在QVBoxlayout中续加控件
                x = self.parentPanel.vScrollBar.maximum()
                # x = x+100 #因为总是获得插入前的滚动条最大值，所以此时的maximum值不包含新添加的流程控件
                # # 所以手动地增大maximum值，实现估计增加后的maximum值为再增加100
                # # 最后用增加后的maximum值设置滚动条的位置就可以滚动追踪最后一条流程控件
                # # 增加多一些，可以留一些空白，否则最后添加不上了
                # self.parentPanel.vScrollBar.setMaximum(x) #要让滚动条一直在最下边必须有这一条语句
                self.parentPanel.vScrollBar.setSliderPosition(x)
        except Exception as e:
            print(e)

    # 创建操作进入撤销栈
    def _insertAction(self, flowPanelWidget: flowStepWidget.FlowStepWidget):
        newDirective = deepcopy(flowPanelWidget.directive)
        self.actionManager.insertUndoAction(self.id, 0, newDirective["line_number"], newDirective)

    # 从数据库打开flow文件，构建指令控件
    def buildFlowWidgetsFromDB(self):
        result = self.directiveDaoObj.getAllDirectives(self.id)
        if result:
            flowPanelWidget = None
            for directive in result:
                widget = self.directiveWidgetFactory.createDirectiveWidget(directive["command"],
                                                                           directive["line_number"],
                                                                           1,
                                                                           directive["flow_title"],
                                                                           self.lineNumberSignal,
                                                                           self)

                if widget:  # 假如成功创建控件,再添加flowPanelWidget.directive["data"] = directive["data"]
                    flowPanelWidget = widget
                    flowPanelWidget.directive["_id"] = directive["_id"]
                    flowPanelWidget.directive["data"] = directive["data"]
                    flowPanelWidget.directive["comment"] = directive["comment"]
                    flowPanelWidget.directive["target"] = directive["target"]
                    flowPanelWidget.directive["targets"] = directive["targets"]
                    flowPanelWidget.directive["value"] = directive["value"]
                    flowPanelWidget.updateSecondLineInfo()
                    if hasattr(flowPanelWidget, "isFirstShow"):
                        flowPanelWidget.isFirstShow = False
                    print("lineNumber Width is:", flowPanelWidget.lineNumberLabel.lineNumberWidth)
                    if directive["line_number"] != 1:
                        lastDigitNumber = math.floor(math.log10(directive["line_number"] - 1)) + 1
                        currentDigitNumber = math.floor(math.log10(directive["line_number"])) + 1
                        if currentDigitNumber > lastDigitNumber:  # 位数多了一位
                            self.lineNumberSignal.emit(flowPanelWidget.lineNumberLabel.lineNumberWidth, None, 0)
                    flowPanelWidget.setErrorLabelVisible(False)
                    flowPanelWidget.setCodePuckerVisible(False)
                    self.dropWidget(flowPanelWidget)
            self.lastFlowWidget = flowPanelWidget  # 更新最后一个流程控件


class FlowScrollAreaWidget(QScrollArea):
    def __init__(self, flowMode, parent=None):
        super(FlowScrollAreaWidget, self).__init__(parent)
        self.flowMode = flowMode
        self.setAcceptDrops(True)
        self.indexingTreeWidget = None
        self.vScrollBar = self.verticalScrollBar()
        self.setWidgetResizable(True) #必须加上这句，否则scroll中的widget不能铺满
        self.initUI()

    def initUI(self):
        #scrollArea仅仅类似一个窗口，只是用来帮助在有限面积中观察更大范围
        #而它自身并不会提供要展示的容器。我们需要自己在ScrollArea中放置待观察的容器，例如这里的innerWidget
        self.innerWidget = InnerWidget(self.flowMode, self)
        self.innerWidget.setObjectName("innerWidget")
        self.setWidget(self.innerWidget)

    def getInnerWidget(self):
        return self.innerWidget

    def setFlowMode(self, flowMode):
        self.flowMode = flowMode
        self.innerWidget.setFlowMode(flowMode)

    def setIndexingTreeWidget(self, indexingTreeWidget):
        self.indexingTreeWidget = indexingTreeWidget
        self.innerWidget.setIndexingTreeWidget(indexingTreeWidget)
