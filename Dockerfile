FROM python:3.6.15-alpine3.15

WORKDIR '/app'

RUN python3 -V
RUN pip3 install virtualenv
RUN virtualenv venv
RUN source venv/bin/activate

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY main.py main.py

COPY config.example.yml config.yml
