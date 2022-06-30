#### !/usr/bin/env python
# coding: utf-8
from molmap.model import RegressionEstimator, MultiClassEstimator, MultiLabelEstimator
from molmap import loadmap, dataset
from molmap.show import imshow_wrap
import molmap

from sklearn.utils import shuffle 
from joblib import load, dump
import numpy as np
import pandas as pd
import os

from chembench import dataset
def get_pos_weights(trainY):
    """pos_weights: neg_n / pos_n """
    dfY = pd.DataFrame(trainY)
    pos = dfY == 1
    pos_n = pos.sum(axis=0)
    neg = dfY == 0
    neg_n = neg.sum(axis=0)
    pos_weights = (neg_n / pos_n).values
    neg_weights = (pos_n / neg_n).values
    return pos_weights, neg_weights


def random_split(df, random_state, split_size = [0.8, 0.1, 0.1]):
    from sklearn.utils import shuffle 
    import numpy as np
    base_indices = np.arange(len(df)) 
    base_indices = shuffle(base_indices, random_state = random_state) 
    nb_test = int(len(base_indices) * split_size[2]) 
    nb_val = int(len(base_indices) * split_size[1]) 
    test_idx = base_indices[0:nb_test] 
    valid_idx = base_indices[(nb_test):(nb_test+nb_val)] 
    train_idx = base_indices[(nb_test+nb_val):len(base_indices)] 
    
    print(len(train_idx), len(valid_idx), len(test_idx)) 
    
    return train_idx, valid_idx, test_idx 


gpuid = 7
result_file = 'muv.csv'
muv = dataset.load_MUV()


random_seeds = [2, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]
file_path = "/raid/shenwanxiang/08_Robustness/dataset_induces/split" #split
tmp_feature_dir = '/raid/shenwanxiang/08_Robustness/tempignore' #feature path



with open(result_file, 'w+') as f:
    f.write('task_name, seed, valid_auc, test_auc\n')
    

res = []
for data in [muv]:
    task_name = data.task_name
    task_type = data.task_type

    X1_name = os.path.join(tmp_feature_dir, 'X1_%s.data' % task_name)
    X1 = load(X1_name)
    fmap_shape1 = X1.shape[1:] 
    
    X2_name = os.path.join(tmp_feature_dir, 'X2_%s.data' % task_name)
    X2 = load(X2_name)
    fmap_shape2 = X2.shape[1:] 

    Y = data.y
    df = data.df
    n_outputs = Y.shape[1]
    Y = pd.DataFrame(Y).fillna(-1).values
    
    for seed in random_seeds:

        train_idx, valid_idx, test_idx = random_split(Y, random_state = seed)

        print(len(train_idx), len(valid_idx), len(test_idx))

        X_train = (X1[train_idx], X2[train_idx])
        y_train = Y[train_idx]

        X_valid = (X1[valid_idx], X2[valid_idx])
        y_valid = Y[valid_idx]

        X_test = (X1[test_idx], X2[test_idx])
        y_test = Y[test_idx]    

        pos_weights, neg_weights = get_pos_weights(y_train)
        loss = lambda y_true, y_pred: molmap.model.loss.weighted_cross_entropy(y_true,y_pred, pos_weights, MASK = -1)
    
        clf = MultiLabelEstimator(n_outputs,
                                  fmap_shape1, 
                                      fmap_shape2, 
                                      batch_size = 128,
                                      dense_layers = [512], #17 outputs
                                      gpuid = gpuid, 
                                      patience = 20,
                                      monitor = 'val_auc',
                                      metric = 'PRC',
                                      loss = loss,
                                     )             
        clf.fit(X_train,y_train, X_valid, y_valid)

        train_aucs = clf._performance.evaluate(X_train,y_train)
        valid_aucs = clf._performance.evaluate(X_valid,y_valid)            
        test_aucs = clf._performance.evaluate(X_test,y_test)
        
        train_auc = np.nanmean(train_aucs)
        valid_auc = np.nanmean(valid_aucs)
        test_auc = np.nanmean(test_aucs)
        
        final_res = {'seed': seed,
                     "task_name": task_name,
                     'train_auc':train_auc, 
                     'valid_auc':valid_auc,                      
                     'test_auc':test_auc,}
        print(final_res)
        
        with open(result_file, 'a+') as f:
            f.write('%s, %s, %s, %s\n' % (task_name, seed, valid_auc, test_auc))

        res.append(final_res)

        test_pred_save_path = os.path.join(file_path, task_name,"%s" % seed, "MolMAP_pred_test.csv")
        valid_pred_save_path = os.path.join(file_path, task_name,"%s" % seed, "MolMAP_pred_val.csv")
        
        test_y_pred_prob = clf.predict_proba(X_test)
        valid_y_pred_prob = clf.predict_proba(X_valid)     
        
        valid_df = df.iloc[valid_idx]
        test_df = df.iloc[test_idx]
        
        pd.DataFrame(test_y_pred_prob, index = test_df['smiles'],columns = data.y_cols).to_csv(test_pred_save_path)
        pd.DataFrame(valid_y_pred_prob, index = valid_df['smiles'],columns = data.y_cols).to_csv(valid_pred_save_path)        
        
pd.DataFrame(res).to_csv(result_file + '.bak.csv')