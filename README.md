# Voice Chat Bot using Gradio and Python
Note: this was compiled using M1 ARM architecture

## Important Notes
Ensure that you have the ffmpeg library installed on your machine

### Pending Actions
1. Adjust the temperature and token_count on openai responses
2. Change the system:content string to adjust and make it as accurate as possible

## Containerizing 
You should only need the following items in your requirements.txt and should be able to omit many of the packages in the current file.

Required Packages: 
- gradio
- openai
- requests
- python-decouple
- pydub

Run application
```console
touch requirements.txt 
touch .env 
docker build -t gradio-bot .
docker run -d -p 7860:7860 gradio-bot
```

Note:
Ensure you have the following variables in `.env` file:
`OPENAI_API_KEY`=sk
`ELEVEN_LABS_API_KEY`=
