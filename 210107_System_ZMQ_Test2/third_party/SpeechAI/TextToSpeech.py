from google.oauth2 import service_account

class Text2Speech: #TTS 객체 (Text-to-Speech object)

    text = ""
    voice_name = ""
    cre_dir = ""
    output_dir = ""
    
    def __init__(self, Text, credir, outputdir, voicename = 'ko-KR-Wavenet-A'): #outputFile = Text2Speech(outputText.run_ttt(), path_example.creditialDirectory, path_example.output_path), voicename은 바꿀 필요 있으면 바꾸기
        self.text = Text
        self.cre_dir = credir
        self.output_dir = outputdir
        self.voice_name = voicename
        
    def run_tts(self):
        """Synthesizes speech from the input string of text."""
        from google.cloud import texttospeech
        
        credentials = service_account.Credentials.from_service_account_file(self.cre_dir)
        
        client = texttospeech.TextToSpeechClient(credentials = credentials)
    
        input_text = texttospeech.SynthesisInput(text = self.text)
    
        # Note: the voice can also be specified by name.
        # Names of voices can be retrieved with client.list_voices().
        # ko-KR-Wavenet-B
        # ko-KR-Wavenet-C
        # ko-KR-Wavenet-D
        # ko-KR-Wavenet-A
        voice = texttospeech.VoiceSelectionParams(
            language_code = "ko-KR",
            name = self.voice_name,
            #ssml_gender = texttospeech.SsmlVoiceGender.FEMALE,
        )
    
        audio_config = texttospeech.AudioConfig(
            audio_encoding = texttospeech.AudioEncoding.MP3
        )
    
        response = client.synthesize_speech(
            request = {"input": input_text, "voice": voice, "audio_config": audio_config}
        )
    
        # The response's audio_content is binary.
        with open(self.output_dir, "wb") as out:
            out.write(response.audio_content)
            print('Audio content written to file "output.wav"')