from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from com.mat.rpa.views.workWindow.middlePanel.middleWindow.node_graphics_view import MODE_EDGE_DRAG


class QMGraphicsLozeNode(QGraphicsItem):
    def __init__(self, node, title='Node Graphics Item', parent=None):
        super().__init__(parent)
        self.node = node
        self._title_color = Qt.black
        self._title_font = QFont("Ubuntu", 10)

        self.title_item = QGraphicsTextItem(self)
        self.width = 180
        self.height = 100
        self.edge_size = 10
        self.title_height = 24
        self._padding = 4.0

        self.initTitle()
        self.title = title
        self._pen_default = QPen(QColor("#7f000000"))
        self._pen_selected = QPen(QColor("#ffffa637"))

        self._brush_title = QBrush(QColor("#ff313131"))
        self._brush_background = QBrush(QColor("#f79a43"))
        self.sizer = HandleItem(self)
        self.sizer.setPos(self.width, self.height)
        self.sizer.posChangeCallbacks.append(self.changeSize)  # Connect the callback

        # self.sizer.setVisible(False)
        self.sizer.setFlag(self.sizer.ItemIsSelectable, True)

        self.initUI()

    def boundingRect(self):
        return QRectF(0, 0, 2 * self.edge_size + self.width, 2 * self.edge_size + self.height
                      ).normalized()

    def initUI(self):
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)

    def initTitle(self):

        self.title_item.setDefaultTextColor(self._title_color)
        self.title_item.setFont(self._title_font)
        self.title_item.setPos(self._padding, 0)
        self.title_item.setTextWidth(
            self.width - 2 * self._padding
        )
        self.title_item.node = self.node

    def changeTitle(self):
        self.node
        return

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value
        self.title_item.setPlainText(self._title)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        # outline
        path_outline = QPainterPath()
        path_outline.addRoundedRect(0, 0, self.width, self.height, self.edge_size, self.edge_size)
        painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path_outline.simplified())
        # title
        path_title = QPainterPath()
        point1 = QPoint(0, self.height / 2)  # 点坐标一
        point2 = QPoint(self.width / 2, 0)  # 点坐标二
        point3 = QPoint(self.width, self.height / 2)  # 点坐标三
        point4 = QPoint(self.width / 2, self.height)  # 点坐标四
        path_title.setFillRule(Qt.WindingFill)
        polygon = QPolygon([point1, point2, point3, point4])  # 四个点坐标
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_background)
        painter.drawPolygon(polygon)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)

        # 更新被选择NODE的EAGE
        for node in self.scene().scene.nodes:
            if node.grNode.isSelected():
                node.updateConnectedEdges()

    def changeSize(self, w, h):
        """ Resize block function """
        # Limit the block size:
        if h < 30:
            h = 30
        if w < 50:
            w = 50
        self.width = w
        self.height = h
        for node in self.scene().scene.nodes:
            node.updateConnectedEdges()
            node.updateConnectedSockets()


