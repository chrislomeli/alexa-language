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

