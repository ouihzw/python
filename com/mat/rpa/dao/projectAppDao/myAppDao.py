# -*- coding:utf-8 -*-
from .. import databaseDict
from PyQt5.QtCore import *

class MyAppDao(QObject):
    queryLimitedAppSignal = pyqtSignal(int, tuple)
    def __init__(self, parent=None):
        super(MyAppDao, self).__init__(parent)
        db = databaseDict.DatabaseDict().dbDict['MongoDB'].db
        self.app = db.get_collection("app")

    def queryLimitedAppsIntoTable(self, skip, limit):
        # def f(tx, pageNumber, recordLimit):
        #     sql = "select * from myapp limit %d, %d" % \
        #           (pageNumber, recordLimit)
        #     rowCount = tx.execute(sql)
        #     allResult = tx.fetchall()
        #     self.queryLimitedAppSignal.emit(rowCount, allResult)
        # #执行回调
        # self.db.dbPool.runInteraction(f, number, limit)
        result = self.app.find({}).sort([("update_time", -1)]).skip(skip).limit(limit)
        return list(result)

    def queryTotalRecordCount(self):
        return self.app.count_documents({})

    # def insertIntoOneRecord(self, recordTuple):
    #     def f(tx, record):
    #         sql = 'INSERT INTO myapp(app_name, update_time, app_status) VALUES (%s, %s, %s)'
    #         tx.execute(sql, record)
    #     # 执行回调
    #     self.db.dbPool.runInteraction(f, recordTuple)

    def deleteApp(self, appId):
        self.app.delete_one({"_id": appId})
