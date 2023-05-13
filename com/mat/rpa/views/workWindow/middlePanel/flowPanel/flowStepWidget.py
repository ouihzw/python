import sys

from com.mat.rpa.dao.workDao.directiveDao import DirectiveDao
from com.mat.rpa.utils import variable
from com.mat.rpa.views.workWindow.middlePanel.directives.startorend.startorendContants import StartorEndConstants
from com.mat.rpa.views.workWindow.middlePanel.flowPanel import flowSettingDialog
from com.mat.rpa.views.workWindow.middlePanel.middleWindow.node_graphics_node import *
from com.mat.rpa.views.workWindow.middlePanel.middleWindow.node_socket import Socket, LEFT_TOP, RIGHT_BOTTON, LEFT_BOTTON, RIGHT_TOP
from collections import OrderedDict

menuStyleSheet = """
QMenu {
    background-color: #fff;
    padding: 2px;
    font-size: 12px;
    border-radius: 5px;
    border-color: #aaa;
    border-width: 1px;
    border-style: solid;
}
QMenu::item {
    padding: 5px;
    margin: 1px;
    border-radius: 4px;
    min-width: 130px;
    color: #333;
}
QMenu::item:default {
    color: red;
}
QMenu::item:selected {
    background-color: #e0e0e0;
}
QMenu::icon {
    padding-left: 10px;
}
"""
class FlowStepWidget(QFrame):
    picPath = "./com/mat/rpa/views/workWindow/images/"
    def __init__(self, scene, title="Undefined Node", type = " Node ", id = None,inputs=[], outputs=[]):
        super().__init__()
        self.scene = scene
        """
        node_type:
        1--普通矩形
        2--菱形
        3--平行四边形
        4--开始节点
        5--结束节点
        """
        self.node_type = 1
        self.type = type
        self._title = title

        # 确定节点的图形
        self.grNode = QMGraphicsNode(self)
        self.title = title
        self.scene.addNode(self)

        self.inputs = []
        self.outputs = []
        self._inputs = inputs
        self._outputs = outputs
        self.socket_spacing = 22
        self.directiveDaoObj = DirectiveDao()
        # 流程编辑区域所对应的flow文件的id
        self.id = id
        self.directive = {"command": "",
                          "line_number": "",
                          "flow_title": "",
                          "data": {},
                          "comment": "",
                          "target": "",
                          "targets": [],
                          "value": ""
                          }
        self.dialog = None
        self.infoFormat = None

        # 用于更新指令信息第二行的函数
    def updateSecondLineInfo(self, info: tuple = ()):
        html = '<p style="color: #666;">' + self.infoFormat + '</p>'
        elements = []
        for item in info:
            text = variable.parseVariable(item)
            if text is not None:
                if text == "":
                    elements.append('<span style="color: #0f7af4;">' + text + '</span>')
                else:
                    elements.append('<span style="color: #0f7af4; background-color: #e0f0ff"> ' + text + ' </span>')
            else:
                elements.append('<span style="color: #0f7af4;">' + item + '</span>')
        if len(info) > 0:
            self.setgrNodeTip(html % tuple(elements))
        else:
            self.setgrNodeTip(html)

    def setgrNodeTip(self, tooltip):
        self.grNode.setToolTip(tooltip)

    def addSockets(self):
        counter = 1
        if self.type == StartorEndConstants.startDirective:
            counter = 3

        for item in self._inputs:
            socket = Socket(node=self, index=counter, position=LEFT_TOP)
            counter += 1
            self.inputs.append(socket)

        counter = 1

        for item in self._outputs:
            socket = Socket(node=self, index=counter, position=RIGHT_BOTTON)
            counter += 1
            self.outputs.append(socket)

    def setgrNode(self):
        self.scene.grScene.addItem(self.grNode)
        self.title = self._title

    def getNextNode(self):
        for edge in self.scene.edges:
            if edge.start_socket is not None and edge.end_socket is not None:
                if edge.start_socket.node == self:
                    return edge.end_socket.node
        return None

    def getSocketPosition(self, index, position):
        if index == 4:
            x = 0
            y = self.grNode.height / 2
        elif index == 2:
            x = self.grNode.width
            y = self.grNode.height / 2
        elif index == 1:
            x = self.grNode.width / 2
            y = 0
        elif index == 3:
            x = self.grNode.width / 2
            y = self.grNode.height
        return [x, y]

    def updateDirectiveData2DB(self, directive_id, data: dict):
        self.directiveDaoObj.updateDirective(directive_id, {"data": data})

    @property
    def pos(self):
        return self.grNode.pos()

    def setPos(self, x, y):
        self.grNode.setPos(x, y)

    def setNode_Type(self,a):
        self.node_type=a

    def updateConnectedEdges(self):
        for socket in self.inputs + self.outputs:
            if socket.hasEdge():
                socket.edge.updatePosition()

    def updateConnectedSockets(self):
        for socket in self.inputs + self.outputs:
            socket.update()

    def remove(self):
        for socket in (self.inputs+self.outputs):
            if socket.hasEdge():
                socket.edge.remove()
        self.scene.grScene.removeItem(self.grNode)
        self.grNode = None
        self.scene.removeNode(self)

    def serialize(self):
        inputs, outputs = [], []
        for socket in self.inputs:
            inputs.append(socket.serialize())
        for socket in self.outputs:
            outputs.append(socket.serialize())
        dialog=self.dialog.serialize()
        return OrderedDict([
            ('id', self.id),
            ('title', self.title),
            ('node_type',self.node_type),
            ('type',self.type),
            ('pos_x', self.grNode.scenePos().x()),
            ('pos_y', self.grNode.scenePos().y()),
            ('inputs', inputs),
            ('outputs', outputs),
            ('dialog',dialog)
        ])

    def deserialize(self, data, hashmap={}):
        self.id = data['id']
        self.node_type = data['node_type']
        hashmap[data['id']] = self
        self.type=data['type']
        self.setPos(data['pos_x'], data['pos_y'])
        self.title = data['title']
        data['inputs'].sort(key=lambda socket: socket['index'] + socket['position'] * 1000)
        data['outputs'].sort(key=lambda socket: socket['index'] + socket['position'] * 1000)
        self.inputs = []
        for socket_data in data['inputs']:
            new_socket = Socket(node=self, index=socket_data['index'], position=socket_data['position'],
                                socket_type=socket_data['socket_type'])
            new_socket.deserialize(socket_data, hashmap)
            self.inputs.append(new_socket)
        self.outputs = []
        for socket_data in data['outputs']:
            new_socket = Socket(node=self, index=socket_data['index'], position=socket_data['position'],
                                socket_type=socket_data['socket_type'])
            new_socket.deserialize(socket_data, hashmap)
            self.outputs.append(new_socket)
        self.setDialog(data['dialog'])
        return True

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value
        self.grNode.title = self._title

    def setDialog(self, data):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = FlowStepWidget(None)
    win.show()
    app.exec_()