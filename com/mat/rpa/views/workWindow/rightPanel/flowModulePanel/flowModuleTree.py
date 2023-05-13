# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from com.mat.rpa.dao.workDao.directiveDao import DirectiveDao
import treeItem
from com.mat.rpa.dao.workDao.workDao import WorkDao
from com.mat.rpa.utils.variable import VariableManager
from bson import ObjectId
import json


class FlowModuleTree(QTreeWidget):
    picPath = "./com/mat/rpa/views/workWindow/rightPanel/images/"
    openSubFlowSignal = pyqtSignal(ObjectId, str)
    closeSubFlowSignal = pyqtSignal(ObjectId)
    nameChangedSignal = pyqtSignal(ObjectId, str)

    def __init__(self, parent=None):
        super(FlowModuleTree, self).__init__(parent)
        self.parentPanel = parent
        # 设置1列
        self.setColumnCount(1)
        # 隐藏header
        self.setHeaderHidden(True)
        # 添加一个默认根节点，后边可以修改名称
        self.rootNode = treeItem.TreeItemWithID(self)
        self.rootNode.setNodeName("rootNode")
        self.rootNode.setText(0, "root应用")
        # 添加引用节点
        self.refNode = treeItem.TreeItemWithID(self)
        self.refNode.setNodeName("refNode")
        self.refNode.setText(0, "引用")
        self.refNode.setIcon(0, QIcon(FlowModuleTree.picPath + "reference.png"))
        # 添加资源节点
        self.resourceNode = treeItem.TreeItemWithID(self)
        self.resourceNode.setNodeName("resourceNode")
        self.resourceNode.setText(0, "资源文件")
        self.resourceNode.setIcon(0, QIcon(FlowModuleTree.picPath + "resource.png"))
        # 添加主流程节点
        self.mainFlowNode = treeItem.TreeItemWithID(self)
        self.mainFlowNode.setNodeName("mainFlowNode")
        self.mainFlowNode.setText(0, "主流程.flow")
        self.mainFlowNode.setIcon(0, QIcon(FlowModuleTree.picPath + "subflow.png"))
        self.workDaoObj = WorkDao()
        self.setIconSize(QSize(20, 20))

    # 添加子流程
    def addSubFlow(self):
        flow = treeItem.TreeItemWithID(self)
        flow.setNodeName("subFlowNode")
        flow.setIcon(0, QIcon(FlowModuleTree.picPath + "subflow.png"))
        # 为子流程创建唯一的流程名
        appId = VariableManager().getAppId()
        names = self.workDaoObj.getFlowNames(appId)
        fullName = "子流程.flow"
        print('---------')
        print(names)
        print('---------')
        if fullName in names:
            unUsedName = False
            i = 2
            while not unUsedName:
                fullName = "子流程 " + str(i) + ".flow"
                unUsedName = fullName not in names
                i += 1
        flow.setText(0, fullName)
        # 插入数据库
        flowId = self.workDaoObj.insertSubFlow(appId, fullName)
        flow.flowId = flowId
        self.setCurrentItem(flow)
        return flow

    # 删除子流程
    def deleteFlow(self, item: treeItem.TreeItemWithID):
        if item.nodeName == "subFlowNode":
            messageBox = QMessageBox(QMessageBox.Question, u"删除子流程",
                                     u"确定要删除这一子流程吗？删除后将无法恢复",
                                     QMessageBox.Yes | QMessageBox.Cancel)
            messageBox.setDefaultButton(QMessageBox.Cancel)
            yesBtn = messageBox.button(QMessageBox.Yes)
            yesBtn.setText(u"确认")
            yesBtn.setStyleSheet("background-color: red; color: white;")
            messageBox.button(QMessageBox.Cancel).setText(u"取消")
            messageBox.setStyleSheet("QMessageBox {background-color: white}")
            messageBox.setContentsMargins(6, 8, 6, 4)
            reply = messageBox.exec()
            if reply == QMessageBox.Yes:
                self.workDaoObj.deleteSubFlow(VariableManager().getAppId(), item.flowId)
                self.closeSubFlowSignal.emit(item.flowId)
                try:
                    item.parent().removeChild(item)
                except Exception:
                    self.takeTopLevelItem(self.indexOfTopLevelItem(item))

    # 加载子流程
    def loadSubFlows(self, subFlow: list):
        for item in subFlow:
            flow = treeItem.TreeItemWithID(self)
            flow.setNodeName("subFlowNode")
            flow.setIcon(0, QIcon(FlowModuleTree.picPath + "subflow.png"))
            flow.setText(0, item["flow_name"])
            flow.flowId = item["id"]

    # 导入子流程
    def importSubFlow(self):
        try:
            fileName, _ = QFileDialog.getOpenFileName(self, u"导入", "", u"Flow流程文件 (*.flow)")
            if fileName == "":
                return
            else:
                with open(fileName, "r", encoding="utf-8") as flow:
                    flowDict = json.load(flow)
                    flowObj = self.addSubFlow()
                    appId = VariableManager().getAppId()
                    names = self.workDaoObj.getFlowNames(appId)
                    if flowDict["name"] not in names:
                        if not flowDict["name"].endswith(".flow"):
                            flowDict["name"] = flowDict["name"] + ".flow"
                        flowObj.setText(0, flowDict["name"])
                        self.workDaoObj.updateFlowName(appId, flowObj.flowId, flowDict["name"])
                    directiveDaoObj = DirectiveDao()
                    for item in flowDict["directives"]:
                        del item["_id"]
                        item["flow_id"] = flowObj.flowId
                        directiveDaoObj.insertDirective(item)
        except Exception as e:
            print(e)
            if flowObj:
                self.workDaoObj.deleteSubFlow(VariableManager().getAppId(), flowObj.flowId)

    # 打开文件名编辑器
    def openEditor(self, item: treeItem.TreeItemWithID):
        if item.nodeName == "subFlowNode":
            if self.itemWidget(item, 0) is None:
                self.setItemWidget(item, 0, Editor(item))

    # 设置快捷键
    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_F2:
            self.openEditor(self.currentItem())
        else:
            super().keyPressEvent(event)

    # 右键打开菜单
    def mousePressEvent(self, e: QMouseEvent) -> None:
        super().mousePressEvent(e)
        if e.button() == Qt.RightButton:
            item = self.itemAt(e.pos())
            if item and item.nodeName == "subFlowNode":
                self.menu = FlowModuleMenu(item)
                self.menu.popup(QCursor.pos())

    # 双击打开文件
    def mouseDoubleClickEvent(self, e: QMouseEvent) -> None:
        item = self.itemAt(e.pos())
        if item and item.nodeName == "subFlowNode":
            self.openSubFlowSignal.emit(item.flowId, item.text(0))


