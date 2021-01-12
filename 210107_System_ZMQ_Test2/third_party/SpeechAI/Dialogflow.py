"""
#   Digital Human Project
#   - Speech AI (TTT)
#
#   Lasted updates : 2021.01.11.
"""

import time
import dialogflow_v2 as dialogflow
from google.oauth2 import service_account

class Dialogflow :
    texts = ""
    cre_dir = ""
    project_id = ""
    text = ""
    
    def __init__(self, input_text, credir, project_id) :
        self.texts = input_text
        self.cre_dir = credir
        self.project_id = project_id

    def run_ttt(self) :
        def get_day() :
            now = time.localtime(time.time())
            daylist = ['월', '화', '수', '목', '금', '토', '일']
            return daylist[now.tm_wday]
        
        credentials = service_account.Credentials.from_service_account_file(self.cre_dir)
        session_client = dialogflow.SessionsClient(credentials = credentials)
        
        session = session_client.session_path(self.project_id, 
                                              '123456')
        
        text_input = dialogflow.types.TextInput(text = self.texts, 
                                                language_code = 'ko_KR')
        
        query_input = dialogflow.types.QueryInput(text = text_input)
    
        response = session_client.detect_intent(session = session,
                                                query_input = query_input)
        
        text = response.query_result.fulfillment_text
        
        print('=' * 20)
        print(f'Query text: {response.query_result.query_text}')
        print(f'Detected intent: {response.query_result.intent.display_name} (confidence: {response.query_result.intent_detection_confidence})\n')
        print(f'Fulfillment text: {response.query_result.fulfillment_text}\n')
        
        now = time.localtime()
        what_time_is_it = ["hour", "min"] # Main trigger of ask Time
        what_is_the_date_today = ["month", "date"] # Main trigger of ask Date
        what_is_the_day_today = ["day"] # Main trigger of ask Day
        day_of_the_week = get_day() # Get Day of the Week
        
        if what_time_is_it[0] in text:
            return(text.replace('hour', str(now.tm_hour)).replace('min', str(now.tm_min)))
        
        elif what_is_the_date_today[0] in text:
            return(text.replace('month', str(now.tm_mon)).replace('date', str(now.tm_mday)))
        
        elif what_is_the_day_today[0] in text:
            return(text.replace('day', str(day_of_the_week)))
        
        else:
            return(text)