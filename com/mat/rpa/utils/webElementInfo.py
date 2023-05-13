class WebElementInfo(object):
    webElementInfoObject = {}
    webElementObjectName = []

    def saveWebElementInfoObject(self, name, info):
        if name in self.webElementInfoObject:
            self.webElementInfoObject[name]["info"] = info
        else:
            self.webElementInfoObject.setdefault(name, {"info": info})
        return self.webElementInfoObject

    def getWebElementInfoObjectInfo(self, name):
        if name in self.webElementInfoObject:
            return self.webElementInfoObject[name]["info"]
        else:
            return

    def getwebElementObjectName(self):
        self.webElementObjectName.clear()
        for key in self.webElementInfoObject.keys():
            self.webElementObjectName.append(key)
        return self.webElementObjectName