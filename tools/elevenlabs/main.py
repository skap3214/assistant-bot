#Weird import buy fix
import sys
sys.path.append("")

#ELEVEN_LABS function requirements
import requests
import playsound
import os
#Langchain requirements
from langchain.agents import Tool

#api key
from decouple import config
ELEVENLABS_API_KEY = config('ELEVEN_LABS')

def convert_text_to_speech(
        text, 
        voice_id='21m00Tcm4TlvDq8ikWAM', 
        optimize_streaming_latency=0, 
        xi_api_key=ELEVENLABS_API_KEY):
    url = f'https://api.elevenlabs.io/v1/text-to-speech/{voice_id}'
    headers = {'xi-api-key': xi_api_key}
    params = {'optimize_streaming_latency': optimize_streaming_latency}
    payload = {'text': text}

    response = requests.post(url, headers=headers, params=params, json=payload)
    
    if response.status_code == 200:
        # Assuming the response contains audio, you can save it to a file
        audio_file_path = 'output.wav'
        with open(audio_file_path, 'wb') as f:
            f.write(response.content)
    else:
        print(f'Request failed with status code: {response.status_code}')
    playsound.playsound('output.wav')
    os.remove('output.wav')
    return "Answer spoken successfully!"

text_to_speech = Tool.from_function(
    name="Text To Speech",
    func=convert_text_to_speech,
    description="Useful when needing to convert text to speech. The input to this tool should be whatever you want to convert to speech"
    )

def text_to_speech_tool():
    return [text_to_speech]
