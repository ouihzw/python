# -*- coding:utf-8 -*-
from com.mat.rpa.utils.globalConstants import GlobalConstants
from com.mat.rpa.views.workWindow.leftPanel.directiveTree import treeItem
from . import conditionConstants

class ConditionSubDirectiveTree(treeItem.TreeItemWithID):
    def __init__(self, parent):
        super(ConditionSubDirectiveTree, self).__init__(parent)
        self.createConditionSubTreeNode()

    def createConditionSubTreeNode(self):
        self.nodeType = GlobalConstants.treeBranchType
        self.directiveType = "condition"
        self.setText(0, "条件判断")
        self.createTreeNode(GlobalConstants.treeLeafType,
                              self, conditionConstants.ConditionConstants.ifConditionDirective, "If条件")
        # self.createTreeNode(GlobalConstants.treeLeafType,
        #                       self, conditionConstants.ConditionConstants.ifMultiConditionDirective, "If多条件")
        self.createTreeNode(GlobalConstants.treeLeafType,
                              self, conditionConstants.ConditionConstants.ifWebPageContainDirective, "If网页包含")
        self.createTreeNode(GlobalConstants.treeLeafType,
                              self, conditionConstants.ConditionConstants.ifWebElementVisibleDirective, "If元素可见(Web)")
        self.createTreeNode(GlobalConstants.treeLeafType,
                              self, conditionConstants.ConditionConstants.ifWindowExistsDirective, "If窗口存在")
        self.createTreeNode(GlobalConstants.treeLeafType,
                              self, conditionConstants.ConditionConstants.ifWindowContainsDirective, "If窗口包含")
        self.createTreeNode(GlobalConstants.treeLeafType,
                              self, conditionConstants.ConditionConstants.ifImageExistsDirective, "If图像存在")
        self.createTreeNode(GlobalConstants.treeLeafType,
                            self, conditionConstants.ConditionConstants.ifTextExistsOnScreenOCRDirective, "If屏幕上存在文本(OCR)")
        self.createTreeNode(GlobalConstants.treeLeafType,
                            self, conditionConstants.ConditionConstants.ifFileExistsDirective, "If文件存在")
        self.createTreeNode(GlobalConstants.treeLeafType,
                            self, conditionConstants.ConditionConstants.ifFolderExistsDirective, "If文件夹存在")
        # self.createTreeNode(GlobalConstants.treeLeafType,
        #                     self, conditionConstants.ConditionConstants.elseIfDirective, "Else If")
        # self.createTreeNode(GlobalConstants.treeLeafType,
        #                     self, conditionConstants.ConditionConstants.elseIfMultiConditionDirective, "Else If多条件")
        # self.createTreeNode(GlobalConstants.treeLeafType,
        #                     self, conditionConstants.ConditionConstants.elseDirective, "Else")
        # self.createTreeNode(GlobalConstants.treeLeafType,
        #                     self, conditionConstants.ConditionConstants.endIfDirective, "End If")