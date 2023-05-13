class WebElementPosition(object):
    webElementPositionObject = {}
    webElementPositionObjectName = []

    def saveWebElementPositionObject(self, name, position):
        if name in self.webElementPositionObject:
            self.webElementPositionObject[name]["position"] = position
        else:
            self.webElementPositionObject.setdefault(name, {"position": position})
        return self.webElementPositionObject

    def getWebElementPosition(self, name):
        if name in self.webElementPositionObject:
            return self.webElementPositionObject[name]["position"]
        else:
            return

    def getWebElementPositionObjectName(self):
        self.webElementPositionObjectName.clear()
        for key in self.webElementPositionObject.keys():
            self.webElementPositionObjectName.append(key)
        return self.webElementPositionObjectName