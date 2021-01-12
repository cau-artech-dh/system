"""
Pyzmq test
- tcp 통신
- PULL / PUSH 방법
- 벤틸레이터 (producer) of Speech

Last Updated : 2021.01.11.

@author: Hannah_Noh
"""

## 동기 방식

import zmq
import asyncio
import zmq.asyncio
import nest_asyncio
import numpy as np
import time
import os
import argparse

from third_party.SpeechAI.SpeechToText import Speech2Text
from third_party.SpeechAI.Dialogflow import Dialogflow
from third_party.SpeechAI.TextToSpeech import Text2Speech

from third_party.SpeechAI.Initial import Records
from third_party.SpeechAI.Initial import Path
from third_party.SpeechAI.Initial import makeRecordFile

project_id = "korea-tfti" # Dialogflow project id
cre_dir = r'.\third_party\SpeechAI\STT_Plus_TTT.json' # Dialogflow project inofrmation json file
remove_ipt_dir = r".\file.mp3" # 지울 녹음파일 경로
opt_dir = r"output.wav" # 대답 음성 파일 저장 경로

# 약 알림 시간 설정
drug_hour = 17
drug_min = 30
drug_sec = 0

'''SPEECH VENTILATOR : 5558'''
port = 5558

ctx = zmq.asyncio.Context()
sock = None
'''
async def run_ventilator(text, file_path) :
    global sock

    if sock == None :
        # sock push 소켓 : 워커들에게 데이터를 전송하기 위한 것
        sock = ctx.socket(zmq.PUSH)
        sock.bind(f'tcp://*:{port}') # 따라서 sock은 바인딩
    
    file_path = os.path.join(os.path.dirname(__file__)) + "\\" + file_path
    msg = {'발화문' : text,
           '파일주소' : file_path}
    await sock.send_json(msg)
'''
"""
#   def get_day()
#
#   : 현재 요일을 반환(localtime 기준)
"""
def get_day() :
    now = time.localtime(time.time())
    daylist = ['월', '화', '수', '목', '금', '토', '일']
    return daylist[now.tm_wday]

