from source.alexa_skill_surface import start_session


def test_handle_start_conjugation():
    # Alexa conjugate verbs
    pass


def test_handle_start_random(language, dialect, speed, pronouns, tenses, verbs):
    # Alexa random verbs
    start_session(language, dialect, speed, pronouns, tenses, verbs)


def test_answer():
    # answer intent
    # if not complete
    #   get next()
    pass


def test_repeat():
    # answer intent
    # if not complete
    #   get next()
    pass


if __name__ == "__main__":
    test_handle_start_random(language="spanish", dialect="mexico", speed="slow", pronouns="he she", tenses="future past", verbs="be stay")
    test_answer()
    test_repeat()

