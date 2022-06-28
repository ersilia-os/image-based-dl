from sklearn.utils import shuffle 
import numpy as np
import random

'Split function that returns indexes for train, validation and test sets'
def Rdsplit(df, random_state = 888, split_size = [0.8, 0.1, 0.1]):
    base_indices = np.arange(len(df)) 
    base_indices = shuffle(base_indices, random_state = random_state) 
    nb_test = int(len(base_indices) * split_size[2]) 
    nb_val = int(len(base_indices) * split_size[1]) 
    test_idx = base_indices[0:nb_test] 
    valid_idx = base_indices[(nb_test):(nb_test+nb_val)] 
    train_idx = base_indices[(nb_test+nb_val):len(base_indices)] 
    print(len(train_idx), len(valid_idx), len(test_idx)) 
    return train_idx, valid_idx, test_idx 

'Sample weight for binary target variable'
def sample_weight(y):
    sw = np.ones(shape=(len(y),))
    if y.tolist().count(0) > y.tolist().count(1):
        sw[y == 1] = (y.tolist().count(0))/(y.tolist().count(1))
    else:
        sw[y == 0] = (y.tolist().count(1))/(y.tolist().count(0))
        
    return sw