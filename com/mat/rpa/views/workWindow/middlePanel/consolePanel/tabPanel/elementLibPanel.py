# -*- coding:utf-8 -*-
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets, QtWebChannel
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineScript, QWebEnginePage
import os
from jinja2 import Template
from com.mat.rpa.views.workWindow.middlePanel.consolePanel.tabPanel import basicConsolePanel
import pyautogui
from com.mat.rpa.dao.elementDao import elementDao
import io
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

class ElementLibPanel(basicConsolePanel.BasicConsolePanel):
    picPath = "./com/mat/rpa/views/workWindow/middlePanel/consolePanel/tabPanel/images/"
    elementNum = 1
    elementType = {"html": "网页框架基本结构块", "body": "网页框架基本结构块", "frameset": "网页框架基本结构块",
                   "frame": "网页框架基本结构块", "noframe": "网页框架基本结构块", "iframe": "网页框架基本结构块",
                   "form": "表单结构块", "filedset": "表单结构块", "legend": "表单结构块", "div": "布局结构块",
                   "p": "段落结构块",
                   "h1": "标题结构块", "h2": "标题结构块", "h3": "标题结构块", "h4": "标题结构块", "h5": "标题结构块", "h6": "标题结构块",
                   "ol": "列表结构块", "ul": "列表结构块", "dl": "列表结构块", "dt": "列表结构块", "dd": "列表结构块", "menu": "列表结构块",
                   "dir": "列表结构块", "center": "居中结构块", "pre": "预定义结构块", "blockquote": "引用结构块",
                   "hr": "结构装饰线", "title": "网页标题框", "span": "行内包含框", "a": "超链接和映射包含框", "area": "超链接和映射包含框",
                   "img": "图像包含框",
                   "abbr": "格式化信息包含框", "b": "格式化信息包含框", "bdo": "格式化信息包含框", "cite": "格式化信息包含框",
                   "code": "格式化信息包含框", "del": "格式化信息包含框", "dfn": "格式化信息包含框", "em": "格式化信息包含框",
                   "font": "格式化信息包含框", "i": "格式化信息包含框", "ins": "格式化信息包含框", "kbd": "格式化信息包含框",
                   "q": "格式化信息包含框", "s": "格式化信息包含框", "samp": "格式化信息包含框", "small": "格式化信息包含框",
                   "strike": "格式化信息包含框", "strong": "格式化信息包含框", "sub": "格式化信息包含框", "sup": "格式化信息包含框",
                   "tt": "格式化信息包含框", "u": "格式化信息包8含框", "var": "格式化信息包含框",
                   "button": "表单对象包含框", "select": "表单对象包含框", "textarea": "表单对象包含框", "label": "表单对象包含框",
                   "applet": "可执行的插件或对象包含框", "object": "可执行的插件或对象包含框",
                   "caption": "表格标题包含框", "noscript": "无脚本包含框", "head": "头部包含框", "basefont": "默认基础字体属性",
                   "link": "链接", "meta": "元信息", "script": "脚本", "style": "样式", "base": "url基础",
                   "input": "输入框", "option": "下拉选框", "optgroup": "下拉框的分组", "li": "列表项",
                   "map": "图像映射包含框", "param": "参数", "br": "换行", "table": "表格框显示", "tr": "表格行显示",
                   "td": "单元格显示", "th": "表格标题显示", "tbody": "表格行组显示", "tfoot": "表格脚注组显示", "thead": "表格标题组显示"}
    def __init__(self, parent=None):
        super(ElementLibPanel, self).__init__(parent)
        self.elementDaoMongo = elementDao.ElementDao()
        self.hintLabel.setText("元素库")



        #创建QToolButoon
        self.newElementCaptureBtn = QPushButton()
        self.newElementCaptureBtn.setText("捕获新元素")
        self.newElementCaptureBtn.setIcon(
            QIcon(QPixmap(ElementLibPanel.picPath+"plusSign.png")))
        self.newElementCaptureBtn.clicked.connect(self.captureNewElement)
        self.newElementCaptureBtn.setMaximumSize(100, 30)
        self.centerPanelLayout.addWidget(self.newElementCaptureBtn, 0, 1)

        self.newElementWindow = QTreeWidget()
        self.newElementWindow.setColumnCount(1)
        self.newElementWindow.setHeaderHidden(True)
        self.centerPanelLayout.addWidget(self.newElementWindow, 0, 0, 2, 1)

    def searchBoxPanelUp(self):
        self.stackedWidget.setCurrentIndex(1)

    def captureNewElement(self):
        xpath_helper = XpathHelper("xpath_helper")
        xpath_helper.posxClicked.connect(self.getPosx)
        xpath_helper.posyClicked.connect(self.getPosy)
        xpath_helper.elementwClicked.connect(self.getElementw)
        xpath_helper.elementhClicked.connect(self.getElementh)
        xpath_helper.xpathClicked.connect(self.getXpath)
        xpath_helper.xpathClicked.connect(self.getElement)
        xpath_helper.urlClicked.connect(self.getUrl)
        xpath_helper.titleClicked.connect(self.getTitle)
        xpath_helper.xpathClicked.connect(self.addElement)
        self.browser = QWebEngineView()
        self.page = WebEnginePage()
        self.page.add_object(xpath_helper)
        self.browser.setPage(self.page)
        #self.browser.load(QUrl("file:///C:/Users/32608/Desktop/combobox.html"))
        self.browser.load(QUrl("https://www.baidu.com"))
        # self.browser.setWindowTitle('RPAP浏览器')
        # self.browser.setWindowIcon(QIcon(QPixmap(ElementLibPanel.picPath + "logo64.png")))
        # self.browser.setWindowState(Qt.WindowMaximized)
        # self.browser.show()

        self.mainWindow = QMainWindow()
        self.mainWindow.setWindowTitle('RPAP浏览器')
        self.mainWindow.setWindowIcon(QIcon(QPixmap(ElementLibPanel.picPath + "logo64.png")))
        self.mainWindow.setWindowState(Qt.WindowMaximized)

        self.mainWindow.setCentralWidget(self.browser)
        # 添加导航栏
        navigation_bar = QToolBar('Navigation')
        # 设定图标的大小
        navigation_bar.setIconSize(QSize(16, 16))
        # 添加导航栏到窗口中
        self.mainWindow.addToolBar(navigation_bar)
        # QAction类提供了抽象的用户界面action，这些action可以被放置在窗口部件中
        # 添加前进、后退、停止加载和刷新的按钮
        back_button = QAction(QIcon(self.picPath+"back.png"),'Back',self)
        next_button = QAction(QIcon(self.picPath+'next.png'), 'Forward', self)
        stop_button = QAction(QIcon(self.picPath+'cross.png'), 'stop', self)
        reload_button = QAction(QIcon(self.picPath+'renew.png'), 'reload', self)
        back_button.triggered.connect(self.browser.back)
        next_button.triggered.connect(self.browser.forward)
        stop_button.triggered.connect(self.browser.stop)
        reload_button.triggered.connect(self.browser.reload)
        # 将按钮添加到导航栏上
        navigation_bar.addAction(back_button)
        navigation_bar.addAction(next_button)
        navigation_bar.addAction(stop_button)
        navigation_bar.addAction(reload_button)
        # 添加URL地址栏
        self.urlbar = QLineEdit()
        # 让地址栏能响应回车按键信号
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navigation_bar.addSeparator()
        navigation_bar.addWidget(self.urlbar)
        # 让浏览器相应url地址的变化
        self.browser.urlChanged.connect(self.renew_urlbar)
        self.mainWindow.show()

    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == '':
            q.setScheme('http')
        self.browser.setUrl(q)

    def renew_urlbar(self, q):
        # 将当前网页的链接更新到地址栏
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    def getPosx(self, posx):
        self.posx = float(posx)

    def getPosy(self, posy):
        self.posy = float(posy)

    def getElementw(self, elementw):
        self.elementw = float(elementw)*1

    def getElementh(self, elementh):
        self.elementh = float(elementh)*1.5

    def getXpath(self, xpath):
        self.xpath = xpath

    def getElement(self, xpath):
        self.elementClass = (xpath.split('/'))[-1]
        if self.elementClass in self.elementType.keys():
            self.elementClass = self.elementType[self.elementClass] + "_元素" + str(self.elementNum)
        else:
            self.elementClass = '元素' + "_元素" + str(self.elementNum)

    def getUrl(self, url):
        self.url = url

    def getTitle(self, title):
        self.title = title

    def addElement(self, xpath):
        if xpath is not None:
            self.posx_count = round(float(self.posx)) + self.browser.geometry().x()
            self.posy_count = round(float(self.posy)) + self.browser.geometry().y()
            #print(QGuiApplication.primaryScreen().logicalDotsPerInch())
            self.elementImage = pyautogui.screenshot('element.png',
                                                     region=(
                                                         float(self.posx_count), float(self.posy_count),
                                                         float(self.elementw), float(self.elementh)))
            self.addElementWindow = QWidget()
            self.addElementWindow.setFixedSize(800, 700)
            self.addElementWindow.setWindowTitle("元素编辑器")
            self.addElementWindowLayout = QGridLayout()
            self.addElementWindow.setLayout(self.addElementWindowLayout)
            self.addElementLayout = QGridLayout()
            self.addElementLayout.setSpacing(10)
            self.receiveBtn = QPushButton("重新捕获(F4)")
            self.addElementLayout.addWidget(self.receiveBtn, 0, 0, 1, 1, Qt.AlignLeft)
            self.similarBtn = QPushButton("捕获相似元素(F6)")
            self.addElementLayout.addWidget(self.similarBtn, 0, 1, 1, 1, Qt.AlignLeft)
            self.elementNameLabel = QLabel("元素名称：")
            self.addElementLayout.addWidget(self.elementNameLabel, 1, 0, 1, 1, Qt.AlignLeft)
            self.elementNameEdit = QLineEdit()
            self.elementNameEdit.setEnabled(True)
            self.elementNameEdit.setMinimumSize(600, 30)
            self.addElementLayout.addWidget(self.elementNameEdit, 1, 1, 1, 5, Qt.AlignLeft)
            self.addElementWindowLayout.addLayout(self.addElementLayout, 0, 0, 1, 6, Qt.AlignTop)
            self.elementView = QTabWidget()
            self.firstTab = QWidget()
            self.showPicLayout = QHBoxLayout()
            self.showPic = QLabel()
            self.showPic.setPixmap(QPixmap('element.png'))
            self.showPicLayout.addWidget(self.showPic, Qt.AlignCenter)
            self.firstTab.setLayout(self.showPicLayout)
            self.elementView.addTab(self.firstTab, "元素预览")
            self.secondTab = QTableWidget()
            self.elementView.addTab(self.secondTab, "编辑")
            self.elementView.setFixedSize(770, 550)
            self.addElementWindowLayout.addWidget(self.elementView, 1, 0, 2, 6, Qt.AlignLeft)
            self.bottomLayout = QHBoxLayout()
            self.helpButton = QPushButton("帮助")
            self.helpButton.setSizePolicy(100, 50)
            self.bottomLayout.addWidget(self.helpButton, 0, Qt.AlignLeft)
            self.saveButton = QPushButton("保存并继续")
            self.saveButton.setSizePolicy(100, 50)
            self.saveButton.clicked.connect(self.addElementWin)
            self.saveButton.clicked.connect(self.addElementWindow.close)
            self.bottomLayout.addWidget(self.saveButton, 50, Qt.AlignRight)
            self.finishButton = QPushButton("完成")
            self.finishButton.setSizePolicy(100, 50)
            self.finishButton.clicked.connect(self.addElementWin)
            self.finishButton.clicked.connect(self.addElementWindow.close)
            self.bottomLayout.addWidget(self.finishButton, 6, Qt.AlignRight)
            self.addElementWindowLayout.addLayout(self.bottomLayout, 3, 0, 1, 6, Qt.AlignBottom)
            self.addElementWindow.show()

    def addElementWin(self):
        self.elementNum = self.elementNum + 1
        img_byte = io.BytesIO()
        self.elementClass = self.elementNameEdit.text()
        self.elementImage.save(img_byte, format='PNG')
        self.img = img_byte.getvalue()
        self.elementDict = {"name": self.elementClass, "xpath": self.xpath, "url": self.url, "title": self.title,
                            "image": self.img, "x": self.posx, "y": self.posy, "w": self.elementw, "h": self.elementh}
        self.elementDaoMongo.insertNewElement(self.elementDict)
        self.root = QTreeWidgetItem(self.newElementWindow)
        self.child = QTreeWidgetItem(self.root)
        self.newElementWindow.itemDoubleClicked.connect(self.mouseDoubieClickEvent)
        if self.root.text == self.title:
            self.child.setText(0, self.elementClass)
        else:
            self.root.setText(0, self.title)
            self.child.setText(0, str(self.elementNameEdit.text()))


    def mouseDoubieClickEvent(self):
        self.addElementWindow2 = QWidget()
        self.addElementWindow2.setFixedSize(800, 700)
        self.addElementWindow2.setWindowTitle("元素编辑器")
        self.addElementWindow2Layout = QGridLayout()
        self.addElementWindow2.setLayout(self.addElementWindow2Layout)
        self.addElement2Layout = QGridLayout()
        self.addElement2Layout.setSpacing(10)
        self.receive2Btn = QPushButton("重新捕获(F4)")
        self.addElement2Layout.addWidget(self.receive2Btn, 0, 0, 1, 1, Qt.AlignLeft)
        self.similar2Btn = QPushButton("捕获相似元素(F6)")
        self.addElement2Layout.addWidget(self.similar2Btn, 0, 1, 1, 1, Qt.AlignLeft)
        self.elementName2Label = QLabel("元素名称：")
        self.addElement2Layout.addWidget(self.elementName2Label, 1, 0, 1, 1, Qt.AlignLeft)
        self.elementName2Edit = QLineEdit()
        self.elementName2Edit.setEnabled(True)
        self.elementName2Edit.setMinimumSize(600, 30)
        self.elementName2Edit.setText(self.elementClass)
        self.addElement2Layout.addWidget(self.elementName2Edit, 1, 1, 1, 5, Qt.AlignLeft)
        self.addElementWindow2Layout.addLayout(self.addElement2Layout, 0, 0, 1, 6, Qt.AlignTop)
        self.element2View = QTabWidget()
        self.first2Tab = QTableWidget()
        self.showPicLayout = QHBoxLayout()
        self.showPicture = QLabel()
        self.pixmapClass = QPixmap()
        self.pixmapClass.loadFromData(self.elementDaoMongo.getOneElement(self.elementClass)["image"], format='png')
        self.showPicture.setPixmap(self.pixmapClass)
        self.showPicLayout.addWidget(self.showPicture)
        self.first2Tab.setLayout(self.showPicLayout)
        self.element2View.addTab(self.first2Tab, "元素预览")
        self.xpathinfo = self.xpath.split('/')
        self.second2Tab = QTableWidget(len(self.xpathinfo)-1, 2)
        self.second2Tab.setHorizontalHeaderLabels(['启用', '元素节点'])
        for i in range(len(self.xpathinfo)):
            newItem = QTableWidgetItem(str(self.xpathinfo[i]))
            self.second2Tab.setItem(i-1, 1, newItem)
            newItem2 = QCheckBox()
            newItem2.setChecked(True)
            self.second2Tab.setCellWidget(i-1, 0, newItem2)
        self.element2View.addTab(self.second2Tab, "编辑")
        self.element2View.setFixedSize(770, 550)
        self.addElementWindow2Layout.addWidget(self.element2View, 1, 0, 2, 6, Qt.AlignLeft)
        self.bottom2Layout = QHBoxLayout()
        self.help2Button = QPushButton("帮助")
        self.help2Button.setSizePolicy(100, 50)
        self.bottom2Layout.addWidget(self.help2Button, 0, Qt.AlignLeft)
        self.finish2Button = QPushButton("完成")
        self.finish2Button.setSizePolicy(100, 50)
        self.finish2Button.clicked.connect(self.addElementWindow2.close)
        self.bottom2Layout.addWidget(self.finish2Button, 6, Qt.AlignRight)
        self.addElementWindow2Layout.addLayout(self.bottom2Layout, 3, 0, 1, 6, Qt.AlignBottom)
        self.addElementWindow2.show()

