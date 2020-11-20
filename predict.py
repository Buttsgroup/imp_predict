
import sys
sys.path.append('./mol_translator/')
sys.path.append('./imp_core/')


import mol_translator.aemol as _aemol
import mol_translator.imp_converter.dataframe_prep as df_prep
import mol_translator.imp_converter.dataframe_write as df_write
import mol_translator.imp_converter.dataframe_read as df_read

from model.gtn_model import GTNmodel
import model.features.graph_input as graph_in

import glob
import numpy as np

import tqdm
import time

def convert_mols():
    
    files = glob.glob("INPUT/*")[:2]
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
    
    mol_df, graphs = graph_in.make_graph_df(atom_df, pair_df)
    
    return atom_df, pair_df
    
def predict_from_model(atom_df, pair_df):
    
    for target in ['HCS', 'CCS']:
    
        print('Predicting: ', target)
    
        modelfile = 'MODEL/' + target + '_model.torch'
        
        model = GTNmodel()
        model.load_model(modelfile)
        
        test_loader = model.get_input(atom_df, pair_df)
        pred_graphs = model.predict(test_loader)
        
        #atom_df, pair_df = model.assign_preds(pred_y, atom_df, pair_df, assign_to="")
        
        # variance predictions:
        '''
        cv_models = glob.glob('MODEL/fchl_set4_' + target + '_cv*.pkl')
        if len(cv_models) == 0:
            cv_pred = np.zeros(len(pred_y))
        else:
            cv_pred_y = []
            for cvmodelfile in cv_models:
                print('    cv: ', cvmodelfile)
                cvmodel = FCHLmodel()
                cvmodel.load_model(cvmodelfile)
                
                test_x, _ = cvmodel.get_input(atom_df, pair_df)
                cv_pred_y.append(cvmodel.predict(test_x))
            cv_pred = np.var(cv_pred_y, 0)
        '''
        atom_df, pair_df = model.assign_preds(graphs_out, atom_df, pair_df, assign_to="")

    return atom_df, pair_df
    
def output_mols(atom_df, pair_df):
    print('Outputting molecules. . .')
    mols = df_read.read_df(atom_df, pair_df)
    for aemol in mols:
        outfile = "OUTPUT/" + str(aemol.info['molid']) + '.nmredata.sdf'
        aemol.prop_tofile(outfile, prop='nmr', format='nmredata')


if __name__ == "__main__":
    time0 = time.time()
    atom_df, pair_df = convert_mols()
    atom_df, pair_df = predict_from_model(atom_df, pair_df)
    output_mols(atom_df, pair_df)
    print('Total time taken: ', (time.time()-time0)/60, ' minutes.')
    
    ## Potential code for continual processing ?
    ## Let me know what you think max. . .
    ## Essentially keep running if there are IDs in input, which aren't in output
    '''
    max_runs = 5
    run = 0
    
    input_ids = [file.split('/')[-1].split('.')[0] for file in glob.glob('INPUT/*')]
    output_ids = [file.split('/')[-1].split('.')[0] for file in glob.glob('OUTPUT/*')]
    condition = False
    for id_in in input_ids:
        if id_in not in output_ids:
            condition = True
            
    while condition:
        run += 1
        atom_df, pair_df = convert_mols()
        atom_df, pair_df = predict_from_model(atom_df, pair_df)
        output_mols(atom_df, pair_df)
        
        input_ids = [file.split('/')[-1].split('.')[0] for file in glob.glob('INPUT/*')]
        output_ids = [file.split('/')[-1].split('.')[0] for file in glob.glob('OUTPUT/*')]
        condition = False
        for id_in in input_ids:
            if id_in not in output_ids:
                condition = True
        if run >= max_runs:
            condition = False
    
    '''