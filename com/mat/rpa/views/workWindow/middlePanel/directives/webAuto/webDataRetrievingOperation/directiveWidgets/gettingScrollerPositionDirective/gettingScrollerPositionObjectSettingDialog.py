# -*- coding:utf-8 -*-
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from com.mat.rpa.dao.elementDao import elementDao
from com.mat.rpa.dao.workDao.directiveDao import DirectiveDao
from com.mat.rpa.utils import webAutoSave
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowSettingDialog

class GettingScrollerPositionObjectSettingDialog(flowSettingDialog.BasicFlowSettingDialog):
    flowTextList = pyqtSignal(list)
    def __init__(self, title, directive_id, id, parent=None):
        super().__init__(title, directive_id, id, parent)
        self.directiveDaoObj = DirectiveDao()
        self.webSave = webAutoSave.WebAutoSave()
        self.elementDaoMongo = elementDao.ElementDao()
        self.setInfoLabelText(u"获取网页或元素中滚动条的当前位置或底部位置(即滚动条长度)")
        self.changeImage(flowSettingDialog.BasicFlowSettingDialog.picPath + "openWebPageBig.png")
        self.screenWidth = 1920
        self.screenHeight = 1030
        self.setFixedSize(self.screenWidth * 0.46, self.screenHeight * 0.6)
        self.center()
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
        self.directive["data"] = {"web_object":"",
                                  "element_Scroller":False,
                                  "element_name":"",
                                  "autoSearch":False,
                                  "Scroller_chosen":0,
                                  "position_chosen":0,
                                  "output":"scroll_value",
                                  "time_out_period": "20",
                                  "log": True,
                                  "handle": 0,
                                  "on_error_output_value": "",
                                  "retry_count": 1,
                                  "retry_interval": 1}


    def regularTabUI(self):
        __font = QFont()
        __font.setPixelSize(20)
        __font.setFamily("Courier")
        self.directiveInputSettingLayout = QGridLayout()
        self.directiveInputSettingLayout.setContentsMargins(10,0,0,0)
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
        self.directiveInputSettingLayout.addWidget(self.webObjectCombobox, 0, 1, 1, 2, Qt.AlignLeft)
        self.webObjectTipLabel = flowSettingDialog.createTipLabel(u"网页对象",
                                                                  u"  输入一个获取到的或者通过\"打开网\n  页\"创建的网页对象")
        self.directiveInputSettingLayout.addWidget(self.webObjectTipLabel, 0, 3, 1, 1, Qt.AlignLeft)

        #元素滚动条选项
        self.elementScrollerCheckBox = QCheckBox()
        self.elementScrollerCheckBox.setText(u"元素滚动条")
        self.elementScrollerCheckBox.setFont(__font)
        self.elementScrollerCheckBox.setChecked(False)
        self.elementScrollerCheckBox.stateChanged.connect(self.ChangeTheTypeOfScroller)
        self.directiveInputSettingLayout.addWidget(self.elementScrollerCheckBox,1,1,1,1,Qt.AlignLeft)
        self.elementScrollerTipLabel = flowSettingDialog.createTipLabel(u"元素滚动条",u"获取指定元素滚动条的位置，否则为整个网页的滚动条")
        self.directiveInputSettingLayout.addWidget(self.elementScrollerTipLabel,1,3,1,1,Qt.AlignLeft)

        #勾选后的选项
        self.objectLabel = QLabel()
        self.objectLabel.setFont(__font)
        self.objectLabel.setText(u"操作目标:")
        self.directiveInputSettingLayout.addWidget(self.objectLabel,2,1,1,1,Qt.AlignLeft)
        self.directiveInputSettingLayout.setSpacing(0)
        self.objectLabel.hide()
        self.elementLayout = QHBoxLayout()
        self.elementLayout.setContentsMargins(0, 0, 0, 0)
        self.elementLayout.setSpacing(10)
        self.elementLabel = QLineEdit()
        self.elementLabel.setEnabled(False)  # 设置不可以编辑
        self.elementLabel.setFont(__font)
        self.elementLabel.setMinimumSize(390, 50)
        self.elementLayout.addWidget(self.elementLabel,5)
        self.pointoutButton = flowSettingDialog.readElementFunctionButton(self.elementLabel,self)
        self.elementLayout.addWidget(self.pointoutButton,1)
        self.directiveInputSettingLayout.setSpacing(10)
        self.directiveInputSettingLayout.addLayout(self.elementLayout,3,1,1,2,Qt.AlignLeft)
        self.elementLabel.hide()
        self.pointoutButton.hide()
        self.matchWayTipLabel = flowSettingDialog.createTipLabel(u"操作目标",u"  选择要操作的网页元素")
        self.directiveInputSettingLayout.addWidget(self.matchWayTipLabel,3,3,1,1,Qt.AlignLeft)
        self.matchWayTipLabel.hide()
        self.elementHasNoScrollerCheckBox = QCheckBox()
        self.elementHasNoScrollerCheckBox.setText(u"元素无滚动条，自动向上查找")
        self.elementHasNoScrollerCheckBox.setFont(__font)
        # self.elementHasNoScrollerCheckBox.stateChanged.connect(self.AutoSearchElementScroller)
        self.directiveInputSettingLayout.addWidget(self.elementHasNoScrollerCheckBox,4,1,1,1,Qt.AlignLeft)
        self.elementHasNoScrollerCheckBox.hide()
        self.elementHasNoScrollerTipLabel = flowSettingDialog.createTipLabel(u"元素无滚动条，自动向上查找",u"  若当前元素无滚动条，自动向上查找有滚动条元素")
        self.directiveInputSettingLayout.addWidget(self.elementHasNoScrollerTipLabel,4,2,1,1,Qt.AlignLeft)
        self.elementHasNoScrollerTipLabel.hide()

        #其他常驻控件
        self.scrollerLabel = QLabel()
        self.scrollerLabel.setFont(__font)
        self.scrollerLabel.setText(u"滚动条:")
        self.directiveInputSettingLayout.addWidget(self.scrollerLabel,5,0,1,1,Qt.AlignRight)
        self.scrollerCombobox = QComboBox()
        self.scrollerCombobox.setObjectName("scrollerCombobox")
        self.scrollerCombobox.setEditable(False)
        self.scrollerCombobox.setFont(__font)
        self.scrollerCombobox.setMinimumSize(600,50)
        self.scrollerCombobox.addItems([u"纵向滚动条",u"横向滚动条"])
        self.scrollerCombobox.setItemDelegate(QStyledItemDelegate())
        self.scrollerCombobox.setStyleSheet("QComboBox QAbstractItemView{selection-background-color: #f0f0f0;selection-color: #000;} QComboBox QAbstractItemView::item{min-height: 50px;}")
        # self.scrollerCombobox.currentIndexChanged.connect(self.changeScrollerType)
        self.directiveInputSettingLayout.addWidget(self.scrollerCombobox,5,1,1,2,Qt.AlignLeft)
        self.scrollerTipLabel = flowSettingDialog.createTipLabel(u"滚动条",u"  根据实际需要选择纵向滚动条或横向滚动条")
        self.directiveInputSettingLayout.addWidget(self.scrollerTipLabel,5,3,1,1,Qt.AlignLeft)

        self.positonLabel = QLabel()
        self.positonLabel.setFont(__font)
        self.positonLabel.setText(u"位置:")
        self.directiveInputSettingLayout.addWidget(self.positonLabel,6,0,1,1,Qt.AlignRight)
        self.positionCombobox = QComboBox()
        self.positionCombobox.setObjectName("positionCombobox")
        self.positionCombobox.setEditable(False)
        self.positionCombobox.setFont(__font)
        self.positionCombobox.setMinimumSize(600,50)
        self.positionCombobox.addItems([u"当前位置",u"底部位置"])
        self.positionCombobox.setItemDelegate(QStyledItemDelegate())
        self.positionCombobox.setStyleSheet("QComboBox QAbstractItemView{selection-background-color: #f0f0f0;selection-color: #000;} QComboBox QAbstractItemView::item{min-height: 50px;}")
        # self.positionCombobox.currentIndexChanged.connect(self.changePosition)
        self.directiveInputSettingLayout.addWidget(self.positionCombobox,6,1,1,2,Qt.AlignLeft)
        self.positionTipLabel = flowSettingDialog.createTipLabel(u"位置",u"  当前位置为当前滚动条所在的位置与顶部的距离，底部位置为滚动条最大可滚动的长度")
        self.directiveInputSettingLayout.addWidget(self.positionTipLabel,6,3,1,1,Qt.AlignLeft)

        self.directiveOutputSettingLayout = QGridLayout()
        self.directiveOutputSettingLayout.setContentsMargins(10, 0, 0, 20)
        self.directiveOutputSettingLayout.setSpacing(10)
        self.directiveOutputSettingPanel.setLayout(self.directiveOutputSettingLayout)

        self.saveScrollerPositionObjectLabel = QLabel()
        self.saveScrollerPositionObjectLabel.setFont(__font)
        self.saveScrollerPositionObjectLabel.setText(u"保存滚动条位置至:")
        self.directiveOutputSettingLayout.addWidget(self.saveScrollerPositionObjectLabel,0,0,1,1,Qt.AlignRight)
        self.outputVariableNameLineEdit = QLineEdit()
        self.outputVariableNameLineEdit.setFont(__font)
        self.outputVariableNameLineEdit.setMinimumSize(600, 50)
        self.outputVariableNameLineEdit.setText("scroll_value")
        self.directiveOutputSettingLayout.addWidget(self.outputVariableNameLineEdit,0,1,1,1,Qt.AlignCenter)
        self.saveScrollerPositionFunctionBtn = flowSettingDialog.addFunctionButton(self.outputVariableNameLineEdit,self)
        self.directiveOutputSettingLayout.addWidget(self.saveScrollerPositionFunctionBtn,0,1,1,1,Qt.AlignRight)
        self.saveScrollerPositionTipLabel = flowSettingDialog.createTipLabel(u"保存滚动条位置至",u"  指定一个表量名称，该变量用于保存获取到的滚动条位置")
        self.directiveOutputSettingLayout.addWidget(self.saveScrollerPositionTipLabel,0,2,1,1,Qt.AlignLeft)

        self.emptyLabel = QLabel()
        self.emptyLabel.setFont(__font)
        self.emptyLabel.setText(u"（当前指令不包含任何输出项）")
        self.emptyLabel.setStyleSheet("color:#838b8b;font-size:16px;font-family:Courier")
        self.emptyLabel.setAlignment(Qt.AlignCenter)
        self.directiveOutputSettingLayout.addWidget(self.emptyLabel, 1, 0, 1, 3, Qt.AlignCenter)
        self.emptyLabel.hide()

        self.directiveOutputSettingLayout.setColumnStretch(0,20)
        self.directiveOutputSettingLayout.setColumnStretch(1,60)
        self.directiveOutputSettingLayout.setColumnStretch(2,20)




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
        self.waitForElementAppearFunctionBtn = flowSettingDialog.addFunctionButton(self.waitForElementAppearLineEdit, self)
        self.seniorTabLayout.addWidget(self.waitForElementAppearFunctionBtn, 0, 1, 1, 1, Qt.AlignRight)
        self.waitForElementAppearTipLabel = flowSettingDialog.createTipLabel(u"等待元素存在(s)",u"  设置网页截图的超时时间")
        self.seniorTabLayout.addWidget(self.waitForElementAppearTipLabel, 0, 2, 1, 1, Qt.AlignLeft)


    def changeOpenWebPageObjectSettingDialogSize(self):
        #在第一列
        if self.settingTabWidget.currentIndex() == 0:
            if self.elementScrollerCheckBox.isChecked():
                self.setFixedSize(self.screenWidth * 0.46,self.screenHeight * 0.7)
            else:
                self.setFixedSize(self.screenWidth * 0.46, self.screenHeight * 0.6)
            self.center()
        elif self.settingTabWidget.currentIndex() == 1:
            self.setFixedSize(self.screenWidth * 0.47, self.screenHeight * 0.27)
            self.center()
        elif self.settingTabWidget.currentIndex() == 2:
            if self.handleErrorWayCombobox.currentIndex() == 0:
                self.setFixedSize(self.screenWidth * 0.46, self.screenHeight * 0.3)
                self.center()
            elif self.handleErrorWayCombobox.currentIndex() == 1:
                self.setFixedSize(self.screenWidth * 0.46, self.screenHeight * 0.42)
                self.center()
            else:
                self.setFixedSize(self.screenWidth * 0.46, self.screenHeight * 0.37)
                self.center()


    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,(screen.height() - size.height()) / 2 - 80)


    """
    self.objectLabel
    self.elementLabel
    self.pointoutButton
    self.matchWayTipLabel
    self.elementHasNoScrollerCheckBox
    self.elementHasNoScrollerTipLabel
    """
    def ChangeTheTypeOfScroller(self):
        if self.elementScrollerCheckBox.isChecked():
            self.changeOpenWebPageObjectSettingDialogSize()
            self.objectLabel.show()
            self.elementLabel.show()
            self.pointoutButton.show()
            self.matchWayTipLabel.show()
            self.elementHasNoScrollerCheckBox.show()
            self.elementHasNoScrollerTipLabel.show()
        else:
            self.changeOpenWebPageObjectSettingDialogSize()
            self.objectLabel.hide()
            self.elementLabel.hide()
            self.pointoutButton.hide()
            self.matchWayTipLabel.hide()
            self.elementHasNoScrollerTipLabel.hide()
            self.elementHasNoScrollerCheckBox.hide()


    def AutoSearchElementScroller(self):
        pass


    def changeScrollerType(self):
        pass


    def changePosition(self):
        pass


    def executeStep(self):
        try:
            handle = self.webSave.getWebObjectHandle(self.webObjectCombobox.currentText())
            client = self.webSave.getWebObjectClient(self.webObjectCombobox.currentText())
            client.switch_to.window(handle)
            if self.elementScrollerCheckBox.isChecked() == False:
                if self.scrollerCombobox.currentIndex() == 0:
                    if self.positionCombobox.currentIndex() == 0:
                        js = '''
let scrollPos;  
if (window.pageYOffset) { 
    scrollPos = window.pageYOffset;
}else if (document.compatMode && document.compatMode != 'BackCompat'){ 
    scrollPos = document.documentElement.scrollTop;
}else if (document.body) { 
    scrollPos = document.body.scrollTop;
}
return scrollPos;   
'''
                        self.scrollerPosition = client.execute_script(js)
                    elif self.positionCombobox.currentIndex() == 1:
                        pass
        except Exception as e:
            print(e)

    def getSettingData(self):
        data = self.getDirectiveSettingDataFromDB(self.directive["_id"])
        self.webObjectCombobox.setCurrentText(data["web_object"])
        self.elementScrollerCheckBox.setChecked(data["element_Scroller"])
        self.elementLabel.setText(data["element_name"])
        self.elementHasNoScrollerCheckBox.setChecked(data["autoSearch"])
        self.scrollerCombobox.setCurrentIndex(data["Scroller_chosen"])
        self.positionCombobox.setCurrentIndex(data["position_chosen"])
        self.outputVariableNameLineEdit.setText(data["output"])
        self.waitForElementAppearLineEdit.setText(data["time_out_period"])
        self.printErrorLogsCheckbox.setChecked(data["log"])
        self.handleErrorWayCombobox.setCurrentIndex(data["handle"])
        self.onErrorOutputVariableLineEdit.setText(data["on_error_output_value"])
        self.retryCountSpinbox.setValue(data["retry_count"])
        self.retryIntervalSpinbox.setValue(data["retry_interval"])
        self.directive["data"] = data

    def updateSettingData(self):
        data = self.directive["data"]
        data["web_object"] = self.webObjectCombobox.currentText()
        data["element_Scroller"] = self.elementScrollerCheckBox.isChecked()
        data["element_name"] = self.elementLabel.text()
        data["autoSearch"] = self.elementHasNoScrollerCheckBox.isChecked()
        data["Scroller_chosen"] = self.scrollerCombobox.currentIndex()
        data["position_chosen"] = self.positionCombobox.currentIndex()
        data["output"] = self.outputVariableNameLineEdit.text()
        data["time_out_period"] = self.waitForElementAppearLineEdit.text()
        data["log"] = self.printErrorLogsCheckbox.isChecked()
        data["handle"] = self.handleErrorWayCombobox.currentIndex()
        data["on_error_output_value"] = self.onErrorOutputVariableLineEdit.text()
        data["retry_count"] = self.retryCountSpinbox.value()
        data["retry_interval"] = self.retryIntervalSpinbox.value()
        self.updateDirectiveData2DB(self.directive["_id"], data)


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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = GettingScrollerPositionObjectSettingDialog("获取滚动条位置",1,1)
    win.show()
    sys.exit(app.exec_())

