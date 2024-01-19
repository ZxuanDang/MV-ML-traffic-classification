import torch
import pandas as pd
from torch.utils.data import Dataset

globa = {
    'nan': 0   
}


class Packet_Dataset(Dataset):
    def __init__(self,dataset_path,label=True):
        super(Packet_Dataset,self).__init__()
        
        
        self.pd=pd.read_csv(dataset_path)
        
        self.label=label
        #Tor
        #self.dic={0:0,1:1,2:2,3:3,4:4,5:5}
        
        #VPN
        #self.dic={0:0,1:1,3:2,5:3,6:4,8:5,9:6,11:7}
        
    def __len__(self):
        return len(self.pd)
    
    def __getitem__(self,idx):
        x=torch.tensor(eval(self.pd["packet"][idx]),dtype=torch.float)
        x1=torch.tensor(eval(self.pd["feature"][idx],globa),dtype=torch.float)
        if self.label:
            y1=torch.tensor(self.pd["h1_label"][idx],dtype=torch.float)
            y2=torch.tensor(self.pd["traffic_label"][idx],dtype=torch.float) 
            return x,x1,y1,y2
        else:
            return x,x1