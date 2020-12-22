import sys
sys.path.append('./mol_translator/')

import glob
import mol_translator.aemol as _aemol
import mol_translator.imp_converter.dataframe_prep as df_prep
import mol_translator.imp_converter.dataframe_write as df_write
import mol_translator.imp_converter.dataframe_read as df_read


from datetime import datetime

def get_time():
    return datetime.now().strftime("%m/%d/%Y::%H:%M:%S")

def convert_mols():
    
    files = glob.glob("INPUT/*")
    if len(files) == 0:
        print(get_time(), ': No files found by glob INPUT, should have been handled already', file=sys.stderr)
        exit(4)
    
    mols = []
    print(get_time(), ': Getting files to predict. . .')
    for file in files:
        ID = file.split('/')[-1].split('.')[0]
        format = file.split('/')[-1].split('.')[-1]
        if format == 'nmredata':
            format = 'sdf'

        print(get_time(), file, ID)
        try:
            aemol = _aemol(ID)
            aemol.from_file(file, format)
            if len(aemol.structure['types']) > 150:
                print(get_time(), 'Molecule too big (>150 atoms), skipping. . .')
                print(get_time(), 'Molecule, ', file, ' bigger than limit (150), size=', len(aemol.structure['types']), file=sys.stderr)
                continue
            aemol = df_prep.prep_mol_nmr(aemol)
            mols.append(aemol)
        except Exception as e:
            print(get_time(), 'Error importing molecule: ', file)
            print(get_time(), 'Error importing molecule: ', file, e, e.__traceback__, file=sys.stderr)

    if len(mols) == 0:
        print(get_time(), 'No valid molecules read, nothing to do . . .')
        print(get_time(), 'No valid molecules read, nothing to do . . .', file=sys.stderr)
        sys.exit(4)

    try:
        atom_df = df_write.make_atom_df(mols)
        pair_df = df_write.make_pair_df(mols, max_bond_distance=6)
    except Exception as e:
        print(get_time(), 'Error making input dataframe')
        print(get_time(), 'Error making input dataframe, ', e, e.__traceback__, file=sys.stderr)
    
    return atom_df, pair_df
    
if __name__ == "__main__":
    atom_df, pair_df = convert_mols()
    try:
        atom_df.to_pickle('tmp/PRE_atoms.pkl', protocol=4)
        pair_df.to_pickle('tmp/PRE_pairs.pkl', protocol=4)
    except Exception as e:
        print(get_time(), 'Error saving pickles')
        print(get_time(), 'Error saving pickles', e, e.__traceback__, file=sys.stderr)