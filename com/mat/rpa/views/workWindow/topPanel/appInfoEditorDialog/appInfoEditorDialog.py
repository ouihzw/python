# -*- coding:utf-8 -*-
import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from com.mat.rpa.dao.workDao.workDao import WorkDao
from com.mat.rpa.utils.variable import VariableManager


class AppInfoEditorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        self.setWindowTitle(u"编辑应用信息")
        __font = QFont()
        __font.setPixelSize(20)
        __font.setFamily("Courier")
        layout = QGridLayout()
        self.setLayout(layout)
        layout.setContentsMargins(30, 30, 40, 20)
        layout.setSpacing(10)
        layout.setVerticalSpacing(20)
        nameLabel = QLabel(text=u"应用名称:", font=__font)
        layout.addWidget(nameLabel, 0, 0, Qt.AlignRight)
        self.nameLineEdit = QLineEdit(font=__font)
        self.nameLineEdit.setMinimumSize(650, 40)
        layout.addWidget(self.nameLineEdit, 0, 1, Qt.AlignCenter)
        exportPathLabel = QLabel(text=u"导出路径:", font=__font)
        layout.addWidget(exportPathLabel, 1, 0, Qt.AlignRight)
        exportPathHLayout = QHBoxLayout()
        exportPathHLayout.setContentsMargins(0, 0, 0, 0)
        exportPathHLayout.setSpacing(0)
        self.exportPathLineEdit = QLineEdit(font=__font)
        self.exportPathLineEdit.setPlaceholderText(u"(选择导出路径)")
        self.exportPathLineEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.exportPathLineEdit.setMinimumHeight(40)
        exportPathHLayout.addWidget(self.exportPathLineEdit)
        self.selectFolderBtn = QPushButton(text=u" 预览... ", font=__font, clicked=self.selectFolder)
        self.selectFolderBtn.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        exportPathHLayout.addWidget(self.selectFolderBtn)
        layout.addLayout(exportPathHLayout, 1, 1, 1, 1, Qt.AlignCenter)
        introLabel = QLabel(text=u"简介:", font=__font)
        layout.addWidget(introLabel, 2, 0, Qt.AlignRight)
        self.introLineEdit = QLineEdit(font=__font)
        self.introLineEdit.setMinimumSize(650, 40)
        layout.addWidget(self.introLineEdit, 2, 1, Qt.AlignCenter)
        manualLabel = QLabel(text=u"使用说明:", font=__font)
        manualLabel.setMinimumHeight(40)
        layout.addWidget(manualLabel, 3, 0, Qt.AlignRight | Qt.AlignTop)
        self.manualTextEdit = QPlainTextEdit(font=__font)
        self.manualTextEdit.setMinimumSize(650, 200)
        layout.addWidget(self.manualTextEdit, 3, 1, Qt.AlignCenter)
        btnLayout = QHBoxLayout()
        btnLayout.setSpacing(15)
        self.infoLabel = QLabel()
        self.infoLabel.setStyleSheet("color: red;")
        btnLayout.addWidget(self.infoLabel, 1)
        self.save = QPushButton(text=u"保存", clicked=self.saveAppInfo)
        self.save.setStyleSheet("background-color: red;")
        self.save.setDefault(True)
        btnLayout.addWidget(self.save)
        self.cancel = QPushButton(text=u"取消", clicked=self.reject)
        btnLayout.addWidget(self.cancel)
        layout.addLayout(btnLayout, 4, 1)
        self.setStyleSheet("QDialog {background-color: white;}")

    def showEvent(self, a0: QShowEvent) -> None:
        appInfo = WorkDao().loadApp(VariableManager().getAppId())
        self.nameLineEdit.setText(appInfo["name"])
        if hasattr(appInfo, "export_path"):
            self.exportPathLineEdit.setText(appInfo["export_path"])
            self.introLineEdit.setText(appInfo["intro"])
            self.manualTextEdit.setPlainText(appInfo["manual"])

    # 选择文件
    def selectFolder(self):
        directory = QFileDialog.getExistingDirectory(self, u"选择文件夹", "")
        if directory:
            self.exportPathLineEdit.setText(directory)

    # 保存应用信息
    def saveAppInfo(self):
        # 名称为空时不能确认
        if self.nameLineEdit.text() == "":
            self.infoLabel.setText(u"* 请输入应用名称")
            return
        appInfo = {
            "name": self.nameLineEdit.text(),
            "export_path": self.exportPathLineEdit.text(),
            "intro": self.introLineEdit.text(),
            "manual": self.manualTextEdit.toPlainText(),
            "update_time": datetime.datetime.now()
        }
        WorkDao().saveAppInfo(VariableManager().getAppId(), appInfo)
        self.accept()
