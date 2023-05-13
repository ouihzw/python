from PyQt5.QtWidgets import QApplication

# 计算屏幕百分比比例函数
def screenPercentage(w: float, h: float):
    rect = QApplication.desktop().availableGeometry()
    return int(w * rect.width()), int(h * rect.height())
