# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowSettingDialog
from com.mat.rpa.utils.sizeCalc import screenPercentage
from com.mat.rpa.dao.workDao.directiveDao import DirectiveDao
from com.mat.rpa.utils.variable import VariableManager
from com.mat.rpa.views.workWindow.rightPanel.globalVariablePanel.globalVariablePanel import GlobalVariablePanel
comboBoxStyleSheet = """
QComboBox QAbstractItemView {
    selection-background-color: #f0f0f0;
    selection-color: #000;
}
QComboBox QAbstractItemView::item {
    min-height: 50px;
}
"""
class ForCircleDialog(flowSettingDialog.BasicFlowSettingDialog):

    def __init__(self, title, directive_id, id, parent=None):
        super().__init__(title, directive_id, id, parent)
        self.directiveDaoObj = DirectiveDao()
        # 改变图片
        self.changeImage(flowSettingDialog.BasicFlowSettingDialog.picPath + "ifConditionBig.png")
        self.infoLabel.setText("条件循环开始标记")
        self.regularTabUI()
        self.times = 0
        self.answer = None
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
        self.directive["data"] = {"obj1": "",
                                  "obj2": "",
                                  "relation": "小于",
                                  "obj3": ""}

    def regularTabUI(self):
        __font = QFont()
        __font.setPixelSize(20)
        __font.setFamily("Courier")
        self.directiveInputSettingLayout = QGridLayout()
        self.directiveInputSettingLayout.setContentsMargins(20, 0, 20, 0)
        self.directiveInputSettingLayout.setSpacing(10)
        self.directiveInputSettingLayout.setVerticalSpacing(30)
        self.directiveInputSettingPanel.setLayout(self.directiveInputSettingLayout)
        checkBoxLabel = QLabel(text="勾选上为右是左否，没勾选上为左是右否：",font=__font)
        self.directiveInputSettingLayout.addWidget(checkBoxLabel, 0, 0, 1, 0,Qt.AlignLeft)
        self.checkBox = QCheckBox()
        self.directiveInputSettingLayout.addWidget(self.checkBox, 0, 1, 1, 1,Qt.AlignCenter)
        objectOneLabel = QLabel(text="对象1:", font=__font)
        self.directiveInputSettingLayout.addWidget(objectOneLabel, 1,0,1,1, Qt.AlignRight)
        self.objectOneComboBox = QComboBox(font=__font, editable=True)
        self.objectOneComboBox.setMinimumSize(650, 50)
        self.objectOneComboBox.setItemDelegate(QStyledItemDelegate())
        self.objectOneComboBox.setStyleSheet(comboBoxStyleSheet)
        self.directiveInputSettingLayout.addWidget(self.objectOneComboBox, 1,1,1,1, Qt.AlignCenter)
        objectOneTipLabel = flowSettingDialog.createTipLabel("对象1", "输入前面指令创建的变量、文本\n或数字，与对象2进行比较")
        self.directiveInputSettingLayout.addWidget(objectOneTipLabel, 1,2,1,1, Qt.AlignLeft)
        objectOneLabel = QLabel(text="步长:", font=__font)
        self.directiveInputSettingLayout.addWidget(objectOneLabel, 2, 0, 1, 1, Qt.AlignRight)
        self.objectThreeComboBox = QComboBox(font=__font, editable=True)
        self.objectThreeComboBox.setMinimumSize(650, 50)
        self.objectThreeComboBox.setItemDelegate(QStyledItemDelegate())
        self.objectThreeComboBox.setStyleSheet(comboBoxStyleSheet)
        self.directiveInputSettingLayout.addWidget(self.objectThreeComboBox, 2, 1, 1, 1, Qt.AlignCenter)
        objectOneTipLabel = flowSettingDialog.createTipLabel("步长", "是变量1的增量")
        self.directiveInputSettingLayout.addWidget(objectOneTipLabel, 2, 2, 1, 1, Qt.AlignLeft)

        relationLabel = QLabel(text="关系:", font=__font)
        self.directiveInputSettingLayout.addWidget(relationLabel, 3,0,1,1, Qt.AlignRight)
        self.relationComboBox = QComboBox(font=__font)
        self.relationComboBox.setMinimumSize(650, 50)
        self.relationComboBox.setItemDelegate(QStyledItemDelegate())
        self.relationComboBox.setStyleSheet(comboBoxStyleSheet)
        self.relationComboBox.addItems(["等于", "不等于", "大于", "大于等于", "小于", "小于等于"])
        self.directiveInputSettingLayout.addWidget(self.relationComboBox, 3,1,1,1, Qt.AlignCenter)
        relationTipLabel = flowSettingDialog.createTipLabel("关系", "选择对象1和对象2的比较方式")
        self.directiveInputSettingLayout.addWidget(relationTipLabel, 3,2,1,1, Qt.AlignLeft)
        objectTwoLabel = QLabel(text="对象2:", font=__font)
        self.directiveInputSettingLayout.addWidget(objectTwoLabel, 4,0,1,1, Qt.AlignRight)
        self.objectTwoComboBox = QComboBox(font=__font, editable=True)
        self.objectTwoComboBox.setMinimumSize(650, 50)
        self.objectTwoComboBox.setItemDelegate(QStyledItemDelegate())
        self.objectTwoComboBox.setStyleSheet(comboBoxStyleSheet)
        self.directiveInputSettingLayout.addWidget(self.objectTwoComboBox, 4,1,1,1, Qt.AlignCenter)
        objectTwoTipLabel = flowSettingDialog.createTipLabel("对象2", "输入前面指令创建的变量、文本\n或数字，与对象1进行比较")
        self.directiveInputSettingLayout.addWidget(objectTwoTipLabel, 4,2,1,1, Qt.AlignLeft)

        hLayout = QHBoxLayout(self.directiveOutputSettingPanel)
        self.directiveOutputSettingPanel.setLayout(hLayout)
        nothingLabel = QLabel(text="(当前指令不包含任何输出项)", font=__font)
        hLayout.addWidget(nothingLabel, 1, Qt.AlignCenter)
        hLayout.setContentsMargins(0,10,0,30)
        self.objectOneComboBox.setEditable(True)

    def showEvent(self, a0: QShowEvent) -> None:
        super().showEvent(a0)
        self.setFixedSize(self.width(), self.height())

    def executeStep(self):
        gvp = GlobalVariablePanel()
        try:
            obj1 = eval(self.objectOneComboBox.currentText())
        except Exception as e:
            obj1 = gvp.getVariableByName(self.objectOneComboBox.currentText())
        try:
            obj2 = eval(self.objectTwoComboBox.currentText())
        except Exception as e:
            obj2 = gvp.getVariableByName(self.objectTwoComboBox.currentText())
        try:
            self.answer = True
            if self.relationComboBox.currentText() == "等于":
                if obj1 + self.times * int(self.objectThreeComboBox.currentText()) == obj2:
                    self.answer = True
                else:
                    self.answer = False

            if self.relationComboBox.currentText() == "不等于":
                if obj1 + self.times * int(self.objectThreeComboBox.currentText()) != obj2:
                    self.answer = True
                else:
                    self.answer = False

            if self.relationComboBox.currentText() == "大于":
                if obj1 + self.times * int(self.objectThreeComboBox.currentText()) > obj2:
                    self.answer = True
                else:
                    self.answer = False

            if self.relationComboBox.currentText() == "大于等于":
                if obj1 + self.times * int(self.objectThreeComboBox.currentText()) >= obj2:
                    self.answer = True
                else:
                    self.answer = False

            if self.relationComboBox.currentText() == "小于":
                if obj1 + self.times * int(self.objectThreeComboBox.currentText()) < obj2:
                    self.answer = True
                else:
                    self.answer = False

            if self.relationComboBox.currentText() == "小于等于":
                if obj1 + self.times * int(self.objectThreeComboBox.currentText()) <= obj2:
                    self.answer = True
                else:
                    self.answer = False
            print("times:" + str(self.times))
            self.times = self.times + 1

            if self.answer:
                if self.checkBox.isChecked():
                    self.answer = 2
                else:
                    self.answer = 4
            else:
                if self.checkBox.isChecked():
                    self.answer = 4
                else:
                    self.answer = 2
                self.times = 0


        except Exception as e:
            print(e)
    #实现确认和取消按钮点击事件
    def handleQuestionBtnClicked(self):
        self.executeStep()

    def handleConfirmBtnClicked(self):
        #self.updateSettingData()
        self.accept()

    def handleCancelBtnClicked(self):
        print("点击取消按钮")
        self.reject()

    def getSettingData(self):
        data = self.getDirectiveSettingDataFromDB(self.directive["_id"])
        self.objectOneComboBox.setCurrentText(data["obj1"])
        self.relationComboBox.setCurrentText(data["relation"])
        self.objectTwoComboBox.setCurrentText(data["obj2"])
        self.objectThreeComboBox.setCurrentText(data["obj3"])
        self.directive["data"] = data

    # 将设置信息更新到数据库
    # def updateSettingData(self):
    #     self.directive["data"]["obj1"] = self.objectOneComboBox.currentText()
    #     self.directive["data"]["obj3"]=self.objectThreeComboBox.currentText()
    #     self.directive["data"]["relation"] = self.relationComboBox.currentText()
    #     self.directive["data"]["obj2"] = self.objectTwoComboBox.currentText()
    #     self.updateDirectiveData2DB(self.directive["_id"], self.directive["data"])
    #
    # def updateDirectiveData2DB(self, directive_id, data: dict):
    #     self.directiveDaoObj.updateDirective(directive_id, {"data": data})
    #
    # def getDirectiveSettingDataFromDB(self, directive_id):
    #     return self.directiveDaoObj.getOneDirective(directive_id)["data"]

    def serialize(self):
        from collections import OrderedDict
        return OrderedDict([
            ('obj1',self.objectOneComboBox.currentText()),
            ('obj3',self.objectThreeComboBox.currentText()),
            ('relation',self.relationComboBox.currentText()),
            ('obj2',self.objectTwoComboBox.currentText())
        ])

    def deserialize(self,data):
        self.objectOneComboBox.setCurrentText(data["obj1"])
        self.relationComboBox.setCurrentText(data["relation"])
        self.objectTwoComboBox.setCurrentText(data["obj2"])
        self.objectThreeComboBox.setCurrentText(data["obj3"])
        self.data = data
        self.accept()

