class WebComboBoxOption(object):
    webComboBoxOptionObject = {}
    webComboBoxOptionObjectName = []

    def saveWebComboBoxOptionObject(self, name, context):
        if name in self.webComboBoxOptionObject:
            self.webComboBoxOptionObject[name]["context"] = context
        else:
            self.webComboBoxOptionObject.setdefault(name, {"context": context})
        return self.webComboBoxOptionObject

    def getwebComboBoxOptionContext(self, name):
        if name in self.webComboBoxOptionObject:
            return self.webComboBoxOptionObject[name]["context"]
        else:
            return

    def getWebComboBoxOptionObjectName(self):
        self.webComboBoxOptionObjectName.clear()
        for key in self.webComboBoxOptionObject.keys():
            self.webComboBoxOptionObjectName.append(key)
        return self.webComboBoxOptionObjectName