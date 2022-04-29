FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
  software-properties-common \
  python3-pip \
  libpq-dev \
  build-essential

RUN mkdir /kafka_manager_api

COPY *.py /kafka_manager_api
COPY kafka_manager /kafka_manager_api/kafka_manager
COPY kafka_manager_app /kafka_manager_api/kafka_manager_app
COPY requirements.txt /kafka_manager_api
COPY dev_requirements.txt /kafka_manager_api

RUN cd /kafka_manager_api && \
  pip3 install -r requirements.txt && \
  pip3 install -r dev_requirements.txt

WORKDIR /kafka_manager_api
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8888"]
