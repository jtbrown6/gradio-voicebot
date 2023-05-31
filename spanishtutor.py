import gradio as gr
import openai, requests, os
from decouple import config
from pydub import AudioSegment

#Include this into .env file: OPENAI_API_KEY= and ELEVEN_LABS_API_KEY= WITHOUT quotes just a string

openai.api_key = config("OPENAI_API_KEY")
ELEVEN_LABS_API_KEY = config("ELEVEN_LABS_API_KEY")


messages = [{"role": "system", "content": 'You are a Spanish Tutor and your name is Maria, the user is called Jamal who is a beginner. Keep responses under 30 words and speak slowly so Jamal can understand you. Your responses should contain both english and spanish translations.'}]

def convert_text_to_speech(message):
    body = {
        "text": message,
        "voice_settings": {
            "stability": 0,
            "similarity_boost": 0
        }
    }

    voice_antoni = "ErXwobaYiN019PkySvjV"

    # Construct request headers and url
    headers = { "xi-api-key": ELEVEN_LABS_API_KEY, "Content-Type": "application/json", "accept": "audio/mpeg" }
    endpoint = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_antoni}"

    try:
        response = requests.post(endpoint, json=body, headers=headers)
    except Exception as e:
        print(e)
        return None

    if response.status_code == 200:
        with open("output.mp3", "wb") as f:  # Save as .mp3
            f.write(response.content)
        # Convert mp3 file to wav
        sound = AudioSegment.from_mp3("output.mp3")
        sound.export("output.wav", format="wav")
    else:
        print(f"Error: {response.status_code}")
        return None

def transcribe(audio):
    global messages

    audio_filename_with_extension = audio + '.wav'
    os.rename(audio, audio_filename_with_extension)
    
    audio_file = open(audio_filename_with_extension, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)

    messages.append({"role": "user", "content": transcript["text"]})

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    system_message = response["choices"][0]["message"]
    messages.append(system_message)

    # Use Eleven Labs API instead of macOS subprocess for text-to-speech conversion
    convert_text_to_speech(system_message['content'])
    chat_transcript = ""
    for message in messages:
        if message['role'] != 'system':
            chat_transcript += message['role'] + ": " + message['content'] + "\n\n"

    return chat_transcript, 'output.wav'  # Return the path to the wav file as the second output

ui = gr.Interface(fn=transcribe, inputs=gr.Audio(source="microphone", type="filepath"), outputs=["text", gr.outputs.Audio(type="filepath")]).launch()
ui.launch()

"""
URL: http://127.0.0.1:7860
How to Suppress warnings.

import warnings

# ... rest of your code ...

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    ui = gr.Interface(fn=transcribe, inputs=gr.Audio(source="microphone", type="filepath"), outputs=["text", gr.outputs.Audio(type="filepath")])
ui.launch()


"""