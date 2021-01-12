import os

from google.oauth2 import service_account

class Speech2Text: #STT 객체(Speech-to-Text object), input_text = Speech2Text("file.wav", path_example.creditialDirectory)
    
    WAVE_OUTPUT_FILENAME = ""
    cre_dir = ""
    
    def __init__(self, rec_file_name, credir):
        self.WAVE_OUTPUT_FILENAME = rec_file_name #녹음파일명 (Recording file name)
        self.cre_dir = credir
        
    def run_stt(self):
        # [START speech_quickstart]
        import io
        #import os
    
        # Imports the Google Cloud client library
        # [START migration_import]
        from google.cloud import speech
        # from google.cloud.speech import enums
        # from google.cloud.speech import types
        
        # [END migration_import]
        
        credentials = service_account.Credentials.from_service_account_file(self.cre_dir)
        
        # Instantiates a client
        # [START migration_client]
        client = speech.SpeechClient(credentials=credentials)
        # [END migration_client]
    
        # The name of the audio file to transcribe
        file_name = os.path.join(os.path.dirname(__file__))
        file_name = file_name.split('\\')
        file_name = '\\'.join(file_name[:-2])
        file_name = file_name + '\\' + self.WAVE_OUTPUT_FILENAME
        
        # Loads the audio into memory
        with io.open(file_name, 'rb') as audio_file:
            content = audio_file.read()
            audio = speech.RecognitionAudio(content=content)
    
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code='ko-KR')
    
        # Detects speech in the audio file
        response = client.recognize(config=config, audio=audio)
        try:
            for result in response.results:
                pass
                #print('Transcript: {}'.format(result.alternatives[0].transcript))
    
            print('Transcript: {}'.format(result.alternatives[0].transcript))
                
            return(result.alternatives[0].transcript)
        except UnboundLocalError:
            return("nothing")