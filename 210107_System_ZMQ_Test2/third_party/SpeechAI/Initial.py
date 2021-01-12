import pyaudio
import wave

class Records: #레코드 관련 초기값 객체 (Record-related initial value object)
    
    FORMAT = pyaudio.paInt16
    CHANNELS = 1  #only mono
    RATE = 16000  #음성데이터의 sampling rate (Sample rate of audio data)
    CHUNK = 1024  #음성데이터 불러올 때 한번에 몇개의 정수를 불러올 지 (How many integers will be called at a time when calling up voice data?)
    #여기서는 한번에 1024개의 정수 불러옴 (Call up 1024 integers at a time here)
    RECORD_SECONDS = 3 #3초 녹음 (Recording 3 second)
    frames = []
    audio = pyaudio.PyAudio()

class Path: #경로 초기값 객체(Path initial value object), path_example = Path('C:/Users/hmkwon/Desktop/speech_1/STT_Plus_TTT.json', r"C:/Users/hmkwon/Desktop/speech_1/file.wav", "C:/Users/hmkwon/Desktop/speech_1/output.wav")
    
    credential_directory = ''
    remove_record_file = ""
    output_path = ""
    
    def __init__(self, cre_dir='', remove_ipt_dir="", opt_dir=""):
        self.credential_directory = cre_dir
        self.remove_record_file = remove_ipt_dir
        self.output_path = opt_dir
            
class makeRecordFile: #음성 파일 만들기 객체 (make record file object)
    
    output_wave_file = ""
    rec_init = Records()
    
    def __init__(self, opwvf): #create_file = makeRecordFile(input_text.WAVE_OUTPUT_FILENAME)
        self.output_wave_file = opwvf
    
    def make_file(self): #파일 생성 (make file), create_file.make_file()
        waveFile = wave.open(self.output_wave_file, 'wb')
        waveFile.setnchannels(self.rec_init.CHANNELS)
        waveFile.setsampwidth(self.rec_init.audio.get_sample_size(self.rec_init.FORMAT))
        waveFile.setframerate(self.rec_init.RATE)
        waveFile.writeframes(b''.join(self.rec_init.frames))
        print(waveFile.getnframes())
        #self.rec_init.frames = []
        waveFile.close()