# -*- coding:utf-8 -*-
import traceback

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from com.mat.rpa.dao.workDao.workDao import WorkDao
from com.mat.rpa.dao.workDao.directiveDao import DirectiveDao
from com.mat.rpa.utils.variable import VariableManager
from bson import ObjectId
import os
import json

class ExportFlow(QObject):
    def __init__(self, flowId: ObjectId, parent = None):
        super().__init__(parent)
        self.id = flowId
        self.appId = VariableManager().getAppId()
        app = WorkDao().loadApp(appId=self.appId)
        # 如果设置了默认输出路径
        if hasattr(app, "export_path"):
            self.exportPath = app["export_path"]
        # 否则留空
        else:
            self.exportPath = ""
        for item in app["flow"]:
            if item["id"] == flowId:
                self.name = item["flow_name"]
                self.type = item["type"]
        # 如果没找到对应的flow数据（不太可能），报错
        assert hasattr(self, "name")

    def save(self):
        try:
            if self.exportPath != "":
                if not os.path.exists(self.exportPath):
                    os.makedirs(self.exportPath)
                fileName, _ = QFileDialog.getSaveFileName(self.parent(), u"确认导出路径",
                                                          self.exportPath + "\\" + self.name,
                                                          u"Flow流程文件 (*.flow)")
            else:
                fileName, _ = QFileDialog.getSaveFileName(self.parent(), u"确认导出路径",
                                                          self.name,
                                                          u"Flow流程文件 (*.flow)")
            # 对话框被关闭时中断函数执行
            if fileName == "":
                return
            else:
                # 写入Flow文件信息
                with open(fileName, 'w', encoding="utf-8") as flow:
                    flowDict = {
                        "id": str(self.id),
                        "name": self.name,
                        "type": self.type,
                        "app_id": str(self.appId)
                    }
                    json.dump(flowDict, flow, indent=2, ensure_ascii=False)
                # 删掉最后的大括号换行符，填写directives:
                with open(fileName, 'ab') as flow:
                    flow.seek(-3, 2)
                    flow.truncate()
                    flow.write(b',\n  "directives": [')
                # 导出数据库中的指令
                with open(fileName, 'a', encoding="utf-8") as flow:
                    first = True
                    for directive in DirectiveDao().getAllDirectives(self.id):
                        if first:
                            first = False
                        else:
                            flow.write(", ")
                        directive["_id"] = str(directive["_id"])
                        del directive["flow_id"]
                        text = json.dumps(directive, indent=2, ensure_ascii=False)
                        text = text.split('\n')
                        indented = text[0]
                        for line in text[1:]:
                            indented += "\n  " + line
                        flow.write(indented)
                    flow.write("]\n}")
        except Exception:
            traceback.print_exc()