"""
#   def loop_recording(proj_id, critical_loudness, record_time)
#
#   : 녹음 시작 및 분석
#   : proj_id - 프로젝트 아이디
#   : critical_loudness - 임계 볼륨
#   : record_time - 녹음 시작으로부터 몇초동안 녹음
"""
def loop_recording(proj_id, critical_loudness, record_time) :
    rec_init = Records()
    path_init = Path()
    
    path_init.credential_directory = cre_dir
    path_init.remove_record_file = remove_ipt_dir
    path_init.output_path = opt_dir
    path_init.project_id = proj_id

    #_data = 0
    loudness = 0 # volume value
    trigger = False # trigger
    sec = time.time() # Get time to start recording
    text = ''
    
    drug_text = '약 드실 시간입니다.'
    drug_alarm = Text2Speech(drug_text, 
                             path_init.credential_directory, 
                             path_init.output_path)
    
    input_text = Speech2Text("file.mp3", 
                             path_init.credential_directory)
    
    create_file = makeRecordFile(input_text.WAVE_OUTPUT_FILENAME)
    
    # Turn on the microphone and start recording
    stream = rec_init.audio.open(format = rec_init.FORMAT, 
                                 channels = rec_init.CHANNELS,
                                 rate = rec_init.RATE, 
                                 input = True,
                                 frames_per_buffer = rec_init.CHUNK)
    print ("recording...")
    
    while(True):
        # (Current time) - (Recording start time) = Time past the start of recording
        delta_time = time.time() - sec
        print("time :", delta_time)
        
        # 음량값 계산
        data = np.fromstring(stream.read(rec_init.CHUNK), dtype = np.int16)
        loudness = int(np.average(np.abs(data)))
        rec_init.frames.append(data)
        print(loudness)
        #_data = _data + 1
        
        # 복용 시간 알람
        time_trig = False
        drug_time = time.localtime(time.time())
        
        if drug_time.tm_hour == drug_hour and drug_time.tm_min == drug_min and drug_time.tm_sec == drug_sec:
            time_trig = True
            
        # 복용 시간 추가
        if time_trig == True :
            '''
            # Stop Recording
            stream.stop_stream()
            stream.close()
            '''
            text = drug_text
            
            drug_alarm.run_tts() # Drug Notification TTS
            
            # Initializing
            time_trig = False
            sec = time.time()
            delta_time = 0
            '''
            stream = rec_init.audio.open(format = rec_init.FORMAT, 
                                         channels = rec_init.CHANNELS,
                                         rate = rec_init.RATE, 
                                         input = True,
                                         frames_per_buffer = rec_init.CHUNK) 
            print ("recording...")
            '''
            #continue
        
        # if only the noise was recorded for 10 seconds, Destroy audio files
        if delta_time > 5 and loudness < critical_loudness and trigger == False :
            
            '''
            # Stop Recording
            stream.stop_stream() 
            stream.close()
            '''  
            create_file.make_file() # create record file
            os.remove(path_init.remove_record_file) # clear recording file
            
            # Initializing
            sec = time.time()
            delta_time = 0

            for i in reversed(range(len(rec_init.frames))):
                del rec_init.frames[i]
            
            #_data = 0
            '''
            stream = rec_init.audio.open(format = rec_init.FORMAT, 
                                         channels = rec_init.CHANNELS,
                                         rate = rec_init.RATE, 
                                         input = True,
                                         frames_per_buffer = rec_init.CHUNK) 
            
            print ("recording...")
            '''
        # If the volume is above the critical volume value and trigger == False, replace it with trigger == True
        if loudness >= critical_loudness and trigger == False :
            print("\nIt's over a critical volume.\n")
            sec = time.time()
            delta_time = 0
            trigger = True
        
        # Start main recording 
        if trigger : 
            # Send file to server more than 3 seconds after recording starts
            if delta_time > record_time :
                '''
                # Stop Recording
                stream.stop_stream()
                stream.close()
                '''
                # create record file
                create_file.make_file()
                save_STT_output = input_text.run_stt() # Save STT output
                
                # 의미 없는 큰 소리가 발생했을 경우, STT에 대한 예외 처리
                if save_STT_output == "nothing" :
                    pass

                # 이외, Dialogflow에서 대화 처리
                else:
                    output_text = Dialogflow(save_STT_output, 
                                             path_init.credential_directory,
                                             path_init.project_id)
                    
                    text = output_text.run_ttt()
                    
                    output_file = Text2Speech(text, 
                                              path_init.credential_directory, 
                                              path_init.output_path)
                    
                    output_file.run_tts()
                
                # Initializing
                output_text = ""
                trigger = False
                sec = time.time()
                delta_time = 0
                
                for i in reversed(range(len(rec_init.frames))):
                    del rec_init.frames[i]

                '''
                stream = rec_init.audio.open(format = rec_init.FORMAT, 
                                             channels = rec_init.CHANNELS,
                                             rate = rec_init.RATE, 
                                             input = True,
                                             frames_per_buffer = rec_init.CHUNK)
                print ("recording...")
                '''
        else :
            text = "음성이 인식되지 않았습니다."
        
        print(text)
        #asyncio.run(run_ventilator(text, path_init.output_path))

"""
#   def main()
#
#   : main method
"""
def main() :
    global project_id, cre_dir

    # 이하는 parsing 기능입니다. 터미널에서 작동시킬 경우에만 동작
    parser = argparse.ArgumentParser("Select speech type first")
    parser.add_argument("--option", 
                        "-o", 
                        type = int, 
                        choices = [1,2], 
                        help = "select speech type\n- 1 : polite speech\n- 2 : informal speech")
    args = parser.parse_args()
    
    # 반/존댓말 스위칭
    #   - 'korea-tfti' 존댓말 프로젝트, '.\STT_Plus_TTT.json' 존댓말 프로젝트의 인증키 파일
    #   - 'responsive-gist-284604' 반말 프로젝트, '.\Integration_2.json' 반말 프로젝트의 인증키 파일
    if args.option == 1:
        project_id = "korea-tfti"
        cre_dir = r'.\SpeechAI\STT_Plus_TTT.json'
        
    elif args.option == 2:
        project_id = "responsive-gist-284604"
        cre_dir = r'.\SpeechAI\Integration_2.json'
    
    # 음성 분석 및 대답        
    loop_recording(project_id, 6000, 3)

if __name__ == '__main__' :
    #nest_asyncio.apply()
    main()