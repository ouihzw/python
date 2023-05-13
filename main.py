# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys,  os
from com.mat.rpa.views.splashScreen import splashWindow
from com.mat.rpa.views.workWindow import mainWindow
from com.mat.rpa.views.loginWindow import loginWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    QApplication.setStyle(QStyleFactory.create("Fusion"))
    # 登录界面
    loginWindowObj = loginWindow.LoginWindow()
    # 返回登录结果
    result = loginWindowObj.exec()
    # 没有成功登录则退出程序
    if result != QDialog.Accepted:
        sys.exit()
    splash = splashWindow.MySplashScreen()
    splash.show()
    projectWindow = mainWindow.WorkMainWindow()
    projectWindow.show()
    splash.finish(projectWindow)
    splash.deleteLater()
    sys.exit(app.exec_())
