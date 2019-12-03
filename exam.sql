create table district (
	id serial primary key,
	name varchar(80) unique
);

create table school (
	id serial primary key,
	district_id int references district(id),
	name varchar(80) unique
);

create table classroom (
	id serial primary key,
	school_id int references school(id),
	capacity int check (capacity >= 0)
);

create table student (
	id serial primary key,
	first_name varchar(80),
	last_name varchar(80),
	school_id int references school(id)
);

create table subj (
	id serial primary key,
	description varchar(80) unique,
	min_grade int check (min_grade <= 100 and min_grade >= 0)
);

create table student_subj (
	student_id int references student(id),
	subj_id int references subj(id)
);	

create table req_subj (
	subj_id int primary key references subj(id)
);

create table exam (
	id serial primary key,
	subj_id int references subj(id),
	day date unique
);

create table grade (
	student_id int references student(id),
	exam_id int references exam(id),
	grade int check (grade <= 100 and grade >= 0),
	primary key (student_id, exam_id)
);

/*
 * reserved_exam_reason - rer
 */
create table rer (
	id serial primary key,
	description  varchar(80) unique
);

create table student_rer (
	student_id int references student(id),
	subj_id int references subj(id),
	rer_id int references rer(id),
	primary key (student_id, subj_id)
);

create table exam_distrib (
	id serial primary key,
	classroom_id int references classroom(id),
	exam_id int references exam(id)
);

create table student_distrib (
	student_id int references student(id),
	exam_distrib_id int references exam_distrib(id)
);
