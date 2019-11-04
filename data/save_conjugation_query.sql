select C.conjugation_id, C.verb, C.tense, C.pronoun, C.conjugation,  R.phrase,
       row_number() over (partition by C.conjugation_id) as rn
from verbs.conjugations C
 join verbs.pronouns P on P.pronoun = C.pronoun
 join verbs.tenses T on T.tense = C.tense
 join verbs.phrases R on R.verb = C.verb
order by C.verb, P.ordinal, T.ordinal, C.tense, C.conjugation, rn;