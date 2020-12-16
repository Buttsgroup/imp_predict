set -e

version=v1.0

conda env remove -n imp_io_${version}
conda create -n imp_io_${version} python=3 -y

conda install -n imp_io_${version} numpy scipy pandas -y
conda install -n imp_io_${version} -c openbabel openbabel -y
conda install -n imp_io_${version} -c rdkit rdkit -y
conda install -n imp_io_${version} -c conda-forge tqdm -y
conda install -n imp_io_${version} pytest -y

conda env remove -n imp_core_${version}
conda create -n imp_core_${version} python=3 -y
conda install -n imp_core_${version} numpy scipy pandas scikit-learn -y
conda install -n imp_core_${version} -c conda-forge tqdm -y
conda install -n imp_core_${version} pytest -y
source activate imp_core_${version}
pip install git+https://github.com/qmlcode/qml@develop --user -U