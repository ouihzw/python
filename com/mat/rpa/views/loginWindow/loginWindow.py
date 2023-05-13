import sys
import hashlib

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

# 通过主程序调用运行
if __name__ != "__main__":
    from ...dao.userDao import userDao

    picPath = "./com/mat/rpa/views/loginWindow/images/"
    iconPath = "./com/mat/rpa/views/images/"

styleSheet = \
    """
#switch{
    background-color: #FFF;
    border-style: none none solid none;
    border-color: #BBB;
    border-width: 2px;
    font-size: 13px;
}
#switch:hover{
    border-color: #ffbbbb;
    background-color: #f9f9f9;
}
#widget{
    background-color: white;
}
QLineEdit{
    border-style: none;
}
QComboBox{
    border-style: none;
    margin-right: 4px;
}
QComboBox::drop-down{
    height: 16px;
    width: 16px;
    border-radius: 3px;
    image: url(:/images/down.png)
}
QComboBox::drop-down:hover{
    background-color: #F0F0F0;
}
QComboBox::drop-down:pressed{
    padding: 1px -1px;
}
QLabel{
    padding: 10px;
}
#box{
    border-style: none none solid none;
    border-width: 1px;
    border-color: gray;
}
#box:hover{
    border-color: red;
}
#hyperlink{
    border-style: none;
    background-color: transparent;
}
#hyperlink:hover{
    color: #ff5555
}
#loginBtn{
    border-radius: 4px;
    border-style: none;
    font-size: 12px;
    color: white;
    background-color: #ff4444
}
#loginBtn:hover{
    background-color: #e33333
}
#loginBtn:pressed{
    margin: 1px 3px;
}
"""
# 激活状态的标签（个人、企业）对应的样式表
activeSheet = "border-color: red;font-weight:bold;"


class RegisterPage(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.setWindowIcon(QIcon(iconPath + 'logo32.png'))
        self.setWindowTitle("注册")
        self.setPalette(QPalette(Qt.white))  # 改窗体背景为白色
        self.setMinimumSize(250, 200)

    def initUI(self):
        # 创建用户名和密码输入框
        self.userNameLineEdit = QLineEdit()
        self.pwLineEdit = PasswordEdit()
        self.confirmPwLineEdit = PasswordEdit()
        self.pwLineEdit.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))
        self.pwLineEdit.setEchoMode(2)  # 设置密码显示为圆点
        self.confirmPwLineEdit.setEchoMode(2)

        # 创建注册按钮
        self.registerBtn = QPushButton("注册")

        # 创建布局，添加控件
        layout = QVBoxLayout()
        layout.addWidget(QLabel("用户名："))
        layout.addWidget(self.userNameLineEdit)
        layout.addWidget(QLabel("密码："))
        layout.addWidget(self.pwLineEdit)
        layout.addWidget(QLabel("确认密码："))
        layout.addWidget(self.confirmPwLineEdit)
        layout.addWidget(self.registerBtn)
        self.setLayout(layout)

        # 绑定注册按钮的点击事件
        self.registerBtn.clicked.connect(self.register)

    def register(self):
        # 检查用户名和密码是否已填写
        userName = self.userNameLineEdit.text().strip()
        pw = self.pwLineEdit.text().strip()
        confirmPw = self.confirmPwLineEdit.text().strip()
        if not userName:
            QMessageBox.warning(self, "警告", "请输入用户名")
            return
        if not pw:
            QMessageBox.warning(self, "警告", "请输入密码")
            return
        if pw != confirmPw:
            QMessageBox.warning(self, "警告", "密码和确认密码不一致")
            return

        self.pwLineEdit.hashPassword()

        self.userDaoObj = userDao.UserDao(self)
        self.userDict = {"user_name": self.userNameLineEdit.text(), "password": self.pwLineEdit.hashedPw}
        self.userDaoObj.insertNewtUser(self.userDict)
        self.close()


class LoginWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.setWindowIcon(QIcon(iconPath + 'logo32.png'))
        self.setWindowTitle("登录")
        # self.resize(800, 400)
        # self.setFixedSize(800, 400)
        self.setPalette(QPalette(Qt.white))  # 改窗体背景为白色
        self.entireLayout = QHBoxLayout(self)
        self.rightPanel = QWidget()  # 为了控制左右面板的比例，再套一层QWidget
        self.rightVLayout = QVBoxLayout(self.rightPanel)  # 右侧面板设置垂直布局
        self.rightPanel.setLayout(self.rightVLayout)
        self.rightPanel.setMinimumSize(270, 370)
        self.topButtons = QHBoxLayout(self.rightPanel)  # 上方的按钮面板 ??
        self.individualBtn = QPushButton(parent=self.rightPanel, text="登录",
                                         objectName="switch", clicked=lambda: self.changePage(0))  # 个人登录按钮
        self.individualBtn.setFixedHeight(35)
        self.individualBtn.setStyleSheet(activeSheet)
        self.enterpriseBtn = QPushButton(parent=self.rightPanel, text="",
                                         objectName="switch", clicked=lambda: self.changePage(1))  # 企业登录按钮
        self.enterpriseBtn.setFixedHeight(35)
        self.topButtons.addWidget(self.individualBtn)
        self.topButtons.addWidget(self.enterpriseBtn)
        self.rightVLayout.addItem(self.topButtons)
        self.stackedWidget = QStackedWidget(self.rightPanel)  # 安装StackedWidget

        self.individualPage = QWidget()  ## 个人登录页面(Index 0)
        self.stackedWidget.addWidget(self.individualPage)
        vLayout = QVBoxLayout()
        self.individualPage.setLayout(vLayout)
        self.individualForm = InputPanel()  # 输入面板
        vLayout.addWidget(self.individualForm)

        vLayout.addStretch(1)
        registHLayout = QHBoxLayout()  # 放置注册按钮
        registHLayout.setContentsMargins(0, 0, 0, 0)
        registHLayout.setSpacing(0)
        self.hintLabel = QLabel(parent=self.individualPage, text="没有账号？ ")
        registHLayout.addWidget(self.hintLabel)
        self.registBtn = QPushButton(parent=self.individualPage, text="注册",
                                     objectName="hyperlink", clicked=self.regist)
        registHLayout.addWidget(self.registBtn)
        registHLayout.addStretch(1)
        vLayout.addItem(registHLayout)
        self.individualLoginBtn = QPushButton(objectName="loginBtn", text="登录",
                                              default=True, clicked=self.individualLogin)
        self.individualLoginBtn.setFixedHeight(44)
        vLayout.addWidget(self.individualLoginBtn)
        self.rightVLayout.addWidget(self.stackedWidget)

        self.enterprisePage = QWidget()  ## 企业登录界面(Index 1)
        self.stackedWidget.addWidget(self.enterprisePage)
        vLayout = QVBoxLayout()
        self.enterprisePage.setLayout(vLayout)
        self.enterpriseForm = InputPanel()
        vLayout.addWidget(self.enterpriseForm)
        vLayout.addStretch(1)
        self.enterpriseLoginBtn = QPushButton(objectName="loginBtn", text="登录", clicked=self.enterpriseLogin)
        self.enterpriseLoginBtn.setFixedHeight(44)
        vLayout.addWidget(self.enterpriseLoginBtn)
        self.rightVLayout.addWidget(self.stackedWidget)

        self.stackedWidget.setCurrentIndex(0)
        self.entireLayout.addWidget(self.rightPanel)
        self.setLayout(self.entireLayout)
        self.setStyleSheet(styleSheet)

        # self.swiperWidget.addPage(picPath + "unicom.jpg")  # 轮播控件添加3页
        # self.swiperWidget.addPage(picPath + "unicomRPASplash800.png")
        # 用户名列表选中项目时，在数据库中查询相应记录
        self.individualForm.userName.currentIndexChanged.connect(self.querySelectedUserName)
        # 是否为启动状态，autoFill函数使用
        self.isStartup = True
        # 初始化数据库
        self.userDaoObj = userDao.UserDao(self)

    # 自动填充输入框
    def autoFill(self, userInfo):
        if userInfo:
            # 填充用户名
            self.individualForm.userName.setText(userInfo["user_name"])
            # 填充“保存密码”勾选框
            if userInfo["password"]:
                self.individualForm.savePw.setChecked(True)
            else:
                self.individualForm.savePw.setChecked(False)
            # 填充密码
            self.individualForm.pwLineEdit.setPassword(userInfo["password"])
            # 填充“自动登录”勾选框
            self.individualForm.autoLogin.setChecked(userInfo["auto_login"])
            # 如果是初次启动登录界面（不是退出再登），检查自动登录功能
            if self.isStartup:
                if userInfo["auto_login"]:
                    self.individualLogin()
                self.isStartup = False

    # 在启动时填写ComboBox下拉列表
    def setDropDownList(self, users):
        for item in users:
            self.individualForm.userName.addItem(item)
        self.autoFill(self.userDaoObj.queryLatestOne())

    # 查询用户名对应的登录记录信息
    def querySelectedUserName(self, idx):
        doc = self.userDaoObj.queryByUserName(self.individualForm.userName.itemText(idx))
        self.autoFill(doc)

    # 个人登录企业登录的换页函数
    def changePage(self, idx):
        if idx == 0:
            self.individualBtn.setStyleSheet(activeSheet)  # 点击个人登录
            self.enterpriseBtn.setStyleSheet("")
            self.individualLoginBtn.setDefault(True)
        else:
            self.enterpriseBtn.setStyleSheet(activeSheet)  # 点击企业登录
            self.individualBtn.setStyleSheet("")
            self.enterpriseLoginBtn.setDefault(True)
        self.stackedWidget.setCurrentIndex(idx)

    # 个人页面点击登录按钮的函数
    def individualLogin(self):
        # 锁定页面
        self.individualPage.setDisabled(True)
        if self.individualForm.userName.isBlank:
            self.individualPage.setDisabled(False)
            self.individualForm.statusLabel.setText("请输入用户名")
            return
        # 将密码框的文本散列，保存到hashedPw中
        self.individualForm.pwLineEdit.hashPassword()
        if self.individualForm.pwLineEdit.hashedPw == "":
            self.individualPage.setDisabled(False)
            self.individualForm.statusLabel.setText("请输入密码")
            return
        # 查询相应的用户密码信息
        self.checkPassword(self.userDaoObj.queryForLogin(self.individualForm.userName.currentText()))

    # 验证密码
    def checkPassword(self, info):
        if info:  # 若有查询结果
            if self.individualForm.pwLineEdit.hashedPw == info["password"]:
                self.individualForm.statusLabel.setText("登录成功")
                userInfo = {"user_name": self.individualForm.userName.currentText(),
                            "auto_login": self.individualForm.autoLogin.isChecked(),
                            "password": None}
                # 勾选了保存密码和自动登录的任一个都会将密码保存
                if self.individualForm.savePw.isChecked() or self.individualForm.autoLogin.isChecked():
                    userInfo["password"] = info["password"]
                # 更新数据记录
                self.userDaoObj.updateNewLogin(userInfo)
                self.individualPage.setDisabled(False)
                # 关闭登录界面，程序继续运行
                self.accept()
                # 清理状态标签
                self.individualForm.statusLabel.setText("")
                return
        self.individualForm.statusLabel.setText("密码错误，请重新输入")
        self.individualPage.setDisabled(False)

    # 企业页面点击登录按钮的函数
    def enterpriseLogin(self):
        print("企业登录")

    # 点击注册按钮的函数
    def regist(self):
        registerDialog = RegisterPage()
        registerDialog.exec_()

    # 固定尺寸
    def showEvent(self, a0: QShowEvent) -> None:
        super().showEvent(a0)
        if self.isStartup:
            self.setFixedSize(self.width(), self.height())
            QTimer.singleShot(200, lambda: self.setDropDownList(self.userDaoObj.queryUserNames()))


class InputPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("widget")
        vLayout = QVBoxLayout()
        vLayout.setSpacing(8)
        vLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(vLayout)

        self.userBox = QWidget()  # 用户名栏
        self.userBox.setObjectName("box")
        self.userIcon = QLabel(self.userBox)
        self.userIcon.setPixmap(QPixmap(picPath + "user.png"))
        self.userIcon.setMaximumSize(36, 36)  # 固定图标尺寸
        self.userIcon.setMinimumSize(36, 36)
        self.userIcon.setScaledContents(True)  # 设置图片自动缩放
        self.userName = ComboBox(self.userBox)
        self.userName.setEditable(True)
        self.userName.setPlaceholderText("用户名")  # 调用重写的方法
        self.userName.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))
        hLayoutUser = QHBoxLayout()
        hLayoutUser.setSpacing(0)
        hLayoutUser.setContentsMargins(0, 0, 0, 0)
        hLayoutUser.addWidget(self.userIcon)
        hLayoutUser.addWidget(self.userName)
        self.userBox.setLayout(hLayoutUser)
        vLayout.addWidget(self.userBox)

        self.pwBox = QWidget()  # 密码栏
        self.pwBox.setObjectName("box")
        self.pwIcon = QLabel(self.pwBox)
        self.pwIcon.setPixmap(QPixmap(picPath + "password.png"))
        self.pwIcon.setMaximumSize(36, 36)
        self.pwIcon.setMinimumSize(36, 36)
        self.pwIcon.setScaledContents(True)
        self.pwLineEdit = PasswordEdit(self.pwBox)
        self.pwLineEdit.setPlaceholderText("密码")
        self.pwLineEdit.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))
        self.pwLineEdit.setEchoMode(2)  # 设置密码显示为圆点
        hLayoutPw = QHBoxLayout()
        hLayoutPw.setSpacing(0)
        hLayoutPw.setContentsMargins(0, 0, 0, 0)
        hLayoutPw.addWidget(self.pwIcon)
        hLayoutPw.addWidget(self.pwLineEdit)
        self.pwBox.setLayout(hLayoutPw)
        vLayout.addWidget(self.pwBox)

        checkBoxHLayout = QHBoxLayout()  # 勾选框
        self.autoLogin = QCheckBox(self)
        self.autoLogin.setText("自动登录")
        self.savePw = QCheckBox(self)
        self.savePw.setText("保存密码")
        checkBoxHLayout.addWidget(self.autoLogin)
        checkBoxHLayout.addWidget(self.savePw)
        checkBoxHLayout.setSpacing(10)
        checkBoxHLayout.setContentsMargins(5, 5, 5, 5)
        checkBoxHLayout.addStretch(1)
        vLayout.addItem(checkBoxHLayout)
        self.statusLabel = QLabel(self)
        self.statusLabel.setStyleSheet("color: red;")
        vLayout.addWidget(self.statusLabel)


