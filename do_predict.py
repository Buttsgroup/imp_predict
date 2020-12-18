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

from datetime import datetime

def get_time():
    return datetime.now().strftime("%m/%d/%Y::%H:%M:%S")

def predict_from_model(atom_df, pair_df):
    
    for target in ['HCS', 'CCS', '1JCH']:
    
        print('Predicting: ', target)
    
        modelfile = 'MODEL/fchl_set4_' + target + '.pkl'
        
        try:
            model = FCHLmodel()
            model.load_model(modelfile)
        except Exception as e:
            print(get_time(), 'Error loading IMPRESSION model')
            print(get_time(), 'Error loading IMPRESSION model', e, e.__traceback__, file=sys.stderr)
            exit(4)
        
        try:
            test_x, _ = model.get_input(atom_df, pair_df)
        except Exception as e:
            print(get_time(), 'Error getting input representations from dataframe')
            print(get_time(), 'Error getting input representations from dataframe', e, e.__traceback__, file=sys.stderr)
            exit(4)

        if len(test_x) == 0:
            print(get_time(), 'No inputs made, nothing to do')
            print(get_time(), 'No input environments made for ', target, ', test_x empty, nothing to do', file=sys.stderr)
            continue
            
        try:
            pred_y = model.predict(test_x)
        except Exception as e:
            print(get_time(), 'Error making predictions')
            print(get_time(), 'Error in model.predict: ', e, e.__traceback__, file=sys.stderr)
            exit(4)
            
        if len(pred_y) == 0:
            print(get_time(), 'No predictions made, nothing to do')
            print(get_time(), 'No predictions made, nothing to do', file=sys.stderr)
            continue
        
        # variance predictions:
        cv_models = glob.glob('MODEL/fchl_set4_' + target + '_cv*.pkl')
        if len(cv_models) == 0:
            print(get_time(), 'No variance models found')
            print(get_time(), 'No variance models found for target:', target, 'glob string:', 'MODEL/fchl_set4_' + target + '_cv*.pkl', file=sys.stderr)
            cv_pred = np.zeros(len(pred_y))
        else:
            cv_pred_y = []
            for cvmodelfile in cv_models:
                print('Making variance predictions: ', cvmodelfile)
                try:
                    cvmodel = FCHLmodel()
                    cvmodel.load_model(cvmodelfile)
                except Exception as e:
                    print(get_time(), 'Error loading cv IMPRESSION model')
                    print(get_time(), 'Error loading cv IMPRESSION model', e, e.__traceback__, file=sys.stderr)
                
                try:
                    test_x, _ = cvmodel.get_input(atom_df, pair_df)
                except Exception as e:
                    print(get_time(), 'Error getting input representations from dataframe')
                    print(get_time(), 'Error getting input representations from dataframe', e, e.__traceback__, file=sys.stderr)
                    
                try:
                    cv_pred_y.append(cvmodel.predict(test_x))
                except Exception as e:
                    print(get_time(), 'Error making predictions')
                    print(get_time(), 'Error in model.predict: ', e, e.__traceback__, file=sys.stderr)
                    
            cv_pred = np.var(cv_pred_y, 0)
        
        if any(np.isnan(cv_pred)):
            print(get_time(), 'WARNING: variance array contains NaN values')
            print(get_time(), 'WARNING: variance array contains NaN values', file=sys.stderr)
        
        try:
            atom_df, pair_df = model.assign_preds(pred_y, atom_df, pair_df, assign_to="", variance=cv_pred)
        except Exception as e:
            print(get_time(), 'Error assigning prediction output to molecules')
            print(get_time(), 'Error assigning prediction output to molecules', e, e.__traceback__, file=sys.stderr)
            exit(4)

    return atom_df, pair_df
    
if __name__ == "__main__":
    try:
        atom_df = pd.read_pickle("tmp/PRE_atoms.pkl")
        pair_df = pd.read_pickle("tmp/PRE_pairs.pkl")
    except Exception as e:
        print(get_time(), 'Error reading pre-processed dataframes')
        print(get_time(), 'Error reading PRE_atoms/PRE_pairs from pickles', e, e.__traceback__, file=sys.stderr)
        exit(4)
    try:
        atom_df = fchl.add_fchl_to_atom_df(atom_df)
    except Exception as e:
        print(get_time(), 'Error generating fchl representations')
        print(get_time(), 'Error adding fchl representations to atom_df', e, e.__traceback__, file=sys.stderr)
        exit(4)
        
    atom_df, pair_df = predict_from_model(atom_df, pair_df)

    try:
        atom_df.to_pickle('tmp/POST_atoms.pkl', protocol=4)
        pair_df.to_pickle('tmp/POST_pairs.pkl', protocol=4)
    except Exception as e:
        print(get_time(), 'Error saving pickles')
        print(get_time(), 'Error saving pickles', e, e.__traceback__, file=sys.stderr)