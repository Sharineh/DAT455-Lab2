FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive

ENV TZ=Europe/London

RUN apt update && apt upgrade -y && apt install -y python3 python3-pip


RUN apt-get install -y python3-tk

COPY  ./src /app

COPY requirements.txt /app

WORKDIR /app

CMD ["python3","graphicsmain.py"]