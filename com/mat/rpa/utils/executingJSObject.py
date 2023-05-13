class ExecutingJS(object):
    executingJSObject = {}
    executingJSObjectName = []

    def saveExecutingJSObject(self, name, result):
        if name in self.executingJSObject:
            self.executingJSObject[name]["result"] = result
        else:
            self.executingJSObject.setdefault(name, {"result": result})
        return self.executingJSObject

    def getExecutingJSResult(self, name):
        if name in self.executingJSObject:
            return self.executingJSObject[name]["result"]
        else:
            return

    def getExecutingJSObjectName(self):
        self.executingJSObjectName.clear()
        for key in self.executingJSObject.keys():
            self.executingJSObjectName.append(key)
        return self.executingJSObjectName