# 重写ComboBox的焦点事件，实现显示占位符的功能
class ComboBox(QComboBox):
    isBlank = True
    placeholder = ""

    # 获得焦点时将占位符清除
    def focusInEvent(self, e: QFocusEvent):
        if self.isBlank:
            self.setCurrentText("")
        self.setStyleSheet("")
        return super().focusInEvent(e)

    # 失去焦点时检测输入框是否为空，为空则填写占位符
    def focusOutEvent(self, e: QFocusEvent):
        if self.currentText() == "":
            self.isBlank = True
            self.setCurrentText(self.placeholder)
            self.setStyleSheet("color: #7F7F7F")
        else:
            self.isBlank = False
        return super().focusOutEvent(e)

    # 重写没有用的设置占位文本的函数，设置self.placeholder
    def setPlaceholderText(self, placeholderText: str):
        self.placeholder = placeholderText
        self.setCurrentText(self.placeholder)
        self.setStyleSheet("color: #7F7F7F")

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.setCurrentText(self.placeholder)
        self.setStyleSheet("color: #7F7F7F")

    # 提供通过程序设置文本的方法，通过程序设置不会触发上面的焦点事件，需要另行判断
    def setText(self, text):
        if text == "":
            self.isBlank = True
            self.setStyleSheet("color: #7F7F7F")
            self.setCurrentText(self.placeholder)
        else:
            self.isBlank = False
            self.setStyleSheet("")
            self.setCurrentText(text)


# 密码输入框，加入MD5散列方法和存储散列密码
class PasswordEdit(QLineEdit):
    hashedPw = ""

    # MD5散列密码，并将散列值存储到hashedPw中
    def hashPassword(self):
        if (self.hashedPw == "") and (self.text() != ""):
            self.hashedPw = hashlib.md5(bytes(self.text().encode())).hexdigest()

    # 自动填写密码时采用此方法
    def setPassword(self, pw):
        if pw:
            self.setText("placeholder")
        else:
            # 若密码字段为None则认为没有密码，填空字符串
            pw = ""
            self.setText(pw)
        self.hashedPw = pw

    # 重写focusInEvent，获取焦点时清除占位符
    def focusInEvent(self, a0: QFocusEvent) -> None:
        if self.hashedPw != "":
            self.hashedPw = ""
            self.setText("")
        return super().focusInEvent(a0)

# if __name__=="__main__":
#     from swiperWidget import SwiperWidget
#     import down_rc
#     sys.path.append('../../')
#     from dao.userDao import userDao
#
#     iconPath = "../images/"
#     picPath = "./images/"
#     app = QApplication(sys.argv)
#     widget = LoginWindow()
#     widget.show()
#     sys.exit(app.exec_())
