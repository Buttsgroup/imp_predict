set -e

conda env remove -n imp_io
conda create -n imp_io python=3 -y
conda install -n imp_io numpy scipy pandas -y
conda install -n imp_io -c openbabel openbabel -y
conda install -n imp_io -c conda-forge xorg-libxrender -y
conda install -n imp_io -c rdkit rdkit -y
conda install -n imp_io -c conda-forge tqdm -y
conda install -n imp_io pytest -y
