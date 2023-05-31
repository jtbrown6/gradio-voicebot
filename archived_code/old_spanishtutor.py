import gradio as gr
import openai, requests, os
from decouple import config

openai.api_key = config("OPENAI_API_KEY")
ELEVEN_LABS_API_KEY = config("ELEVEN_LABS_API_KEY")


messages = [{"role": "system", "content": 'You are a spanish tutor for beginners. Assist the user with learning. You will also speak slowly.'}]

def convert_text_to_speech(message):
    body = {
        "text": message,
        "voice_settings": {
            "stability": 0,
            "similarity_boost": 0
        }
    }

    voice_antoni = "21m00Tcm4TlvDq8ikWAM"

    # Construct request headers and url
    headers = { "xi-api-key": ELEVEN_LABS_API_KEY, "Content-Type": "application/json", "accept": "audio/mpeg" }
    endpoint = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_antoni}"

    try:
        response = requests.post(endpoint, json=body, headers=headers)
    except Exception as e:
        print(e)
        return None

    if response.status_code == 200:
        return response.content
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
    audio_data = convert_text_to_speech(system_message['content'])
    if audio_data is None:
        print("Error generating speech output")
    else:
        with open("output.wav", "wb") as f:
            f.write(audio_data)

    chat_transcript = ""
    for message in messages:
        if message['role'] != 'system':
            chat_transcript += message['role'] + ": " + message['content'] + "\n\n"

    return chat_transcript

ui = gr.Interface(fn=transcribe, inputs=gr.Audio(source="microphone", type="filepath"), outputs="text").launch()
ui.launch()
