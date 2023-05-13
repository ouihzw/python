drop table if exists user;
create table user (
    id int unsigned auto_increment,
    user_name varchar(30) not null unique,
    password char(32) not null,
    class int not null default 1,
    create_time datetime not null default CURRENT_TIMESTAMP,
    status tinyint not null default 1,
    primary key(id),
    index(user_name)
)engine=innodb default charset = utf8;

insert into user (user_name, password, class) values  
("admin", "21232f297a57a5a743894a0e4a801fc3", 0);