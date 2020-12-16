import sys
sys.path.append('./imp_core/')

from model.fchl_model import FCHLmodel
import model.features.fchl_input as fchl

import glob
import numpy as np
import pandas as pd

import pickle

import tqdm
import time

def predict_from_model(atom_df, pair_df):
    
    for target in ['HCS', 'CCS', '1JCH']:
    
        print('Predicting: ', target)
    
        modelfile = 'MODEL/fchl_set4_' + target + '.pkl'
        
        model = FCHLmodel()
        model.load_model(modelfile)
        
        test_x, _ = model.get_input(atom_df, pair_df)

        if len(test_x) == 0:
            print('No input environments made, nothing to do')
            return 4
        pred_y = model.predict(test_x)
        if len(pred_y) == 0:
            print('No predictions made, nothing to do')
            return 4
        
        #atom_df, pair_df = model.assign_preds(pred_y, atom_df, pair_df, assign_to="")
        
        # variance predictions:
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
        atom_df, pair_df = model.assign_preds(pred_y, atom_df, pair_df, assign_to="", variance=cv_pred)

    return atom_df, pair_df
    
if __name__ == "__main__":
    atom_df = pd.read_pickle("tmp/PRE_atoms.pkl")
    pair_df = pd.read_pickle("tmp/PRE_pairs.pkl")
    atom_df = fchl.add_fchl_to_atom_df(atom_df)
    atom_df, pair_df = predict_from_model(atom_df, pair_df)

    atom_df.to_pickle('tmp/POST_atoms.pkl', protocol=4)
    pair_df.to_pickle('tmp/POST_pairs.pkl', protocol=4)