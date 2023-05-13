class WebPageScreenshot(object):
    webPageScreenshotObject = {}
    webPageScreenshotObjectName = []

    def saveWebPageScreenshotObject(self, name, imagePath):
        if name in self.webPageScreenshotObject:
            self.webPageScreenshotObject[name]["imagePath"] = imagePath
        else:
            self.webPageScreenshotObject.setdefault(name, {"imagePath": imagePath})
        return self.webPageScreenshotObject

    def getWebPageScreenshotObjectImagePath(self, name):
        if name in self.webPageScreenshotObject:
            return self.webPageScreenshotObject[name]["imagePath"]
        else:
            return

    def getWebPageScreenshotObjectName(self):
        self.webPageScreenshotObjectName.clear()
        for key in self.webPageScreenshotObject.keys():
            self.webPageScreenshotObjectName.append(key)
        return self.webPageScreenshotObjectName