import torch
from torch.utils.data import Dataset, DataLoader
import os
from lib.machinelearning import *

class AudioDataset(Dataset):
    samples = []
    paths = []
    length = 0

    def __init__(self, basedir, paths):
        self.paths = paths
		
        for index,path in enumerate(paths):
            totalpath = os.path.join(basedir,path)
            for file in os.listdir(totalpath):
                if( file.endswith(".wav") ):
                    full_filename = os.path.join(totalpath, file)
                    self.samples.append([full_filename,index])

    def feature_engineering_cached(self, filename):
        cached_filename = filename + "mf";
        if( os.path.isfile( cached_filename ) == False ):
            data_row, frequency = feature_engineering(filename)
            np.savetxt( cached_filename, data_row )
        
        return np.loadtxt( cached_filename, dtype='float' )

                    
    def __len__(self):
        return len( self.samples )

    def __getitem__(self, idx):
        filename = self.samples[idx][0]
        data_row = self.feature_engineering_cached(filename)
        return torch.tensor(data_row).float(), self.samples[idx][1]
		
    def get_labels(self):
        return self.paths
