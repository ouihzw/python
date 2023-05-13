# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys


class MySplashScreen(QSplashScreen):
    # picPath = "./com/mat/rpa/views/splashScreen/images/unicomRPASplash800.jpg"
    # picPath = "./images/unicomRPASplash800.jpg"
    picPath = "./com/mat/rpa/views/splashScreen/images/rpa.jpg"
    def __init__(self, parent=None):
        super(MySplashScreen, self).__init__(parent)
        self.setPixmap(QPixmap(MySplashScreen.picPath))  # 设置背景图片
        # 初始文本
        __font = QFont()
        __font.setFamily("Consolas")
        __font.setPixelSize(32)
        __font.setBold(True)
        self.showMessage("欢迎大家使用RPA", Qt.AlignHCenter | Qt.AlignBottom, Qt.black)
        self.setFont(__font)
    # 鼠标点击事件
    def mousePressEvent(self, event):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MySplashScreen()
    win.show()
    sys.exit(app.exec_())