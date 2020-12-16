
import sys
sys.path.append('./mol_translator/')


import mol_translator.aemol as _aemol
import mol_translator.imp_converter.dataframe_prep as df_prep
import mol_translator.imp_converter.dataframe_write as df_write
import mol_translator.imp_converter.dataframe_read as df_read

import pandas as pd

def output_mols(atom_df, pair_df):
    print('Outputting molecules. . .')
    mols = df_read.read_df(atom_df, pair_df)
    if len(mols) == 0:
        print('No mols to process, nothing to do')
        return 4
    for aemol in mols:
        outfile = "OUTPUT/" + str(aemol.info['molid']) + '.nmredata.sdf'
        aemol.prop_tofile(outfile, prop='nmr', format='nmredata')
    
if __name__ == "__main__":
    atom_df = pd.read_pickle("tmp/POST_atoms.pkl")
    pair_df = pd.read_pickle("tmp/POST_pairs.pkl")
    output_mols(atom_df, pair_df)