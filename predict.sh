source activate imp_io_v2.0
mkdir tmp
echo Converting input molecules ...
python setup_pred.py
conda deactivate
source activate imp_core_v2.0
echo Making predictions ...
python do_predict_STG1.py
python do_predict_STG2.py
conda deactivate
source activate imp_io_v2.0
echo Converting output molecules ...
python output_pred.py
conda deactivate
#rm -r tmp