class QMGraphicsNode(QGraphicsItem):
    def __init__(self, node, title='Node Graphics Item', parent=None):
        super().__init__(parent)
        self.node = node
        self._title_color = Qt.black
        self._title_font = QFont("Ubuntu", 10)

        self.title_item = QGraphicsTextItem(self)
        self.width = 180
        self.height = 100
        self.edge_size = 10
        self.title_height = 24
        self._padding = 4.0

        self.initTitle()
        self.title = title
        self._pen_default = QPen(QColor("#7f000000"))
        self._pen_selected = QPen(QColor("#ffffa637"))

        self._brush_title = QBrush(QColor("#ff313131"))
        self._brush_background = QBrush(QColor("#4ac1f1"))
        self.sizer = HandleItem(self)
        self.sizer.setPos(self.width, self.height)
        self.sizer.posChangeCallbacks.append(self.changeSize)  # Connect the callback
        # self.sizer.setVisible(False)
        self.sizer.setFlag(self.sizer.ItemIsSelectable, True)
        self.initUI()

    def boundingRect(self):
        return QRectF(0, 0, 2 * self.edge_size + self.width, 2 * self.edge_size + self.height
                      ).normalized()

    def initUI(self):
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)

    def initTitle(self):
        self.title_item.setDefaultTextColor(self._title_color)
        self.title_item.setFont(self._title_font)
        self.title_item.setPos(self._padding, 0)
        self.title_item.setTextWidth(
            self.width - 2 * self._padding
        )

        self.title_item.node = self.node

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value
        self.title_item.setPlainText(self._title)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        # outline
        path_outline = QPainterPath()
        path_outline.addRoundedRect(0, 0, self.width, self.height, self.edge_size, self.edge_size)
        painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path_outline.simplified())
        # title
        path_title = QPainterPath()
        path_title.setFillRule(Qt.WindingFill)
        path_title.addRoundedRect(0, 0, self.width, self.title_height, self.edge_size, self.edge_size)
        path_title.addRect(0, self.title_height - self.edge_size, self.edge_size, self.edge_size)
        path_title.addRect(self.width - self.edge_size, self.title_height - self.edge_size, self.edge_size,
                           self.edge_size)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_background)
        painter.drawPath(path_title.simplified())
        # content
        path_content = QPainterPath()
        path_content.setFillRule(Qt.WindingFill)
        path_content.addRoundedRect(0, self.title_height, self.width, self.height - self.title_height, self.edge_size,
                                    self.edge_size)
        path_content.addRect(0, self.title_height, self.edge_size, self.edge_size)
        path_content.addRect(self.width - self.edge_size, self.title_height, self.edge_size, self.edge_size)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_background)
        painter.drawPath(path_content.simplified())

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)

        # 更新被选择NODE的EAGE
        for node in self.scene().scene.nodes:
            if node.grNode.isSelected():
                node.updateConnectedEdges()

    def changeSize(self, w, h):
        """ Resize block function """
        # Limit the block size:
        if h < 30:
            h = 30
        if w < 50:
            w = 50
        self.width = w
        self.height = h
        for node in self.scene().scene.nodes:
            node.updateConnectedEdges()
            node.updateConnectedSockets()


class QMGraphicsParaNode(QGraphicsItem):
    def __init__(self, node, title='Node Graphics Item', parent=None):
        super().__init__(parent)
        self.node = node
        self._title_color = Qt.black
        self._title_font = QFont("Ubuntu", 10)

        self.title_item = QGraphicsTextItem(self)
        self.width = 180
        self.height = 100
        self.edge_size = 10
        self.title_height = 24
        self._padding = 4.0

        self.initTitle()
        self.title = title

        self._pen_default = QPen(QColor("#7f000000"))
        self._pen_selected = QPen(QColor("#ffffa637"))

        self._brush_title = QBrush(QColor("#ff313131"))
        self._brush_background = QBrush(QColor("#40c001"))
        self.sizer = HandleItem(self)
        self.sizer.setPos(self.width, self.height)
        self.sizer.posChangeCallbacks.append(self.changeSize)  # Connect the callback
        # self.sizer.setVisible(False)
        self.sizer.setFlag(self.sizer.ItemIsSelectable, True)
        self.initUI()

    def boundingRect(self):
        return QRectF(0, 0, 2 * self.edge_size + self.width, 2 * self.edge_size + self.height
                      ).normalized()

    def initUI(self):
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)

    def initTitle(self):

        self.title_item.setDefaultTextColor(self._title_color)
        self.title_item.setFont(self._title_font)
        self.title_item.setPos(self._padding, 0)
        self.title_item.setTextWidth(
            self.width - 2 * self._padding
        )

        self.title_item.node = self.node

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value
        self.title_item.setPlainText(self._title)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        # outline
        path_outline = QPainterPath()
        path_outline.addRoundedRect(0, 0, self.width, self.height, self.edge_size, self.edge_size)
        painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path_outline.simplified())
        # title
        path_title = QPainterPath()
        point1 = QPoint(self.width / 4, 0)  # 点坐标一
        point2 = QPoint(self.width, 0)  # 点坐标二
        point3 = QPoint(3 * self.width / 4, self.height)  # 点坐标三
        point4 = QPoint(0, self.height)  # 点坐标四
        path_title.setFillRule(Qt.WindingFill)
        polygon = QPolygon([point1, point2, point3, point4])  # 四个点坐标
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_background)
        painter.drawPolygon(polygon)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)

        # 更新被选择NODE的EAGE
        for node in self.scene().scene.nodes:
            if node.grNode.isSelected():
                node.updateConnectedEdges()

    def changeSize(self, w, h):
        """ Resize block function """
        # Limit the block size:
        if h < 30:
            h = 30
        if w < 50:
            w = 50
        self.width = w
        self.height = h
        for node in self.scene().scene.nodes:
            node.updateConnectedEdges()
            node.updateConnectedSockets()


