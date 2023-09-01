FROM python:3.8-alpine

RUN apk update && apk upgrade

RUN apk add gcc musl-dev python3-dev libxslt-dev

RUN pip install pip==23.2.1

WORKDIR /usr/app

COPY requirements.txt /usr/app

RUN pip install -r /usr/app/requirements.txt

COPY src/ /usr/app

EXPOSE 80

ARG APP_VERSION=dev

ENV APP_VERSION=$APP_VERSION

ENTRYPOINT ["gunicorn", "-b", ":80", "bringel.wsgi"]
