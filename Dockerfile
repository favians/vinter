FROM python:3.7.5-slim-stretch

MAINTAINER Vinter "Virtual-Internship"

WORKDIR /app

RUN mkdir storage && \
    mkdir storage/log && \
    touch storage/log/app.log

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT [ "python3", "app.py" ]

