# -*- coding:utf-8 -*-
from com.mat.rpa.views.workWindow.middlePanel.middleWindow.node_graphics_edge import *
from com.mat.rpa.views.workWindow.middlePanel.middleWindow.node_serializable import Serializable
from collections import OrderedDict
EDGE_TYPE_DIRECT = 1
EDGE_TYPE_BEZIER = 2

class Edge(Serializable):
    def __init__(self, scene, start_socket=None,end_socket=None,edge_type=1):
        super().__init__()

        self.scene = scene

        self.start_socket = start_socket
        self.end_socket = end_socket
        self.edge_type = edge_type

        self.scene.addEdge(self)


    @property
    def start_socket(self):
        return self._start_socket

    @start_socket.setter
    def start_socket(self, value):
        self._start_socket = value
        if self.start_socket is not None:
            self.start_socket.edge = self

    @property
    def end_socket(self):
        return self._end_socket

    @end_socket.setter
    def end_socket(self, value):
        self._end_socket = value
        if self.end_socket is not None:
            self.end_socket.edge = self

    @property
    def edge_type(self):
        return self._edge_type

    @edge_type.setter
    def edge_type(self, value):
        if hasattr(self,'grEdge') and self.grEdge is not None:
            self.scene.grScene.removeItem(self.grEdge)
        self._edge_type = 1
        if self.edge_type == 1:
            self.grEdge = QDMGraphicsEdgeDirect(self)
        self.scene.grScene.addItem(self.grEdge)
        if self.start_socket is not None:
            self.updatePosition()

    def updatePosition(self):
        source_pos = self.start_socket.getSocketPosition()
        a=self.start_socket.getindex()
        source_pos[0] += self.start_socket.node.grNode.pos().x()
        source_pos[1] += self.start_socket.node.grNode.pos().y()
        self.grEdge.getSourceindex(a)
        self.grEdge.setSource(*source_pos)
        if self.end_socket is not None:
            b=self.end_socket.getindex()
            end_pos = self.end_socket.getSocketPosition()
            end_pos[0] += self.end_socket.node.grNode.pos().x()
            end_pos[1] += self.end_socket.node.grNode.pos().y()
            self.grEdge.getDestinationindex(b)
            self.grEdge.setDestination(*end_pos)
        else:
            self.grEdge.getDestinationindex(0)
            self.grEdge.setDestination(*source_pos)
        self.grEdge.update()

    def remove_from_socket(self):
        if self.start_socket is not None:
            self.start_socket.edge = None
        if self.end_socket is not None:
            self.end_socket.edge = None
        self.start_socket=None
        self.end_socket=None
    def remove(self):
        self.remove_from_socket()
        self.scene.grScene.removeItem(self.grEdge)
        self.grEdge = None
        self.scene.removeEdge(self)


    def serialize(self):
        if self.end_socket is not None and self.start_socket is not None:
            return OrderedDict([
                ('id',self.id),
                ('edge_type', self.edge_type),
                ('start_socket', self.start_socket.id),
                ('end_socket', self.end_socket.id),
            ])
        else : return None



    def deserialize(self, data, hashmap={}):
        if data is not None:
            self.id = data['id']
            self.start_socket = hashmap[data['start_socket']]
            self.end_socket = hashmap[data['end_socket']]
            self.edge_type = data['edge_type']
            return True