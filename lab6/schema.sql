drop table if exists users;
create table users (
	id integer primary key autoincrement,
	fullname string not null,
	photo string not null
);

drop table if exists logins;
create table logins (
	uid integer,
	username string not null,
	password string not null,
	FOREIGN KEY(uid) REFERENCES users(id)
);
