-- auto-generated definition
create table user
(
    id   int auto_increment
        primary key,
    name varchar(16)            not null,
    tel  varchar(32) default '' not null
);


