# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

styleSheet = \
"""
#logoText {
    font-size: 30px; 
    font-family: Microsoft YaHei;
    margin-right: 40px;
    margin-left: 10px;
}
QToolButton {
    border-radius: 4px;
    padding: 5px;
}
QToolButton:hover {
    background-color: #e0e0e0;
    border-style: none;
}
QToolButton:pressed {
    background-color: #d0d0d0;
    border-style: none;
}
QToolButton::menu-indicator {
    image: none;
}
QMenu {
    background-color: #fff;
    padding: 5px;
    font-size: 13px;
    border-color: #e0e0e0;
    border-width: 1px;
    border-style: solid;
}
QMenu::item {
    padding: 8px;
    border-radius: 4px;
    min-width: 120px;
}
QMenu::item:selected {
    background-color: #eee
}
QMenu::icon {
    padding-left: 12px;
}
#userNameLabel {
    font-size: 14px;
    margin: 8px 8px 13px;
}
"""

class TopToolBar(QToolBar):
    def __init__(self, parent=None):
        super(TopToolBar, self).__init__(parent)
        self.parentWindow = parent
        self.initUI()

    def initUI(self):
        __font = QFont()
        __font.setPixelSize(20)
        __font.setFamily("Microsoft YaHei")
        # __font.setBold(True)
        self.logoLabel = QLabel()
        self.logoLabel.setPixmap(QPixmap("./com/mat/rpa/views/images/logo64.png"))
        # self.logoLabel.setPixmap(QPixmap("../../images/logo64.png"))
        self.addWidget(self.logoLabel)
        self.logoTextLabel = QLabel()
        self.logoTextLabel.setText("RPA Studio")
        self.logoTextLabel.setObjectName("logoText")
        self.addWidget(self.logoTextLabel)
        self.myAppAction = QAction()
        self.myAppAction.setText("我的应用")
        self.myAppAction.setFont(__font)
        # self.myAppAction.triggered.connect(self.triggerMyAppAction)
        self.addAction(self.myAppAction)
        self.selfDefinedCommandAction = QAction()
        self.selfDefinedCommandAction.setText("我的指令")
        self.selfDefinedCommandAction.setFont(__font)
        self.addAction(self.selfDefinedCommandAction)
        self.executeOnScheduleAction = QAction()
        self.executeOnScheduleAction.setText("计划执行")
        self.executeOnScheduleAction.setFont(__font)
        self.addAction(self.executeOnScheduleAction)
        # self.BotMarketAction = QAction()
        # self.BotMarketAction.setText("Bot市场")
        # self.BotMarketAction.setFont(__font)
        # self.addAction(self.BotMarketAction)
        # self.videoTutorialtAction = QAction()
        # self.videoTutorialtAction.setText("视频教程")
        # self.videoTutorialtAction.setFont(__font)
        # self.addAction(self.videoTutorialtAction)
        # self.communityAction = QAction()
        # self.communityAction.setText("社区")
        # self.communityAction.setFont(__font)
        # self.addAction(self.communityAction)

        # #弹簧控件
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.addWidget(spacer)
        # 图像存储路径
        picPath = "./com/mat/rpa/views/projectWindow/topToolPanel/images/"
        # 右侧三个按钮
        self.settingsBtn = QToolButton(parent=self, icon=QIcon(picPath + "setting.png"))
        self.ellipsisBtn = QToolButton(parent=self, icon=QIcon(picPath + "ellipsis.png"))
        self.userBtn = QToolButton(parent=self, icon=QIcon(picPath + "user.png"))
        # 省略号按钮的菜单
        self.ellipsisMenu = QMenu(self.ellipsisBtn)
        self.browserAction = QAction(text="RPA浏览器")
        self.mobileAction = QAction(text="手机管理器")
        self.helpAction = QAction(text="帮助")
        self.ellipsisMenu.addActions([self.browserAction, self.mobileAction, self.helpAction])
        self.ellipsisBtn.setMenu(self.ellipsisMenu)
        self.ellipsisBtn.setPopupMode(QToolButton.InstantPopup)
        # 用户按钮的菜单
        self.userMenu = QMenu(self.userBtn)
        widgetAction = QWidgetAction(self.userMenu)
        # 在菜单中增加一个显示用户名的标签
        self.userNameLabel = QLabel(text="你好，", objectName="userNameLabel")
        widgetAction.setDefaultWidget(self.userNameLabel)
        self.logoutAction = QAction(icon=QIcon(picPath + "logout.png"), text="退出登录")
        self.userMenu.addActions([widgetAction, self.logoutAction])
        self.userBtn.setMenu(self.userMenu)
        self.userBtn.setPopupMode(QToolButton.InstantPopup)
        self.addWidget(self.settingsBtn)
        self.addWidget(self.ellipsisBtn)
        self.addWidget(self.userBtn)
        self.setContentsMargins(0, 0, 10, 0)
        self.setStyleSheet(styleSheet)

    def triggerMyAppAction(self):
        print("点击了我的应用按钮")

    # 设置用户菜单中显示的用户名
    def setUserName(self, userName):
        self.userNameLabel.setText("你好，" + userName)

if __name__ == "__main__":
    app =  QApplication(sys.argv)
    win = TopToolBar()
    win.show()
    sys.exit(app.exec_())