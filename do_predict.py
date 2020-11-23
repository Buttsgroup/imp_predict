
import sys
sys.path.append('./imp_core/')

from model.gtn_model import GTNmodel
import model.features.graph_input as graph_in

import glob
import numpy as np
import pandas as pd

import pickle

import copy

import tqdm
import time


def predict_from_model(atom_df, pair_df):
    
    mol_df, graphs = graph_in.make_graph_df(atom_df, pair_df)
    
    #for target in ['CCS', 'HCS']:
    
    #print('Predicting: ', target)
    
    #modelfile = 'MODEL/' + target + '_model.torch'
    modelfile = 'MODEL/all_model.torch'
    model = GTNmodel()
    model.load_model(modelfile)
    print(model.args['targetflag'])
    
    tmp_graphs = copy.deepcopy(graphs)
    
    test_loader = model.get_input(tmp_graphs, mol_df)
    graphs_out = model.predict(test_loader)
    
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
    atom_df, pair_df = model.assign_preds(graphs_out, mol_df, atom_df, pair_df, assign_to="")

    return atom_df, pair_df



if __name__ == "__main__":
    time0 = time.time()
    atom_df = pd.read_pickle("tmp/PRE_atoms.pkl")
    pair_df = pd.read_pickle("tmp/PRE_pairs.pkl")
    
    atom_df, pair_df = predict_from_model(atom_df, pair_df)

    pickle.dump(atom_df, open('tmp/POST_atoms.pkl', 'wb'))
    pickle.dump(pair_df, open('tmp/POST_pairs.pkl', 'wb'))
    
    print('Total time taken: ', (time.time()-time0)/60, ' minutes.')
    