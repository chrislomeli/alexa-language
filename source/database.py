from typing import List

import psycopg2


# db = psycopg2.connect(
#     database="postgres",
#     user="postgres",
#     password="chinois1",
#     host="127.0.0.1",
#     port="5432")


class Database(object):
    pronouns = {
        "i": ("first_person", "valid_i"),
        "he": ("third_person", None),
        "she": ("third_person", None),
        "it": ("third_person", None),
        "you": ("first_person", "valid_you"),
        "we": ("first_person", "valid_we"),
        "they": ("first_person", "valid_their"),
    }

    tenses = {
        "present": "present_tense",
        "past": "past_tense",
        "future": "future_tense",

    }

    def __init__(self, user: str, password: str, url: str, port: str, database: str):
        self.sql_statement = ""
        self.connection = psycopg2.connect(
            database=database,
            user=user,
            password=password,
            host=url,
            port="5432")

    def fetch_rows(self, offset, page_size) -> List[dict]:
        sql = self.sql_statement + f""" limit {page_size} offset {offset}"""
        cur = self.connection.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        response = []
        for row in rows:
            response.append(dict(verb=row[0], tense=row[1], phrase=row[2], conjugationId=row[3], expressionId=row[4]))
        return response

    def set_query(self, pronouns: List[str], tenses: List[str]):
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
                sqlStatement: str = f"""select C.verb, C.tense, 
                concat('{pronoun} ', {person}, ' ', E.phrase) as phrase, C.conjugation_id, E.expression_id
                    from verbs.conjugations C 
                    join verbs.expressions E on E.verb = C.verb
                    where tense = '{tense}' and E.{tense_field}{validation_clause} """
                unions.append(sqlStatement)

        union_string: str = '\nunion distinct\n'.join(unions)
        sql_statement = f"""select verb, tense, phrase, conjugation_id, expression_id from ({union_string}) X1 
        order by verb, tense"""
        self.sql_statement = sql_statement


if __name__ == "__main__":
    verbs = Database(database="postgres", user="postgres", password="chinois1", url="127.0.0.1", port="5432")
    verbs.set_query(["we"], ["future", "past"])

    page_size = 25
    offset = 0
    for i in range(100):
        rows = verbs.fetch_rows(page_size=page_size, offset=offset)
        if len(rows) == 0:
            break
        print("\n---fetch---")
        for r in rows:
            print("%r" % r)
        offset += page_size

    pass
