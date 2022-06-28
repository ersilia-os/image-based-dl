import numpy as np
import h5py
from tensorflow import keras

class Hdf5Generator(keras.utils.Sequence):
    'Generates data for Keras'
    def __init__(self, h5_filename_X1, dim_X1, n_channels_X1, h5_filename_X2, dim_X2, n_channels_X2, Y, n_classes, batch_size=128, sample_weight=False, shuffle=True):
        
        'Initialization'
        self.h5_filename_X1 = h5_filename_X1
        self.dim_X1 = dim_X1
        self.n_channels_X1 = n_channels_X1
        
        self.h5_filename_X2 = h5_filename_X2
        self.dim_X2 = dim_X2
        self.n_channels_X2 = n_channels_X2
        
        self.y = Y
        self.n_classes = n_classes
        self.list_IDs = np.arange(len(self.y))
        
        self.sample_weight = sample_weight
        if self.sample_weight:
            self.sw = np.ones(shape=(len(self.y),))
            if self.y.tolist().count(0) > self.y.tolist().count(1):
                self.sw[self.y == 1] = (self.y.tolist().count(0))/(self.y.tolist().count(1))
            else:
                self.sw[self.y == 0] = (self.y.tolist().count(1))/(self.y.tolist().count(0))
        
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.on_epoch_end()

        self.partitions_file = 20
        self.batch_size_file = int(np.floor(len(self.y)/self.partitions_file))
        
    def __len__(self):
        'Denotes the number of batches per epoch'
        return int(np.floor(len(self.y) / self.batch_size))

    def __getitem__(self, index):
        'Generate one batch of data'
        # Generate indexes of the batch
        indexes = self.indexes[index*self.batch_size:(index+1)*self.batch_size]
        
        # Find list of IDs
        list_IDs_temp = [self.list_IDs[k] for k in indexes]
        
        if self.sample_weight:
            # Generate data
            (X1, X2), y, sw = self.__data_generation(list_IDs_temp)
            if (index+1) == int(np.floor(len(self.y) / self.batch_size)):
                self.on_epoch_end() 
            return (X1, X2), y, sw
        else:
            # Generate data
            (X1, X2), y = self.__data_generation(list_IDs_temp)
            if (index+1) == int(np.floor(len(self.y) / self.batch_size)):
                self.on_epoch_end()  
            return (X1, X2), y
        
    def on_epoch_end(self):
        'Updates indexes after each epoch'
        self.indexes = np.arange(len(self.list_IDs))
        if self.shuffle == True:
            np.random.shuffle(self.indexes)

    def __data_generation(self, list_IDs_temp):
        'Generates data containing batch_size samples'     
        # Initialization
        X1 = np.empty((self.batch_size, *self.dim_X1, self.n_channels_X1), dtype=np.float32)
        X2 = np.empty((self.batch_size, *self.dim_X2, self.n_channels_X2), dtype=np.float32)
        y = np.empty((self.batch_size), dtype=int)
        if self.sample_weight:
            sw = np.empty((self.batch_size), dtype=int)
        
        # Save current and sorted index order
        list_IDs_temp_sorted = np.sort(list_IDs_temp)
        original_order = np.argsort(np.argsort(list_IDs_temp))
        
        # Read from disk in batches
        k = 0
        for index_file in range(0, self.partitions_file):
            X1_batch = []
            X2_batch = []
            start = index_file*self.batch_size_file
            end = (index_file+1)*self.batch_size_file
            with h5py.File(self.h5_filename_X1, "r") as f:
                X1_batch = np.array(f["data"][start:end], dtype=np.float32)
            with h5py.File(self.h5_filename_X2, "r") as f:
                X2_batch = np.array(f["data"][start:end], dtype=np.float32)  
            
            list_file_temp = [x for x in list_IDs_temp_sorted if ((x >= start) and (x < end))]

            i = k
            for j in list_file_temp:
                X1[i] = X1_batch[j - start]
                X2[i] = X2_batch[j - start]
                i = i + 1
            k = i
        
        # Get X1, X2 data
        X1 = np.array([X1[i] for i in original_order], dtype=np.float32)
        X2 = np.array([X2[i] for i in original_order], dtype=np.float32)
            
        # Generate data Y, sw
        for i, ID in enumerate(list_IDs_temp):
            y[i] = self.y[ID]
        
        if self.sample_weight:
            for i, ID in enumerate(list_IDs_temp):
                sw[i] = self.sw[ID]
        
        # Return
        if self.sample_weight:
            return (X1, X2), keras.utils.to_categorical(y, num_classes=self.n_classes), sw
        else:
            return (X1, X2), keras.utils.to_categorical(y, num_classes=self.n_classes)
    