class Element(QtCore.QObject):
    def __init__(self, name, parent=None):
        super(Element, self).__init__(parent)
        self._name = name
        #print("name is:", name)

    @property
    def name(self):
        return self._name

    def script(self):
        return ""


class WebEnginePage(QtWebEngineWidgets.QWebEnginePage):
    def __init__(self, parent=None):
        super(WebEnginePage, self).__init__(parent)
        self.loadFinished.connect(self.onLoadFinished)
        self._objects = []
        self._scripts = []

    def add_object(self, obj):
        self._objects.append(obj)

    @QtCore.pyqtSlot(bool)
    def onLoadFinished(self, ok):
        if ok:
            self.load_qwebchannel()
            self.add_objects()

    def load_qwebchannel(self):
        file = QtCore.QFile(os.path.join(CURRENT_DIR, "qwebchannel.js"))
        if file.open(QtCore.QIODevice.ReadOnly):
            content = file.readAll()
            file.close()
            self.runJavaScript(content.data().decode())
        if self.webChannel() is None:
            channel = QtWebChannel.QWebChannel(self)
            self.setWebChannel(channel)

    def add_objects(self):
        if self.webChannel() is not None:
            objects = {obj.name: obj for obj in self._objects}
            self.webChannel().registerObjects(objects)
            _script = """
            {% for obj in objects %}
            var {{obj}};
            {% endfor %}
            new QWebChannel(qt.webChannelTransport, function (channel) {
            {% for obj in objects %}
                {{obj}} = channel.objects.{{obj}}; //这里将PyQt对象传给JavaScript，包括xpath_helper
            {% endfor %}
            }); 
            """
            self.runJavaScript(Template(_script).render(objects=objects.keys()))
            for obj in self._objects:
                if isinstance(obj, Element):
                    self.runJavaScript(obj.script())


