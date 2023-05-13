# -*- coding:utf-8 -*-
from com.mat.rpa.views.workWindow.middlePanel.middleWindow.node_graphics_socket import QDMGraphicsSocket
from com.mat.rpa.views.workWindow.middlePanel.middleWindow.node_serializable import Serializable
from collections import OrderedDict
LEFT_TOP = 1
LEFT_BOTTON = 2
RIGHT_TOP = 3
RIGHT_BOTTON = 4

class Socket(Serializable):
    def __init__(self, node, index=1, position=LEFT_TOP,socket_type=None):

        super().__init__()
        self.socket_type=None
        self.node = node
        self.index = index
        self.position = position
        self.edge=None
        self.grSocket = QDMGraphicsSocket(self)
        self.grSocket.setPos(*self.node.getSocketPosition(index, position))
    def getSocketPosition(self):
        return self.node.getSocketPosition(self.index, self.position)
    def setConnectedEdge(self, edge=None):
        self.edge = edge
    def hasEdge(self):
        return self.edge is not None
    def update(self):
        self.grSocket.setPos(*self.node.getSocketPosition(self.index, self.position))
    def getindex(self):
        return self.index
    def serialize(self):
        return OrderedDict([
            ('id',self.id),
            ('index', self.index),
            ('position', self.position),
            ('socket_type', self.socket_type),

        ])

    def deserialize(self, data, hashmap={}):
        self.id = data['id']
        hashmap[data['id']] = self
        return True
    def setsocket_type(self,socket_type):
        self.socket_type=socket_type