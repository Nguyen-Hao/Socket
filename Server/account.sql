create database account
go

use account
go

create table account (
	username nchar(20) not null,
	pass nchar(20) not null,
)
go
insert into account(username, pass) values ('nguyenhao', '1234')
insert into account(username, pass) values ('123', '1234')
insert into account(username, pass) values ('1', '2')
go

select * from account
