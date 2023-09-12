create type query_t as enum ('insert' , 'delete', 'update');
create table Book(
	isbn varchar(13),
	title varchar(50) not null,
	description varchar(256) ,
	versionNum int not null,
	publicationName varchar(50) not null,
	publishTime Date not null,
	isTranslated boolean not null,
	type_query query_t ,
	query_time Date ,
	primary key( isbn , query_time , type_query) 
);
create table BookCopy(
	bookCopyId int ,
	isbn varchar(13) not null,
        type_query query_t ,
	query_time Date ,
	primary key( bookCopyId , query_time , type_query) 
);
create table authorFor(
	id int,
	isbn varchar(13) not null,
	authorName varchar(50) not null,
        type_query query_t ,
	query_time Date ,
	primary key( id , query_time , type_query) 
);
create table GenreFor(
	id int ,
	isbn varchar(13) not null,
	genre varchar(50) not null,
       type_query query_t ,
	query_time Date ,
	primary key( id , query_time , type_query) 
);
create table languageFor(
	id int ,
	isbn varchar(13) not null ,
	languageN varchar(50) not null,
        type_query query_t ,
	query_time Date ,
	primary key( id , query_time , type_query) 
);
create table translateFor(
	id int ,
	isbn varchar(13) not null ,
	translatorName varchar(50) not null,
       type_query query_t ,
	query_time Date ,
	primary key( id , query_time , type_query) 
);
create table person(
	membership int ,
	name varchar(50) not null,
	birthday Date not null,
	membershipDate Date not null,
	address varchar(256) not null,
	phoneNum varchar(256) not null,
	type_query query_t ,
	query_time Date ,
	primary key( membership , query_time , type_query) 
);
create table lends(
	bookCopyId int not null ,
	membership int not null,
	startTime Date not null,
	endTime Date not null,
       type_query query_t ,
	query_time Date ,
	primary key( bookCopyId , query_time , type_query) 
);

