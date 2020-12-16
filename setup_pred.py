

import sys
sys.path.append('./mol_translator/')

import glob
import mol_translator.aemol as _aemol
import mol_translator.imp_converter.dataframe_prep as df_prep
import mol_translator.imp_converter.dataframe_write as df_write
import mol_translator.imp_converter.dataframe_read as df_read

import pandas as pd
import pickle

def convert_mols():
    
    files = glob.glob("INPUT/*")[:2]
    mols = []
    
    print('Getting files to predict. . .')
    for file in files:
        ID = file.split('/')[-1].split('.')[0]
        format = file.split('/')[-1].split('.')[1]
        if format == 'nmredata':
            format = 'sdf'
        
        try:
            aemol = _aemol(ID)
            aemol.from_file(file, format)
            aemol = df_prep.prep_mol_nmr(aemol)
            mols.append(aemol)
        except Exception as e:
            print('Error reading file: ', e)
            print('Skipping molecule: ', file)

    if len(mols) == 0:
        print('No molecules read, nothing to do . . .')
        sys.exit(4)

    atom_df = df_write.make_atom_df(mols)
    pair_df = df_write.make_pair_df(mols, max_bond_distance=6)
    
    return atom_df, pair_df
    
if __name__ == "__main__":
    atom_df, pair_df = convert_mols()
    atom_df.to_pickle('tmp/PRE_atoms.pkl', protocol=4)
    pair_df.to_pickle('tmp/PRE_pairs.pkl', protocol=4)