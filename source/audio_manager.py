import boto3

from source.model import AudioPlayer, StorageManager, FlashCard


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