class XpathHelper(Element):
    posxClicked = QtCore.pyqtSignal(str)
    posyClicked = QtCore.pyqtSignal(str)
    elementwClicked = QtCore.pyqtSignal(str)
    elementhClicked = QtCore.pyqtSignal(str)
    xpathClicked = QtCore.pyqtSignal(str)
    urlClicked = QtCore.pyqtSignal(str)
    titleClicked = QtCore.pyqtSignal(str)

    def script(self):
        js = ""
        file = QtCore.QFile(os.path.join(CURRENT_DIR, "xpath_from_element.js"))
        if file.open(QtCore.QIODevice.ReadOnly):
            content = file.readAll()
            file.close()
            js = content.data().decode()

        js += """
        document.addEventListener('click', function(e) {
            e = e || window.event;
            if (e.ctrlKey) {
               var clickx = e.clientX;
               var clicky = e.clientY;
               element = document.elementFromPoint(clickx, clicky);
               rec = element.getBoundingClientRect();
               var x = rec.left;
               var y = rec.top;
               var w = element.offsetWidth;
               var h = element.offsetHeight;
               {{name}}.receive_posx(x);
               {{name}}.receive_posy(y);
               {{name}}.receive_elementw(w);
               {{name}}.receive_elementh(h);
               var target = e.target || e.srcElement;
               var xpath = Elements.DOMPath.xPath(target, false); 
               {{name}}.receive_xpath(xpath); //所以这里可以调用xpath_helper.receive_xpath(xpath)
               var url = window.location.href;
               {{name}}.receive_url(url); //返回url
               var title = document.title;
               {{name}}.receive_title(title); //返回title
            }
        }, true);
        function get_current_element(event){
        var x = event.clientX, y = event.clientY,
        element = document.elementFromPoint(x, y);
        return element
        }
        var last_element = null
        function highlight(element){
        element.style.outline = '#f00 solid 2px'
        }
        function remove_hightlight(element){
        element.style.removeProperty('outline')
        }
        function track_mouse(event){
        var elementMouseIsOver = get_current_element(event)
        if (elementMouseIsOver === last_element) {
            return
        }
        if (last_element != null) {
            remove_hightlight(last_element)
        }
        highlight(elementMouseIsOver)
        last_element = elementMouseIsOver
        }
        window.onmousemove = track_mouse"""
        return Template(js).render(name=self.name)

    @QtCore.pyqtSlot(str)
    def receive_posx(self, posx):
        self.posxClicked.emit(posx)

    @QtCore.pyqtSlot(str)
    def receive_posy(self, posy):
        self.posyClicked.emit(posy)

    @QtCore.pyqtSlot(str)
    def receive_elementw(self, elementw):
        self.elementwClicked.emit(elementw)

    @QtCore.pyqtSlot(str)
    def receive_elementh(self, elementh):
        self.elementhClicked.emit(elementh)

    @QtCore.pyqtSlot(str)
    def receive_xpath(self, xpath):
        self.xpathClicked.emit(xpath)

    @QtCore.pyqtSlot(str)
    def receive_url(self, url):
        self.urlClicked.emit(url)

    @QtCore.pyqtSlot(str)
    def receive_title(self, title):
        self.titleClicked.emit(title)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ElementLibPanel()
    win.show()
    app.exec_()