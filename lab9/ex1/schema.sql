drop table if exists users;
create table users (
id integer primary key autoincrement,
username string not null,
fullname string not null,
photo string not null
);
