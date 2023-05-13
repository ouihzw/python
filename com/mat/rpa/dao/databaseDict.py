# -*- coding:utf-8 -*-
from com.mat.rpa import settings
from com.mat.rpa.dao import mongodbObject
class DatabaseDict(object):
    __instance = None  # 单例模式
    _isFirstInit = True  # 判断首次构造的标记

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super(DatabaseDict, cls).__new__(cls)
        return cls.__instance

    def __init__(self): #将数据库每个配置都创建唯一一个数据库对象
        # 获取type类
        cls = type(self)
        # 判断类的构造函数是否初次执行
        if cls._isFirstInit:
            self.dbDict = {}
            for dbkey, dbconfig in settings.DATABASES.items():
                # if dbconfig["ENGINE"] == "mysql": #创建一个mysql数据库实例
                #     self.dbDict[dbkey] = MySQLObject.MySQLObject(host=dbconfig["HOST"], port=dbconfig["PORT"],
                #                                                  username=dbconfig["USER"], password=dbconfig["PASSWORD"],
                #                                                  database=dbconfig["NAME"])
                # elif dbconfig["ENGINE"] == "sqlite": #创建一个sqlite数据库实例
                #     self.dbDict[dbkey] = sqliteObject.SQLiteObject(db = dbconfig["NAME"])
                # if dbconfig["ENGINE"] == "sqlite": #创建一个sqlite数据库实例
                #     self.dbDict[dbkey] = sqliteObject.SQLiteObject(db=dbconfig["NAME"])
                if dbconfig["ENGINE"] == "mongodb": #创建一个mongodb数据库实例
                    self.dbDict[dbkey] = mongodbObject.MongodbObject(host=dbconfig["HOST"],
                                                                     port=dbconfig["PORT"],
                                                                     db_name=dbconfig["NAME"])
            # 将首次构造的标记置为False
            cls._isFirstInit = False

