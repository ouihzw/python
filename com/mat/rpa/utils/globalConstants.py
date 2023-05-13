# -*- coding:utf-8 -*-
from com.mat.rpa.views.workWindow.middlePanel.directives import directiveConstants
class GlobalConstants():
    myappType = "myAppType"
    selfDefinedDirectiveType = "selfDefinedDirectiveType"
    executingScheduleType = "executingScheduleType"
    appStatusEditing = 0
    appStatusPublished = 1
    #定义树节点类型
    treeBranchType = "branch"
    treeLeafType = "leaf"
    #流程节点模式
    PCAppMode = 0 #PC流程应用
    MobileAppMode = 1 #手机流程应用
    directiveConstants = directiveConstants.DirectiveConstants
    variableDataType = [u"任意类型", u"整数", u"小数", u"布尔值", u"纯文本", u"字符串",
                        u"列表", u"字典", u"二进制数据", u"任意对象", u"网页对象",
                        u"网页元素", u"窗口对象", u"文件"]

