import datetime

if __name__ != "__main__":
    from .. import databaseDict
from PyQt5.QtCore import *



class UserDao(QObject):
    # resultAutoFillSignal = pyqtSignal(tuple)
    # queryUserNamesSignal = pyqtSignal(tuple)
    # queryForLoginSignal = pyqtSignal(tuple)

    def __init__(self, parent=None):
        super().__init__(parent)
        db = databaseDict.DatabaseDict().dbDict['MongoDB'].db
        self.userLogin = db.get_collection("user_login")
        self.user = db.get_collection("user")

    # 查询所有记录的用户名
    def insertNewtUser(self, user: dict):
        result = self.user.insert_one(user)
        return result



    def queryUserNames(self):
        # def f(tx):
        #     sql = "select user_name, latest_login from user_login order by latest_login desc"
        #     tx.execute(sql)
        #     results = tx.fetchall()
        #     self.queryUserNamesSignal.emit(results)
        # self.db.dbPool.runInteraction(f)
        result = self.userLogin.find({}, {"user_name": 1, "latest_login": 1}).sort([("latest_login", -1)])
        resultList = []
        for item in result:
            resultList.append(item["user_name"])
        return resultList

    # 根据所给用户名查询记录
    def queryByUserName(self, userName):
        # def f(tx, name):
        #     sql = "select * from user_login where user_name='%s'" % name
        #     tx.execute(sql)
        #     result = tx.fetchone()
        #     self.resultAutoFillSignal.emit(result)
        # self.db.dbPool.runInteraction(f, userName)
        result = self.userLogin.find_one({"user_name": userName})
        return result

    # 查询最近登录的记录
    def queryLatestOne(self):
        # def f(tx):
        #     sql = "select * from user_login order by latest_login desc"
        #     tx.execute(sql)
        #     result = tx.fetchone()
        #     self.resultAutoFillSignal.emit(result)
        # self.db.dbPool.runInteraction(f)
        result = self.userLogin.find({}).sort([("latest_login", -1)])
        try:
            return next(result)
        except StopIteration:
            return None

    # 更新、插入数据（userInfo: dict{user_name, password, auto_login}）
    def updateNewLogin(self, userInfo):
        # def f(tx, list):
        #     sql = "select count(*) from user_login where user_name='%s'" % list[0]
        #     tx.execute(sql)
        #     if tx.fetchone():
        #         sql = "update user_login set password=%s, auto_login=%s, latest_login=NOW() where user_name=%s"
        #         list.append(list.pop(0))
        #         print(tx.execute(sql, list))
        #     else:
        #         sql = "insert into user_login(user_name, password, auto_login, latest_login) values (%s, %s, %s, NOW())"
        #         tx.execute(sql, list)
        # self.db.dbPool.runInteraction(f, userInfo)
        userInfo["latest_login"] = datetime.datetime.now()
        self.userLogin.update_one({"user_name": userInfo["user_name"]}, {"$set": userInfo}, upsert=True)

    # 按用户名删除登录信息
    def deleteByUserName(self, userName):
        # def f(tx, name):
        #     sql = "delete from user_login where user_name='%s'" % name
        #     print(tx.execute(sql))
        # self.db.dbPool.runInteraction(f, userName)
        self.userLogin.delete_one({"user_name": userName})

    # 清理用户登录信息
    def deleteAllRecord(self):
        # def f(tx):
        #     sql = "delete from user_login"
        #     tx.execute(sql)
        # self.db.dbPool.runInteraction(f)
        self.userLogin.delete_many({})

    # 登录查询
    def queryForLogin(self, userName):
        # def f(tx, name):
        #     sql = "select * from user where user_name='%s'" % name
        #     tx.execute(sql)
        #     result = tx.fetchone()
        #     if not result:
        #         result = ()
        #     self.queryForLoginSignal.emit(result)
        # self.db.dbPool.runInteraction(f, userName)
        result = self.user.find_one({"user_name": userName})
        return result

if __name__ == "__main__":
    import sys
    sys.path.append('../../')
    from dao import databaseDict
    dao = UserDao(QObject())
    dao.queryUserNames()
    dao.queryByUserName("12345")
    dao.queryLatestOne()
    list = ["abc", None, False]
    dao.deleteByUserName("abc")
