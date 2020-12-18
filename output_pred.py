
import sys
sys.path.append('./mol_translator/')


import mol_translator.aemol as _aemol
import mol_translator.imp_converter.dataframe_prep as df_prep
import mol_translator.imp_converter.dataframe_write as df_write
import mol_translator.imp_converter.dataframe_read as df_read

import pandas as pd
from datetime import datetime


def get_time():
    return datetime.now().strftime("%d/%m/%Y::%H:%M:%S")


def output_mols(atom_df, pair_df):
    print(get_time(), 'Outputting molecules. . .')
    try:
        mols = df_read.read_df(atom_df, pair_df)
    except Exception as e:
        print(get_time(), 'Error outputting molecules')
        print(get_time(), 'Error getting molecules from dataframes into aemol objects', e, e.__traceback__, file=sys.stderr)
        exit(4)
    if len(mols) == 0:
        print(get_time(), 'No molecules output, nothing to do')
        exit(4)
    for aemol in mols:
        outfile = "OUTPUT/" + str(aemol.info['molid']) + '.nmredata.sdf'
        try:
            aemol.prop_tofile(outfile, prop='nmr', format='nmredata')
        except Exception as e:
            print(get_time(), 'Error making nmredata file, ' , aemol.info['molid'])
            print(get_time(), 'Error making nmredata file, ' , aemol.info['molid'], e, e.__traceback__, file=sys.stderr)
    
if __name__ == "__main__":
    try:
        atom_df = pd.read_pickle("tmp/POST_atoms.pkl")
        pair_df = pd.read_pickle("tmp/POST_pairs.pkl")
    except:
        print(get_time(), 'Error reading dataframes from prediction output')
        print(get_time(), 'Error reading dataframes from prediction output', e, e.__traceback__, file=sys.stderr)
        exit(4)
    output_mols(atom_df, pair_df)
    print(get_time(), 'Done.')