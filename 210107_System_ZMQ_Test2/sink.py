"""
Pyzmq test
- tcp 통신
- PULL / PUSH 방법
- 싱크 (result collector)

Last Updated : 2021.01.11.

@author: Hannah_Noh
"""

## 동기 방식

import zmq
import asyncio
import zmq.asyncio
import nest_asyncio

'''UNREAL SINK : 5556'''
port = 5556

ctx = zmq.asyncio.Context()

async def run_sink() :
    sock = ctx.socket(zmq.PULL)
    sock.bind(f'tcp://*:{port}')
    
    while True :
        result = await sock.recv_json()
        
        text = result['v_발화문']
        
        print("-------------------------------------------")
        print("[Face Detection Result]") 
        print("\t>> emotion : {}".format(result['v_감정']))
        print("\t>> age : {}".format(result['v_나이']))
        print("\t>> gender : {}".format(result['v_성별']))
        print(f'\t>> 발화문 : {text}')
        print("\t>> 파일 위치 : {}".format(result['v_파일주소']))
        print("[Speech Result]")
        print("\t>> 발화문 : {}".format(result['s_발화문']))
        print("\t>> 파일 위치 : {}".format(result['s_파일주소']))
        
    ctx.destroy()
    print("###DONE###")
    

if __name__ == '__main__':
    nest_asyncio.apply()
    asyncio.run(run_sink())