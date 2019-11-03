

"""
    "es-ES": dict(VoiceId='Conchita', TargetLanguageCode="es"),
    "es-MX": dict(VoiceId='Mia', TargetLanguageCode="es"),
    "es-US": dict(VoiceId='Lupe', TargetLanguageCode="es"),
    "it-IT": dict(VoiceId='Giorgio', TargetLanguageCode="it"),
    "fr-FR": dict(VoiceId='Mathieu', TargetLanguageCode="fr"),
    "fr-CA": dict(VoiceId='Chantal', TargetLanguageCode="fr")

"""
from source.application_main import AudioManager
from source.configure import Configuration
from source.database import Database
from source.storage_local import LocalStorage
from source.translator import Translator


class SkillSurface(object):
    locales = {
        "spanish": ("es", "MX"),
        "french": ("fr", "FR"),
        "italian": ("it", "IT")
    }

    dialects = {
        "mexico": "MX",
        "spain": "ES",
        "united states": "US",
        "italy": "IT",
        "france": "FR",
        "canadian": "CA"
    }
    voices = {
        "es-ES": 'Conchita',
        "es-MX": 'Mia',
        "es-US": 'Lupe',
        "it-IT": 'Giorgio',
        "fr-FR": 'Mathieu',
        "fr-CA": 'Chantal'
    }

    def __init__(self):
        pass

    def start(self):
        # start asking questions
        # valid state = collecting
        pass

    def next_flash_card(self):
        # go to next
        # valid state = in-progress
        pass

    def previous_flash_card(self):
        # go to previous
        # valid state = in-progress
        pass

    def repeat_flash_card(self):
        # go to previous
        # valid state = in-progress
        pass

    def cancel_session(self):
        # end asking questions
        # valid state = any
        pass

    def queue_more_flash_cards(self, language, dialect, speed, pronouns, tenses, verbs):
        # user queues more cards to collection before starting 
        # valid state = collecting
        pass

    def initialize_flash_card_session(self, language, dialect, speed, pronouns, tenses, verbs) -> dict:
        # intent to start a new collection of quiz's
        # valid state = none
        # valid state = any -> cancel
        target = self.locales[language]
        target_lang = target[0]
        target_dialect = target[0]
        if dialect is not None:
            target_dialect = self.dialects[dialect]
        locale = f"{target_lang}-{target_dialect}"
        voice = self.voices[locale]
        session_data = dict(
            state="start",
            source_language="en",
            dest_language=target_lang,
            dialect=target_dialect,
            voice=voice,
            speed=speed,
            pronouns=pronouns,
            tenses=tenses,
            verbs=verbs,
            offset=0,
            page_size=1
        )
        f = self.generate_flash_cards(session_attributes=session_data)
        flash_card, session_attributes = next(f)

    def generate_flash_cards(self, session_attributes):
        # get the configurations
        # valid state = ?? collecting or in-progress
        config = Configuration.get_instance()

        # get the Database
        verbs = Database.get_instance()

        # get query parameters from the session
        pronouns = None
        tenses = None
        verb_list=None
        speed="slow"
        offset_num = 0
        page_size_num = 1
        if 'pronouns' in session_attributes:
            pronouns = session_attributes['pronouns'].split(",")
        if 'tenses' in session_attributes:
            tenses = session_attributes['tenses'].split(",")
        if 'verbs' in session_attributes:
            verb_list = session_attributes['verbs'].split(",")
        if 'offset' in session_attributes:
            offset_num = int(session_attributes['offset'])
        if 'page_size' in session_attributes:
            page_size_num = int(session_attributes['page_size'])
        if 'speed' in session_attributes:
            speed = int(session_attributes['speed'])

        # create a query
        verbs.set_query(pronouns, tenses, verb_list)

        # get the translator for the destination language
        spanish_translator = Translator(source_lang=session_attributes["source_language"], target_lang=session_attributes["dest_language"])

        # configuration
        storage_mgr =config.get_file_manager()
        player = config.get_player()
        audio_handler = AudioManager(player=player, file_manager=storage_mgr, target_speed=speed)

        for i in range(page_size_num):
            rows = verbs.fetch_rows(page_size=page_size_num, offset=offset_num)
            if len(rows) == 0:
                break
            print("\n---fetch---")
            for r in rows:
                print("%r" % r.to_string())
                flash_card = spanish_translator.translate(r)
                # audio_handler.play(flash_card=flash_card)
                offset_num += 1
                session_attributes['offset'] = offset_num
                yield flash_card, session_attributes
