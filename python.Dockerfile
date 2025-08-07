FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt upgrade -y
RUN apt install -y python3.11 python3.11-dev python3-pip
RUN apt install -y libpq-dev
RUN apt install -y git --fix-missing
RUN apt install -y libmagic1

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip

RUN python3.11 -m pip install --no-cache-dir -r requirements.txt

SHELL [ "/bin/bash", "-c" ]
