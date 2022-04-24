FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
  software-properties-common \
  python3-pip \
  libpq-dev \
  build-essential

RUN mkdir /code

COPY *.py /code/
COPY kafka_manager /code/kafka_manager
COPY ./requirements.txt /code/
COPY ./dev_requirements.txt /code/

RUN pip3 install -r /code/requirements.txt && \
  pip3 install -r /code/dev_requirements.txt

WORKDIR /code
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8888"]
