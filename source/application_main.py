from time import sleep

import boto3

from source.database import Database
from source.model import AudioPlayer, StorageManager, FlashCard
from source.player_local import LocalPlayer
from source.storage_local import LocalStorage
from source.translator import Translator


class AudioManager(object):
    polly_client = boto3.Session(region_name='us-west-2').client('polly')

    def __init__(self, player: AudioPlayer, file_manager: StorageManager, target_speed):
        self.file_manager = file_manager
        self.player = player
        self.speed = target_speed

    def play(self, flash_card: FlashCard):
        self.file_manager.set_flash_card(flash_card=flash_card)
        if self.file_manager.check_exists():
            url = self.file_manager.read_audio()
        else:
            response = self.create_audio(flash_card=flash_card)
            url = self.file_manager.write_audio(response['AudioStream'].read())

        self.player.play_audio(url=url)
        return self.file_manager.flash_card

    def create_audio(self, flash_card: FlashCard) -> dict:
        ssml_text = """<speak><prosody rate="%s">%s</prosody></speak>""" % (self.speed, flash_card.dest_phrase)
        return self.polly_client.synthesize_speech(
            VoiceId=flash_card.dest_voice,
            OutputFormat='mp3',
            SampleRate="24000",
            TextType="ssml",
            Text=ssml_text)





def test_service(from_lang, to_lang, speed):
    verbs = Database(database="postgres", user="postgres", password="chinois1", host="127.0.0.1", port="5432")
    verbs.set_query(["she", "he"], ["past"], ["being"])

    spanish_translator = Translator(source_lang=from_lang, target_lang=to_lang)

    storage_mgr = LocalStorage("/Users/clomeli/tmp")
    # storage_mgr = S3Storage("clomeli-language-phrases")

    player = LocalPlayer()
    # player = AlexaPlayer()

    audio_handler = AudioManager(player=player, file_manager=storage_mgr, target_speed=speed)

    page_size_num = 2
    offset_num = 0
    for i in range(5):
        rows = verbs.fetch_rows(page_size=page_size_num, offset=offset_num)
        if len(rows) == 0:
            break
        print("\n---fetch---")
        for r in rows:
            print("%r" % r.to_string())
            flash_card = spanish_translator.translate(r)
            audio_handler.play(flash_card=flash_card)
            sleep(5)

        offset_num += page_size_num


if __name__ == "__main__":
    # test_service(from_lang="en_US", to_lang="it-IT", speed="slow")
    # test_service(from_lang="en_US", to_lang="fr-FR", speed="slow")
    test_service(from_lang="en_US", to_lang="es-MX", speed="slow")
