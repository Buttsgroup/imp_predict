version=v2.0
conda env remove -n imp_predictor_${version}
conda create -n imp_predictor_${version} python=3 -y
source activate imp_predictor_${version}
conda install -n imp_predictor_${version} numpy scipy pandas -y
conda install -n imp_predictor_${version} pytorch torchvision -y # CPU VERSION
conda install -n imp_predictor_${version} -c openbabel openbabel -y
conda install -n imp_predictor_${version} -c rdkit rdkit -y
conda install -n imp_predictor_${version} -c conda-forge tqdm cytoolz tensorboard -y
conda install -n imp_predictor_${version} -c dglteam dgl -y # CPU VERSION
conda install -n imp_predictor_${version} requests -y
conda install -n imp_predictor_${version} pytest -y