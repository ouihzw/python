# -*- coding:utf-8-*-
import json
from com.mat.rpa.views.workWindow.middlePanel.middleWindow.node_edge import Edge

from com.mat.rpa.views.workWindow.middlePanel.middleWindow.node_serializable import Serializable
import json
from collections import OrderedDict
from com.mat.rpa.dao.appDataDao import appDataDao
from middleWindow.node_graphics_scene import QDMGraphicsScene
from middleWindow.node_node import Node, BeginNode, EndNode


class Scene(Serializable):
    def __init__(self):
        super().__init__()
        self.nodes = []
        self.edges = []

        self.scene_width, self.scene_height = 64000, 64000
        self.initUI()
        self.startNode=None
        self.endNode=[]
        self.currentNode=None
        self.currentSocket=None
        self.appDataDao = appDataDao.appDataDao()
    def initUI(self):
        self.grScene = QDMGraphicsScene(self)
        self.grScene.setGrScene(self.scene_width,self.scene_height)

    def addNode(self,node):
        self.nodes.append(node)

    def addEdge(self,edge):
        self.edges.append(edge)

    def removeNode(self,node):
        self.nodes.remove(node)

    def removeEdge(self, edge):
        self.edges.remove(edge)

    def serialize(self):
        nodes, edges = [],[]
        for node in self.nodes:
            nodes.append(node.serialize())
        for edge in self.edges:
            edges.append(edge.serialize())
        return OrderedDict([
            ('id',self.id),
            ('scene_width',self.scene_width),
            ('scene_height',self.scene_height),
            ('nodes',nodes),
            ('edges',edges),
        ])

    def deserialize(self, data, hashmap={}):
        print('解码数据', data)

        self.clear()
        hashmap = {}

        # 创建nodes
        for node_data in data['nodes']:
            if node_data['node_type']==1:
                Node(self).deserialize(node_data, hashmap)
            elif node_data['node_type']==4:
                BeginNode(self).deserialize(node_data, hashmap)
            elif node_data['node_type']==5:
                EndNode(self).deserialize(node_data, hashmap)
        # 创建edges
        for edge_data in data['edges']:
            Edge(self).deserialize(edge_data, hashmap)
        return True

    def saveToFile(self, filename):
        with open(filename, 'w') as file:
            file.write(json.dumps(self.serialize(), indent=4, ensure_ascii=False))
        print(filename, "保存成功")

    def saveToMongo(self,id):
        dict = self.serialize()
        dict["robotId"] = id
        data = self.appDataDao.getOneByAppid(id)
        if data == None:
            self.appDataDao.insert(dict)
        else:
            self.appDataDao.update(data, dict)

    def loadFromFlie(self, filename):
        with open(filename, 'r') as file:
            raw_data = file.read()
            data = json.loads(raw_data)
            self.deserialize(data)

    def loadFromMongo(self, id):
        data = self.appDataDao.getOneByAppid(id)
        if data != None:
            self.deserialize(data)

    def clear(self):
        while len(self.nodes) > 0:
            self.nodes[0].remove()

    def run(self):
        self.endNode = []
        boolStart = True
        boolEnd = True
        for node in self.nodes:
            if node.type == "startDirective":
                self.startNode = node
                boolStart = False
                print("找到开始控件")
            if node.type == "endDirective" or node.type == "quittingFlowDirective":
                self.endNode.append(node)
                boolEnd = False
                print("找到结束控件")
        if boolStart or boolEnd:
            print("开始或结束控件不全")
            return False
        self.currentNode = self.startNode.getNextNode()

        while self.currentNode not in self.endNode and self.currentNode:
            self.currentNode.dialog.executeStep()
            print("当前运行节点：" + self.currentNode.title)
            self.currentNode = self.currentNode.getNextNode()
        print("运行结束")
        return True

