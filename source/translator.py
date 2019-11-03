import boto3

from source.model import FlashCard

voices = {
    "es-ES": dict(VoiceId='Conchita', TargetLanguageCode="es"),
    "es-MX": dict(VoiceId='Mia', TargetLanguageCode="es"),
    "es-US": dict(VoiceId='Lupe', TargetLanguageCode="es"),
    "it-IT": dict(VoiceId='Giorgio', TargetLanguageCode="it"),
    "fr-FR": dict(VoiceId='Mathieu', TargetLanguageCode="fr"),
    "fr-CA": dict(VoiceId='Chantal', TargetLanguageCode="fr")
}


class Translator(object):
    def __init__(self, source_lang, target_lang):
        self.translate_client = boto3.client(service_name='translate', region_name='us-east-1', use_ssl=True)
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.metadata = voices[self.target_lang]
        self.target_language_code = self.metadata["TargetLanguageCode"]
        self.voice_id = self.metadata["VoiceId"]

    def translate(self, flash_card: FlashCard):
        result = self.translate_client.translate_text(Text=flash_card.source_phrase,
                                                      SourceLanguageCode=flash_card.source_lang,
                                                      TargetLanguageCode=self.target_language_code)

        translated_text = result.get('TranslatedText')
        print('TranslatedText: ' + translated_text)
        flash_card.dest_voice = self.voice_id
        flash_card.dest_phrase = translated_text
        flash_card.dest_lang = self.target_lang
        return flash_card


