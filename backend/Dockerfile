FROM python:3.11
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

WORKDIR /app
COPY requirements.txt .

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

RUN python -m pip install --upgrade pip && \
    pip install pip-tools && \
    pip install -r requirements.txt

COPY . .

CMD ["bash", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
