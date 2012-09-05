
drop table if exists users;
create table users(
 id INT NOT NULL auto_increment PRIMARY KEY,
 nickname varchar(32) default NULL,
 email varchar(64) NOT NULL,
 password varchar(64) NOT NULL,
 salt varchar(32) NOT NULL,
 status bit NOT NULL default 1
);
insert into users(nickname, email, password, salt) 
values('test', 'test', 'test', 'test');
