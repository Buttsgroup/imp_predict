set -e

conda env remove -n imp_core
conda create -n imp_core python=3 -y
conda install -n imp_core numpy scipy pandas scikit-learn -y
conda install -n imp_core -c conda-forge tqdm -y
conda install -n imp_core pytest -y
source activate imp_core
pip install git+https://github.com/qmlcode/qml@develop --user -U
