# The build-stage image:
FROM continuumio/miniconda3 AS build

# Install the package as normal:
COPY environment.yml .
RUN conda env create -f environment.yml

# Install conda-pack:
RUN conda install -c conda-forge conda-pack

# Use conda-pack to create a standalone enviornment
# in /venv:
RUN conda-pack -n crome-cgg -o /tmp/env.tar && \
  mkdir /venv && cd /venv && tar xf /tmp/env.tar && \
  rm /tmp/env.tar

# We've put venv in same path it'll be in final image,
# so now fix up paths:
RUN /venv/bin/conda-unpack


FROM pmallozzi/ltltools:latest AS runtime

RUN apt-get -y update
RUN apt-get -y install git

RUN apt-get update
RUN apt-get -y install gcc

WORKDIR /home

ENV GIT_SSL_NO_VERIFY=1
COPY . /home/crome-cgg
RUN git clone https://github.com/pierg/crome-contracts.git --branch main --single-branch
RUN git clone https://github.com/pierg/crome-logic.git --branch main --single-branch
RUN git clone https://github.com/pierg/crome-synthesis.git --branch main --single-branch

WORKDIR /home/crome-cgg

# Copy /venv from the previous stage:
COPY --from=build /venv ./venv

#CMD . venv/bin/activate
#RUN poetry install


ENV PYTHONPATH "${PYTHONPATH}:/home/crome-cgg:/home/crome-contracts:/home/crome-logic:/home/crome-synthesis"

## When image is run, run the code with the environment
## activated:
#SHELL ["/bin/bash", "-c"]
#ENTRYPOINT source /venv/bin/activate && \
#           python -c "import numpy; print('success!')"

ENTRYPOINT ["./entrypoint.sh"]
