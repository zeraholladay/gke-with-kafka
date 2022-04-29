FROM ubuntu:latest

RUN apt-get update && apt-get install -y
RUN apt -y install curl
RUN curl -sL https://deb.nodesource.com/setup_16.x | bash -
RUN apt -y install nodejs

RUN mkdir /kafka_manager_frontend

COPY *.js /kafka_manager_frontend
COPY *.json /kafka_manager_frontend
COPY public kafka_manager_frontend/public
COPY src /kafka_manager_frontend/src

RUN cd /kafka_manager_frontend && npm install

WORKDIR /kafka_manager_frontend
CMD ["npm", "run", "serve"]
