FROM ubuntu:16.04
SHELL [ "/bin/bash", "-c"]
RUN apt-get update \
  && apt-get install -y wget \
  && apt-get install -y git \
  && apt-get install -y gfortran libblas-dev liblapack-dev \
  && rm -rf /var/lib/apt/lists/*

# Copy gcloud related tooling to root/tmp
COPY make_conda_env.sh /usr/local/bin/
RUN chmod u+x /usr/local/bin/entrypoint.sh

COPY imp_predict/predict.py /predict.py

RUN mkdir /INPUT /MODEL /OUTPUT
# install miniconda
ENV MINICONDA_VERSION 4.8.2
ENV CONDA_DIR $HOME/miniconda3
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-py37_4.8.3-Linux-x86_64.sh -O ~/miniconda.sh && \
    chmod +x ~/miniconda.sh && \
    ~/miniconda.sh -b -p $CONDA_DIR && \
    rm ~/miniconda.sh
# make non-activate conda commands available
ENV PATH=$CONDA_DIR/bin:$PATH
# make conda activate command available from /bin/bash --login shells
RUN echo ". $CONDA_DIR/etc/profile.d/conda.sh" >> ~/.profile
# make conda activate command available from /bin/bash --interative shells
RUN conda init bash

# build the conda environment
ENV ENV_PREFIX v1.0
RUN bash /usr/local/bin/make_conda_env.sh $ENV_PREFIX

# COPY PACKAGES
COPY imp_predict/imp_core /imp_core
COPY imp_predict/mol_translator /mol_translator

WORKDIR /
