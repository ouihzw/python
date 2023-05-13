drop table if exists myapp;
create table myapp (
    id int auto_increment not null,
    app_class varchar(200) not null default '我创建的应用',
    app_name varchar(200) not null default '',
    update_time datetime default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
    app_status int not null default 0,
    primary key(id)
)engine=innodb default charset = utf8;