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


config = OmegaConf.load('./train_config.yaml')


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





t_dataset=Packet_Dataset(config.dataset.train_set)
t_dataloader=DataLoader(t_dataset,shuffle=True,batch_size=batch_size,num_workers=4)

v_dataset=Packet_Dataset(config.dataset.valid_set)
v_dataloader=DataLoader(v_dataset,shuffle=True,batch_size=batch_size,num_workers=4)



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

for epoch in range(resume,epoch_num):
    start=time.time()
    
    train_acc1=0.0
    train_acc2=0.0
    
    train_loss=0.0
    
    valid_acc1=0.0
    valid_acc2=0.0
    
    valid_pre=np.zeros(num_class)
    valid_recall=np.zeros(num_class)
    valid_f1=np.zeros(num_class)
    
    valid_confusion_matrix=np.zeros((num_class,num_class))
    
    model.train() #model.train()会启动model里面的dropout和Layernorm
    for i,data in enumerate(t_dataloader):

        """
        data[0]:x    packet
        data[1]:x1   feature
        data[2]:y1   h1_label
        data[3]:y2   traffic_label
        """
        optimizer.zero_grad()
        model.zero_grad()
        x=data[0].cuda()
        x1=data[1].cuda()
        #print(i)
        #print(x.shape)
        h1_out,h2_out,cat_h=model(x,x1)
        #print(pred)
        #print(data[1])
        
        loss1=criterion(h1_out,data[2].long().cuda())
        loss2=criterion(h2_out,data[3].long().cuda())
        
        a1=torch.tensor(nn.functional.one_hot(data[2].long(),num_classes=2),dtype=torch.float16)
        a2=torch.tensor(nn.functional.one_hot(data[3].long(),num_classes=num_class),dtype=torch.float16)
        
        loss3=criterion_BCE(cat_h,torch.cat((a1,a2),dim=1).cuda()) ##BCELOSS
        
        
        #print(np.argmax(pred.cpu().data.numpy(), axis=1))
        #input()
        #print(data[1].numpy())
        acc1=np.sum(np.argmax(h1_out.cpu().data.numpy(), axis=1) == data[2].numpy())
        acc2=np.sum(np.argmax(h2_out.cpu().data.numpy(), axis=1) == data[3].numpy())
        
        #print("batch_acc:{}".format(acc/batch_size))
        train_acc1 += acc1
        train_acc2 += acc2
        
        #print(loss1)
        #print(loss2)
        #print(loss3)
        
        if epoch>49:
            b=0.7
            c=0.2
            
        loss=a*loss1+b*loss2+c*loss3
        #loss=loss1+loss2+loss3
        
        train_loss+=loss1+loss2+loss3
        
        loss.backward()
        optimizer.step()
    
    torch.save(model.state_dict(),os.path.join(model_state_path,"model_%d.pt" % epoch))
    torch.save(optimizer.state_dict(),os.path.join(optimizer_state_path,"optimizer_%d.pt" % epoch))

    
    model.eval() #eval()不会启动dropout和layernorm将整个网络进行训练
    with torch.no_grad():
        for i,data in enumerate(v_dataloader):
            
            x=data[0].cuda()
            x1=data[1].cuda()
            
            h1_out,h2_out,cat_h=model(x,x1)
            
            v_acc1=np.sum(np.argmax(h1_out.cpu().data.numpy(),axis=1) == data[2].numpy())
            v_acc2=np.sum(np.argmax(h2_out.cpu().data.numpy(),axis=1) == data[3].numpy())
            
            valid_acc1+=v_acc1
            valid_acc2+=v_acc2
            
            #计算了h2的混淆矩阵
            v_confusion_matrix=confusion_matrix(data[3].numpy(),np.argmax(h2_out.cpu().data.numpy(),axis=1),labels=list(range(num_class)))
            valid_confusion_matrix+=v_confusion_matrix
        
        
        valid_pre=np.diag(valid_confusion_matrix)/np.sum(valid_confusion_matrix,axis=0)
                    
        valid_recall=np.diag(valid_confusion_matrix)/np.sum(valid_confusion_matrix,axis=1)
          
        valid_f1=2*valid_pre*valid_recall/(valid_pre+valid_recall)
        
        
        print("valid_acc1:{:.4f},valid_acc2:{:.4f},\
        valid_pre:{},valid_recall:{},valid_f1:{}\n".format(valid_acc1/v_dataset.__len__(),valid_acc2/v_dataset.__len__(),valid_pre,valid_recall,valid_f1))
        print("confusion_matrix:{}\n".format(valid_confusion_matrix))
        
        file.write("valid_acc1:{:.4f},valid_acc2:{:.4f},\
        valid_pre:{},valid_recall:{},valid_f1:{}\n".format(valid_acc1/v_dataset.__len__(),valid_acc2/v_dataset.__len__(),valid_pre,valid_recall,valid_f1))
        file.write("confusion_matrix:{}\n".format(valid_confusion_matrix))
        
        file.flush()#将缓冲区数据全部写入文件
    
    t_length = t_dataset.__len__()
    v_length = v_dataset.__len__()
    vis.draw(
        train_loss=train_loss,
        epoch=epoch,
        valid_pre=valid_pre,
        valid_recall=valid_recall,
        valid_f1=valid_f1,
        valid_acc1=valid_acc1,
        valid_acc2=valid_acc2,
        t_length=t_length,
        v_length=v_length,
        valid_confusion_matrix=valid_confusion_matrix,
        )
    
    CosLR.step()
    
    print("time:",time.time()-start)
    
file.close()