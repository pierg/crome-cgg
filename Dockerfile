FROM continuumio/miniconda3 AS build

COPY environment.yml .
RUN conda env create -f environment.yml

# Use conda-pack to create a standalone enviornment in /venv:
RUN conda install -c conda-forge conda-pack
RUN conda-pack -n crome-cgg -o /tmp/env.tar && \
  mkdir /venv && cd /venv && tar xf /tmp/env.tar && \
  rm /tmp/env.tar
RUN /venv/bin/conda-unpack


FROM pmallozzi/ltltools:latest AS runtime

RUN apt-get -y update
RUN apt-get -y install git

WORKDIR /home

ENV GIT_SSL_NO_VERIFY=1
COPY . /home/crome-cgg
RUN git clone https://github.com/pierg/crome-logic.git --branch main --single-branch

WORKDIR /home/crome-cgg

# Copy /venv from the previous stage:
COPY --from=build /venv ./venv

ENV PYTHONPATH "/home/crome-cgg:/home/crome-logic"


ENTRYPOINT ["./entrypoint.sh"]
