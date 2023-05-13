# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowSettingDialog

scrollAreaStyleSheet = """
QScrollArea {
    border-style: none;
}
"""
scrollBarStyleSheet = """
QScrollBar:vertical {
    width: 8px;
}
QScrollBar::handle:vertical {
    border-radius: 4px;
    border-style: none;
    background-color: #bbb;
}
QScrollBar::handle:vertical:hover {
    background-color: #b0b0b0;
}
QScrollBar::handle:vertical:pressed {
    background-color: #999;
}
QScrollBar::add-line:vertical {
    border-style: none;
}
QScrollBar::sub-line:vertical {
    border-style: none;
}
"""
comboBoxStyleSheet = """
QComboBox QAbstractItemView {
    selection-background-color: #f0f0f0;
    selection-color: #000;
}
QComboBox QAbstractItemView::item {
    min-height: 40px;
}
"""
deleteBtnStyleSheet = """
QPushButton {
    background-color: transparent;
    border-style: none;
    border-radius: 5px;
    height: 38px;
    width: 38px;
    margin: 0 4px;
}
QPushButton:hover {
    background-color: #e0e0e0;
}
QPushButton:pressed {
    background-color: #d5d5d5;
}
"""
relationList = ["等于", "不等于", "大于", "大于等于", "小于", "小于等于", "包含", "不包含",
                "等于True", "等于False", "等于None", "不等于None", "是空字符串",
                "不是空字符串", "以对象2开头", "不以对象2开头", "以对象2结束", "不以对象2结束"]


class IfMultiConditionObjectSettingDialog(flowSettingDialog.BasicFlowSettingDialog):
    conditions = []
    conditionLayouts = []
    conditionCount = 0

    def __init__(self, title, parent=None):
        super().__init__(title, parent)
        self.__font = QFont()
        self.__font.setPixelSize(20)
        self.__font.setFamily("Courier")
        # 改变图片
        self.changeImage(flowSettingDialog.BasicFlowSettingDialog.picPath + "ifConditionBig.png")
        self.infoLabel.setText("条件判断开始标记")
        self.regularTabUI()

    def regularTabUI(self):
        self.directiveInputSettingLayout = QGridLayout()
        self.directiveInputSettingLayout.setContentsMargins(20, 20, 20, 20)
        self.directiveInputSettingLayout.setSpacing(10)
        self.directiveInputSettingLayout.setVerticalSpacing(15)
        self.directiveInputSettingPanel.setLayout(self.directiveInputSettingLayout)
        relationLabel = QLabel(text="条件关系:", font=self.__font)
        self.directiveInputSettingLayout.addWidget(relationLabel, 0, 0, 1, 1, Qt.AlignRight)
        self.relationComboBox = QComboBox(font=self.__font)
        self.relationComboBox.setMinimumSize(650, 40)
        self.relationComboBox.setItemDelegate(QStyledItemDelegate())
        self.relationComboBox.setStyleSheet(comboBoxStyleSheet)
        self.relationComboBox.addItems(["符合以下全部条件", "符合以下任意条件"])
        self.directiveInputSettingLayout.addWidget(self.relationComboBox, 0, 1, 1, 1, Qt.AlignCenter)
        relationTipLabel = flowSettingDialog.createTipLabel("条件关系", "下面使用的条件将会以此关系进行\n合并得到最终的结果")
        self.directiveInputSettingLayout.addWidget(relationTipLabel, 0, 2, 1, 1, Qt.AlignLeft)
        conditionListLabel = QLabel(text="条件列表:", font=self.__font)
        self.directiveInputSettingLayout.addWidget(conditionListLabel, 1, 0, 1, 1, Qt.AlignRight)
        self.scrollArea = QScrollArea(self.directiveInputSettingPanel)
        self.innerWidget = QWidget(self.scrollArea)
        self.scrollArea.setWidget(self.innerWidget)
        self.scrollArea.verticalScrollBar().setStyleSheet(scrollBarStyleSheet)
        self.scrollArea.setStyleSheet(scrollAreaStyleSheet)
        self.scrollArea.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setMaximumSize(650, 40)
        self.scrollArea.setMinimumWidth(650)
        self.innerWidgetVLayout = QVBoxLayout(self.innerWidget)
        self.innerWidgetVLayout.setContentsMargins(0, 0, 0, 0)
        self.innerWidgetVLayout.setSpacing(10)
        self.innerWidget.setLayout(self.innerWidgetVLayout)
        self.innerWidgetVLayout.addWidget(ConditionWidget(self))
        self.directiveInputSettingLayout.addWidget(self.scrollArea, 1, 1, 1, 1, Qt.AlignCenter)
        self.addConditionBtn = QPushButton(
            icon=QIcon(QPixmap(flowSettingDialog.BasicFlowSettingDialog.picPath + "add_condition.png")),
            text="添加条件", clicked=lambda: self.innerWidgetVLayout.addWidget(ConditionWidget(self)))
        self.addConditionBtn.setMinimumWidth(650)
        self.directiveInputSettingLayout.addWidget(self.addConditionBtn, 2, 1, 1, 1, Qt.AlignLeft | Qt.AlignTop)

        hLayout = QHBoxLayout(self.directiveOutputSettingPanel)
        self.directiveOutputSettingPanel.setLayout(hLayout)
        nothingLabel = QLabel(text="(当前指令不包含任何输出项)", font=self.__font)
        hLayout.addWidget(nothingLabel, 1, Qt.AlignCenter)
        hLayout.setContentsMargins(0, 10, 0, 30)

    # 设定指定数量的条件控件
    def setNumberedConditions(self, count: int = 1):
        diff = self.innerWidgetVLayout.count() - count
        if diff < 0:
            for i in range(-diff):
                self.innerWidgetVLayout.addWidget(ConditionWidget(self))
        elif diff > 0:
            for i in range(diff):
                self.innerWidgetVLayout.itemAt(i).widget().deleteCondition()

    def showEvent(self, a0: QShowEvent) -> None:
        super().showEvent(a0)
        self.setFixedSize(self.width(), self.height())

    # 实现确认和取消按钮点击事件
    def handleQuestionBtnClicked(self):
        print("点击执行命令按钮")

    def handleConfirmBtnClicked(self):
        print("点击确定按钮")
        self.accept()

    def handleCancelBtnClicked(self):
        print("点击取消按钮")
        self.reject()


