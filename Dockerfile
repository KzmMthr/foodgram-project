FROM python:3.8.5

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV APP_HOME=/code

COPY ./requirements.txt .

RUN python3 -m pip install --upgrade pip \
    && pip install -r requirements.txt --no-cache-dir \
    && rm requirements.txt

WORKDIR $APP_HOME
COPY . $APP_HOME

CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000