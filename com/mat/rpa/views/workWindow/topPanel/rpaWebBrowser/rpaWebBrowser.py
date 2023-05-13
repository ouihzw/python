from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets, QtWebChannel
from PyQt5.QtWebEngineWidgets import *
import sys,os,datetime
CURRENT_DIR = os.getcwd()
DEBUG_PORT = '5588'
DEBUG_URL = 'http://127.0.0.1:%s' % DEBUG_PORT
os.environ['QTWEBENGINE_REMOTE_DEBUGGING'] = DEBUG_PORT

class RPAWebBrowser(QTabWidget):
    picPath = "./com/mat/rpa/views/workWindow/topPanel/rpaWebBrowser/images/"
    def __init__(self,parent=None):
        super(RPAWebBrowser, self).__init__(parent)
        self.desktop = QApplication.desktop()
        self.rect = self.desktop.availableGeometry()
        self.setGeometry(self.rect.x(), self.rect.y(), self.rect.width(), self.rect.height())
        self.move(0, 0)
        self.setContentsMargins(0,0,0,0)
        self.setWindowFlags(Qt.CustomizeWindowHint)
        self.setDocumentMode(True)
        self.setStyleSheet(
        "QTabBar::tab{width:300}""QTabBar::close-button{image:url(./com/mat/rpa/views/workWindow/topPanel/rpaWebBrowser/images/smallClose.png);border:none;icon-size}""QTabBar::close-button::hover{background-color:#C0C0C0;border:none;}")
        self.tabCloseRequested.connect(self.closeTab)
        self.setTabBar(TabBar())
        self.windowIconPanel = QWidget()
        self.windowIconPanelLayout = QHBoxLayout()
        self.windowIconPanelLayout.setContentsMargins(0,0,0,0)
        self.windowIconPanel.setLayout(self.windowIconPanelLayout)
        self.windowIconPanelLayout.setSpacing(0)
        self.windowIconPanelLayout.setContentsMargins(0, 0, 0, 0)
        self.windowBtn=QPushButton()
        self.windowBtn.setFixedSize(50,50)
        self.windowBtn.setStyleSheet("border:none")
        self.windowBtn.setIcon(QIcon(QPixmap(RPAWebBrowser.picPath +"Robot.png")))
        self.windowBtn.setIconSize(QSize(30,30))
        self.windowIconPanelLayout.addWidget(self.windowBtn)
        self.setCornerWidget(self.windowIconPanel , Qt.TopLeftCorner)

        #浏览器中新建网页
        self.tab1=Tab(self)
        self.tab1.getRPAWebBrowserWin(self)
        self.addTab(self.tab1, "新建标签页".encode("unicode_escape").decode("unicode_escape"))
        self.setTabsClosable(True)

        #“新建网页”按钮，点击按钮新建网页
        #self.addTabBtn=QPushButton()
        #self.addTabBtn.setFixedSize(20,20)
        #self.addTabBtn.setIcon(QIcon(QPixmap(RPAWebBrowser.picPath + "add.png")))
        #self.addTabBtn.setIconSize(QtCore.QSize(25,25))
        #self.addTabBtn.setStyleSheet("QPushButton{border:none;}""QPushButton:hover{background-color:#C0C0C0;border:none;}")
        #self.addLabelPageTab=QWidget()
        #self.addTab(self.addLabelPageTab,"")
        #self.addLabelPageTab.setStyleSheet("height:20;width:30")
        #self.tabBar().setTabButton(1, self.tabBar().RightSide, self.addTabBtn)
        #self.addTabBtn.clicked.connect(lambda :self.addLabelPage(self.count()-1))
        #self.tabBarClicked.connect(self.addLabelPage)

        #安装浏览器的最小化、最大化、还原、关闭按钮
        self.btnPanel=QWidget()
        self.btnPanelLayout=QHBoxLayout()
        self.btnPanel.setLayout(self.btnPanelLayout)
        self.btnPanelLayout.setSpacing(0)
        self.btnPanelLayout.setContentsMargins(0,0,0,0)
        self.minimumButton = QPushButton()
        self.minimumButton.setFixedSize(50,50)
        self.minimumButton.setStyleSheet("QPushButton{border:none;}""QPushButton:hover{background-color:#C0C0C0;border:none;}")
        self.minimumButton.setIcon(QIcon(QPixmap(RPAWebBrowser.picPath + "minusSign.png")))
        self.minimumButton.clicked.connect(self.webBrowserShowMinimized)
        self.btnPanelLayout.addWidget(self.minimumButton)
        ## 最大化/还原按钮
        self.maximumButton = QPushButton()
        self.maximumButton.setStyleSheet("QPushButton{border:none;}""QPushButton:hover{background-color:#C0C0C0;border:none;}")
        self.maximumButton.setFixedSize(50,50)
        self.maximumButton.setIcon(QIcon(QPixmap(RPAWebBrowser.picPath + "shrinkWindow.png")))
        self.maximumButton.setIconSize(QSize(30, 30))
        self.maximumButton.clicked.connect(self.webBrowserShowMaximized)
        self.isWindowFillFullScreen=False
        self.btnPanelLayout.addWidget(self.maximumButton)
        ## 关闭按钮
        self.closeButton = QPushButton()
        self.closeButton.setStyleSheet("QPushButton{border:none;}""QPushButton:hover{background-color:#F08080;border:none;}")
        self.closeButton.setFixedSize(50,50)
        self.closeButton.setIcon(QIcon(QPixmap(RPAWebBrowser.picPath + "close.png")))
        self.closeButton.clicked.connect(self.closeRpaWebBrowser)
        self.btnPanelLayout.addWidget(self.closeButton)
        self.setCornerWidget(self.btnPanel,Qt.TopRightCorner)
    #新建网页
    def addLabelPage(self,index):
        if index==self.count()-1:
            self.insertTab(self.count()-1, Tab(),"新建标签页".encode("unicode_escape").decode("unicode_escape"))
            self.setCurrentIndex(self.count()-2)
    #最小化浏览器
    def webBrowserShowMinimized(self):
        self.showMinimized()
    #最大化/还原浏览器
    def webBrowserShowMaximized(self):
        if self.isWindowFillFullScreen:
            self.isWindowFillFullScreen = False
            self.setGeometry(self.rect.x(), self.rect.y(),self.rect.width(),self.rect.height())
            self.move(0,0)
            self.maximumButton.setIcon(QIcon(QPixmap(RPAWebBrowser.picPath + "shrinkWindow.png")))
            self.maximumButton.setIconSize(QSize(30, 30))
            self.tab1.browserHistoryPanel.move(self.desktop.availableGeometry().width()-300,97)
        elif not(self.isWindowFillFullScreen):
            self.isWindowFillFullScreen = True
            self.setGeometry(300, 100, 1355, 730)
            self.maximumButton.setIcon(QIcon(QPixmap(RPAWebBrowser.picPath + "restoreWindow.png")))
            self.maximumButton.setIconSize(QSize(20, 20))
            self.tab1.browserHistoryPanel.move(1355, 197)
    #关闭浏览器,清空temporaryTXTFile下的所有txt
    def closeRpaWebBrowser(self):
        self.close()
        path="./com/mat/rpa/views/workWindow/topPanel/rpaWebBrowser/temporaryTXTFile/"
        if not os.path.exists(path):
            os.mkdir(path)
        del_list = os.listdir(path)
        for f in del_list:
            file_path = os.path.join(path, f)
            if os.path.isfile(file_path):
                os.remove(file_path)

    #关闭网页
    def closeTab(self,index):
        if index==0:
            self.close()
        else:self.removeTab(index)

    #浏览器可移动
    def mouseMoveEvent(self, e: QMouseEvent):  # 重写移动事件
        self._endPos = e.pos() - self._startPos
        self.move(self.pos() + self._endPos)
        self.tab1.browserHistoryPanel.move(self.width()+ self.pos().x()+self._endPos.x()-300, 105+self.pos().y()+self._endPos.y())
    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self.isWindowFillFullScreen = True
            self.setGeometry(300, 100, 1355, 730)
            self.tab1.browserHistoryPanel.move(1355, 200)
            self.maximumButton.setIcon(QIcon(QPixmap(RPAWebBrowser.picPath + "restoreWindow.png")))
            self.maximumButton.setIconSize(QSize(20, 20))
            self._isTracking = True
            self._startPos = QPoint(e.x(), e.y())
    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None
    def getRPAWebBrowserWin(self,rpaWebBrowserWin):
        self.tab1.getRPAWebBrowserWin(rpaWebBrowserWin)
