FROM ubuntu:20.04

LABEL maintainer "staka@vole.jp"

RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y tzdata
ENV TZ=Asia/Tokyo 

RUN apt-get install -y language-pack-ja-base language-pack-ja
RUN locale-gen en_US.UTF-8  
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8

RUN apt-get install -y git curl cmake build-essential python3-pip libpq-dev python-dev python3-setuptools
RUN pip3 install openpyxl jupyter ipython
ENTRYPOINT ["tail", "-f", "/dev/null"]
