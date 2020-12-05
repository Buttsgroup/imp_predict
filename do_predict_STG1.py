
import sys
sys.path.append('./imp_core1/')

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
    modelfile = 'MODEL/all_model_STG1.torch'
    model = GTNmodel()
    model.load_model(modelfile)
    model.params['batch_size'] = 4
    print(model.args['targetflag'])
    
    tmp_graphs = copy.deepcopy(graphs)
    
    test_loader = model.get_input(tmp_graphs, mol_df)
    graphs_out = model.predict(test_loader)
    
    atom_df, pair_df = model.assign_preds(graphs_out, mol_df, atom_df, pair_df, assign_to="qm9_")

    return atom_df, pair_df



if __name__ == "__main__":
    time0 = time.time()
    atom_df = pd.read_pickle("tmp/PRE_atoms.pkl")
    pair_df = pd.read_pickle("tmp/PRE_pairs.pkl")
    
    atom_df, pair_df = predict_from_model(atom_df, pair_df)

    pickle.dump(atom_df, open('tmp/STG1_atoms.pkl', 'wb'))
    pickle.dump(pair_df, open('tmp/STG1_pairs.pkl', 'wb'))
    
    print('Total time taken: ', (time.time()-time0)/60, ' minutes.')
    