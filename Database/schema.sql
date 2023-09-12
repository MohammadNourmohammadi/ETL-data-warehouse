create table Book(
	isbn varchar(13) primary key,
	title varchar(50) not null,
	description varchar(256) ,
	versionNum int not null,
	publicationName varchar(50) not null,
	publishTime Date not null,
	isTranslated boolean not null
);
create table BookCopy(
	bookCopyId int  primary key,
	isbn varchar(13) not null,
	constraint isbn_fk
		foreign key (isbn) references Book (isbn)
            on update cascade
);
create table authorFor(
	id int primary key,
	isbn varchar(13) not null,
	authorName varchar(50) not null,
	constraint isbn_fk
		foreign key (isbn) references Book (isbn)
            on update cascade
);
create table GenreFor(
	id int primary key,
	isbn varchar(13) not null,
	genre varchar(50) not null,
	constraint isbn_fk
		foreign key (isbn) references Book (isbn)
            on update cascade
);
create table languageFor(
	id int primary key,
	isbn varchar(13) not null ,
	languageN varchar(50) not null,
	constraint isbn_fk
		foreign key (isbn) references Book (isbn)
            on update cascade
);
create table translateFor(
	id int primary key,
	isbn varchar(13) not null ,
	translatorName varchar(50) not null,
	constraint isbn_fk
		foreign key (isbn) references Book (isbn)
            on update cascade
);
create table person(
	membership int primary key,
	name varchar(50) not null,
	birthday Date not null,
	membershipDate Date not null,
	address varchar(256) not null,
	phoneNum varchar(256) not null
);
create table lends(
	bookCopyId int not null primary key,
	membership int not null,
	startTime Date not null,
	endTime Date not null,
	constraint membership_fk
		foreign key (membership) references person (membership)
            on update cascade
	, 
	constraint bookCopyId_fk
		foreign key (bookCopyId) references BookCopy (bookCopyId)
            on update cascade
);

