class WebPageInfo(object):
    webPageInfoObject = {}
    webPageInfoObjectName = []

    def saveWebPageInfoObject(self, name, info):
        if name in self.webPageInfoObject:
            self.webPageInfoObject[name]["info"] = info
        else:
            self.webPageInfoObject.setdefault(name, {"info": info})
        return self.webPageInfoObject

    def getWebPageInfoPosition(self, name):
        if name in self.webPageInfoObject:
            return self.webPageInfoObject[name]["info"]
        else:
            return

    def getWebPageInfoObjectName(self):
        self.webPageInfoObjectName.clear()
        for key in self.webPageInfoObject.keys():
            self.webPageInfoObjectName.append(key)
        return self.webPageInfoObjectName