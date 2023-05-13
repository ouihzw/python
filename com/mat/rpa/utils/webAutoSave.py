# -*- coding:utf-8 -*-
class WebAutoSave(object):
    instance = None
    webObject = {}
    webObjectName = []

    def __new__(cls, *args, **kwargs):
        if cls.instance == None:
            cls.instance = object.__new__(cls)
        return cls.instance

    def webObjectSave(self, name, handle, client):
        if name in self.webObject:
            self.webObject[name]["handle"] = handle
            self.webObject[name]["client"] = client
        else:
            self.webObject.setdefault(name, {"handle": handle, "client": client})
            self.webObjectName.append(name)
        return self.webObject

    def getWebObjectHandle(self, name):
        if name in self.webObject:
            return self.webObject[name]["handle"]
        else:
            return

    def getWebObjectClient(self, name):
        if name in self.webObject:
            return self.webObject[name]["client"]
        else:
            return

    def webObjectSave_onlyName(self, name):
        if name in self.webObject:
            self.webObject[name]["handle"] = ""
            self.webObject[name]["client"] = ""
        else:
            self.webObject.setdefault(name, {"handle": "", "client": ""})
        return self.webObject

    def getWebObjectName(self):
        return self.webObjectName
