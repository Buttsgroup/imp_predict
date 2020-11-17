

import mol_translator.aemol as _aemol
import mol_translator.imp_converter.dataframe_prep as df_prep
import mol_translator.imp_converter.dataframe_write as df_write
import mol_translator.imp_converter.dataframe_read as df_read

from imp_core.model.fchl_model import FCHLmodel

def convert_mols():
    
    files = "INPUT/*"
    mols = []
    
    for file in files:
        ID = file.split('/')[-1].split('.')[0]
        format = file.split('/')[-1].split('.')[1]
        if format == 'nmredata.sdf':
            format = 'sdf'
        
        aemol = _aemol(ID)
        aemol.from_file(file, format)
        aemol = df_prep.prep_mol_nmr(aemol)
        
        mols.append(aemol)

    atom_df = df_write.make_atom_df(aemols)
    pair_df = df_write.make_pair_df(aemols, max_bond_distance=6)
    
    return atom_df, pair_df
    
def predict_from_model(atom_df, pair_df):
    
    for target in ['HCS', 'CCS', '1JCH']:
    
        modelfile = 'MODEL/impression_model_ ' + target + '.pkl'
        
        model = FCHLmodel()
        model.load_model(modelfile)
        
        test_x, _ = model.get_input(atom_df, pair_df)
        pred_y = model.predict(test_x)
        
        atom_df, pair_df = model.assign_preds(pred_y, atom_df, pair_df, assign_to="")

    return atom_df, pair_df
    
def output_mols(atom_df, pair_df):
    
    mols = df_read.read_df(atom_df, pair_df)
    for aemol in mols:
        outname = "OUTPUT/" + str(aemol.info['molid']) + '.nmredata.sdf'
        aemol.prop_tofile(outname, prop='nmr', format='nmredata')


if __name__ == "__main__":
    atom_df, pair_df = convert_mols()
    atom_df, pair_df = predict_from_model(atom_df, pair_df)
    output_mols(atom_df, pair_df)