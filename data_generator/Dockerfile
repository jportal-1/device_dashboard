FROM python:3.10.14-slim-bookworm

RUN apt-get -y update && apt-get install -y rabbitmq-server
COPY . /data_generator
WORKDIR /data_generator
RUN chmod +x ./start.sh
RUN pip install -r requirements.txt

CMD ["./start.sh"]