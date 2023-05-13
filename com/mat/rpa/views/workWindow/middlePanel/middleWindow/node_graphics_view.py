from PyQt5.QtWidgets import QGraphicsView, QMenu, QAction, QSpinBox, QDialog, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from com.mat.rpa.dao.workDao.directiveDao import DirectiveDao
from com.mat.rpa.views.workWindow.middlePanel.middleWindow.node_edge import EDGE_TYPE_BEZIER, Edge, QDMGraphicsEdge
from com.mat.rpa.views.workWindow.middlePanel.middleWindow.node_graphics_socket import QDMGraphicsSocket



MODE_NOOP = 1
MODE_EDGE_DRAG = 2
EDGE_DRAG_START_THRESHOLD = 10


class QDMGraphicsView(QGraphicsView):
    def __init__(self, grScene, parent=None, flowMode=0):
        super().__init__(parent)
        self.grScene = grScene
        self.item=None
        self.flowMode = flowMode
        self.initUI()
        self.setScene(self.grScene)
        self.mode=1
        self.zoomInFactor = 1.25
        self.zoom = 5
        self.zoomStep = 1
        self.zoomClamp = False
        self.zoomRange = [0,10]
        self.setAcceptDrops(True)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.editingFlag = False
        self.setMouseTracking(True)
        self.sp = QSpinBox()
        self.sp.setValue(10)
        self.sp.setSingleStep(2)
        self.dialog = QDialog()
        self.dialog.resize(250, 100)
        self.dialog.setWindowTitle("修改字体大小")
        self.l1 = QLabel('当前字体大小:10')
        self.btn1 = QPushButton("确认")
        self.sp.setMaximum(24)
        self.sp.setMinimum(8)
        self.directiveDaoObj = DirectiveDao()

    def initUI(self):
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)

        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

    def mousePressEvent(self, event):
        if event.button() == Qt.MidButton:
            self.middleMouseButtonPress(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonPress(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonPress(event)
        else:
            super().mousePressEvent(event)
    def changeConnect(self):
        self.grScene.ifconnetableChange()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonRelease(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonRelease(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonRelease(event)
        else:
            super().mouseReleaseEvent(event)

    # 双击事件

    def mouseDoubleClickEvent(self, event):
        item = self.getItemAtClick(event)

        if item is not None:
            self.settingDialog = item.node.dialog
            self.settingDialog.getSettingData()
            self.settingDialog.show()


    def middleMouseButtonPress(self, event):

        #当鼠标中键按下时，将产生一个假的鼠标按键松开的事件
        releaseEvent = QMouseEvent(QEvent.MouseButtonRelease,event.localPos(),event.screenPos(),
                                   Qt.LeftButton,Qt.NoButton,event.modifiers())
        super().mouseReleaseEvent(releaseEvent)

        #变为抓取手势
        self.setDragMode(QGraphicsView.ScrollHandDrag)

        #产生一个鼠标按下左键的假事件
        fakeEvent = QMouseEvent(event.type(),event.localPos(),event.screenPos(),
                                Qt.LeftButton,event.buttons() | Qt.LeftButton,event.modifiers())
        super().mousePressEvent(fakeEvent)

    def middleMouseButtonRelease(self, event):
        fakeEvent = QMouseEvent(event.type(),event.localPos(),event.screenPos(),
                                Qt.LeftButton,event.buttons() | Qt.LeftButton,event.modifiers())
        super().mouseReleaseEvent(fakeEvent)
        self.setDragMode(QGraphicsView.NoDrag)

    def leftMouseButtonPress(self, event):

        item = self.getItemAtClick(event)
        self.last_lmb_click_scene_pos = self.mapToScene(event.pos())
        if hasattr(item, "node") or isinstance(item, QDMGraphicsEdge) or item is None:
            if event.modifiers() & Qt.ShiftModifier:
                event.ignore()
                fakeEvent = QMouseEvent(QEvent.MouseButtonPress, event.localPos(), event.screenPos(),
                                        Qt.LeftButton, event.button() | Qt.LeftButton,
                                        event.modifiers() | Qt.ControlModifier)
                super().mousePressEvent(fakeEvent)
                return
        if (type(item) is QDMGraphicsSocket) and self.grScene.ifconnetable:
            if self.mode == MODE_NOOP:
                self.mode = MODE_EDGE_DRAG
                self.edgeDragStart(item)
                return

        if self.mode == MODE_EDGE_DRAG:
            res = self.edgeDragEnd(item)
            if res: return

        super().mousePressEvent(event)

    def edgeDragStart(self, item):
        self.previousEdge = item.socket.edge
        self.last_start_socket = item.socket
        self.dragEdge = Edge(self.grScene.scene, item.socket, None, EDGE_TYPE_BEZIER)

    def leftMouseButtonRelease(self, event):
        # 获得我们所选择的Item
        item = self.getItemAtClick(event)

        if self.mode == MODE_EDGE_DRAG:
            if self.distanceBetweenClickReleaseIsOff(event):
                res = self.edgeDragEnd(item)
                if res: return

        super().mouseReleaseEvent(event)
        if hasattr(item, "node") or isinstance(item, QDMGraphicsEdge) or item is None:
            if event.modifiers() & Qt.ShiftModifier:
                event.ignore()
                fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                        Qt.LeftButton, Qt.NoButton,
                                        event.modifiers() | Qt.ControlModifier)
                super().mouseReleaseEvent(fakeEvent)
                return

    def rightMouseButtonPress(self, event):
        self.item = self.getItemAtClick(event)
        if self.item is not None:
            menu = QMenu()
            Delete = QAction("删除", self)
            Delete.triggered.connect(self.deleteSelected)
            menu.addAction(Delete)
            TextSize = QAction("文本大小", self)
            TextSize.triggered.connect(lambda: self.spinBoxAppear())
            menu.addAction(TextSize)
            menu.exec_(QCursor.pos())  # 在鼠标位置显示
            return

    def rightMouseButtonRelease(self,event):
        return super().mouseReleaseEvent(event)


    def wheelEvent(self, event):
        #计算缩放系数
        zoomOutFactor = 1/self.zoomInFactor

        #计算缩放
        if event.angleDelta().y()>0:
            zoomFactor = self.zoomInFactor
            self.zoom += self.zoomStep
        else:
            zoomFactor = zoomOutFactor
            self.zoom -= self.zoomStep

        clamped = False
        if self.zoom < self.zoomRange[0]:
            self.zoom,clamped = self.zoomRange[0],True
        if self.zoom > self.zoomRange[1]:
            self.zoom, clamped = self.zoomRange[1], True

        #设置场景比例
        if not clamped or self.zoomClamp:
            self.scale(zoomFactor,zoomFactor)
    def getItemAtClick(self,event):
        #获取鼠标下的ITEM obj
        pos = event.pos()
        obj = self.itemAt(pos)

        return obj

    def edgeDragEnd(self, item):
        """返回True来跳过代码 """
        self.mode = MODE_NOOP

        if type(item) is QDMGraphicsSocket:
            if item.socket !=self.last_start_socket:
                if item.socket.hasEdge():
                    item.socket.edge.remove()
                if self.previousEdge is not None:
                    self.previousEdge.remove()
                self.dragEdge.start_socket = self.last_start_socket
                self.dragEdge.end_socket = item.socket
                self.dragEdge.start_socket.setConnectedEdge(self.dragEdge)
                self.dragEdge.end_socket.setConnectedEdge(self.dragEdge)
                self.dragEdge.updatePosition()
                return True

        self.dragEdge.remove()

        self.dragEdge = None

        if self.previousEdge is not None:
            self.previousEdge.start_socket.edge = self.previousEdge

        return False

    def distanceBetweenClickReleaseIsOff(self,event):
        #处理按下松开太近的问题
        new_lmb_release_scene_pos = self.mapToScene(event.pos())
        dist_scene = new_lmb_release_scene_pos - self.last_lmb_click_scene_pos
        edge_darg_threshold_sq = EDGE_DRAG_START_THRESHOLD * EDGE_DRAG_START_THRESHOLD
        return (dist_scene.x()*dist_scene.x() + dist_scene.y()*dist_scene.y()) > edge_darg_threshold_sq

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if self.mode == MODE_EDGE_DRAG:
            pos = self.mapToScene(event.pos())
            self.dragEdge.grEdge.setDestination(pos.x(), pos.y())
            self.dragEdge.grEdge.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            if not self.editingFlag:
                self.deleteSelected()
            else:
                super().keyPressEvent(event)
        elif event.key() == Qt.Key_S and event.modifiers() & Qt.ControlModifier:
            self.save()
        elif event.key() == Qt.Key_L and event.modifiers() & Qt.ControlModifier:
            self.grScene.scene.loadFromFlie('graph.json')
        else:
            super().keyPressEvent(event)
    def save(self):
        self.grScene.scene.saveToFile('graph.json')
    def deleteSelected(self):
        for item in self.grScene.selectedItems():
            if isinstance(item, QDMGraphicsEdge):
                item.edge.remove()
            elif hasattr(item, 'node'):
                item.node.remove()

    def changeFont(self):

        self.item._title_font= QFont("Ubuntu", self.sp.value())
        self.item.initTitle()
    def Valuechange(self):
        # 显示当前计数器地数值
        self.l1.setText('当前字体大小:' + str(self.sp.value()))
    def spinBoxAppear(self):
        vbox = QVBoxLayout()
        vbox.addWidget(self.l1)
        vbox.addWidget(self.sp)
        vbox.addWidget(self.btn1)
        self.dialog.setLayout(vbox)
        self.sp.valueChanged.connect(self.Valuechange)
        self.btn1.clicked.connect(lambda :self.changeFont())
        self.dialog.exec_()

