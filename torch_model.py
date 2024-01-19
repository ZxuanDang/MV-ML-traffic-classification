import torch
import torch.nn as nn
from functools import partial
from einops.layers.torch import Rearrange,Reduce


class PreNormResidual(nn.Module):
    def __init__(self,dim,fn):
        super(PreNormResidual,self).__init__()
        self.fn=fn
        self.norm=nn.LayerNorm(dim)
        
    def forward(self,x):
        return self.fn(self.norm(x)) + x

def FeedForward(dim,expansion_factor=4,dropout=0.,dense=nn.Linear):
    return nn.Sequential(
        dense(dim,dim*expansion_factor),
        nn.GELU(),
        nn.Dropout(dropout),
        dense(dim*expansion_factor,dim),
        nn.Dropout(dropout)
    )

class Mutil_Mixer3(nn.Module):
    def __init__(self,hparam):
        super(Mutil_Mixer3,self).__init__()
        
        chan_first=partial(nn.Conv1d,kernel_size=1)
        chan_last=nn.Linear
        
        self.relu=nn.ReLU()
        
        self.h_index=hparam.head_index
        self.b_index=hparam.body_index
        
        num_patchs_h= self.h_index.shape[0] // hparam.patch_size     #  h==num_patchs
        
        self.head_extractor=nn.Sequential(
            #torch.Size([batch_size, 1, 1, head_index_length])
            Rearrange('b c h (w p1) -> b w (h p1 c)',p1=hparam.patch_size),
            nn.Linear( hparam.patch_size,hparam.dim),
            
            *[
                nn.Sequential(
                    PreNormResidual(hparam.dim,FeedForward(num_patchs_h,hparam.expansion_factor,hparam.dropout,chan_first)), #num_patch对应输入通道数
                    PreNormResidual(hparam.dim,FeedForward(hparam.dim,hparam.expansion_factor,hparam.dropout,chan_last))
                )for _ in range(1)
            ],
            nn.LayerNorm(hparam.dim),
        )  #[b,1,dim] 
        
        
        assert (self.b_index.shape[0] % hparam.patch_size)==0
        
        num_patchs= self.b_index.shape[0] // hparam.patch_size     #  h==num_patchs
        
        self.body_extractor=nn.Sequential(
            
            #torch.Size([batch_size, 1, 1, bode_index_length])
            Rearrange('b c h (w p1)-> b w (p1 h c)',p1=hparam.patch_size),
            nn.Linear( hparam.patch_size,hparam.dim),
            *[
                nn.Sequential(
                    PreNormResidual(hparam.dim,FeedForward(num_patchs,hparam.expansion_factor,hparam.dropout,chan_first)), #num_patch对应输入通道数
                    PreNormResidual(hparam.dim,FeedForward(hparam.dim,hparam.expansion_factor,hparam.dropout,chan_last))
                )for _ in range(2)
            ], #[b,n,dim]
            nn.LayerNorm(hparam.dim),
            #Reduce('b n c -> b c','mean'), #[b,dim]
        )
        
        self.mixerlayer1=nn.Sequential(
            *[
                nn.Sequential(
                    PreNormResidual(hparam.dim,FeedForward(num_patchs+num_patchs_h+1,hparam.expansion_factor,hparam.dropout,chan_first)), #num_patch对应输入通道数
                    PreNormResidual(hparam.dim,FeedForward(hparam.dim,hparam.expansion_factor,hparam.dropout,chan_last))  #不能少
                )
            ],
            nn.LayerNorm(hparam.dim),
            #Reduce('b n c -> b c','mean'),
            #nn.Linear(hparam.dim,hparam.num_class)
        )
        
        self.mixerlayer2=nn.Sequential(
            *[
                nn.Sequential(
                    PreNormResidual(hparam.dim,FeedForward(num_patchs+num_patchs_h+1,hparam.expansion_factor,hparam.dropout,chan_first)), #num_patch对应输入通道数
                    PreNormResidual(hparam.dim,FeedForward(hparam.dim,hparam.expansion_factor,hparam.dropout,chan_last))  #不能少
                )
            ],
            nn.LayerNorm(hparam.dim),
            Reduce('b n c -> b c','mean'),
        )
        
        self.mixerlayer3=nn.Sequential(
            *[
                nn.Sequential(
                    PreNormResidual(hparam.dim,FeedForward(num_patchs+num_patchs_h+1,hparam.expansion_factor,hparam.dropout,chan_first)), #num_patch对应输入通道数
                    PreNormResidual(hparam.dim,FeedForward(hparam.dim,hparam.expansion_factor,hparam.dropout,chan_last))  #不能少
                )
            ],
            nn.LayerNorm(hparam.dim),
            Reduce('b n c -> b c','mean'),
        )
        
        self.feature_linear=nn.Linear(8,hparam.dim)
        
        self.h1_linear1=nn.Linear(hparam.dim,hparam.h1_class)
        self.h1_linear2=nn.Linear(hparam.dim,hparam.h1_class)
        
        self.h2_linear1=nn.Linear(hparam.dim,hparam.num_class)
        self.h2_linear2=nn.Linear(hparam.dim,hparam.num_class)
    
    def forward(self,x,x1):
        x=x.unsqueeze(1)     #torch.Size([batchsize,1,1500])
        x=x.unsqueeze(1)     #torch.Size([batchsize,1,1,1500])
        
        #head=torch.index_select(x,2,self.h_index).cuda()
        
        x1=self.feature_linear(x1)
        x1=x1.unsqueeze(1)

        head_extract=self.head_extractor(torch.index_select(x,3,self.h_index)) #torch.Size([batch_size,1,hparam.dim])

        body_extract=self.body_extractor(torch.index_select(x,3,self.b_index))   #torch.Size([batch_size,num_patch,hparam.dim])
        
        out1=self.mixerlayer1(torch.cat([body_extract,head_extract,x1],dim=1))       #[b, n+1+1,dim]
        
        out2=self.mixerlayer2(out1)
        
        out3=self.mixerlayer3(out1)
        
        
        h1_out=self.h1_linear1( self.relu(out2) ) 
        
        h2_out=self.h2_linear1( self.relu(out2 + out3) )
        #pre=self.classifier(torch.cat([out,x1],dim=1))
        
        
        h1_out_=self.h1_linear2( self.relu(out2) ) 
        
        h2_out_=self.h2_linear2( self.relu(out2 + out3) )
        
        h1_mod=nn.Sigmoid()(h1_out_)
        h2_mod=nn.Sigmoid()(h2_out_)
        
        cat_h1_h2=torch.cat((h1_mod,h2_mod),dim=1)
        
        
        return h1_out,h2_out,cat_h1_h2
    