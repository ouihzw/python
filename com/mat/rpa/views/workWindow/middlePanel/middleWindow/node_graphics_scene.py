from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import math
from com.mat.rpa.views.workWindow.middlePanel.middleWindow.node_node import Node, BeginNode, EndNode, LozeNode, ParaNode
from com.mat.rpa.utils.node_type_name import *
from com.mat.rpa.views.workWindow.middlePanel.directives import directiveWidgetFactory


class QDMGraphicsScene(QGraphicsScene):
    def __init__(self, scene, parent=None):
        super().__init__(parent)

        self.scene = scene
        # self.setAcceptDrops(True)
        # self.setMouseTracking(True)
        self.id = None
        # setting
        self.gridSize = 10
        self.gridSquares = 3

        self._color_background = QColor("#edeefe")
        self._color_light = QColor("#edeefe")
        self._color_drak = QColor("#edeefe")

        self._pen_light = QPen(self._color_light)
        self._pen_light.setWidth(2)
        self._pen_drak = QPen(self._color_drak)
        self._pen_drak.setWidth(3)
        self.ifconnetable = False

        self.setBackgroundBrush(self._color_background)

    def setGrScene(self, width, height):
        self.setSceneRect(-width // 2, -height // 2, width, height)

    def ifconnetableChange(self):
        if self.ifconnetable == False:
            self.ifconnetable = True
        else:
            self.ifconnetable = False
        return self.ifconnetable

    def dragMoveEvent(self, QGraphicsSceneDragDropEvent):
        QGraphicsSceneDragDropEvent.accept()

    def getType(self):
        return self.ifconnetable

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            self.type = event.mimeData().text().split('|', 2)[1]
            self.title = event.mimeData().text().split('|', 2)[2]
            self.objectName = event.mimeData().objectName()
            if (self.objectName == "leaf") or (self.objectName == "flowStepWidget"):
                event.accept()
            else:
                event.ignore()

    def dropEvent(self, event):
        try:
            res = directiveWidgetFactory.DirectiveWidgetFactory().createDirectiveWidget(self.scene, self.title,
                                                                                        self.type, self.id)
        except Exception as e:
            print(e)
            res = None
        if (res != None):
            print("使用工厂模式创建对象成功")
            res.setgrNode()
            res.addSockets()
            e = event.scenePos()
            res.setPos(e.x() - 80, e.y() - 40)
        else:
            # 网页操作
            if self.type == "clickingWebElementDirective":
                self.addNode(self.title, self.type, event, self.id)
            if self.type == "closingWebPageDirective":
                self.addNode(self.title, self.type, event, self.id)
            if self.type == "fillingInWebInputDirective":
                self.addNode(self.title, self.type, event, self.id)
            if self.type == "gettingOpenWebPageObjectDirective":
                self.addNode(self.title, self.type, event, self.id)
            if self.type == "mouseHoveringOverWebElementDirective":
                self.addNode(self.title, self.type, event, self.id)
            if self.type == "openningWebPageDirective":
                self.addNode(self.title, self.type, event, self.id)
            if self.type == "gettingAllFilteredCookiesDirective":
                self.addNode(self.title, self.type, event, self.id)
            if self.type == "gettingScrollerPositionDirective":
                self.addNode(self.title, self.type, event, self.id)
            if self.type == "gettingSpecifiedCookieInfoDirective":
                self.addNode(self.title, self.type, event, self.id)
            if self.type == "gettingWebComboBoxOption":
                self.addNode(self.title, self.type, event, self.id)
            if self.type == "gettingWebDialogContentDirective":
                self.addNode(self.title, self.type, event, self.id)
            if self.type == "gettingWebElementInfoDirective":
                self.addNode(self.title, self.type, event, self.id)
            if self.type == "gettingWebElementPositionDirective":
                self.addNode(self.title, self.type, event, self.id)
            if self.type == "gettingWebPageInfoDirective":
                self.addNode(self.title, self.type, event, self.id)
            if self.type == "gettingWebRequestResultDirective":
                self.addNode(self.title, self.type, event, self.id)
            if self.type == "massDataGrabbingDirective":
                self.addNode(self.title, self.type, event, self.id)
            if self.type == "startingListeningWebRequestDirective":
                self.addNode(self.title, self.type, event, self.id)
            if self.type == "stoppingListeningWebRequestDirective":
                self.addNode(self.title, self.type, event, self.id)
            if self.type == "webPageScreenshotDirective":
                self.addNode(self.title, self.type, event, self.id)
            # web元素操作
            if self.type == "draggingWebElementDirective":
                self.addNode(self.title, self.type, event, self.id)
            if self.type == "waitingForWebElementDirective":
                self.addNode(self.title, self.type, event, self.id)
            if self.type == "fillingInPasswordWebInputDirective":
                self.addNode(self.title, self.type, event, self.id)
            if self.type == "settingWebComboboxDirective":
                self.addNode(self.title, self.type, event, self.id)
            if self.type == "settingWebCheckBoxDirective":
                self.addNode(self.title, self.type, event, self.id)
            if self.type == "settingWebElementValueDirective":
                self.addNode(self.title, self.type, event, self.id)
            if self.type == "settingWebElementPropertyDirective":
                self.addNode(self.title, self.type, event, self.id)
            if self.type == "gettingWebElementObjectDirective":
                self.addNode(self.title, self.type, event, self.id)
            if self.type == "gettingRelatedWebElementDirective":
                self.addNode(self.title, self.type, event, self.id)
            if self.type == "gettingSimilarWebElementListDirective":
                self.addNode(self.title, self.type, event, self.id)
            # web页面操作
            if self.type == "executingJSDirective":
                self.addNode(self.title, self.type, event, self.id)
            if self.type == "gettingWebPageObjectListDirective":
                self.addNode(self.title, self.type, event, self.id)
            if self.type == "mouseScrollingPageDirective":
                self.addNode(self.title, self.type, event, self.id)
            if self.type == "redirectingToNewWebPageDirective":
                self.addNode(self.title, self.type, event, self.id)
            if self.type == "removingSpecificCookieDirective":
                self.addNode(self.title, self.type, event, self.id)
            if self.type == "settingWebCookieDirective":
                self.addNode(self.title, self.type, event, self.id)
            if self.type == "stoppingLoadingPageDirective":
                self.addNode(self.title, self.type, event, self.id)
            if self.type == "waitingForLoadingPageDirective":
                self.addNode(self.title, self.type, event, self.id)
            # 鼠标键盘（键盘输入；鼠标点击；鼠标滑轮）           0/3
            if self.type == "keyboardInputDirective":
                self.addNode(self.title, self.type, event, self.id)
            if self.type == "mouseClickDirective":
                self.addNode(self.title, self.type, event, self.id)
            if self.type == "scrollingMouseWheelDirective":
                self.addNode(self.title, self.type, event, self.id)
            if self.type == "downloadingFileDirective":
                self.addNode(self.title, self.type, event, self.id)
            # 变量产生
            if self.type == "settingVariableDirective":
                self.addNode(self.title, self.type, event, self.id)

            # winapp自动化
            name_class = NodeName()
            win_type_name = name_class.win_node_name
            for name in win_type_name:
                if self.type == name:
                    self.addNode(self.title, self.type, event, self.id)

            # 子流程
            if self.type == "callingFlowDirective":
                self.addNode(self.title, self.type, event, self.id)

            if self.type == "callingModuleDirective":
                self.addNode(self.title, self.type, event, self.id)

            if self.type == "quittingFlowDirective":
                self.addNode(self.title, self.type, event, self.id)

            # # if条件的用菱形
            if self.type == "ifConditionDirective":
                self.addLozeNode(self.title, self.type, event, self.id)
            if self.type == "forCircleDirective":
                self.addParaNode(self.title, self.type, event, self.id)
            # elif self.type == "ifFileExistsDirective":
            #     self.addLozeNode(self.title, self.type, event)
            # elif self.type == "ifFolderExistsDirective":
            #     self.addLozeNode(self.title, self.type, event)
            # elif self.type == "ifImageExistsDirective":
            #     self.addLozeNode(self.title, self.type, event)
            # elif self.type == "ifMultiConditionDirective":
            #     self.addLozeNode(self.title, self.type, event)
            # elif self.type == "ifTextExistsOnScreenOCRDirective":
            #     self.addLozeNode(self.title, self.type, event)
            # elif self.type == "ifWebElementVisibleDirective":
            #     self.addLozeNode(self.title, self.type, event)
            # elif self.type == "ifWebPageContainDirective":
            #     self.addLozeNode(self.title, self.type, event)
            # elif self.type == "ifWindowContainsDirective":
            #     self.addLozeNode(self.title, self.type, event)
            # elif self.type == "ifWindowExistsDirective":
            #     self.addLozeNode(self.title, self.type, event)
            # elif self.type == "startDirective":
            #     self.addBeginNode(self.title, self.type, event)
            # elif self.type == "endDirective":
            #     self.addEndNode(self.title, self.type, event)
            # # 输入输出用平行四边形
            # elif self.type == "clickingWebElementDirective":
            #     self.addParaNode(self.title, self.type, event)
            # # 其他用矩形
            # else:
            #     self.addNode(self.title, self.type, event)
        event.setDropAction(Qt.MoveAction)
        event.accept()

    def addNode(self, text, directiveType, e, id):
        e = e.scenePos()
        self.node1 = Node(self.scene, text, directiveType, id, inputs=[1, 2, 3, 4], outputs=[])
        self.node1.setPos(e.x() - 80, e.y() - 40)

    def addBeginNode(self, text, directiveType, e, id):
        e = e.scenePos()
        node1 = BeginNode(self.scene, text, directiveType, id, inputs=[1], outputs=[])
        node1.setPos(e.x() - 80, e.y() - 40)

    def addEndNode(self, text, directiveType, e, id):
        e = e.scenePos()
        node1 = EndNode(self.scene, text, directiveType, id, inputs=[1], outputs=[])
        node1.setPos(e.x() - 80, e.y() - 40)

    def addLozeNode(self, text, directiveType, e, id):
        e = e.scenePos()
        node1 = LozeNode(self.scene, text, directiveType, id, inputs=[1, 2, 3, 4], outputs=[])
        node1.setPos(e.x()-80,e.y()-40)

    def addParaNode(self, text, directiveType, e, id):
        e = e.scenePos()
        node1 = ParaNode(self.scene, text, directiveType, inputs=[1, 2, 3, 4], outputs=[])
        node1.setPos(e.x()-80, e.y()-40)

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)

        left = int(math.floor(rect.left()))
        right = int(math.ceil(rect.right()))
        top = int(math.floor(rect.top()))
        bottom = int(math.ceil(rect.bottom()))

        first_left = left - (left % self.gridSize)
        first_top = top - (top % self.gridSize)
        lines_light, lines_drak = [], []
        for x in range(first_left, right, self.gridSize):
            if (x % 100 != 0):
                lines_light.append(QLine(x, top, x, bottom))
            else:
                lines_drak.append(QLine(x, top, x, bottom))

        for y in range(first_top, bottom, self.gridSize):
            if (y % 100 != 0):
                lines_light.append(QLine(left, y, right, y))
            else:
                lines_drak.append(QLine(left, y, right, y))

        painter.setPen(self._pen_light)
        # painter.drawLine(lines_light)
        for i in lines_light:
            painter.drawLine(i)
        painter.setPen(self._pen_drak)
        for i in lines_drak:
            painter.drawLine(i)
