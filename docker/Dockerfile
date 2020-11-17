FROM ubuntu:16.04
SHELL [ "/bin/bash", "-c"]
RUN apt-get update \
  && apt-get install -y wget \
  && apt-get install -y git \
  && rm -rf /var/lib/apt/lists/*

COPY docker/environment.yml docker/requirements.txt /tmp/
COPY docker/postBuild /usr/local/bin/postBuild.sh
COPY docker/entrypoint.sh /usr/local/bin/
RUN chmod u+x /usr/local/bin/entrypoint.sh

#COPY autoenrich /autoenrich # Dont need this anymore

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

# create a project directory inside user home
ENV PROJECT_DIR $HOME/app
RUN mkdir $PROJECT_DIR
WORKDIR $PROJECT_DIR

# build the conda environment
ENV ENV_PREFIX v1.0
RUN bash make_conda_env.sh $ENV_PREFIX
'''
RUN conda update --name base --channel defaults conda && \
    conda env create --prefix $ENV_PREFIX --file /tmp/environment.yml --force && \
    conda clean --all --yes
'''
# run the postBuild script to install any JupyterLab extensions
RUN source activate imp_predictor_$ENV_PREFIX && \
  #  /usr/local/bin/postBuild.sh && \
    conda deactivate


RUN apt-get install git
# This might cause a problem because imp_core is private,
# this would pull the most recent commit from the branch at runtime, maybe overkill
# can just do this manually when needed
RUN git submodule update --remote

# COPY predict_from_model.py /predict_from_model.py ## dont think we need this anymore, script is in repo
# -------------------
# GCLOUD RUN SPECIFIC
# -------------------
ARG SERVICE_KEY_FILE
RUN echo $SERVICE_KEY_FILE
RUN if [[ -z "$SERVICE_KEY_FILE" ]] ; \
 then echo "No service account key file in local context specified" ; exit 1 ; fi

COPY ./$SERVICE_KEY_FILE /service-acc-key.json
ENV GOOGLE_APPLICATION_CREDENTIALS /service-acc-key.json

COPY gcloud_imp_tools /gcloud_imp_tools
COPY download_pickles.py /download_pickles.py
COPY pre_predict.py /pre_predict.py
COPY post_predict.py /post_predict.py

WORKDIR /

RUN source activate $ENV_PREFIX && \
    python /download_pickles.py \
    conda deactivate

ENTRYPOINT [ "/usr/local/bin/entrypoint.sh" ]