import boto3

voices = {
    "es-ES": dict(VoiceId='Conchita', TargetLanguageCode="es"),
    "es-MX": dict(VoiceId='Mia', TargetLanguageCode="es"),
    "es-US": dict(VoiceId='Lupe', TargetLanguageCode="es"),
    "it-IT": dict(VoiceId='Giorgio', TargetLanguageCode="it"),
    "fr-FR": dict(VoiceId='Mathieu', TargetLanguageCode="fr"),
    "fr-CA": dict(VoiceId='Chantal', TargetLanguageCode="fr")
    
}


class Translator(object):
    def __init__(self, target_lang, target_speed):
        self.translate_client = boto3.client(service_name='translate', region_name='us-east-1', use_ssl=True)
        self.polly_client = boto3.Session(region_name='us-west-2').client('polly')
        self.target_lang = target_lang
        self.target_speed = target_speed
        self.metadata = voices[self.target_lang]
        self.target_language_code = self.metadata["TargetLanguageCode"]
        self.voice_id = self.metadata["VoiceId"]
        
    def translate_text(self, english_text, verb_tense):
        result = self.translate_client.translate_text(Text=english_text,
                                                 SourceLanguageCode="en", TargetLanguageCode=self.target_language_code)
        
        verb_tense = "%s-%s.mp3" % (self.target_lang, verb_tense)
        translated_text = result.get('TranslatedText')
        print('TranslatedText: ' + translated_text)
        
        ssml_text = """<speak><prosody rate="%s">%s</prosody></speak>""" % (self.target_speed, translated_text)
        response = self.polly_client.synthesize_speech(
            VoiceId=self.voice_id,
            OutputFormat='mp3',
            SampleRate="24000",
            TextType="ssml",
            Text=ssml_text)
        
        file = open(verb_tense, 'wb')
        file.write(response['AudioStream'].read())
        file.close()


spanish_translator = Translator("es-MX", "x-slow")

spanish_translator.translate_text(english_text="I had money", verb_tense="to-have-past")
spanish_translator.translate_text(english_text="I'll have money", verb_tense="to-have-future")