# 文件名编辑器
class Editor(QWidget):
    def __init__(self, item: QTreeWidgetItem, parent=None):
        super().__init__()
        self.targetItem = item
        text = item.text(0)
        self.postfix = '.' + text.split('.')[-1]
        self.oldName = text[: -len(self.postfix)]
        hLayout = QHBoxLayout()
        hLayout.setContentsMargins(0, 0, 0, 0)
        hLayout.setSpacing(0)
        self.setLayout(hLayout)
        self.lineEdit = QLineEdit()
        self.setFixedHeight(28)
        self.lineEdit.setText(self.oldName)
        self.lineEdit.setSelection(0, len(self.oldName))
        self.lineEdit.editingFinished.connect(self.closeEditor)
        validator = QRegExpValidator(QRegExp('[^/\\\\:\*\?"<>\|]*'))
        self.lineEdit.setValidator(validator)
        hLayout.addWidget(self.lineEdit)
        postfixLabel = QLabel(self.postfix)
        postfixLabel.setStyleSheet("color: white;")
        hLayout.addWidget(postfixLabel)
        hLayout.addSpacing(10)

    # 自动获取焦点
    def showEvent(self, a0: QShowEvent) -> None:
        super().showEvent(a0)
        self.lineEdit.setFocus()

    # 结束编辑
    def closeEditor(self):
        try:
            text = self.lineEdit.text()
            text = text.lstrip()
            if text != "":
                appId = VariableManager().getAppId()
                names = self.targetItem.treeWidget().workDaoObj.getFlowNames(appId)
                if (text + self.postfix) not in names:
                    fullName = text + self.postfix
                    self.targetItem.treeWidget().workDaoObj.updateFlowName(appId,
                                                                           self.targetItem.flowId,
                                                                           fullName)
                    self.targetItem.setText(0, fullName)
                    self.targetItem.treeWidget().nameChangedSignal.emit(self.targetItem.flowId,
                                                                        fullName)
            self.targetItem.treeWidget().removeItemWidget(self.targetItem, 0)
            self.deleteLater()
        except Exception as e:
            print(e)


menuStyleSheet = """
QMenu {
    background-color: #fff;
    padding: 2px;
    margin: 4px;
    font-size: 12px;
    border-radius: 5px;
    border-color: #aaa;
    border-width: 1px;
    border-style: solid;
}
QMenu::item {
    padding: 5px;
    margin: 1px;
    border-radius: 4px;
    min-width: 130px;
    color: #333;
}
QMenu::item:default {
    color: red;
}
QMenu::item:selected {
    background-color: #e0e0e0;
}
QMenu::icon {
    padding-left: 10px;
}
"""


class FlowModuleMenu(QMenu):
    picPath = "./com/mat/rpa/views/workWindow/rightPanel/images/"

    def __init__(self, item, parent=None):
        super().__init__(parent)
        self.rename = QAction(QIcon(self.picPath + "rename.png"), u"重命名", self)
        self.rename.setShortcut(Qt.Key_F2)
        self.rename.triggered.connect(lambda: item.treeWidget().openEditor(item))
        self.delete = QAction(QIcon(self.picPath + "delete.png"), u"删除", self)
        self.delete.setShortcut(Qt.CTRL + Qt.Key_D)
        self.delete.triggered.connect(lambda: item.treeWidget().deleteFlow(item))
        self.setStyleSheet(menuStyleSheet)
        self.setDefaultAction(self.delete)
        self.item = item
        self.addActions([self.rename, self.delete])
        # 透明背景
        self.setAttribute(Qt.WA_TranslucentBackground)
        # 无边框，去除阴影
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        # 加阴影
        shadow = QGraphicsDropShadowEffect()
        shadow.setOffset(0, 0)
        shadow.setBlurRadius(6)
        shadow.setColor(QColor(70, 70, 70))
        self.setGraphicsEffect(shadow)
