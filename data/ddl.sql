create table verbs
(
	id int auto_increment
		primary key,
	verb text null
);

-- alter table verbs.verbs owner to postgres;
create table expressions
(
	expression_id int auto_increment
		primary key,
	verb text null,
	phrase text null,
	present_tense tinyint(1) default 1 not null,
	past_tense tinyint(1) default 1 null,
	future_tense tinyint(1) default 1 null,
	valid_i tinyint(1) default 1 not null,
	valid_you tinyint(1) default 1 not null,
	valid_they tinyint(1) default 1 not null,
	valid_we tinyint(1) default 1 not null
);



-- alter table verbs.expressions owner to postgres;

create table verbs.conjugations
(
	conjugation_id int auto_increment
			primary key,
	verb text,
	tense text,
	modifier text,
	first_person text,
	third_person text
);

-- alter table verbs.conjugations owner to clomeli;

