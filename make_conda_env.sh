version=$1
conda env remove -n imp_predictor_"${version}"
conda create -n imp_predictor_"${version}" python=3 -y
source activate imp_predictor_"${version}"
conda install -n imp_predictor_"${version}" numpy scipy pandas -y
conda install -n imp_predictor_"${version}" -c openbabel openbabel -y
conda install -c conda-forge xorg-libxrender -y
conda install -n imp_predictor_"${version}" -c rdkit rdkit -y
conda install -n imp_predictor_"${version}" -c conda-forge tqdm -y
conda install -n imp_predictor_"${version}" pytest
pip install git+https://github.com/qmlcode/qml@develop --user -U
