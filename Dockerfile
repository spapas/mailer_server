FROM python:2.7-alpine

RUN mkdir /code
WORKDIR /code

ADD . /code/

# RUN apt-get update && apt-get install -y libsasl2-dev python-dev libldap2-dev libssl-dev python-dev
RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add openldap-dev postgresql-dev

RUN pip install -r requirements/docker.txt

EXPOSE 8000
ENV DJANGO_SETTINGS_MODULE mailer_server.settings.docker

WORKDIR /src/

