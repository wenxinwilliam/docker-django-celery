FROM python:3.4

ADD . /app/

WORKDIR /app/
RUN pip install -r requirements.txt
RUN adduser --disabled-password --gecos '' myuser