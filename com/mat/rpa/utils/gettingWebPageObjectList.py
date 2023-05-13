class GettingWebPageObjectList(object):
    gettingWebPageObjectListObject = {}
    gettingWebPageObjectListObjectName = []

    def saveGettingWebPageObjectListObject(self, name,list):
        if name in self.gettingWebPageObjectListObject:
            self.gettingWebPageObjectListObject[name]["list"] = list
        else:
            self.gettingWebPageObjectListObject.setdefault(name, {"list": list})
        return self.gettingWebPageObjectListObject

    def gettingWebPageObjectList(self, name):
        if name in self.gettingWebPageObjectListObject:
            return self.gettingWebPageObjectListObject[name]["list"]
        else:
            return

    def getGettingWebPageObjectListObjectName(self):
        self.gettingWebPageObjectListObjectName.clear()
        for key in self.gettingWebPageObjectListObject.keys():
            self.gettingWebPageObjectListObjectName.append(key)
        return self.gettingWebPageObjectListObjectName