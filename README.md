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

### Containerizing: Volumes
Sure, Docker volumes are the preferred mechanism for persisting data generated by and used by Docker containers. Docker volumes have several advantages:

- Volumes are easier to back up or migrate than bind mounts.
- You can manage volumes using Docker CLI commands or the Docker API.
- Volumes work on both Linux and Windows containers.
- Volumes can be more safely shared among multiple containers.
- Volume drivers allow you to store volumes on remote hosts or cloud providers, to encrypt the contents of volumes, or to add other functionality.

In your case, the application creates `output.mp3` and `output.wav` files. To ensure these files are not lost when the container stops, you might want to create a volume for the `/app` directory where these files are created.

First, you would define a volume in your Dockerfile with the `VOLUME` command:

```Dockerfile
# Define a volume for the /app directory
VOLUME /app
```

Then, when you run your Docker container, you can use the `-v` option to specify the volume:

```bash
docker run -p 8000:8000 -v /path/to/your/host/directory:/app spanishtutor
```

This command will map `/path/to/your/host/directory` on your host machine to the `/app` directory in the Docker container. Now, any files that are created in the `/app` directory in the container (like `output.mp3` and `output.wav`) will also appear in `/path/to/your/host/directory` on your host machine, and they will persist even after the container stops.

Do note that you need to replace `/path/to/your/host/directory` with the actual path on your host machine where you want the files to be stored.

Please remember that using Docker volumes for sensitive data also has security implications, as the data is persisted on the host machine and could potentially be accessed by other users or applications. Therefore, make sure to secure your volume directories appropriately.
