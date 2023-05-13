// 初始化MongoDB数据库，建立索引，插入测试数据
connect = new Mongo('mongodb://localhost:27017');
db = connect.getDB("rpa");
db.createCollection("app");
db.createCollection("directive");
db.createCollection("element");
db.createCollection("variable");
db.createCollection("user_login");
db.createCollection("user");
db.app.createIndex({"status": 1, "name": 1, "update_time": -1});
db.directive.createIndex({"flow_id": 1});
db.variable.createIndex({"parent_id": 1, "directive_id": 1, "name": 1});
db.user.createIndex({"user_name": 1});
// admin admin
db.user.insertOne({"user_name": "admin", "password": "21232f297a57a5a743894a0e4a801fc3", "class": 0, "status": 1});
db.user_login.createIndex({"user_name": 1});
