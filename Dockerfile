FROM python:3.8.0-alpine
WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN apk add make
RUN apk add build-base

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

COPY . /usr/src/app/

EXPOSE 5000
CMD ["flask", "db", "upgrade"]
CMD ["gunicorn"  , "-b", "0.0.0.0:5000", "wsgi:app"]