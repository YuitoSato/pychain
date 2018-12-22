FROM base_pychain-base

ENV LANG C.UTF-8

ARG project_dir=/usr/src/app/

ADD * $project_dir
WORKDIR $project_dir

ARG node_number
ENV node_number=$node_number

RUN chmod +x docker-entrypoint.sh
ENTRYPOINT "docker/docker-entrypoint.sh" $node_number
