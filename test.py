import os
import glob
import struct
import torch
from torch.utils.data import Dataset,DataLoader
import torch.nn as nn
import numpy as np
import torch.nn.functional as F
from functools import partial
from einops.layers.torch import Rearrange,Reduce
import pandas as pd
from argparse import Namespace
from visdom import Visdom
from sklearn.metrics import precision_score,recall_score,confusion_matrix
from sklearn import preprocessing
import time
import torch.optim as optim
from omegaconf import DictConfig, ListConfig, OmegaConf

from torch_model import Mutil_Mixer3
from dataset import Packet_Dataset
from visualization import vis_matrix_tor,vis_matrix_ustc,vis_matrix_vpn


config = OmegaConf.load('./test_config.yaml')


hparam=Namespace(
    **{
        'patch_size':config.model.patch_size,
        'head_index':torch.arange(0,40,1).cuda(),
        'body_index':torch.arange(40,1500,1).cuda(),
        'dim':config.model.dim,
        'packet_size':config.model.packet_size,
        'expansion_factor':config.model.expansion_factor,
        'depth':config.model.depth,
        'h1_class':config.model.h1_class,
        'num_class':config.model.num_class,        
        'dropout':config.model.dropout
    }
)

batch_size = config.model.batch_size
resume = config.model.resume
a = config.model.a
b = config.model.b
c = config.model.c
epoch_num = config.model.epoch_num
learning_rate = config.model.learning_rate
num_class = config.model.num_class

model_state_path = config.model.model_state_path
optimizer_state_path = config.model.optimizer_state_path
output_file_path = config.model.output_file_path





test_dataset=Packet_Dataset(config.dataset.test_set)
test_dataloader=DataLoader(test_dataset,shuffle=True,batch_size=batch_size,num_workers=4)



if resume>0:
    file=open(output_file_path,"a")
else:
    file=open(output_file_path,'w')
    

if num_class == 14:
    vis = vis_matrix_tor()
elif num_class == 12:
    vis = vis_matrix_vpn()
elif num_class == 18:
    vis = vis_matrix_ustc()

model=Mutil_Mixer3(hparam).cuda()


criterion=nn.CrossEntropyLoss()
criterion_BCE=nn.BCEWithLogitsLoss() 

optimizer=optim.SGD(model.parameters(),lr=learning_rate,momentum=0.9)
CosLR=torch.optim.lr_scheduler.CosineAnnealingLR(optimizer,T_max=epoch_num)

if resume>0:
    model.load_state_dict(torch.load(os.path.join(model_state_path,"model_"+str(resume-1)+".pt")))
    optimizer.load_state_dict(torch.load(os.path.join(optimizer_state_path,"optimizer_"+str(resume-1)+".pt")))

for epoch in range(resume,resume+1):
    start=time.time()
    
    train_acc1=0.0
    train_acc2=0.0
    
    train_loss=0.0
    
    valid_acc1=0.0
    valid_acc2=0.0
    
    #计算h1
    valid_pre_h1=np.zeros(2)
    valid_recall_h1=np.zeros(2)
    valid_f1_h1=np.zeros(2)
    
    valid_confusion_matrix_h1=np.zeros((2,2))
    #计算h2
    valid_pre=np.zeros(num_class)
    valid_recall=np.zeros(num_class)
    valid_f1=np.zeros(num_class)
    
    valid_confusion_matrix=np.zeros((num_class,num_class))
    
    model.eval()
    with torch.no_grad():
        for i,data in enumerate(test_dataloader):
            
            x=data[0].cuda()
            x1=data[1].cuda()
            
            h1_out,h2_out,cat_h=model(x,x1)
            
            v_acc1=np.sum(np.argmax(h1_out.cpu().data.numpy(),axis=1) == data[2].numpy())
            v_acc2=np.sum(np.argmax(h2_out.cpu().data.numpy(),axis=1) == data[3].numpy())
            
            valid_acc1+=v_acc1
            valid_acc2+=v_acc2
            
            #计算h1的混淆矩阵
            h1_confusion=confusion_matrix(data[2].numpy(),np.argmax(h1_out.cpu().data.numpy(),axis=1),labels=[0,1])
            valid_confusion_matrix_h1+=h1_confusion
            
            #计算了h2的混淆矩阵
            v_confusion_matrix=confusion_matrix(data[3].numpy(),np.argmax(h2_out.cpu().data.numpy(),axis=1),labels=list(range(num_class)))
            valid_confusion_matrix+=v_confusion_matrix
        
        #计算h1的三个指标
        valid_pre_h1=np.diag(valid_confusion_matrix_h1)/np.sum(valid_confusion_matrix_h1,axis=0)
        valid_recall_h1=np.diag(valid_confusion_matrix_h1)/np.sum(valid_confusion_matrix_h1,axis=1)
        valid_f1_h1=(2*valid_recall_h1*valid_pre_h1)/(valid_pre_h1+valid_recall_h1)
        
        #计算h2的三个指标
        valid_pre=np.diag(valid_confusion_matrix)/np.sum(valid_confusion_matrix,axis=0)
            
        valid_recall=np.diag(valid_confusion_matrix)/np.sum(valid_confusion_matrix,axis=1)
        
        valid_f1=2*valid_pre*valid_recall/(valid_pre+valid_recall)
        
        
        print("valid_acc1:{:.4f},valid_acc2:{:.4f},\
        valid_pre:{},valid_recall:{},valid_f1:{}\n".format(valid_acc1/test_dataset.__len__(),valid_acc2/test_dataset.__len__(),valid_pre,valid_recall,valid_f1))
        print("confusion_matrix:{}\n".format(valid_confusion_matrix))
        
        file.write("valid_acc1:{:.4f},valid_acc2:{:.4f},\
        valid_pre:{},valid_recall:{},valid_f1:{}\n".format(valid_acc1/test_dataset.__len__(),valid_acc2/test_dataset.__len__(),valid_pre,valid_recall,valid_f1))
        file.write("confusion_matrix:{}\n".format(valid_confusion_matrix))
        
        print("------------")
        
        #写入h1的数据
        print("valid_pre:{},valid_recall:{},valid_f1:{}\n".format(valid_pre_h1,valid_recall_h1,valid_f1_h1))
        print("confusion_matrix:{}\n".format(valid_confusion_matrix_h1))
        
        file.write("valid_pre:{},valid_recall:{},valid_f1:{}\n".format(valid_pre_h1,valid_recall_h1,valid_f1_h1))
        file.write("confusion_matrix:{}\n".format(valid_confusion_matrix_h1))
        
        
        file.flush()#将缓冲区数据全部写入文件
    
    
    
    CosLR.step()
    
    print("time:",time.time()-start)
    
file.close()