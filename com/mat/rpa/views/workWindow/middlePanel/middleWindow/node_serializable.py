class Serializable():  # 其中serialize用于编码，并返回编码，deserialize负责解码
    def __init__(self):
        self.id = id(self)

    def serialize(self):
        raise NotImplemented()

    def deserialize(self, data, hashmap={}):
        raise NotImplemented()
# -*- coding:utf-8 -*-
