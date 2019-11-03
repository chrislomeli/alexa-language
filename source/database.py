from typing import List

import psycopg2

from source.configure import Configuration
from source.model import FlashCard


class Database(object):
    pronouns = {
        "i": ("pronoun_i", "valid_i"),
        "he": ("pronoun_he", "valid_he"),
        "she": ("pronoun_he", "valid_he"),
        "it": ("pronoun_he", "valid_he"),
        "you": ("pronoun_you", "valid_you"),
        "we": ("pronoun_we", "valid_we"),
        "they": ("pronoun_they", "valid_their"),
    }

    tenses = {
        "present": "present_tense",
        "past": "past_tense",
        "future": "future_tense",

    }

    _instance = None

    @staticmethod
    def get_instance():
        if Database._instance is None:
            c = Configuration.get_instance()
            Database._instance = Database(
                user=c.database_user,
                password=c.database_password,
                host=c.database_host,
                port=c.database_port,
                database=c.database)
        return Database._instance

    def __init__(self, user: str, password: str, host: str, port: str, database: str):
        self.sql_statement = ""
        self.connection = psycopg2.connect(
            database=database,
            user=user,
            password=password,
            host=host,
            port="5432")

    def fetch_rows(self, offset, page_size) -> List[FlashCard]:
        sql = self.sql_statement + f""" limit {page_size} offset {offset}"""
        cur = self.connection.cursor()
        cur.execute(sql)
        query_rows = cur.fetchall()
        response = []
        for row in query_rows:
            flashCard = FlashCard(
                verb=row[0],
                tense=row[1],
                source_phrase=row[2],
                source_lang="en",
                conjugation_id=row[3],
                expression_id=row[4],
                pronoun=row[5])
            response.append(flashCard)
        return response

    def set_query(self, pronouns: List[str], tenses: List[str], verb_list: List[str]=None):
        unions: List[str] = []
        for pronoun in pronouns:
            for tense in tenses:
                pronoun = pronoun.title()
                person = Database.pronouns[pronoun.lower()][0]
                validation_fld = Database.pronouns[pronoun.lower()][1]
                tense_field = self.tenses[tense]
                validation_clause = ""
                if validation_fld:
                    validation_clause = f" and E.{validation_fld} "

                sqlStatement: str = f"""select 
                        C.verb, 
                        C.tense, 
                        concat('{pronoun} ', {person}, ' ', E.phrase) as phrase, 
                        C.conjugation_id, 
                        E.expression_id, 
                        '{pronoun}'  as pronoun
                        from verbs.conjugations C 
                        join verbs.expressions E on E.verb = C.verb
                        where tense = '{tense}' and E.{tense_field}{validation_clause} """

                if verb_list and len(verb_list) > 0:
                    for v in verb_list:
                        unions.append(sqlStatement+f" and C.verb = '{v}'")
                else:
                    unions.append(sqlStatement)

        union_string: str = '\nunion distinct\n'.join(unions)
        sql_statement = f"""select verb, tense, phrase, conjugation_id, expression_id, pronoun 
            from ({union_string}) X1 
            order by verb, tense"""
        self.sql_statement = sql_statement


if __name__ == "__main__":
    verbs = Database(database="postgres", user="postgres", password="chinois1", host="127.0.0.1", port="5432")
    verbs.set_query(["i", "he"], ["past"], ["being"])

    page_size_num = 25
    offset_num = 0
    for i in range(100):
        rows = verbs.fetch_rows(page_size=page_size_num, offset=offset_num)
        if len(rows) == 0:
            break
        print("\n---fetch---")
        for r in rows:
            print("%r" % r.to_string())
        offset_num += page_size_num

    pass