class HandleItem(QGraphicsEllipseItem):
    """ A handle that can be moved by the mouse """

    def __init__(self, parent=None):
        super(HandleItem, self).__init__(QRectF(-4.0, -4.0, 8.0, 8.0), parent)
        self.posChangeCallbacks = []
        self.setBrush(QBrush(Qt.white))
        self.setFlag(self.ItemIsMovable, True)
        self.setFlag(self.ItemSendsScenePositionChanges, True)
        self.setCursor(QCursor(Qt.SizeFDiagCursor))

    def itemChange(self, change, value):
        if change == self.ItemPositionChange:
            x, y = value.x(), value.y()
            # TODO: make this a signal?
            # This cannot be a signal because this is not a QObject
            for cb in self.posChangeCallbacks:
                res = cb(x, y)
                if res:
                    x, y = res
                    value = QPointF(x, y)
            return value
        # Call superclass method:
        return super(HandleItem, self).itemChange(change, value)


class QMGraphicsBeginNode(QGraphicsItem):
    def __init__(self, node, title='Node Graphics Item', parent=None):
        super().__init__(parent)
        self.node = node
        self._title_color = Qt.black
        self._title_font = QFont("Ubuntu", 10)

        self.title_item = QGraphicsTextItem(self)
        self.width = 100
        self.height = 100
        self.edge_size = 10
        self.title_height = 24
        self._padding = 4.0

        self.initTitle()
        self.title = title
        self._pen_default = QPen(QColor("#7f000000"))
        self._pen_selected = QPen(QColor("#ffffa637"))

        self._brush_title = QBrush(QColor("#ff313131"))
        self._brush_background = QBrush(QColor("#b8ccd0"))
        self.sizer = HandleItem(self)
        self.sizer.setPos(self.width, self.height)
        self.sizer.posChangeCallbacks.append(self.changeSize)  # Connect the callback
        # self.sizer.setVisible(False)
        self.sizer.setFlag(self.sizer.ItemIsSelectable, True)

        self.initUI()

    def boundingRect(self):
        return QRectF(0, 0, 2 * self.edge_size + self.width, 2 * self.edge_size + self.height
                      ).normalized()

    def initUI(self):
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)

    def initTitle(self):

        self.title_item.setDefaultTextColor(self._title_color)
        self.title_item.setFont(self._title_font)
        self.title_item.setPos(self._padding, 0)
        self.title_item.setTextWidth(
            self.width - 2 * self._padding
        )
        self.title_item.node = self.node

    def changeTitle(self):
        self.node
        return

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value
        self.title_item.setPlainText(self._title)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        # outline
        path_outline = QPainterPath()
        path_outline.addRoundedRect(0, 0, self.width, self.height, self.edge_size, self.edge_size)
        painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path_outline.simplified())
        # title
        path_title = QPainterPath()
        point1 = QPoint(self.width / 4, 0)  # 点坐标1
        point2 = QPoint(3 * self.width / 4, 0)  # 点坐标2
        point3 = QPoint(self.width / 4, self.height)  # 点坐标3
        point4 = QPoint(3 * self.width / 4, self.height)  # 点坐标4

        path_title.setFillRule(Qt.WindingFill)

        polygon = QPolygon([point1, point2, point4, point3])  # 四个点坐标
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_background)
        painter.drawPolygon(polygon)
        painter.drawEllipse(0, 0, self.width / 2, self.height)
        painter.drawEllipse(self.width / 2, 0, self.width / 2, self.height)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)

        # 更新被选择NODE的EAGE
        for node in self.scene().scene.nodes:
            if node.grNode.isSelected():
                node.updateConnectedEdges()

    def changeSize(self, w, h):
        """ Resize block function """
        # Limit the block size:
        if h < 30:
            h = 30
        if w < 50:
            w = 50
        self.width = w
        self.height = h
        for node in self.scene().scene.nodes:
            node.updateConnectedEdges()
            node.updateConnectedSockets()
