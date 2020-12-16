source activate imp_io
mkdir tmp
echo Converting input molecules ...
python setup_pred.py
# Read exit status and attempt to exit if not 0
exit_status=$?
if [ "${exit_status}" -ne 0 ];
then
    return ${exit_status} 2>/dev/null || exit "${exit_status}"
fi
conda deactivate
source activate imp_core
echo Making predictions ...
python do_predict.py
# Read exit status and attempt to exit if not 0
exit_status=$?
if [ "${exit_status}" -ne 0 ];
then
    return ${exit_status} 2>/dev/null || exit "${exit_status}"
fi
conda deactivate
source activate imp_io
echo Converting output molecules ...
python output_pred.py
# Read exit status and attempt to exit if not 0
exit_status=$?
if [ "${exit_status}" -ne 0 ];
then
    return ${exit_status} 2>/dev/null || exit "${exit_status}"
fi
conda deactivate