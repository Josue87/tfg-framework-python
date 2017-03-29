FROM ubuntu:latest
MAINTAINER Josué Encinar

RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN pip3 install --upgrade pip
RUN apt-get install -y build-essential libssl-dev libffi-dev python3-dev tcpdump
RUN pip3 install scapy-python3
RUN pip3 install paramiko

RUN mkdir /src
WORKDIR /src
RUN mkdir jf
WORKDIR jf


ADD framework .

CMD ["python3","jf.py"]
