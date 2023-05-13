drop table if exists user_login;
create table user_login (
    id int unsigned auto_increment,
    user_name varchar(30) not null unique,
    password char(32),
    auto_login boolean not null default 0,
    latest_login datetime not null,
    primary key(id),
    index(latest_login)
)engine=innodb default charset = utf8;

insert into user_login (user_name, latest_login) values 
("12345", "2022-01-09 20:00:00"), 
("54321", "2022-01-10 10:00:00"), 
("11111", "2022-01-10 11:00:00");
insert into user_login (user_name, password, auto_login, latest_login) values
("55555", "c5fe25896e49ddfe996db7508cf00534", 0, "2022-01-11 10:00:00"),
("66666", "c5fe25896e49ddfe996db7508cf00534", 1, NOW());
