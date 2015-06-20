FROM python:3.4

ADD . /app/

WORKDIR /app/
RUN pip install -r requirements.txt
RUN adduser --disabled-password --gecos '' myuser

RUN curl -sL https://deb.nodesource.com/setup | bash -
RUN apt-get install -y nodejs
RUN npm install -g bower

RUN bash install_static.sh