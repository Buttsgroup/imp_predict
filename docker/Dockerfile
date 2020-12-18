FROM ubuntu:16.04
SHELL [ "/bin/bash", "-c"]
RUN apt-get update \
  && apt-get install -y wget \
  && apt-get install -y git \
  && apt-get install -y gfortran libblas-dev liblapack-dev \
  && apt-get install -y vim \
  && rm -rf /var/lib/apt/lists/*

# Copy gcloud related tooling to root/tmp
COPY tooling/requirements.txt /tmp/
COPY imp_predict/make_conda_env.sh /usr/local/bin/
COPY tooling/make_gcloud_conda_env.sh /usr/local/bin/
COPY tooling/entrypoint.sh /usr/local/bin/
RUN chmod u+x /usr/local/bin/entrypoint.sh

ENV PYTHONPATH "${PYTHONPATH}:/"
COPY tooling /tooling
COPY imp_predict/predict.sh imp_predict/do_predict.py imp_predict/setup_pred.py imp_predict/output_pred.py /
RUN mkdir /INPUT /MODEL /OUTPUT && chmod +x /predict.sh
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

# build the conda environments (imp_*_v?.?, imp_gcloud)
ENV _VERSION="v1.0"
RUN bash /usr/local/bin/make_conda_env.sh ${_VERSION} && bash /usr/local/bin/make_gcloud_conda_env.sh

# COPY PACKAGES
COPY imp_predict/imp_core /imp_core
COPY imp_predict/mol_translator /mol_translator

# -------------------
# GCLOUD RUN SPECIFIC
# -------------------
ARG SERVICE_KEY_FILE
RUN echo $SERVICE_KEY_FILE
RUN if [[ -z "$SERVICE_KEY_FILE" ]] ; \
 then echo "No service account key file in local context specified" ; exit 1 ; fi

COPY ./$SERVICE_KEY_FILE /service-acc-key.json
ENV GOOGLE_APPLICATION_CREDENTIALS /service-acc-key.json

WORKDIR /

RUN source activate imp_gcloud && \
    python /tooling/download_pickles.py \
    conda deactivate

ENTRYPOINT [ "/usr/local/bin/entrypoint.sh" ]