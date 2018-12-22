FROM python:3.6

ENV LANG C.UTF-8

ARG project_dir=/usr/src/app/

ADD requirements.txt $project_dir
WORKDIR $project_dir

RUN apt-get -y upgrade
RUN apt-get -y update
RUN apt-get -y install sqlite3 libsqlite3-dev

#RUN apt-get install sqlite3 libsqlite3-dev -y
RUN pip install -r requirements.txt
