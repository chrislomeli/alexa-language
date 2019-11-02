-- I, You, We, They
select concat('I ', first_person, ' ', phrase), E.* from verbs.conjugations C join verbs.expressions E on E.verb = C.verb where tense = 'present' and E.present_tense and E.valid_i order by C.verb;
select concat('I ', first_person, ' ', phrase), E.* from verbs.conjugations C join verbs.expressions E on E.verb = C.verb where tense = 'past' and E.past_tense  and E.valid_i  order by C.verb;
select concat('I ', first_person, ' ', phrase), E.* from verbs.conjugations C join verbs.expressions E on E.verb = C.verb where tense = 'future' and E.future_tense and E.valid_i  order by C.verb;

select concat('You ', first_person, ' ', phrase), E.* from verbs.conjugations C join verbs.expressions E on E.verb = C.verb where tense = 'present' and E.present_tense  and E.valid_you  order by C.verb;
select concat('You ', first_person, ' ', phrase), E.* from verbs.conjugations C join verbs.expressions E on E.verb = C.verb where tense = 'past' and E.past_tense  and E.valid_you  order by C.verb;
select concat('You ', first_person, ' ', phrase), E.* from verbs.conjugations C join verbs.expressions E on E.verb = C.verb where tense = 'future' and E.future_tense  and E.valid_you  order by C.verb;

select concat('We ', first_person, ' ', phrase), E.* from verbs.conjugations C join verbs.expressions E on E.verb = C.verb where tense = 'present' and E.present_tense  and E.valid_we order by C.verb;
select concat('We ', first_person, ' ', phrase), E.* from verbs.conjugations C join verbs.expressions E on E.verb = C.verb where tense = 'past' and E.past_tense   and E.valid_we order by C.verb;
select concat('We ', first_person, ' ', phrase), E.* from verbs.conjugations C join verbs.expressions E on E.verb = C.verb where tense = 'future' and E.future_tense  and E.valid_we  order by C.verb;

select concat('They ', first_person, ' ', phrase), E.* from verbs.conjugations C join verbs.expressions E on E.verb = C.verb where tense = 'present' and E.present_tense   and E.valid_they   order by C.verb;
select concat('They ', first_person, ' ', phrase), E.* from verbs.conjugations C join verbs.expressions E on E.verb = C.verb where tense = 'past' and E.past_tense   and E.valid_they  order by C.verb;
select concat('They ', first_person, ' ', phrase), E.* from verbs.conjugations C join verbs.expressions E on E.verb = C.verb where tense = 'future' and E.future_tense   and E.valid_they   order by C.verb;



-- He, She
select concat('She ', third_person, ' ', phrase), E.* from verbs.conjugations C join verbs.expressions E on E.verb = C.verb where tense = 'present' and E.present_tense order by C.verb;
select concat('She ', third_person, ' ', phrase), E.* from verbs.conjugations C join verbs.expressions E on E.verb = C.verb where tense = 'past' and E.past_tense  order by C.verb;
select concat('She ', third_person, ' ', phrase), E.* from verbs.conjugations C join verbs.expressions E on E.verb = C.verb where tense = 'future' and E.future_tense  order by C.verb;





