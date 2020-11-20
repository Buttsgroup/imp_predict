set -e

version=v2.0

conda env remove -n imp_core_${version}
conda create -n imp_core_${version} python=3 -y
conda install -n imp_core_${version} pytorch=1.6 -y # CPU VERSION
conda install -n imp_core_${version} numpy scipy pandas -y
conda install -n imp_core_${version} -c conda-forge tqdm cytoolz tensorboard -y
conda install -n imp_core_${version} -c dglteam dgl -y # CPU VERSION
conda install -n imp_core_${version} requests -y
conda install -n imp_core_${version} pytest -y

conda env remove -n imp_io_${version}
conda create -n imp_io_${version} python=3 -y
conda install -n imp_io_${version} numpy scipy pandas pytest -y
conda install -n imp_io_${version} -c openbabel openbabel -y
conda install -n imp_io_${version} -c rdkit rdkit -y
conda install -n imp_io_${version} -c conda-forge tqdm -y

