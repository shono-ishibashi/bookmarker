FROM python:3.9.1-alpine3.12

ENV LANG C.UTF-8
ENV TZ Asia/Tokyo
ENV PYTHONPATH /app/.pip
ENV PYTHONUNBUFFERED 1

RUN apk add --update --no-cache make bash gcc g++ tzdata git\
    && pip install --upgrade pip \
    && pip install uvicorn==0.11.8

ADD docker/wait-for-it.sh /usr/local/bin/wait-for-it.sh

RUN chmod +x /usr/local/bin/wait-for-it.sh
