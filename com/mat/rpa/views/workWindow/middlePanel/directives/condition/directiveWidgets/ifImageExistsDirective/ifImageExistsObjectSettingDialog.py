# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowSettingDialog
from com.mat.rpa.utils.sizeCalc import screenPercentage
comboBoxStyleSheet = """
QComboBox QAbstractItemView {
    selection-background-color: #f0f0f0;
    selection-color: #000;
}
QComboBox QAbstractItemView::item {
    min-height: 50px;
}
"""
class IfImageExistsObjectSettingDialog(flowSettingDialog.BasicFlowSettingDialog):

    def __init__(self, title, parent=None):
        super().__init__(title, parent)
        __font = QFont()
        __font.setPixelSize(20)
        __font.setFamily("Courier")
        # 改变图片
        self.changeImage(flowSettingDialog.BasicFlowSettingDialog.picPath + "openWebPageBig.png")
        self.infoLabel.setText("判断目标图像是否存在")
        self.regularTabUI()

    def regularTabUI(self):
        __font = QFont()
        __font.setPixelSize(20)
        __font.setFamily("Courier")
        self.directiveInputSettingLayout = QGridLayout()
        self.directiveInputSettingLayout.setContentsMargins(20, 0, 20, 0)
        self.directiveInputSettingLayout.setSpacing(10)
        self.directiveInputSettingLayout.setVerticalSpacing(20)
        self.directiveInputSettingPanel.setLayout(self.directiveInputSettingLayout)
        searchRangeLabel = QLabel(text="搜索范围:", font=__font)
        self.directiveInputSettingLayout.addWidget(searchRangeLabel, 0, 0, 1, 1, Qt.AlignRight)
        self.searchRangeComboBox = QComboBox(font=__font)
        self.searchRangeComboBox.setMinimumSize(650, 50)
        self.searchRangeComboBox.setItemDelegate(QStyledItemDelegate())
        self.searchRangeComboBox.setStyleSheet(comboBoxStyleSheet)
        self.searchRangeComboBox.addItems(["整个屏幕", "窗口对象", "当前激活窗口"])
        self.directiveInputSettingLayout.addWidget(self.searchRangeComboBox, 0, 1, 1, 1, Qt.AlignCenter)
        searchRangeTipLabel = flowSettingDialog.createTipLabel("搜索范围", "可选择整个屏幕或指定的窗口")
        self.directiveInputSettingLayout.addWidget(searchRangeTipLabel, 0, 2, 1, 1, Qt.AlignLeft)
        # “窗口对象”只有在searchRangeComboBox选择“窗口对象”时才会显示，默认隐藏
        self.windowObjectLabel = QLabel(text="窗口对象:", font=__font)
        self.directiveInputSettingLayout.addWidget(self.windowObjectLabel, 1, 0, 1, 1, Qt.AlignRight)
        self.windowObjectComboBox = QComboBox(font=__font)
        self.windowObjectComboBox.setMinimumSize(650, 50)
        self.windowObjectComboBox.setItemDelegate(QStyledItemDelegate())
        self.windowObjectComboBox.setStyleSheet(comboBoxStyleSheet)
        self.directiveInputSettingLayout.addWidget(self.windowObjectComboBox, 1, 1, 1, 1, Qt.AlignCenter)
        self.windowObjectTipLabel = flowSettingDialog.createTipLabel("窗口对象", "选择一个窗口对象")
        self.directiveInputSettingLayout.addWidget(self.windowObjectTipLabel, 1, 2, 1, 1, Qt.AlignLeft)
        self.windowObjectLabel.hide()
        self.windowObjectComboBox.hide()
        self.windowObjectTipLabel.hide()
        # 查找方式
        searchMethodLabel = QLabel(text="查找方式:", font=__font)
        self.directiveInputSettingLayout.addWidget(searchMethodLabel, 2, 0, 1, 1, Qt.AlignRight)
        self.searchMethodComboBox = QComboBox(font=__font)
        self.searchMethodComboBox.setMinimumSize(650, 50)
        self.searchMethodComboBox.setItemDelegate(QStyledItemDelegate())
        self.searchMethodComboBox.setStyleSheet(comboBoxStyleSheet)
        self.searchMethodComboBox.addItems(["存在", "不存在"])
        self.directiveInputSettingLayout.addWidget(self.searchMethodComboBox, 2, 1, 1, 1, Qt.AlignCenter)
        searchMethodTipLabel = flowSettingDialog.createTipLabel("查找方式", "选择查找范围内的指定图像存\n在还是不存在")
        self.directiveInputSettingLayout.addWidget(searchMethodTipLabel, 2, 2, 1, 1, Qt.AlignLeft)
        self.imageUI()

        hLayout = QHBoxLayout(self.directiveOutputSettingPanel)
        self.directiveOutputSettingPanel.setLayout(hLayout)
        nothingLabel = QLabel(text="(当前指令不包含任何输出项)", font=__font)
        hLayout.addWidget(nothingLabel, 1, Qt.AlignCenter)
        hLayout.setContentsMargins(0, 10, 0, 30)
        self.searchRangeComboBox.currentIndexChanged.connect(self.changeMode)

    def imageUI(self):
        __font = QFont()
        __font.setPixelSize(20)
        __font.setFamily("Courier")
        targetImageLabel = QLabel("目标图像:", font=__font)
        self.directiveInputSettingLayout.addWidget(targetImageLabel, 3, 0, 1, 1, Qt.AlignRight)
        targetImageGridLayout = QGridLayout()
        targetImageGridLayout.setContentsMargins(0, 0, 0, 0)
        targetImageGridLayout.setSpacing(5)
        # 图像列表
        self.imageList = QListWidget(font=__font)
        self.imageList.setMinimumSize(400, 250)
        # 功能按钮
        targetImageGridLayout.addWidget(self.imageList, 0, 0, 3, 1)
        self.imageLibBtn = QPushButton(text="去图像库选择", font=__font)
        targetImageGridLayout.addWidget(self.imageLibBtn, 0, 1, 1, 1)
        self.deleteImageBtn = QPushButton(text="删除目标图像", font=__font)
        targetImageGridLayout.addWidget(self.deleteImageBtn, 1, 1, 1, 1)
        # 图像预览控件
        self.imagePreview = QLabel()
        self.imagePreview.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.imagePreview.setStyleSheet("background-color: #F0F0F0;")
        targetImageGridLayout.addWidget(self.imagePreview, 2, 1, 1, 1)
        self.directiveInputSettingLayout.addLayout(targetImageGridLayout, 3, 1, 1, 1, Qt.AlignCenter)
        targetImageTipLabel = flowSettingDialog.createTipLabel("目标图像", "可以从图像库中选择多张图像")
        self.directiveInputSettingLayout.addWidget(targetImageTipLabel, 3, 2, 1, 1, Qt.AlignLeft)
        checkBoxHLayout = QHBoxLayout()
        checkBoxHLayout.setContentsMargins(0, 0, 0, 0)
        self.allImageSatisfied = QCheckBox(text="全部图像存在(不存在)后再执行", font=__font)
        self.allImageSatisfied.setMinimumHeight(40)
        checkBoxHLayout.addWidget(self.allImageSatisfied, alignment=Qt.AlignLeft)
        allImageSatisfiedTipLabel = flowSettingDialog.createTipLabel("全部图像存在(不存在)后再执行",
                                                                      "检测所有图像，或是其中一张符合便停止")
        checkBoxHLayout.addWidget(allImageSatisfiedTipLabel, alignment=Qt.AlignLeft)
        checkBoxHLayout.addStretch(1)
        self.directiveInputSettingLayout.addLayout(checkBoxHLayout, 4, 1, 1, 1)


    def changeMode(self, idx: int):
        if idx == 1:
            self.windowObjectLabel.show()
            self.windowObjectComboBox.show()
            self.windowObjectTipLabel.show()
            self.setFixedHeight(self.height() + 70)
        elif not self.windowObjectTipLabel.isHidden():
            self.windowObjectLabel.hide()
            self.windowObjectComboBox.hide()
            self.windowObjectTipLabel.hide()
            self.setFixedHeight(self.height() - 70)
