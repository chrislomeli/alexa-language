create table verbs.verbs
(
	id integer not null
		constraint verbs_pk
			primary key,
	verb text
);

alter table verbs.verbs owner to postgres;

create table verbs.expressions
(
	expression_id serial not null
		constraint expressions_pk
			primary key,
	verb text,
	phrase text,
	present_tense boolean default true not null,
	past_tense boolean default true,
	future_tense boolean default true,
	valid_i boolean default true not null,
	valid_you boolean default true not null,
	valid_they boolean default true not null,
	valid_we boolean default true not null,
	valid_he boolean default true
);

alter table verbs.expressions owner to postgres;

create table verbs.conjugations
(
	conjugation_id serial not null
		constraint conjugations_pk
			primary key,
	verb text,
	tense text,
	modifier text,
	pronoun_i text,
	pronoun_he text,
	pronoun_you text,
	pronoun_they text,
	pronoun_we text
);

alter table verbs.conjugations owner to postgres;

create table verbs.past
(
	conjugation_id integer,
	verb text,
	tense text,
	modifier text,
	pronoun_i text,
	pronoun_he text,
	pronoun_you text,
	pronoun_they text,
	pronoun_we text
);

alter table verbs.past owner to postgres;

create table verbs.future
(
	conjugation_id integer,
	verb text,
	tense text,
	modifier text,
	pronoun_i text,
	pronoun_he text,
	pronoun_you text,
	pronoun_they text,
	pronoun_we text
);

alter table verbs.future owner to postgres;

create table verbs.present
(
	conjugation_id integer,
	verb text,
	tense text,
	modifier text,
	pronoun_i text,
	pronoun_he text,
	pronoun_you text,
	pronoun_they text,
	pronoun_we text
);

alter table verbs.present owner to postgres;

create table verbs.imports
(
	expression_id integer,
	verb text,
	phrase text,
	present_tense boolean,
	past_tense boolean,
	future_tense boolean,
	valid_i boolean,
	valid_you boolean,
	valid_they boolean,
	valid_we boolean,
	valid_he boolean
);

alter table verbs.imports owner to postgres;

