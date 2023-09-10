FROM python:3.8-alpine

RUN apk update && apk upgrade

RUN apk add gcc musl-dev python3-dev libxslt-dev libffi-dev

RUN pip install pip==23.2.1

RUN adduser -D user

USER user

ENV PATH="$PATH:/home/user/.local/bin"

WORKDIR /usr/app

COPY --chown=user:user requirements.txt /usr/app

RUN pip install -r /usr/app/requirements.txt

COPY --chown=user:user entrypoint.sh  /usr/app

COPY --chown=user:user src/ /usr/app

EXPOSE 80

ARG APP_VERSION=dev

ENV APP_VERSION=$APP_VERSION

ARG APP_MODE=web

ENV APP_MODE=$APP_MODE

ENTRYPOINT ["/usr/app/entrypoint.sh"]
