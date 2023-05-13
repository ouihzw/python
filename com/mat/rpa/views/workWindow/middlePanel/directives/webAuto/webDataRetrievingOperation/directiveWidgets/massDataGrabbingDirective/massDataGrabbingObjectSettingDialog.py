# -*- coding:utf-8 -*-
import csv
import sys
import time
from os import path

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from selenium.webdriver.common.by import By

from com.mat.rpa.dao.workDao.directiveDao import DirectiveDao
from com.mat.rpa.utils import webAutoSave
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowSettingDialog
import openpyxl


class MassDataGrabbingObjectSettingDialog(flowSettingDialog.BasicFlowSettingDialog):
    def __init__(self, title, directive_id, id, parent=None):
        super().__init__(title, directive_id, id, parent)
        self.directiveDaoObj = DirectiveDao()
        self.webSave = webAutoSave.WebAutoSave()
        self.setInfoLabelText(u"自动获取当前页面的商品信息，并将商品信息自动保存至csv文件中")
        self.changeImage(flowSettingDialog.BasicFlowSettingDialog.picPath + "img.png")
        self.regularTabUI()
        self.setFixedHeight(1000)
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
        __font.setPixelSize(30)
        __font.setFamily("Courier")
        # 布局指令输入面板
        self.directiveInputSettingLayout = QGridLayout()
        self.directiveInputSettingLayout.setContentsMargins(50, 0, 20, 0)
        self.directiveInputSettingLayout.setSpacing(10)
        self.directiveInputSettingLayout.setVerticalSpacing(30)
        self.directiveInputSettingPanel.setLayout(self.directiveInputSettingLayout)
        self.webPageObjLabel = QLabel()
        self.webPageObjLabel.setFont(__font)
        self.webPageObjLabel.setText("网页对象:")
        self.directiveInputSettingLayout.addWidget(self.webPageObjLabel, 0, 0, 1, 1, Qt.AlignRight)
        self.webPageObjCombobox = QComboBox()
        self.webPageObjCombobox.setObjectName("webPageObjCombobox")
        self.webPageObjCombobox.setFont(__font)
        self.webPageObjCombobox.setMinimumSize(600, 50)
        self.webPageObjCombobox.setEditable(False)

        for i in range(len(self.webSave.getWebObjectName())):
            self.webPageObjCombobox.addItem(self.webSave.getWebObjectName()[i])

        self.webPageObjCombobox.setItemDelegate(QStyledItemDelegate())
        self.webPageObjCombobox.setStyleSheet(
            "QComboBox QAbstractItemView{selection-background-color: #f0f0f0;selection-color: #000;} QComboBox QAbstractItemView::item{min-height: 50px;}"
        )
        self.directiveInputSettingLayout.addWidget(self.webPageObjCombobox, 0, 1, 1, 1, Qt.AlignLeft)
        self.webObjectTipLabel = flowSettingDialog.createTipLabel(u"网页对象",
                                                                  u"  输入一个获取到的或者通过\"打开网\n  页\"创建的网页对象")
        self.directiveInputSettingLayout.addWidget(self.webObjectTipLabel, 0, 2, 1, 1, Qt.AlignLeft)
        self.classnameLabel = QLabel()
        self.classnameLabel.setFont(__font)
        self.classnameLabel.setText('class_name:')
        self.directiveInputSettingLayout.addWidget(self.classnameLabel, 1, 0, 1, 1, Qt.AlignRight)
        self.classnameLineEdit = QLineEdit()
        self.classnameLineEdit.setFont(__font)
        self.classnameLineEdit.setMinimumSize(600, 30)
        self.directiveInputSettingLayout.addWidget(self.classnameLineEdit, 1, 1, 1, 1, Qt.AlignLeft)

        self.priceLabel = QLabel()
        self.priceLabel.setFont(__font)
        self.priceLabel.setText('price:')
        self.directiveInputSettingLayout.addWidget(self.priceLabel, 2, 0, 1, 1, Qt.AlignRight)
        self.priceLineEdit = QLineEdit()
        self.priceLineEdit.setFont(__font)
        self.priceLineEdit.setMinimumSize(600, 30)
        self.directiveInputSettingLayout.addWidget(self.priceLineEdit, 2, 1, 1, 1, Qt.AlignLeft)

        self.nameLabel = QLabel()
        self.nameLabel.setFont(__font)
        self.nameLabel.setText('name:')
        self.directiveInputSettingLayout.addWidget(self.nameLabel, 3, 0, 1, 1, Qt.AlignRight)
        self.nameLineEdit = QLineEdit()
        self.nameLineEdit.setFont(__font)
        self.nameLineEdit.setMinimumSize(600, 30)
        self.directiveInputSettingLayout.addWidget(self.nameLineEdit, 3, 1, 1, 1, Qt.AlignLeft)

        self.commitLabel = QLabel()
        self.commitLabel.setFont(__font)
        self.commitLabel.setText('commit:')
        self.directiveInputSettingLayout.addWidget(self.commitLabel, 4, 0, 1, 1, Qt.AlignRight)
        self.commitLineEdit = QLineEdit()
        self.commitLineEdit.setFont(__font)
        self.commitLineEdit.setMinimumSize(600, 30)
        self.directiveInputSettingLayout.addWidget(self.commitLineEdit, 4, 1, 1, 1, Qt.AlignLeft)

        self.labelLabel = QLabel()
        self.labelLabel.setFont(__font)
        self.labelLabel.setText('label:')
        self.directiveInputSettingLayout.addWidget(self.labelLabel, 5, 0, 1, 1, Qt.AlignRight)
        self.labelLineEdit = QLineEdit()
        self.labelLineEdit.setFont(__font)
        self.labelLineEdit.setMinimumSize(600, 30)
        self.directiveInputSettingLayout.addWidget(self.labelLineEdit, 5, 1, 1, 1, Qt.AlignLeft)

        self.linklabel = QLabel()
        self.linklabel.setFont(__font)
        self.linklabel.setText('link:')
        self.directiveInputSettingLayout.addWidget(self.linklabel, 6, 0, 1, 1, Qt.AlignRight)
        self.linkLineEdit = QLineEdit()
        self.linkLineEdit.setFont(__font)
        self.linkLineEdit.setMinimumSize(600,30)
        self.directiveInputSettingLayout.addWidget(self.linkLineEdit,6, 1, 1, 1, Qt.AlignLeft)

        self.nextPageBtnLabel = QLabel("下一页按钮：")
        self.nextPageBtnLabel.setFont(__font)
        self.directiveInputSettingLayout.addWidget(self.nextPageBtnLabel, 7, 0, 1, 1, Qt.AlignRight)
        self.nextPageLineEdit = QLineEdit()
        self.nextPageLineEdit.setFont(__font)
        self.nextPageLineEdit.setMinimumSize(390, 30)
        self.nextPageLineEdit.setEnabled(False)
        self.directiveInputSettingLayout.addWidget(self.nextPageLineEdit, 7, 1, 1, 1, Qt.AlignLeft)

        self.pointoutButton = flowSettingDialog.readElementFunctionButton(self.nextPageLineEdit, self)
        self.directiveInputSettingLayout.addWidget(self.pointoutButton, 7, 1, 1, 1, Qt.AlignRight)

        self.grabPageNumberLabel = QLabel("抓取页数：")
        self.grabPageNumberLabel.setFont(__font)
        self.directiveInputSettingLayout.addWidget(self.grabPageNumberLabel, 8, 0, 1, 1, Qt.AlignRight)

        self.pageNumberLineEdit = QLineEdit()
        self.pageNumberLineEdit.setFont(__font)
        self.pageNumberLineEdit.setMinimumSize(300, 30)
        self.directiveInputSettingLayout.addWidget(self.pageNumberLineEdit, 8, 1, 1, 1, Qt.AlignLeft)


    def executeStep(self):
        try:
            handle = self.webSave.getWebObjectHandle(self.webPageObjCombobox.currentText())
            client = self.webSave.getWebObjectClient(self.webPageObjCombobox.currentText())
            client.switch_to.window(handle)
            time.sleep(10)
            goods = client.find_elements(By.CLASS_NAME, self.classnameLineEdit.text())
            data = []
            i = 0
            for good in goods:
                # 获取商品链接
                link = good.find_element(By.TAG_NAME, 'a').get_attribute('href')
                # 获取商品标题名称
                title = good.find_element(By.CSS_SELECTOR, self.nameLineEdit.text()).text.replace('\n', '')
                # 获取商品价格
                price = good.find_element(By.CSS_SELECTOR, self.priceLineEdit.text()).text.replace('\n', '')
                # 获取商品评价数量
                commit = good.find_element(By.CSS_SELECTOR, self.commitLineEdit.text()).text.replace('\n', '')
                # 获取商品标签
                lables = good.find_elements(By.CSS_SELECTOR, self.labelLineEdit.text())
                lable = ' '.join([i.text for i in lables])
                # 将商品数据存入字典
                good_data = {
                    '商品标题': title,
                    '商品价格': price,
                    '商品链接': link,
                    '评论量': commit,
                    '标签': lable
                }
                data.append(good_data)
            header = ['商品标题', '商品价格', '商品链接', '评论量', '标签']
            # 获取当前文件路径
            paths = path.dirname(__file__)
            # 将当前文件路径与文件名拼接起来作为商品数据的存储路径
            file = path.join(paths, 'good_data.csv')
            # 以追加写入的方式将商品数据保存到文件中
            with open(file, 'a+', encoding='utf-8', newline='') as wf:
                f_csv = csv.DictWriter(wf, header)
                f_csv.writeheader()
                f_csv.writerows(data)
        except Exception as e:
            print(e)

    # 实现确认和取消按钮点击事件
    def handleQuestionBtnClicked(self):
        print("点击获取信息按钮")

    def handleConfirmBtnClicked(self):
        self.accept()

    def handleCancelBtnClicked(self):
        self.reject()

    # def handleExecutionBtnClicked(self): 根据情况实现指令执行按钮事件
    #   print("点击执行按钮)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MassDataGrabbingObjectSettingDialog("电商商品信息获取", 1, 1)
    win.show()
    app.exec_()