#TabBar变成一个类，使鼠标点击TabBar时浏览器可移动
class TabBar(QTabBar):
    def __init__(self,parent=None):
        super(TabBar, self).__init__(parent)
        self.setContentsMargins(0,0,0,0)
class Tab(QMainWindow):
    picPath = "./com/mat/rpa/views/workWindow/topPanel/rpaWebBrowser/images/"
    def __init__(self,parent=None):
        super(Tab, self).__init__(parent)
        __font = QFont()
        __font.setPixelSize(20)
        __font.setFamily("Cambria")
        self.centralWidget=QWidget()
        self.centralWidget.setStyleSheet("background-color:#f2f2f2 ")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.centralWidget.setLayout(self.horizontalLayout)
        self.setCentralWidget(self.centralWidget)
        self.rpaWebBrowserWin=None

        self.browser = WebEngineView()
        self.horizontalLayout.addWidget(self.browser)
        self.browser.load(QUrl('https://www.baidu.com'))
        self.browser.titleChanged.connect(self.setWebTitle)
        self.browser.iconChanged.connect(self.setWebIcon)
        self.browser.urlChanged.connect(self.urlBeChanged)
        #网页的顶部面板
        self.topPanel=QToolBar()
        self.topPanel.setStyleSheet("background-color:white")
        self.addToolBar(self.topPanel)
        #后退
        self.backBtn=QPushButton()
        self.backBtn.setToolTip("后退".encode("unicode_escape").decode("unicode_escape"))
        self.backBtn.setStyleSheet("border:none")
        self.backBtn.setFixedSize(50,50)
        self.backBtn.setIcon(QIcon(QPixmap(Tab.picPath + "backEnabled.png")))
        self.backBtn.clicked.connect(self.browser.back)
        self.topPanel.addWidget(self.backBtn)
        #前进
        self.forwardBtn = QPushButton()
        self.forwardBtn.setToolTip("前进".encode("unicode_escape").decode("unicode_escape"))
        self.forwardBtn.setFixedSize(50,50)
        self.forwardBtn.setStyleSheet("border:none")
        self.forwardBtn.setIcon(QIcon(QPixmap(Tab.picPath + "forwardEnabled.png")))
        self.forwardBtn.clicked.connect(self.browser.forward)
        self.topPanel.addWidget(self.forwardBtn)
        #刷新
        self.reloadBtn = QPushButton()
        self.reloadBtn.setToolTip("重新加载此页".encode("unicode_escape").decode("unicode_escape"))
        self.reloadBtn.setFixedSize(50, 50)
        self.reloadBtn.setStyleSheet("QPushButton{border:none;}""QPushButton:hover{background-color:#f2f2f2;border:none;}")
        self.reloadBtn.setIcon(QIcon(QPixmap(Tab.picPath + "refresh.png")))
        self.reloadBtn.clicked.connect(self.browser.reload)
        self.topPanel.addWidget(self.reloadBtn)
        #打开主页
        self.homePageBtn = QPushButton()
        self.homePageBtn .setToolTip("打开主页".encode("unicode_escape").decode("unicode_escape"))
        self.homePageBtn.setFixedSize(50, 50)
        self.homePageBtn.setStyleSheet("QPushButton{border:none;}""QPushButton:hover{background-color:#f2f2f2;border:none;}")
        self.homePageBtn.clicked.connect(self.skipToHomePage)
        self.homePageBtn.setIcon(QIcon(QPixmap(Tab.picPath + "homePage.png")))
        self.topPanel.addWidget(self.homePageBtn)
        self.topPanel.addSeparator()
        #网址输入
        self.inputUrlLineEdit=InputUrlLineEdit()
        self.inputUrlLineEdit.returnPressed.connect(self.skipToNewPage)
        self.inputUrlLineEdit.setPlaceholderText("请输入网址".encode("unicode_escape").decode("unicode_escape"))
        self.topPanel.addWidget(self.inputUrlLineEdit)
        self.skipToNewPageBtn = QPushButton()
        self.skipToNewPageBtn.setFixedSize(50, 50)
        self.skipToNewPageBtn.setStyleSheet("QPushButton{border:none;}""QPushButton:hover{background-color:#f2f2f2;border:none;}")
        self.skipToNewPageBtn.setIcon(QIcon(QPixmap(Tab.picPath + "skipToNewPage.png")))
        self.skipToNewPageBtn.clicked.connect(self.skipToNewPage)
        self.topPanel.addWidget(self.skipToNewPageBtn)
        self.topPanel.addSeparator()
        #百度搜索
        self.baiduBtn = QPushButton()
        self.baiduBtn.setFixedSize(50, 50)
        self.baiduBtn.setStyleSheet("border:none")
        self.baiduBtn.setIcon(QIcon(QPixmap(Tab.picPath + "baiduLogo.png")))
        self.topPanel.addWidget(self.baiduBtn)
        self.inputWebNameLineEdit = QLineEdit()
        self.inputWebNameLineEdit.setFixedWidth(200)
        self.inputWebNameLineEdit.setStyleSheet("background-color:white;border:none")
        self.topPanel.addWidget(self.inputWebNameLineEdit)
        self.searchBtn = QPushButton()
        self.searchBtn.setFixedSize(50, 50)
        self.searchBtn.setStyleSheet("QPushButton{border:none;}""QPushButton:hover{background-color:#f2f2f2;border:none;}")
        self.searchBtn.setIcon(QIcon(QPixmap(Tab.picPath + "search.png")))
        self.topPanel.addWidget(self.searchBtn)
        self.topPanel.addSeparator()
        #历史记录按钮
        self.showWebHistoryBtn = QPushButton()
        self.showWebHistoryBtn.setToolTip("历史记录".encode("unicode_escape").decode("unicode_escape"))
        self.showWebHistoryBtn.setFixedSize(50, 50)
        self.showWebHistoryBtn.setStyleSheet("QPushButton{border:none;}""QPushButton:hover{background-color:#f2f2f2;border:none;}")
        self.showWebHistoryBtn.setIcon(QIcon(QPixmap(Tab.picPath + "webHistory.png")))
        self.showWebHistoryBtn.clicked.connect(self.showWebHistory)
        self.topPanel.addWidget(self.showWebHistoryBtn)
        #前端开发者工具按钮
        self.showInspectorBtn = QPushButton()
        self.showInspectorBtn.setToolTip("前端开发者工具".encode("unicode_escape").decode("unicode_escape"))
        self.showInspectorBtn.setFixedSize(50, 50)
        self.showInspectorBtn.setStyleSheet("QPushButton{border:none;}""QPushButton:hover{background-color:#f2f2f2;border:none;}")
        self.showInspectorBtn.setIcon(QIcon(QPixmap(Tab.picPath + "toolBar.png")))
        self.showInspectorBtn.clicked.connect(self.showInspector)
        self.topPanel.addWidget(self.showInspectorBtn)

        #历史记录面板
        self.browserHistoryPanel=QWidget()
        self.browserHistoryPanel.setWindowFlag(Qt.Popup)
        self.browserHistoryPanelLayout=QVBoxLayout()
        self.browserHistoryPanel.setLayout(self.browserHistoryPanelLayout)
        self.browserHistoryPanelLayout.setContentsMargins(0,0,0,0)
        self.browserHistoryPanelLayout.setSpacing(0)
        self.browserHistoryWidget=QTableWidget()
        self.browserHistoryWidget.setContentsMargins(0,0,0,0)
        self.browserHistoryWidget.setStyleSheet("QTableWidget::item{background-color:white}""QTableWidget::item::hover{background-color:#f2f2f2 }""QTableWidget::item::selected{color:#000000;background-color:#f2f2f2 }")
        self.browserHistoryPanelLayout.addWidget( self.browserHistoryWidget)
        desktop = QApplication.desktop()
        self.browserHistoryPanel.move(desktop.availableGeometry().width()-300,105)
        self.browserHistoryWidget.clicked.connect(self.skipToOldPage)
        #浏览器右键菜单
        self.browser.setContextMenuPolicy(Qt.CustomContextMenu)
        self.browser.customContextMenuRequested.connect(self.showBrowserMenu)
        self.backAct = QAction("返回(B)".encode("unicode_escape").decode("unicode_escape"))
        self.backAct.setEnabled(False)
        self.backAct.triggered.connect(self.browser.back)
        self.forwardAct = QAction("前进(F)".encode("unicode_escape").decode("unicode_escape"))
        self.forwardAct.setEnabled(False)
        self.forwardAct.triggered.connect(self.browser.forward)
        self.viewWebSourceCode = QAction("查看网页源代码(V)".encode("unicode_escape").decode("unicode_escape"))
        self.viewWebSourceCode.triggered.connect(self.printWebSourceCode)
    #显示右键菜单
    def showBrowserMenu(self):
        self.webMenu = QMenu()
        self.webMenu.addAction(self.backAct)
        self.webMenu.addAction(self.forwardAct)
        self.webMenu.addAction(self.viewWebSourceCode)
        self.webMenu.exec_(QCursor.pos())
    #打印网页源码
    def printWebSourceCode(self):
        self.browser.page().toHtml(self.pasteWebSourceCode)
    #将网页源码粘贴到记事本（目前只确定适用于windows系统）
    def pasteWebSourceCode(self,webSourceCode):
        path="./com/mat/rpa/views/workWindow/topPanel/rpaWebBrowser/temporaryTXTFile/"
        if not os.path.exists(path):
            os.mkdir(path)
        with open( path+datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.txt', 'w',encoding="utf-8") as f:
            f.write(webSourceCode)
        #if platform.system().lower()=='windows':
        os.system('start notepad '+path +datetime.datetime.now().strftime('%Y%m%d%H%M%S')+'.txt')
        #elif  platform.system().lower()=='linux':

    #输入url跳转到新网页
    def skipToNewPage(self):
        if self.inputUrlLineEdit.text().startswith('https://') or self.inputUrlLineEdit.text().startswith('http://'):
            self.browser.load(QUrl(self.inputUrlLineEdit.text()))
        else:
            self.browser.load(QUrl('https://' + self.inputUrlLineEdit.text()))
    #跳转到浏览器主页
    def skipToHomePage(self):
        self.browser.load(QUrl('https://www.baidu.com'))
    #设置网页（Tab）标题
    def setWebTitle(self,title):
        if len(title) > 12:
            title = title[0:13]+"..."
        self.rpaWebBrowserWin.setTabText(0,title)
    #设置网页（Tab）图标
    def setWebIcon(self,icon):
        self.rpaWebBrowserWin.setTabIcon(0,icon)
    #当url改变时，更新历史记录以及前进后退按钮状态
    def urlBeChanged(self):
        history = self.browser.history()
        if history.currentItemIndex() == 0:
            self.inputUrlLineEdit.setText("")
            self.browser.load(QUrl('https://www.baidu.com'))
        else:
           self.inputUrlLineEdit.setText(self.browser.url().toString())
        if history.count() > 1:
            if history.currentItemIndex() == history.count() - 1:
                self.backAct.setEnabled(True)
                self.forwardAct.setEnabled(False)
                self.backBtn.setIcon(QIcon(QPixmap(Tab.picPath + "back.png")))
                self.backBtn.setStyleSheet("QPushButton{border:none;}""QPushButton:hover{background-color:#f2f2f2;border:none;}")
                self.forwardBtn.setIcon(QIcon(QPixmap(Tab.picPath + "forwardEnabled.png")))
                self.forwardBtn.setStyleSheet("border:none;")
            elif history.currentItemIndex() == 0:
                self.backAct.setEnabled(False)
                self.forwardAct.setEnabled(True)
                self.backBtn.setIcon(QIcon(QPixmap(Tab.picPath + "backEnabled.png")))
                self.backBtn.setStyleSheet("border:none;")
                self.forwardBtn.setIcon(QIcon(QPixmap(Tab.picPath + "forward.png")))
                self.forwardBtn.setStyleSheet(
                    "QPushButton{border:none;}""QPushButton:hover{background-color:#f2f2f2;border:none;}")
            else:
                self.backAct.setEnabled(True)
                self.forwardAct.setEnabled(True)
                self.backBtn.setIcon(QIcon(QPixmap(Tab.picPath + "back.png")))
                self.backBtn.setStyleSheet(
                    "QPushButton{border:none;}""QPushButton:hover{background-color:#f2f2f2;border:none;}")
                self.forwardBtn.setIcon(QIcon(QPixmap(Tab.picPath + "forward.png")))
                self.forwardBtn.setStyleSheet(
                    "QPushButton{border:none;}""QPushButton:hover{background-color:#f2f2f2;border:none;}")
    #显示历史记录panel
    def showWebHistory(self):
        self.browserHistoryWidget.clear()
        self.browserHistoryWidget.setRowCount(self.browser.history().count())
        self.browserHistoryWidget.setColumnCount(1)
        self.browserHistoryWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.browserHistoryWidget.horizontalHeader().setStretchLastSection(True)
        self.browserHistoryWidget.horizontalHeader().setVisible(False)
        self.browserHistoryWidget.verticalHeader().setVisible(False)
        i=self.browser.history().count()
        j=0
        while i>=1:
            item=self.browser.history().itemAt(i-1)
            self.browserHistoryWidget.setItem(j,0,QTableWidgetItem(item.title()))
            i-=1
            j+=1
        self.browserHistoryPanel.show()
    #点击历史记录，跳转到相应网页
    def skipToOldPage(self,index):
        historyCount= self.browser.history().count()
        historyItem=self.browser.history().itemAt(historyCount-index.row()-1)
        self.browser.history().goToItem(historyItem)
    #显示前端开发者工具panel
    def showInspector(self):
        self.inspector = QWebEngineView()
        self.inspector.load(QUrl(DEBUG_URL))
        self.inspector.setWindowTitle("DevTools")
        self.inspector.setGeometry(300, 100, 1355, 730)
        self.browser.page().setDevToolsPage(self.inspector.page())
        self.inspector.show()

    def getRPAWebBrowserWin(self,rpaWebBrowserWin):
        self.rpaWebBrowserWin=rpaWebBrowserWin
#双击url输入框时，选中输入框中的所有字符串
class InputUrlLineEdit(QLineEdit):
    def __init__(self,parent=None):
        super(InputUrlLineEdit, self).__init__(parent)
        __font = QFont()
        __font.setPixelSize(20)
        __font.setFamily("Cambria")
        self.setStyleSheet("background-color:white;border:none")
        self.setFont(__font)
    def mouseDoubleClickEvent(self, e):
        self.selectAll()
#点击网页中的链接有响应
class WebEngineView(QtWebEngineWidgets.QWebEngineView):
    def createWindow(self,QWebEnginePage_WebWindowType):
        page = WebEngineView(self)
        page.urlChanged.connect(self.on_url_changed)
        return page

    def on_url_changed(self,url):
        self.load(url)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    titleBar=RPAWebBrowser()
    titleBar.show()
    sys.exit(app.exec_())