# 动态添加的指令控件
class ConditionWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settingDialog = parent
        self.__font = QFont()
        self.__font.setPixelSize(20)
        self.__font.setFamily("Courier")
        hLayout = QHBoxLayout()
        self.setLayout(hLayout)
        hLayout.setContentsMargins(0, 0, 0, 0)
        hLayout.setSpacing(0)
        self.objectOne = QComboBox(editable=True, font=self.__font, minimumHeight=40)
        self.relation = QComboBox(font=self.__font, minimumHeight=40)
        self.relation.addItems(relationList)
        self.relation.setItemDelegate(QStyledItemDelegate())
        self.relation.setStyleSheet(comboBoxStyleSheet)
        self.objectTwo = QComboBox(editable=True, font=self.__font, minimumHeight=40)
        self.deleteBtn = QPushButton(icon=QIcon(QPixmap(flowSettingDialog.BasicFlowSettingDialog.picPath + "delete.png")),
                                     clicked=self.deleteCondition,
                                     styleSheet=deleteBtnStyleSheet, iconSize=QSize(32, 32), parent=self)
        hLayout.addWidget(self.objectOne, 2)
        hLayout.addWidget(self.relation, 1)
        hLayout.addWidget(self.objectTwo, 2)
        hLayout.addWidget(self.deleteBtn)
        count = self.settingDialog.innerWidgetVLayout.count()
        if (count < 4) and (count > 0):
            self.settingDialog.scrollArea.setMinimumHeight(40 * (count + 1) + 10 * count)
            self.settingDialog.setFixedHeight(self.settingDialog.height() + 50)

    # 删除条件
    def deleteCondition(self):
        if self.settingDialog:
            count = self.settingDialog.innerWidgetVLayout.count()
            if count > 1:
                self.settingDialog.innerWidgetVLayout.removeWidget(self)
                if count <= 4:
                    self.settingDialog.scrollArea.setMinimumHeight(40 * (count - 1) + 10 * (count - 2))
                    self.settingDialog.setFixedHeight(self.settingDialog.height() - 50)
                self.deleteLater()
            else:
                self.objectOne.setCurrentText("")
                self.relation.setCurrentIndex(0)
                self.objectTwo.setCurrentText("")

    # 设值
    def setCondition(self, condition: list):
        self.objectOne.setCurrentText(condition[0])
        self.relation.setCurrentText(condition[1])
        self.relation.setCurrentText(condition[2])

    # 取值
    def getCondition(self):
        return [self.objectOne.currentText(),
                self.relation.currentText(),
                self.objectTwo.currentText()]
