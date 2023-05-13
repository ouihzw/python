# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class QDMGraphicsEdge(QGraphicsPathItem):
    def __init__(self, edge, parent=None):
        super().__init__(parent)

        self.edge = edge

        self._color = QColor("#555555")
        self._color_selected = QColor("#f29022")
        self._pen = QPen(self._color)
        self._pen_selected = QPen(self._color_selected)
        self._pen.setWidth(2.0)
        self._pen_selected.setWidth(2.0)
        self._pen_dragging = QPen(self._color)
        self._pen_dragging.setStyle(Qt.DashLine)
        self._pen_dragging.setWidth(2.0)

        self.setFlag(QGraphicsItem.ItemIsSelectable)

        self.setZValue(-1)

        self.posSource = [0, 0]
        self.posDestination = [200, 100]
        self.posSourceindex = 0
        self.posDestinationindex = 0

    def paint(self, painter, QStyleOptionGraphicsItem, widge=None):
        self.updatePath()

        if self.edge.end_socket is None:
            painter.setPen(self._pen_dragging)
        else:
            painter.setPen(self._pen if not self.isSelected() else self._pen_selected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(self.path())

    def updatePath(self):
        # 画一条A指向B的线
        raise NotImplemented("This method has to be overriden in a child class")

class QDMGraphicsEdgeDirect(QDMGraphicsEdge):
    def updatePath(self):

        # self.length
        self.Sourceway = 0
        self.Destinationway = 0
        self.SourcetoDestinationX = 0
        self.SourcetoDestinationY = 0
        if self.posSource[0] > self.posDestination[0]:
            self.SourcetoDestinationX = -1
        if self.posSource[0] < self.posDestination[0]:
            self.SourcetoDestinationX = 1
        if self.posSource[1] > self.posDestination[1]:
            self.SourcetoDestinationY = -2
        if self.posSource[1] < self.posDestination[1]:
            self.SourcetoDestinationY = 2

        if self.posDestinationindex == 1:
            self.Destinationway = -2
        if self.posDestinationindex == 2:
            self.Destinationway = 1
        if self.posDestinationindex == 3:
            self.Destinationway = 2
        if self.posDestinationindex == 4:
            self.Destinationway = -1

        path = QPainterPath(QPointF(self.posSource[0], self.posSource[1]))


        if self.posSourceindex == 1:
            path.lineTo(self.posSource[0], self.posSource[1] - 16)
            self.Sourceway = -2
        if self.posSourceindex == 2:
            path.lineTo(self.posSource[0] + 16, self.posSource[1])
            self.Sourceway = 1
        if self.posSourceindex == 3:
            path.lineTo(self.posSource[0], self.posSource[1] + 16)
            self.Sourceway = 2
        if self.posSourceindex == 4:
            path.lineTo(self.posSource[0] - 16, self.posSource[1])
            self.Sourceway = -1

        ##index1
        if self.Sourceway == -2:
            if self.SourcetoDestinationY == -2:
                if self.SourcetoDestinationX == 1:
                    if self.posDestinationindex == 1:
                        path.lineTo(self.posSource[0], self.posDestination[1] - 16)
                        path.lineTo(self.posDestination[0], self.posDestination[1] - 16)
                    if self.posDestinationindex == 3:
                        path.lineTo(self.posDestination[0], self.posSource[1] - 16)
                        path.lineTo(self.posDestination[0], self.posDestination[1] + 16)
                    if self.posDestinationindex == 2:
                        path.lineTo(self.posDestination[0] + 16, self.posSource[1] - 16)
                        path.lineTo(self.posDestination[0] + 16, self.posDestination[1])
                    if self.posDestinationindex == 4:
                        path.lineTo(self.posSource[0], self.posDestination[1])
                        path.lineTo(self.posDestination[0] - 16, self.posDestination[1])
                if self.SourcetoDestinationX == -1:
                    if self.posDestinationindex == 1:
                        path.lineTo(self.posSource[0], self.posDestination[1] - 16)
                        path.lineTo(self.posDestination[0], self.posDestination[1] - 16)
                    if self.posDestinationindex == 3:
                        path.lineTo(self.posDestination[0], self.posSource[1] - 16)
                        path.lineTo(self.posDestination[0], self.posDestination[1] + 16)
                    if self.posDestinationindex == 2:
                        path.lineTo(self.posSource[0], self.posDestination[1])
                        path.lineTo(self.posDestination[0] + 16, self.posDestination[1])
                    if self.posDestinationindex == 4:
                        path.lineTo(self.posDestination[0] - 16, self.posSource[1] - 16)
                        path.lineTo(self.posDestination[0] - 16, self.posDestination[1])
            if self.SourcetoDestinationY == 2:
                if self.Destinationway == -2:
                    path.lineTo(self.posDestination[0], self.posSource[1] - 16)
                    path.lineTo(self.posDestination[0], self.posDestination[1] - 16)
                if self.Destinationway == 2:
                    path.lineTo((self.posSource[0] + self.posDestination[0]) / 2, self.posSource[1] - 16)
                    path.lineTo((self.posSource[0] + self.posDestination[0]) / 2, self.posDestination[1]+16)
                    path.lineTo(self.posDestination[0], self.posDestination[1]+16)
                if self.Destinationway == 1:
                    path.lineTo(self.posDestination[0] + 16, self.posSource[1] - 16)
                    path.lineTo(self.posDestination[0] + 16, self.posDestination[1])
                if self.Destinationway == -1:
                    path.lineTo(self.posDestination[0] - 16, self.posSource[1] - 16)
                    path.lineTo(self.posDestination[0] - 16, self.posDestination[1])
        ##index3
        if self.Sourceway == 2:
            if self.SourcetoDestinationY == 2:
                if self.SourcetoDestinationX == 1:
                    if self.posDestinationindex == 3:
                        path.lineTo(self.posSource[0], self.posDestination[1] + 16)
                        path.lineTo(self.posDestination[0], self.posDestination[1] + 16)
                    if self.posDestinationindex == 2:
                        path.lineTo(self.posDestination[0] + 16, self.posSource[1] + 16)
                        path.lineTo(self.posDestination[0] + 16, self.posDestination[1])
                    if self.posDestinationindex == 1:
                        path.lineTo(self.posDestination[0], self.posSource[1] + 16)
                        path.lineTo(self.posDestination[0] , self.posDestination[1]-16)
                    if self.posDestinationindex == 4:
                        path.lineTo(self.posSource[0], self.posDestination[1])
                        path.lineTo(self.posDestination[0] - 16, self.posDestination[1])
                if self.SourcetoDestinationX == -1:
                    if self.posDestinationindex == 1:
                        path.lineTo(self.posDestination[0], self.posSource[1] + 16)
                        path.lineTo(self.posDestination[0], self.posDestination[1] - 16)
                    if self.posDestinationindex == 3:
                        path.lineTo(self.posSource[0], self.posDestination[1] + 16)
                        path.lineTo(self.posDestination[0], self.posDestination[1] + 16)
                    if self.posDestinationindex == 2:
                        path.lineTo(self.posSource[0], self.posDestination[1])
                        path.lineTo(self.posDestination[0] - 16, self.posDestination[1])
                    if self.posDestinationindex == 4:
                        path.lineTo(self.posDestination[0] - 16, self.posSource[1] + 16)
                        path.lineTo(self.posDestination[0] - 16, self.posDestination[1])
            if self.SourcetoDestinationY == -2:
                if self.Destinationway == 2:
                    path.lineTo(self.posDestination[0], self.posSource[1] + 16)
                    path.lineTo(self.posDestination[0], self.posDestination[1] + 16)
                if self.Destinationway == -2:
                    path.lineTo((self.posSource[0] + self.posDestination[0]) / 2, self.posSource[1] + 16)
                    path.lineTo((self.posSource[0] + self.posDestination[0]) / 2, self.posDestination[1]-16)
                    path.lineTo(self.posDestination[0], self.posDestination[1]-16)
                if self.Destinationway == 1:
                    path.lineTo(self.posDestination[0] + 16, self.posSource[1] + 16)
                    path.lineTo(self.posDestination[0] + 16, self.posDestination[1])
                if self.Destinationway == -1:
                    path.lineTo(self.posDestination[0] - 16, self.posSource[1] + 16)
                    path.lineTo(self.posDestination[0] - 16, self.posDestination[1])
        ##index2
        if self.Sourceway == 1:
            if self.SourcetoDestinationX == 1:
                if self.SourcetoDestinationY == 2:
                    if self.posDestinationindex == 2:
                        path.lineTo(self.posDestination[0] + 16, self.posSource[1])
                        path.lineTo(self.posDestination[0] + 16, self.posDestination[1])
                    if self.posDestinationindex == 4:
                        path.lineTo(self.posSource[0] + 16, self.posDestination[1])
                        path.lineTo(self.posDestination[0] - 16, self.posDestination[1])
                    if self.posDestinationindex == 3:
                        path.lineTo(self.posSource[0] + 16,self.posDestination[1] + 16 )
                        path.lineTo( self.posDestination[0],self.posDestination[1] + 16)
                    if self.posDestinationindex == 1:
                        path.lineTo(self.posDestination[0],self.posSource[1] )
                        path.lineTo(self.posDestination[0],self.posDestination[1] + 16 )
                if self.SourcetoDestinationY == -2:
                    if self.posDestinationindex == 2:
                        path.lineTo(self.posDestination[0] + 16,self.posSource[1])
                        path.lineTo(self.posDestination[0] + 16,self.posDestination[1] )
                    if self.posDestinationindex == 4:
                        path.lineTo(self.posSource[0] + 16,self.posDestination[1] )
                        path.lineTo(self.posDestination[0] - 16,self.posDestination[1])
                    if self.posDestinationindex == 3:
                        path.lineTo(self.posDestination[0],self.posSource[1] )
                        path.lineTo(self.posDestination[0],self.posDestination[1] - 16 )
                    if self.posDestinationindex == 1:
                        path.lineTo(self.posSource[0] + 16,self.posDestination[1] - 16 )
                        path.lineTo(self.posDestination[0],self.posDestination[1] - 16 )
            if self.SourcetoDestinationX == -1:
                if self.Destinationway == 1:
                    path.lineTo(self.posSource[0] + 16,self.posDestination[1])
                    path.lineTo( self.posDestination[0] + 16,self.posDestination[1])
                if self.Destinationway == -1:
                    path.lineTo(self.posSource[0] + 16,(self.posSource[1] + self.posDestination[1]) / 2)
                    path.lineTo(self.posDestination[0]-16,(self.posSource[1] + self.posDestination[1]) / 2 )
                    path.lineTo(self.posDestination[0]-16,self.posDestination[1] )
                if self.Destinationway == -2:
                    path.lineTo(self.posSource[0] + 16,self.posDestination[1] - 16 )
                    path.lineTo(self.posDestination[0],self.posDestination[1] - 16 )
                if self.Destinationway == 2:
                    path.lineTo(self.posSource[0] + 16,self.posDestination[1] + 16 )
                    path.lineTo(self.posDestination[0],self.posDestination[1] + 16)
        ##index4
        if self.Sourceway == -1:
            if self.SourcetoDestinationX == -1:
                if self.SourcetoDestinationY == -2:
                    if self.posDestinationindex == 4:
                        path.lineTo(self.posDestination[0] - 16, self.posSource[1])
                        path.lineTo(self.posDestination[0] - 16, self.posDestination[1])
                    if self.posDestinationindex == 2:
                        path.lineTo(self.posSource[0] - 16, self.posDestination[1])
                        path.lineTo(self.posDestination[0] + 16, self.posDestination[1])
                    if self.posDestinationindex == 1:
                        path.lineTo(self.posSource[0] - 16, self.posDestination[1] - 16)
                        path.lineTo(self.posDestination[0], self.posDestination[1] - 16)
                    if self.posDestinationindex == 3:
                        path.lineTo(self.posDestination[0], self.posSource[1])
                        path.lineTo(self.posDestination[0], self.posDestination[1] - 16)
                if self.SourcetoDestinationY == 2:
                    if self.posDestinationindex == 4:
                        path.lineTo(self.posDestination[0] - 16, self.posSource[1])
                        path.lineTo(self.posDestination[0] - 16, self.posDestination[1])
                    if self.posDestinationindex == 2:
                        path.lineTo(self.posSource[0] - 16, self.posDestination[1])
                        path.lineTo(self.posDestination[0] + 16, self.posDestination[1])
                    if self.posDestinationindex == 1:
                        path.lineTo(self.posDestination[0], self.posSource[1])
                        path.lineTo(self.posDestination[0], self.posDestination[1] + 16)
                    if self.posDestinationindex == 3:
                        path.lineTo(self.posSource[0] - 16, self.posDestination[1] + 16)
                        path.lineTo(self.posDestination[0], self.posDestination[1] + 16)
            if self.SourcetoDestinationX == 1:
                if self.Destinationway == -1:
                    path.lineTo(self.posSource[0] - 16, self.posDestination[1])
                    path.lineTo(self.posDestination[0] - 16, self.posDestination[1])
                if self.Destinationway == 1:
                    path.lineTo(self.posSource[0] - 16, (self.posSource[1] + self.posDestination[1]) / 2)
                    path.lineTo(self.posDestination[0] + 16, (self.posSource[1] + self.posDestination[1]) / 2)
                    path.lineTo(self.posDestination[0] + 16, self.posDestination[1])
                if self.Destinationway == 2:
                    path.lineTo(self.posSource[0] - 16, self.posDestination[1] + 16)
                    path.lineTo(self.posDestination[0], self.posDestination[1] + 16)
                if self.Destinationway == -2:
                    path.lineTo(self.posSource[0] - 16, self.posDestination[1] - 16)
                    path.lineTo(self.posDestination[0], self.posDestination[1] - 16)

        ##画箭头
        if self.Destinationway == 1:
            path.lineTo(self.posDestination[0], self.posDestination[1])
            path.lineTo(self.posDestination[0] + 10, self.posDestination[1] -10)
            path.lineTo(self.posDestination[0], self.posDestination[1])
            path.lineTo(self.posDestination[0] + 10, self.posDestination[1] + 10)
        if self.Destinationway == 2:
            path.lineTo(self.posDestination[0], self.posDestination[1])
            path.lineTo(self.posDestination[0] - 10, self.posDestination[1] + 10)
            path.lineTo(self.posDestination[0], self.posDestination[1])
            path.lineTo(self.posDestination[0] + 10, self.posDestination[1] + 10)
        if self.Destinationway == -1:
            path.lineTo(self.posDestination[0], self.posDestination[1])
            path.lineTo(self.posDestination[0] - 10, self.posDestination[1] -10)
            path.lineTo(self.posDestination[0], self.posDestination[1])
            path.lineTo(self.posDestination[0] - 10, self.posDestination[1] + 10)
        if self.Destinationway == -2:
            path.lineTo(self.posDestination[0], self.posDestination[1])
            path.lineTo(self.posDestination[0] - 10, self.posDestination[1] - 10)
            path.lineTo(self.posDestination[0], self.posDestination[1])
            path.lineTo(self.posDestination[0] + 10, self.posDestination[1] - 10)
        if self.Destinationway == 0:
            ##当前终点并非index
            if self.posSourceindex==2 or self.posSourceindex==4:
                path.lineTo(self.posDestination[0],self.posSource[1])
                path.lineTo(self.posDestination[0], self.posDestination[1])
            elif self.posSourceindex==1 or self.posSourceindex==3:
                path.lineTo(self.posSource[0], self.posDestination[1])
                path.lineTo(self.posDestination[0], self.posDestination[1])
        self.setPath(path)
    def setSource(self, x, y):
        self.posSource = [x, y]

    def setDestination(self,x ,y):
        self.posDestination = [x,y]
    def getSourceindex (self,x):
        self.posSourceindex = x

    def getDestinationindex (self,x):
        self.posDestinationindex = x
