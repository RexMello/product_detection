RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
web: gunicorn app:app --host 0.0.0.0 --port $PORT