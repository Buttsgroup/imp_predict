

import sys
sys.path.append('./mol_translator/')


import mol_translator.aemol as _aemol
import mol_translator.imp_converter.dataframe_prep as df_prep
import mol_translator.imp_converter.dataframe_write as df_write
import mol_translator.imp_converter.dataframe_read as df_read

import glob
import numpy as np

import pickle

import tqdm
import time

def convert_mols():
    
    files = glob.glob("INPUT/*")[:2]
    # shortcut for doing DT3 predictions
    # DONT COMMIT THIS !!!
    files = glob.glob("/Users/willgerrard/code/bg_code/datasets/Data3/Data3_nmredata/*.sdf")
    mols = []
    
    print('Getting files to predict. . .')
    for file in files:
        print(file)
        ID = file.split('/')[-1].split('.')[0]
        format = file.split('/')[-1].split('.')[1]
        if format == 'nmredata':
            format = 'sdf'
        
        aemol = _aemol(ID)
        aemol.from_file(file, format)
        aemol = df_prep.prep_mol_nmr(aemol)
        
        mols.append(aemol)

    atom_df = df_write.make_atom_df(mols)
    pair_df = df_write.make_pair_df(mols, max_bond_distance=6)
    
    return atom_df, pair_df

if __name__ == "__main__":
    time0 = time.time()
    atom_df, pair_df = convert_mols()
    
    pickle.dump(atom_df, open('tmp/PRE_atoms.pkl', 'wb'))
    pickle.dump(pair_df, open('tmp/PRE_pairs.pkl', 'wb'))
    
    print('Total time taken: ', (time.time()-time0)/60, ' minutes.')