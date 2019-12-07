FROM python:2.7-slim

WORKDIR /

ADD . /

RUN apt-get update && apt-get install -y git

RUN pip install git+https://github.com/lanpa/tensorboardX \
    tensorboard \
    tensorflow \
    awscli

EXPOSE 8080

CMD tensorboard --logdir s3://test-automation-pydata/tests/ --port 8080