import json
import os
from abc import abstractmethod


class FlashCard:
    def __init__(self, conjugated: str, infinitive: str, source_lang: str, source_phrase: str, tense: str, conjugation_id: str, expression_id: str, pronoun: str):
        self.id = f"{conjugation_id}-{expression_id}"
        # self.conjugated_verb = conjugated
        self.infinitive_form = "to " + infinitive
        self.source_lang = source_lang
        self.tense = tense
        self.pronoun = pronoun.title()
        self.source_phrase = pronoun.title() + " " + conjugated + " " + source_phrase
        self.dest_lang = None
        self.dest_phrase = None
        self.dest_voice = None
        self.buffer = None
        self.url = None
        self.meta_data = None

    def to_string(self):
        return json.dumps(self.__dict__)


class StorageManager:
    def __init__(self):
        self.flash_card = None

    def set_flash_card(self, flash_card: FlashCard):
        path = os.path.join(f"{flash_card.source_lang}-{flash_card.dest_lang}",
                            flash_card.conjugated_verb, flash_card.tense, flash_card.pronoun)
        flash_card.url = f"{path}/{flash_card.id}.mp3"
        flash_card.meta_data = {'language': flash_card.dest_lang, 'phrase': flash_card.dest_phrase}
        self.flash_card = flash_card

    @abstractmethod
    def write_audio(self, buffer: bytes) -> str:
        raise Exception("Cannot call abstract method")

    @abstractmethod
    def read_audio(self) -> (dict, bool):
        raise Exception("Cannot call abstract method")

    @abstractmethod
    def check_exists(self) -> bool:
        raise Exception("Cannot call abstract method")


class AudioPlayer:

    @abstractmethod
    def play_audio(self, url: bytes):
        # call self.url_manager.get_audio_url(flashcard)
        # if not exists:
        #    create audio with Polly
        #    self.url_manager.create_audio_url(flash_card)
        # play(url)
        raise Exception("Cannot call abstract method")


