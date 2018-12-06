FROM python:3.6

ENV LANG C.UTF-8

ARG project_dir=/usr/src/app/
ARG port="5001"
ENV port=$port

COPY * $project_dir

WORKDIR $project_dir
RUN pip install -r requirements.txt

EXPOSE $port

CMD python app.py ${port}
