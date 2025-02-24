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

RUN python manage.py collectstatic --noinput

CMD ["bash", "-c", "gunicorn main.wsgi:application --bind 0.0.0.0:8000 --reload"]
