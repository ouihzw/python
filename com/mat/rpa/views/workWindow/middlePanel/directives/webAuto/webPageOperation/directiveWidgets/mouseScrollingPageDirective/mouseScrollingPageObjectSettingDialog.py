# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from com.mat.rpa.utils import webAutoSave
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowSettingDialog
from com.mat.rpa.dao.workDao.directiveDao import DirectiveDao
class MouseScrollingPageObjectSettingDialog(flowSettingDialog.BasicFlowSettingDialog):
    def __init__(self, title, directive_id, id, parent=None):
        # 参照修改infolabel的提示信息
        super(MouseScrollingPageObjectSettingDialog, self).__init__(title, directive_id, id, parent)
        self.webSave = webAutoSave.WebAutoSave()
        self.setInfoLabelText(u'在指定的网页中滚动鼠标，可以设置为滚动到顶部、底部或者指定位置')
        self.changeImage(flowSettingDialog.BasicFlowSettingDialog.picPath + "openWebPageBig.png")
        self.screenWidth = 1920
        self.screenHeight = 1030
        self.setFixedSize(self.screenWidth * 0.45, self.screenHeight * 0.6)
        self.center()
        self.regularTabUI()
        self.seniorTabUI()
        self.errorHandlingTabUI()
        self.settingTabWidget.currentChanged.connect(self.changeOpenWebPageObjectSettingDialogSize)
        self.directiveDaoObj = DirectiveDao()
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
                                  "scroll_range": False,
                                  "element": "",
                                  "element_scroller": False,
                                  "scroller_position": 0,
                                  "abscissa": "0",
                                  "ordinate": "0",
                                  "scroller_effect": 0,
                                  "time_out": "20",
                                  "log": True,
                                  "handle": 0,
                                  "retry_count": 1,
                                  "retry_interval": 1}
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
        self.directiveInputSettingLayout.addWidget(self.webObjectCombobox, 0, 1, 1, 3, Qt.AlignLeft)
        self.webObjectTipLabel = flowSettingDialog.createTipLabel(u"网页对象",
                                                                  u"  输入一个获取到的或者通过\"打开网\n  页\"创建的网页对象")
        self.directiveInputSettingLayout.addWidget(self.webObjectTipLabel, 0, 4, 1, 1, Qt.AlignLeft)

        self.scrollOverSpecifiedElementCheckbox = QCheckBox()
        self.scrollOverSpecifiedElementCheckbox.setText(u"在指定元素上滚动")
        self.scrollOverSpecifiedElementCheckbox.setFont(__font)
        self.scrollOverSpecifiedElementCheckbox.stateChanged.connect(self.scrollOverSpecifiedElement)
        self.directiveInputSettingLayout.addWidget(self.scrollOverSpecifiedElementCheckbox, 1, 1, 1, 2, Qt.AlignLeft)
        self.scrollOverSpecifiedElementTipLabel = flowSettingDialog.createTipLabel(u"在指定元素上滚动",
                                                                    u"  是否在指定元素上滚动")
        self.directiveInputSettingLayout.addWidget(self.scrollOverSpecifiedElementTipLabel, 1, 3, 1, 1, Qt.AlignLeft)

        self.objectLabel = QLabel()
        self.objectLabel.setFont(__font)
        self.objectLabel.setText(u"操作目标:")
        self.directiveInputSettingLayout.addWidget(self.objectLabel, 2, 0, 1, 1, Qt.AlignRight)
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
        self.directiveInputSettingLayout.addLayout(self.elementLayout, 2, 1, 1, 3, Qt.AlignLeft)
        self.matchWayTipLabel = flowSettingDialog.createTipLabel(u"操作目标",
                                                                 u"  选择要操作的网页元素")
        self.directiveInputSettingLayout.addWidget(self.matchWayTipLabel, 2, 4, 1, 1, Qt.AlignLeft)
        self.objectLabel.hide()
        self.elementLabel.hide()
        self.pointoutButton.hide()
        self.matchWayTipLabel.hide()

        self.elementHasNoScrollerCheckbox = QCheckBox()
        self.elementHasNoScrollerCheckbox.setText(u"元素无滚动条，自动向上查找")
        self.elementHasNoScrollerCheckbox.setFont(__font)
        self.directiveInputSettingLayout.addWidget(self.elementHasNoScrollerCheckbox, 3, 1, 1, 2, Qt.AlignLeft)
        self.elementHasNoScrollerTipLabel = flowSettingDialog.createTipLabel(
            u"元素无滚动条，自动向上查找", u"  若当前元素无滚动条，自动向上查找有\n  滚动条的元素")
        self.directiveInputSettingLayout.addWidget(self.elementHasNoScrollerTipLabel, 3, 3, 1, 1, Qt.AlignLeft)
        self.elementHasNoScrollerCheckbox.hide()
        self.elementHasNoScrollerTipLabel.hide()

        self.scrollPositionLabel = QLabel()
        self.scrollPositionLabel.setFont(__font)
        self.scrollPositionLabel.setText(u"滚动位置:")
        self.directiveInputSettingLayout.addWidget(self.scrollPositionLabel, 4, 0, 1, 1, Qt.AlignRight)
        self.scrollPositionCombobox = QComboBox()
        self.scrollPositionCombobox.setObjectName("scrollPositionCombobox")
        self.scrollPositionCombobox.setFont(__font)
        self.scrollPositionCombobox.setMinimumSize(600, 50)
        self.scrollPositionCombobox.addItems([u"滚动到底部", u"滚动到顶部", u"滚动到指定位置", u"滚动一屏"])
        self.scrollPositionCombobox.currentIndexChanged.connect(self.changeRegularTab)
        self.scrollPositionCombobox.setItemDelegate(QStyledItemDelegate())
        self.scrollPositionCombobox.setStyleSheet(
            "QComboBox QAbstractItemView{selection-background-color: #f0f0f0;selection-color: #000;} QComboBox QAbstractItemView::item{min-height: 50px;}")
        self.directiveInputSettingLayout.addWidget(self.scrollPositionCombobox, 4, 1, 1, 3, Qt.AlignCenter)
        self.scrollPositionTipLabel = flowSettingDialog.createTipLabel(u"滚动位置",
                                                                          u"  指定网页滚动到的目标位置")
        self.directiveInputSettingLayout.addWidget(self.scrollPositionTipLabel, 4, 4, 1, 1, Qt.AlignLeft)

        self.abscissaLabel = QLabel()
        self.abscissaLabel.setFont(__font)
        self.abscissaLabel.setText(u"横坐标:")
        self.directiveInputSettingLayout.addWidget(self.abscissaLabel, 5, 1, 1, 1, Qt.AlignLeft)
        self.abscissaLineEdit = QLineEdit()
        self.abscissaLineEdit.setFont(__font)
        self.abscissaLineEdit.setMinimumSize(520, 50)
        self.abscissaLineEdit.setValidator(QIntValidator())
        self.directiveInputSettingLayout.addWidget(self.abscissaLineEdit, 5, 2, 1, 2, Qt.AlignCenter)
        self.abscissaFunctionBtn = flowSettingDialog.addFunctionButton(self.abscissaLineEdit,self)
        self.directiveInputSettingLayout.addWidget(self.abscissaFunctionBtn, 5, 2, 1, 2, Qt.AlignRight)
        self.abscissaTipLabel = flowSettingDialog.createTipLabel(u"横坐标",
                                                                 u"  鼠标移动到的目标位置的横坐标")
        self.directiveInputSettingLayout.addWidget(self.abscissaTipLabel, 5, 4, 1, 1, Qt.AlignLeft)
        self.abscissaLabel.hide()
        self.abscissaLineEdit.hide()
        self.abscissaFunctionBtn.hide()
        self.abscissaTipLabel.hide()

        self.ordinateLabel = QLabel()
        self.ordinateLabel.setFont(__font)
        self.ordinateLabel.setText(u"纵坐标:")
        self.directiveInputSettingLayout.addWidget(self.ordinateLabel, 6, 1, 1, 1, Qt.AlignLeft)
        self.ordinateLineEdit = QLineEdit()
        self.ordinateLineEdit.setFont(__font)
        self.ordinateLineEdit.setMinimumSize(520, 50)
        self.ordinateLineEdit.setValidator(QIntValidator())
        self.directiveInputSettingLayout.addWidget(self.ordinateLineEdit, 6, 2, 1, 2, Qt.AlignCenter)
        self.ordinateFunctionBtn = flowSettingDialog.addFunctionButton(self.ordinateLineEdit,self)
        self.directiveInputSettingLayout.addWidget(self.ordinateFunctionBtn, 6, 2, 1, 2, Qt.AlignRight)
        self.ordinateTipLabel = flowSettingDialog.createTipLabel(u"纵坐标",
                                                                 u"  鼠标移动到的位置的纵坐标")
        self.directiveInputSettingLayout.addWidget(self.ordinateTipLabel, 6, 4, 1, 1, Qt.AlignLeft)
        self.ordinateLabel.hide()
        self.ordinateLineEdit.hide()
        self.ordinateFunctionBtn.hide()
        self.ordinateTipLabel.hide()

        self.scrollEffectLabel = QLabel()
        self.scrollEffectLabel.setFont(__font)
        self.scrollEffectLabel.setText(u"滚动效果:")
        self.directiveInputSettingLayout.addWidget(self.scrollEffectLabel, 7, 0, 1, 1, Qt.AlignRight)
        self.scrollEffectCombobox = QComboBox()
        self.scrollEffectCombobox.setObjectName("scrollEffectCombobox")
        self.scrollEffectCombobox.setFont(__font)
        self.scrollEffectCombobox.setMinimumSize(600, 50)
        self.scrollEffectCombobox.addItems([u"平滑滚动", u"瞬间滚动"])
        self.scrollEffectCombobox.setItemDelegate(QStyledItemDelegate())
        self.scrollEffectCombobox.setStyleSheet(
            "QComboBox QAbstractItemView{selection-background-color: #f0f0f0;selection-color: #000;} QComboBox QAbstractItemView::item{min-height: 50px;}")
        self.directiveInputSettingLayout.addWidget(self.scrollEffectCombobox,7, 1, 1, 3, Qt.AlignCenter)
        self.scrollEffectTipLabel = flowSettingDialog.createTipLabel(u"滚动效果",
                                                                       u"  指定鼠标的滚动效果，可以是平滑滚动或\n  者瞬间滚动")
        self.directiveInputSettingLayout.addWidget(self.scrollEffectTipLabel, 7, 4, 1, 1, Qt.AlignLeft)
        self.directiveInputSettingLayout.setColumnStretch(0, 20)
        self.directiveInputSettingLayout.setColumnStretch(1, 5)
        self.directiveInputSettingLayout.setColumnStretch(2, 17)
        self.directiveInputSettingLayout.setColumnStretch(3, 48)
        self.directiveInputSettingLayout.setColumnStretch(4, 10)

        self.directiveOutputSettingLayout = QGridLayout()
        self.directiveOutputSettingLayout.setContentsMargins(10, 0, 0, 20)
        self.directiveOutputSettingLayout.setSpacing(10)
        self.directiveOutputSettingPanel.setLayout(self.directiveOutputSettingLayout)

        self.emptyLabel = QLabel()
        self.emptyLabel.setFont(__font)
        self.emptyLabel.setText(u"当前指令不包含任何输出项")
        self.emptyLabel.setStyleSheet("color:#838b8b;font-size:16px;font-family:Courier")
        self.emptyLabel.setAlignment(Qt.AlignCenter)
        self.directiveOutputSettingLayout.addWidget(self.emptyLabel, 0, 0, 1, 1, Qt.AlignCenter)

    def scrollOverSpecifiedElement(self):
        if self.scrollOverSpecifiedElementCheckbox.isChecked():
            self.objectLabel.show()
            self.elementLabel.show()
            self.pointoutButton.show()
            self.matchWayTipLabel.show()
            self.elementHasNoScrollerCheckbox.show()
            self.elementHasNoScrollerTipLabel.show()
            self.changeOpenWebPageObjectSettingDialogSize()
        else:
            self.objectLabel.hide()
            self.elementLabel.hide()
            self.pointoutButton.hide()
            self.matchWayTipLabel.hide()
            self.elementHasNoScrollerCheckbox.hide()
            self.elementHasNoScrollerTipLabel.hide()
            self.changeOpenWebPageObjectSettingDialogSize()

    def changeRegularTab(self):
        if self.scrollPositionCombobox.currentIndex() == 2:
            self.abscissaLabel.show()
            self.abscissaLineEdit.show()
            self.abscissaFunctionBtn.show()
            self.abscissaTipLabel.show()
            self.ordinateLabel.show()
            self.ordinateLineEdit.show()
            self.ordinateFunctionBtn.show()
            self.ordinateTipLabel.show()
            self.changeOpenWebPageObjectSettingDialogSize()
        else:
            self.abscissaLabel.hide()
            self.abscissaLineEdit.hide()
            self.abscissaFunctionBtn.hide()
            self.abscissaTipLabel.hide()
            self.ordinateLabel.hide()
            self.ordinateLineEdit.hide()
            self.ordinateFunctionBtn.hide()
            self.ordinateTipLabel.hide()
            self.changeOpenWebPageObjectSettingDialogSize()

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

        self.waitElementExistLabel = QLabel()
        self.waitElementExistLabel.setFont(__font)
        self.waitElementExistLabel.setText(u"等待元素存在(s):")
        self.seniorTabLayout.addWidget(self.waitElementExistLabel, 0, 0, 1, 1, Qt.AlignRight)
        self.waitElementExistLineEdit = QLineEdit()
        self.waitElementExistLineEdit.setFont(__font)
        self.waitElementExistLineEdit.setMinimumSize(600, 50)
        self.waitElementExistLineEdit.setText("20")
        self.seniorTabLayout.addWidget(self.waitElementExistLineEdit, 0, 1, 1, 1, Qt.AlignCenter)
        self.waitElementExistFunctionBtn = flowSettingDialog.addFunctionButton(self.waitElementExistLineEdit, self)
        self.seniorTabLayout.addWidget(self.waitElementExistFunctionBtn, 0, 1, 1, 1, Qt.AlignRight)
        self.waitElementExistTipLabel = flowSettingDialog.createTipLabel(
            u"等待元素存在(s)",
            u"  等待元素存在的超时时间")
        self.seniorTabLayout.addWidget(self.waitElementExistTipLabel, 0, 2, 1, 1, Qt.AlignLeft)

    def changeOpenWebPageObjectSettingDialogSize(self):
        if self.settingTabWidget.currentIndex() == 0:
            if self.scrollOverSpecifiedElementCheckbox.isChecked():
                if self.scrollPositionCombobox.currentIndex() == 2:
                    self.setFixedSize(self.screenWidth * 0.45, self.screenHeight * 0.9)
                    self.center()
                else:
                    self.setFixedSize(self.screenWidth * 0.45, self.screenHeight * 0.75)
                    self.center()
            else:
                if self.scrollPositionCombobox.currentIndex() == 2:
                    self.setFixedSize(self.screenWidth * 0.45, self.screenHeight * 0.75)
                    self.center()
                else:
                    self.setFixedSize(self.screenWidth * 0.45, self.screenHeight * 0.6)
                    self.center()
        elif self.settingTabWidget.currentIndex() == 1:
            self.setFixedSize(self.screenWidth * 0.47, self.screenHeight * 0.32)
            self.center()
        elif self.settingTabWidget.currentIndex() == 2:
            if self.handleErrorWayCombobox.currentIndex() == 2:
                self.setFixedSize(self.screenWidth * 0.46, self.screenHeight * 0.37)
                self.center()
            else:
                self.setFixedSize(self.screenWidth * 0.46, self.screenHeight * 0.3)
                self.center()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2-50)

    def executeStep(self):
        try:
            handle = self.webSave.getWebObjectHandle(self.webObjectCombobox.currentText())
            client = self.webSave.getWebObjectClient(self.webObjectCombobox.currentText())
            client.switch_to.window(handle)
            if self.scrollOverSpecifiedElementCheckbox.isChecked():
                WebDriverWait(client, int(self.waitElementExistLineEdit.text())).until(
                    lambda p: p.find_element(By.XPATH,
                                             self.elementDaoMongo.getOneElement(
                                                 self.elementLabel.text())[
                                                 "xpath"]).is_displayed())
                rollHeight = client.execute_script("return action=document.evaluate(\""+self.elementDaoMongo.getOneElement(self.elementLabel.text())["xpath"]+"\",document).iterateNext().scrollTop")
                rollWidth = client.execute_script("return action=document.evaluate(\""+self.elementDaoMongo.getOneElement(self.elementLabel.text())["xpath"]+"\",document).iterateNext().scrollLeft")
                scrollHeight =client.execute_script("return action=document.evaluate(\""+self.elementDaoMongo.getOneElement(self.elementLabel.text())["xpath"]+"\",document).iterateNext().scrollHeight")
                clientHeight = client.execute_script("return action=$(window).height(); ")
                if self.scrollEffectCombobox.currentIndex() == 0:
                    if self.scrollPositionCombobox.currentIndex() == 0:
                        height = rollHeight + scrollHeight % 10
                        while height < scrollHeight:
                            height = height + 10
                            client.execute_script("document.evaluate(\""+self.elementDaoMongo.getOneElement(self.elementLabel.text())["xpath"]+"\",document).iterateNext().scrollTo(" + str(rollHeight) + ", %s)" % (height))
                    elif self.scrollPositionCombobox.currentIndex() == 1:
                        height = rollHeight - rollHeight % 10
                        while height > 0:
                            height = height - 10
                            client.execute_script("document.evaluate(\""+self.elementDaoMongo.getOneElement(self.elementLabel.text())["xpath"]+"\",document).iterateNext().scrollTo(" + str(rollHeight) + ", %s)" % (height))
                    elif self.scrollPositionCombobox.currentIndex() == 2:
                        if self.abscissaLineEdit.text() == "":
                            self.abscissaLineEdit.setText("0")
                        if self.ordinateLineEdit.text() == "":
                            self.ordinateLineEdit.setText("0")
                        count = abs(int(self.ordinateLineEdit.text()) - rollHeight) / 10
                        if count != 0:
                            lateralMovementDistance = abs(int(self.abscissaLineEdit.text()) - rollWidth) / count
                        else:
                            lateralMovementDistance = 10
                        if int(self.abscissaLineEdit.text()) > rollWidth:
                            width = rollWidth + abs(
                                int(self.abscissaLineEdit.text()) - rollWidth) % lateralMovementDistance
                            if int(self.ordinateLineEdit.text()) > rollHeight:
                                height = rollHeight + abs(int(self.ordinateLineEdit.text()) - rollHeight) % 10
                                while height < int(self.ordinateLineEdit.text()):
                                    width += lateralMovementDistance
                                    height += 10
                                    client.execute_script("document.evaluate(\""+self.elementDaoMongo.getOneElement(self.elementLabel.text())["xpath"]+"\",document).iterateNext().scrollTo(" + str(width) + "," + str(height) + ");")
                            elif int(self.ordinateLineEdit.text()) == rollHeight:
                                while width < int(self.abscissaLineEdit.text()):
                                    width += lateralMovementDistance
                                    client.execute_script("document.evaluate(\""+self.elementDaoMongo.getOneElement(self.elementLabel.text())["xpath"]+"\",document).iterateNext().scrollLeft=" + str(width))
                            else:
                                height = rollHeight - abs(int(self.ordinateLineEdit.text()) - rollHeight) % 10
                                while height > int(self.ordinateLineEdit.text()):
                                    width += lateralMovementDistance
                                    height -= 10
                                    client.execute_script("document.evaluate(\""+self.elementDaoMongo.getOneElement(self.elementLabel.text())["xpath"]+"\",document).iterateNext().scrollTo(" + str(width) + "," + str(height) + ");")
                        elif int(self.abscissaLineEdit.text()) == rollWidth:
                            if int(self.ordinateLineEdit.text()) > rollHeight:
                                height = rollHeight + abs(int(self.ordinateLineEdit.text()) - rollHeight) % 10
                                while height < int(self.ordinateLineEdit.text()):
                                    height += 10
                                    client.execute_script("document.evaluate(\""+self.elementDaoMongo.getOneElement(self.elementLabel.text())["xpath"]+"\",document).iterateNext().scrollTo(" + str(rollHeight) + ", %s)" % (height))
                            elif int(self.ordinateLineEdit.text()) == rollHeight:
                                pass
                            else:
                                height = rollHeight - abs(int(self.ordinateLineEdit.text()) - rollHeight) % 10
                                while height > int(self.ordinateLineEdit.text()):
                                    height -= 10
                                    client.execute_script("document.evaluate(\""+self.elementDaoMongo.getOneElement(self.elementLabel.text())["xpath"]+"\",document).iterateNext().scrollTo(" + str(rollHeight) + ", %s)" % (height))
                        else:
                            width = rollWidth - abs(
                                int(self.abscissaLineEdit.text()) - rollWidth) % lateralMovementDistance
                            if float(self.ordinateLineEdit.text()) > rollHeight:
                                height = rollHeight + abs(int(self.ordinateLineEdit.text()) - rollHeight) % 10
                                while height < int(self.ordinateLineEdit.text()):
                                    width -= lateralMovementDistance
                                    height += 10
                                    client.execute_script("document.evaluate(\""+self.elementDaoMongo.getOneElement(self.elementLabel.text())["xpath"]+"\",document).iterateNext().scrollTo(" + str(width) + "," + str(height) + ");")
                            elif int(self.ordinateLineEdit.text()) == rollHeight:
                                while width > int(self.abscissaLineEdit.text()):
                                    width -= lateralMovementDistance
                                    client.execute_script("document.evaluate(\""+self.elementDaoMongo.getOneElement(self.elementLabel.text())["xpath"]+"\",document).iterateNext().scrollLeft=" + str(width))
                            else:
                                height = rollHeight - abs(int(self.ordinateLineEdit.text()) - rollHeight) % 10
                                print(height, abs(int(self.ordinateLineEdit.text()) - rollHeight) % 10)
                                while height > int(self.ordinateLineEdit.text()):
                                    width -= lateralMovementDistance
                                    height -= 10
                                    print(width, height)
                                    client.execute_script("document.evaluate(\""+self.elementDaoMongo.getOneElement(self.elementLabel.text())["xpath"]+"\",document).iterateNext().scrollTo(" + str(width) + "," + str(height) + ");")
                    elif self.scrollPositionCombobox.currentIndex() == 3:
                        height = rollHeight + clientHeight % 10
                        while height < rollHeight + clientHeight:
                            height = height + 10
                            client.execute_script("document.evaluate(\""+self.elementDaoMongo.getOneElement(self.elementLabel.text())["xpath"]+"\",document).iterateNext().scrollTo(" + str(rollHeight) + ", %s)" % (height))
                elif self.scrollEffectCombobox.currentIndex() == 1:
                    if self.scrollPositionCombobox.currentIndex() == 0:
                        client.execute_script("document.evaluate(\""+self.elementDaoMongo.getOneElement(self.elementLabel.text())["xpath"]+"\",document).iterateNext().scrollTo(" + str(rollHeight) + "," + str(scrollHeight) + ")")
                    elif self.scrollPositionCombobox.currentIndex() == 1:
                        client.execute_script("document.evaluate(\""+self.elementDaoMongo.getOneElement(self.elementLabel.text())["xpath"]+"\",document).iterateNext().scrollTo(" + str(rollHeight) + ",0)")
                    elif self.scrollPositionCombobox.currentIndex() == 2:
                        if self.abscissaLineEdit.text() == "":
                            self.abscissaLineEdit.setText("0")
                        if self.ordinateLineEdit.text() == "":
                            self.ordinateLineEdit.setText("0")
                        client.execute_script(
                            "document.evaluate(\""+self.elementDaoMongo.getOneElement(self.elementLabel.text())["xpath"]+"\",document).iterateNext().scrollTo(" + self.abscissaLineEdit.text() + "," + self.ordinateLineEdit.text() + ");")
                    elif self.scrollPositionCombobox.currentIndex() == 3:
                        client.execute_script(
                            "document.evaluate(\""+self.elementDaoMongo.getOneElement(self.elementLabel.text())["xpath"]+"\",document).iterateNext().scrollTo(" + str(rollHeight) + "," + str(rollHeight + clientHeight) + ");")
            else:
                rollHeight = client.execute_script("return action=document.documentElement.scrollTop")
                rollWidth = client.execute_script("return action=document.documentElement.scrollLeft")
                scrollHeight = client.execute_script("return action=document.documentElement.scrollHeight")
                clientHeight = client.execute_script("return action=document.documentElement.clientHeight")
                if self.scrollEffectCombobox.currentIndex() == 0:
                    if self.scrollPositionCombobox.currentIndex() == 0:
                        height = rollHeight + scrollHeight % 10
                        while height < scrollHeight:
                            height = height + 10
                            client.execute_script("window.scrollTo(" + str(rollHeight) + ", %s)" % (height))
                    elif self.scrollPositionCombobox.currentIndex() == 1:
                        height = rollHeight - rollHeight % 10
                        while height > 0:
                            height = height - 10
                            client.execute_script("window.scrollTo(" + str(rollHeight) + ", %s)" % (height))
                    elif self.scrollPositionCombobox.currentIndex() == 2:
                        if self.abscissaLineEdit.text() == "":
                            self.abscissaLineEdit.setText("0")
                        if self.ordinateLineEdit.text() == "":
                            self.ordinateLineEdit.setText("0")
                        count = abs(int(self.ordinateLineEdit.text()) - rollHeight) / 10
                        if count != 0:
                            lateralMovementDistance = abs(int(self.abscissaLineEdit.text()) - rollWidth) / count
                        else:
                            lateralMovementDistance = 10
                        if int(self.abscissaLineEdit.text()) > rollWidth:
                            width = rollWidth + abs(
                                int(self.abscissaLineEdit.text()) - rollWidth) % lateralMovementDistance
                            if int(self.ordinateLineEdit.text()) > rollHeight:
                                height = rollHeight + abs(int(self.ordinateLineEdit.text()) - rollHeight) % 10
                                while height < int(self.ordinateLineEdit.text()):
                                    width += lateralMovementDistance
                                    height += 10
                                    client.execute_script("window.scrollTo(" + str(width) + "," + str(height) + ");")
                            elif int(self.ordinateLineEdit.text()) == rollHeight:
                                while width < int(self.abscissaLineEdit.text()):
                                    width += lateralMovementDistance
                                    client.execute_script("document.documentElement.scrollLeft=" + str(width))
                            else:
                                height = rollHeight - abs(int(self.ordinateLineEdit.text()) - rollHeight) % 10
                                while height > int(self.ordinateLineEdit.text()):
                                    width += lateralMovementDistance
                                    height -= 10
                                    client.execute_script("window.scrollTo(" + str(width) + "," + str(height) + ");")
                        elif int(self.abscissaLineEdit.text()) == rollWidth:
                            if int(self.ordinateLineEdit.text()) > rollHeight:
                                height = rollHeight + abs(int(self.ordinateLineEdit.text()) - rollHeight) % 10
                                while height < int(self.ordinateLineEdit.text()):
                                    height += 10
                                    client.execute_script("window.scrollTo(" + str(rollHeight) + ", %s)" % (height))
                            elif int(self.ordinateLineEdit.text()) == rollHeight:
                                pass
                            else:
                                height = rollHeight - abs(int(self.ordinateLineEdit.text()) - rollHeight) % 10
                                while height > int(self.ordinateLineEdit.text()):
                                    height -= 10
                                    client.execute_script("window.scrollTo(" + str(rollHeight) + ", %s)" % (height))
                        else:
                            width = rollWidth - abs(
                                int(self.abscissaLineEdit.text()) - rollWidth) % lateralMovementDistance
                            if float(self.ordinateLineEdit.text()) > rollHeight:
                                height = rollHeight + abs(int(self.ordinateLineEdit.text()) - rollHeight) % 10
                                while height < int(self.ordinateLineEdit.text()):
                                    width -= lateralMovementDistance
                                    height += 10
                                    client.execute_script("window.scrollTo(" + str(width) + "," + str(height) + ");")
                            elif int(self.ordinateLineEdit.text()) == rollHeight:
                                while width > int(self.abscissaLineEdit.text()):
                                    width -= lateralMovementDistance
                                    client.execute_script("document.documentElement.scrollLeft=" + str(width))
                            else:
                                height = rollHeight - abs(int(self.ordinateLineEdit.text()) - rollHeight) % 10
                                print(height, abs(int(self.ordinateLineEdit.text()) - rollHeight) % 10)
                                while height > int(self.ordinateLineEdit.text()):
                                    width -= lateralMovementDistance
                                    height -= 10
                                    print(width, height)
                                    client.execute_script("window.scrollTo(" + str(width) + "," + str(height) + ");")
                    elif self.scrollPositionCombobox.currentIndex() == 3:
                        height = rollHeight + clientHeight % 10
                        while height < rollHeight + clientHeight:
                            height = height + 10
                            client.execute_script("window.scrollTo(" + str(rollHeight) + ", %s)" % (height))
                elif self.scrollEffectCombobox.currentIndex() == 1:
                    if self.scrollPositionCombobox.currentIndex() == 0:
                        client.execute_script("window.scrollTo(" + str(rollHeight) + "," + str(scrollHeight) + ")")
                    elif self.scrollPositionCombobox.currentIndex() == 1:
                        client.execute_script("window.scrollTo(" + str(rollHeight) + ",0)")
                    elif self.scrollPositionCombobox.currentIndex() == 2:
                        if self.abscissaLineEdit.text() == "":
                            self.abscissaLineEdit.setText("0")
                        if self.ordinateLineEdit.text() == "":
                            self.ordinateLineEdit.setText("0")
                        client.execute_script(
                            "window.scrollTo(" + self.abscissaLineEdit.text() + "," + self.ordinateLineEdit.text() + ");")
                    elif self.scrollPositionCombobox.currentIndex() == 3:
                        client.execute_script(
                            "window.scrollTo(" + str(rollHeight) + "," + str(rollHeight + clientHeight) + ");")
        except Exception as e:
            print(e)
    def getSettingData(self):
        data = self.getDirectiveSettingDataFromDB(self.directive["_id"])
        self.webObjectCombobox.setCurrentText(data["web_object"])
        self.scrollOverSpecifiedElementCheckbox.setChecked(data["scroll_range"])
        self.elementLabel.setText(data["element"])
        self.elementHasNoScrollerCheckbox.setChecked(data["element_scroller"])
        self.scrollPositionCombobox.setCurrentIndex(data["scroller_position"])
        self.abscissaLineEdit.setText(data["abscissa"])
        self.ordinateLineEdit.setText(data["ordinate"])
        self.scrollEffectCombobox.setCurrentIndex(data["scroller_effect"])
        self.waitElementExistLineEdit.setText(data["time_out"])
        self.printErrorLogsCheckbox.setChecked(data["log"])
        self.handleErrorWayCombobox.setCurrentIndex(data["handle"])
        self.retryCountSpinbox.setValue(data["retry_count"])
        self.retryIntervalSpinbox.setValue(data["retry_interval"])
        self.directive["data"] = data

    def updateSettingData(self):
        data = self.directive["data"]
        data["web_object"] = self.webObjectCombobox.currentText()
        data["scroll_range"]=self.scrollOverSpecifiedElementCheckbox.isChecked()
        data["element"]=self.elementLabel.text()
        data["element_scroller"]= self.elementHasNoScrollerCheckbox.isChecked()
        data["scroller_position"]=self.scrollPositionCombobox.currentIndex()
        data["abscissa"]=self.abscissaLineEdit.text()
        data["ordinate"]=self.ordinateLineEdit.text()
        data["scroller_effect"]=self.scrollEffectCombobox.currentIndex()
        data["time_out"]=self.waitElementExistLineEdit.text()
        data["log"] = self.printErrorLogsCheckbox.isChecked()
        data["handle"] = self.handleErrorWayCombobox.currentIndex()
        data["retry_count"] = self.retryCountSpinbox.value()
        data["retry_interval"] = self.retryIntervalSpinbox.value()
        self.updateDirectiveData2DB(self.directive["_id"], self.directive["data"])
        self.updateSecondLineInfo()

    def handleQuestionBtnClicked(self):
        print("点击使用说明按钮")

    def handleConfirmBtnClicked(self):
        self.accept()

    def handleCancelBtnClicked(self):
        self.reject()

    def handleExecutionBtnClicked(self):
        self.executeStep()

    def updateDirectiveData2DB(self, directive_id, data: dict):
        self.directiveDaoObj.updateDirective(directive_id, {"data": data})

    def getDirectiveSettingDataFromDB(self, directive_id):
        return self.directiveDaoObj.getOneDirective(directive_id)["data"]