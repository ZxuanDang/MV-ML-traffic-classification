from visdom import Visdom
import numpy as np


class vis_matrix_tor():
    def __init__(self) -> None:
        
        self.viz = Visdom(env="tor")

        
        self.viz.line([0.],[0.],win="train_loss",opts=dict(title='train_loss'))
        self.viz.line([0.],[0.],win="valid_acc_h1",opts=dict(title='valid_acc_h1'))
        self.viz.line([0.],[0.],win="valid_acc_h2",opts=dict(title='valid_acc_h2'))

        
        self.viz.line(X=[0.],Y=[[0.,0.,0.]],win="0_chat",opts=dict(title='chat',legend=['precision','recall','f1']))
        self.viz.line(X=[0.],Y=[[0.,0.,0.]],win="1_Tor_chat",opts=dict(title='Tor_chat',legend=['precision','recall','f1']))

        self.viz.line(X=[0.],Y=[[0.,0.,0.]],win="2_email",opts=dict(title='email',legend=['precision','recall','f1']))
        self.viz.line(X=[0.],Y=[[0.,0.,0.]],win="3_Tor_email",opts=dict(title='Tor_email',legend=['precision','recall','f1']))

        self.viz.line(X=[0.],Y=[[0.,0.,0.]],win="4_streaming",opts=dict(title='streaming',legend=['precision','recall','f1']))
        self.viz.line(X=[0.],Y=[[0.,0.,0.]],win="5_Tor_streaming",opts=dict(title='Tor_streaming',legend=['precision','recall','f1']))

        self.viz.line(X=[0.],Y=[[0.,0.,0.]],win="6_Browsing",opts=dict(title='Browsing',legend=['precision','recall','f1']))
        self.viz.line(X=[0.],Y=[[0.,0.,0.]],win="7_Tor_Browsing",opts=dict(title='Tor_Browsing',legend=['precision','recall','f1']))

        self.viz.line(X=[0.],Y=[[0.,0.,0.]],win="8_FTP",opts=dict(title='FTP',legend=['precision','recall','f1']))
        self.viz.line(X=[0.],Y=[[0.,0.,0.]],win="9_Tor_FTP",opts=dict(title='Tor_FTP',legend=['precision','recall','f1']))

        self.viz.line(X=[0.],Y=[[0.,0.,0.]],win="10_VoIP",opts=dict(title='VoIP',legend=['precision','recall','f1']))
        self.viz.line(X=[0.],Y=[[0.,0.,0.]],win="11_Tor_VoIP",opts=dict(title='Tor_VoIP',legend=['precision','recall','f1']))

        self.viz.line(X=[0.],Y=[[0.,0.,0.]],win="12_P2P",opts=dict(title='P2P',legend=['precision','recall','f1']))
        self.viz.line(X=[0.],Y=[[0.,0.,0.]],win="13_Tor_P2P",opts=dict(title='Tor_P2P',legend=['precision','recall','f1']))

    def draw(
        self,
        train_loss,
        epoch,
        valid_pre,
        valid_recall,
        valid_f1,
        valid_acc1,
        valid_acc2,
        t_length,
        v_length,
        valid_confusion_matrix,
    ):
        
        self.viz.line([(train_loss/t_length).item()],[epoch],win="train_loss",update='append')
        self.viz.line([(valid_acc1/v_length).item()],[epoch],win='valid_acc_h1',update="append")
        self.viz.line([(valid_acc2/v_length).item()],[epoch],win='valid_acc_h2',update="append")
        
        self.viz.line(X=[epoch],Y=[[(valid_pre)[0],(valid_recall)[0],(valid_f1)[0]]],win="0_chat",update='append')
        self.viz.line(X=[epoch],Y=[[(valid_pre)[1],(valid_recall)[1],(valid_f1)[1]]],win="1_Tor_chat",update='append')

        self.viz.line(X=[epoch],Y=[[(valid_pre)[2],(valid_recall)[2],(valid_f1)[2]]],win="2_email",update='append')
        self.viz.line(X=[epoch],Y=[[(valid_pre)[3],(valid_recall)[3],(valid_f1)[3]]],win="3_Tor_email",update='append')

        self.viz.line(X=[epoch],Y=[[(valid_pre)[4],(valid_recall)[4],(valid_f1)[4]]],win="4_streaming",update='append')
        self.viz.line(X=[epoch],Y=[[(valid_pre)[5],(valid_recall)[5],(valid_f1)[5]]],win="5_Tor_streaming",update='append')

        self.viz.line(X=[epoch],Y=[[(valid_pre)[6],(valid_recall)[6],(valid_f1)[6]]],win="6_Browsing",update='append')
        self.viz.line(X=[epoch],Y=[[(valid_pre)[7],(valid_recall)[7],(valid_f1)[7]]],win="7_Tor_Browsing",update='append')

        self.viz.line(X=[epoch],Y=[[(valid_pre)[8],(valid_recall)[8],(valid_f1)[8]]],win="8_FTP",update='append')
        self.viz.line(X=[epoch],Y=[[(valid_pre)[9],(valid_recall)[9],(valid_f1)[9]]],win="9_Tor_FTP",update='append')
        
        self.viz.line(X=[epoch],Y=[[(valid_pre)[10],(valid_recall)[10],(valid_f1)[10]]],win="10_VoIP",update='append')
        self.viz.line(X=[epoch],Y=[[(valid_pre)[11],(valid_recall)[11],(valid_f1)[11]]],win="11_Tor_VoIP",update='append')
            
        self.viz.line(X=[epoch],Y=[[(valid_pre)[12],(valid_recall)[12],(valid_f1)[12]]],win="12_P2P",update='append')
        self.viz.line(X=[epoch],Y=[[(valid_pre)[13],(valid_recall)[13],(valid_f1)[13]]],win="13_Tor_P2P",update='append')
        
        
        self.viz.heatmap(valid_confusion_matrix/np.max(valid_confusion_matrix),win="x",
            opts={
                    "rownames" : ["chat",'Tor_chat','email','Tor_email',"streaming", 'Tor_streaming',"Browsing", 'Tor_Browsing',"FTP",'Tor_FTP','VoIP','Tor_VoIP','P2P','Tor_P2P'],
                    "columnnames" : ["chat",'Tor_chat','email','Tor_email',"streaming", 'Tor_streaming',"Browsing", 'Tor_Browsing',"FTP",'Tor_FTP','VoIP','Tor_VoIP','P2P','Tor_P2P'],
                    "title" : "confusion_matrix"
                })



class vis_matrix_vpn():
    def __init__(self) -> None:
        
        self.viz = Visdom(env="vpn")

       
        self.viz.line([0.],[0.],win="train_loss",opts=dict(title='train_loss'))
        self.viz.line([0.],[0.],win="valid_acc_h1",opts=dict(title='valid_acc_h1'))
        self.viz.line([0.],[0.],win="valid_acc_h2",opts=dict(title='valid_acc_h2'))

        
        self.viz.line(X=[0.],Y=[[0.,0.,0.]],win="0_chat",opts=dict(title='chat',legend=['precision','recall','f1']))
        self.viz.line(X=[0.],Y=[[0.,0.,0.]],win="6_VPN_chat",opts=dict(title='VPN_chat',legend=['precision','recall','f1']))

        self.viz.line(X=[0.],Y=[[0.,0.,0.]],win="1_email",opts=dict(title='email',legend=['precision','recall','f1']))
        self.viz.line(X=[0.],Y=[[0.,0.,0.]],win="8_VPN_email",opts=dict(title='VPN_email',legend=['precision','recall','f1']))

        self.viz.line(X=[0.],Y=[[0.,0.,0.]],win="3_streaming",opts=dict(title='streaming',legend=['precision','recall','f1']))
        self.viz.line(X=[0.],Y=[[0.,0.,0.]],win="9_VPN_streaming",opts=dict(title='VPN_streaming',legend=['precision','recall','f1']))

        self.viz.line(X=[0.],Y=[[0.,0.,0.]],win="5_VoIP",opts=dict(title='VoIP',legend=['precision','recall','f1']))
        self.viz.line(X=[0.],Y=[[0.,0.,0.]],win="11_VPN_VoIP",opts=dict(title='VPN_VoIP',legend=['precision','recall','f1']))

        self.viz.line(X=[0.],Y=[[0.,0.,0.]],win="2_File_Transfer",opts=dict(title='File_Transfer',legend=['precision','recall','f1']))
        self.viz.line(X=[0.],Y=[[0.,0.,0.]],win="7_VPN_File_Transfer",opts=dict(title='VPN_File_Transfer',legend=['precision','recall','f1']))

        self.viz.line(X=[0.],Y=[[0.,0.,0.]],win="4_Torrent",opts=dict(title='Torrent',legend=['precision','recall','f1']))
        self.viz.line(X=[0.],Y=[[0.,0.,0.]],win="10_VPN_Torrent",opts=dict(title='VPN_Torrent',legend=['precision','recall','f1']))
    
    def draw(
        self,
        train_loss,
        epoch,
        valid_pre,
        valid_recall,
        valid_f1,
        valid_acc1,
        valid_acc2,
        t_length,
        v_length,
        valid_confusion_matrix,
    ):
        
        self.viz.line([(train_loss/t_length).item()],[epoch],win="train_loss",update='append')
        self.viz.line([(valid_acc1/v_length).item()],[epoch],win='valid_acc_h1',update="append")
        self.viz.line([(valid_acc2/v_length).item()],[epoch],win='valid_acc_h2',update="append")
        
        self.viz.line(X=[epoch],Y=[[(valid_pre)[0],(valid_recall)[0],(valid_f1)[0]]],win="0_chat",update='append')
        self.viz.line(X=[epoch],Y=[[(valid_pre)[6],(valid_recall)[6],(valid_f1)[6]]],win="6_VPN_chat",update='append')

        self.viz.line(X=[epoch],Y=[[(valid_pre)[1],(valid_recall)[1],(valid_f1)[1]]],win="1_email",update='append')
        self.viz.line(X=[epoch],Y=[[(valid_pre)[8],(valid_recall)[8],(valid_f1)[8]]],win="8_VPN_email",update='append')

        self.viz.line(X=[epoch],Y=[[(valid_pre)[3],(valid_recall)[3],(valid_f1)[3]]],win="3_streaming",update='append')
        self.viz.line(X=[epoch],Y=[[(valid_pre)[9],(valid_recall)[9],(valid_f1)[9]]],win="9_VPN_streaming",update='append')

        self.viz.line(X=[epoch],Y=[[(valid_pre)[5],(valid_recall)[5],(valid_f1)[5]]],win="5_VoIP",update='append')
        self.viz.line(X=[epoch],Y=[[(valid_pre)[11],(valid_recall)[11],(valid_f1)[11]]],win="11_VPN_VoIP",update='append')
        
        self.viz.line(X=[epoch],Y=[[(valid_pre)[2],(valid_recall)[2],(valid_f1)[2]]],win="2_File_Transfer",update='append')
        self.viz.line(X=[epoch],Y=[[(valid_pre)[7],(valid_recall)[7],(valid_f1)[7]]],win="7_VPN_File_Transfer",update='append')
        
        self.viz.line(X=[epoch],Y=[[(valid_pre)[4],(valid_recall)[4],(valid_f1)[4]]],win="4_Torrent",update='append')
        self.viz.line(X=[epoch],Y=[[(valid_pre)[10],(valid_recall)[10],(valid_f1)[10]]],win="10_VPN_Torrent",update='append')
        
        
        
        self.viz.heatmap(valid_confusion_matrix/np.max(valid_confusion_matrix),win="x",
            opts={
                    "rownames" : ["chat",'email',"File_Transfer","streaming", "Torrent",'VoIP',"VPN_chat",'VPN_File_Transfer','VPN_email','VPN_streaming','VPN_Torrent','VPN_VoIP'],
                    "columnnames" :["chat",'email',"File_Transfer","streaming", "Torrent",'VoIP',"VPN_chat",'VPN_File_Transfer','VPN_email','VPN_streaming','VPN_Torrent','VPN_VoIP'],
                    "title" : "confusion_matrix"
                    
        })


class vis_matrix_ustc():
    def __init__(self) -> None:
        
        self.viz = Visdom(env="ustc")

        
        self.viz.line([0.],[0.],win="train_loss",opts=dict(title='train_loss'))
        self.viz.line([0.],[0.],win="valid_acc_h1",opts=dict(title='valid_acc_h1'))
        self.viz.line([0.],[0.],win="valid_acc_h2",opts=dict(title='valid_acc_h2'))

        #
        self.viz.line(X=[0.],Y=[[0.,0.,0.]],win="0_chat",opts=dict(title='chat',legend=['precision','recall',"f1"]))
        self.viz.line(X=[0.],Y=[[0.,0.,0.]],win="1_Database",opts=dict(title='Database',legend=['precision','recall',"f1"]))

        self.viz.line(X=[0.],Y=[[0.,0.,0.]],win="2_email",opts=dict(title='email',legend=['precision','recall',"f1"]))
        self.viz.line(X=[0.],Y=[[0.,0.,0.]],win="3_FTP",opts=dict(title='FTP',legend=['precision','recall',"f1"]))

        self.viz.line(X=[0.],Y=[[0.,0.,0.]],win="4_game",opts=dict(title='game',legend=['precision','recall',"f1"]))
        self.viz.line(X=[0.],Y=[[0.,0.,0.]],win="5_P2P",opts=dict(title='P2P',legend=['precision','recall',"f1"]))

        self.viz.line(X=[0.],Y=[[0.,0.,0.]],win="6_Social_Network",opts=dict(title='Social_Network',legend=['precision','recall',"f1"]))
        self.viz.line(X=[0.],Y=[[0.,0.,0.]],win="7_Streaming",opts=dict(title='Streaming',legend=['precision','recall',"f1"]))

        self.viz.line(X=[0.],Y=[[0.,0.,0.]],win="8_Cridex",opts=dict(title='Cridex',legend=['precision','recall',"f1"]))
        self.viz.line(X=[0.],Y=[[0.,0.,0.]],win="9_Geodo",opts=dict(title='Geodo',legend=['precision','recall',"f1"]))

        self.viz.line(X=[0.],Y=[[0.,0.,0.]],win="10_Htbot",opts=dict(title='Htbot',legend=['precision','recall',"f1"]))
        self.viz.line(X=[0.],Y=[[0.,0.,0.]],win="11_Miuref",opts=dict(title='Miuref',legend=['precision','recall',"f1"]))

        self.viz.line(X=[0.],Y=[[0.,0.,0.]],win="12_Neris",opts=dict(title='Neris',legend=['precision','recall',"f1"]))
        self.viz.line(X=[0.],Y=[[0.,0.,0.]],win="13_Nsis-ay",opts=dict(title='Nsis-ay',legend=['precision','recall',"f1"]))

        self.viz.line(X=[0.],Y=[[0.,0.,0.]],win="14_Shifu",opts=dict(title='Shifu',legend=['precision','recall',"f1"]))
        self.viz.line(X=[0.],Y=[[0.,0.,0.]],win="15_Tinba",opts=dict(title='Tinba',legend=['precision','recall',"f1"]))

        self.viz.line(X=[0.],Y=[[0.,0.,0.]],win="16_Virut",opts=dict(title='Virut',legend=['precision','recall',"f1"]))
        self.viz.line(X=[0.],Y=[[0.,0.,0.]],win="17_Zeus",opts=dict(title='Zeus',legend=['precision','recall',"f1"]))

    def draw(
        self,
        train_loss,
        epoch,
        valid_pre,
        valid_recall,
        valid_f1,
        valid_acc1,
        valid_acc2,
        t_length,
        v_length,
        valid_confusion_matrix,
    ):
        
        self.viz.line([(train_loss/t_length.__len__()).item()],[epoch],win="train_loss",update='append')
        self.viz.line([(valid_acc1/v_length.__len__()).item()],[epoch],win='valid_acc_h1',update="append")
        self.viz.line([(valid_acc2/v_length.__len__()).item()],[epoch],win='valid_acc_h2',update="append")
        
        self.viz.line(X=[epoch],Y=[[(valid_pre)[0],(valid_recall)[0],(valid_f1)[0]]],win="0_chat",update='append')
        self.viz.line(X=[epoch],Y=[[(valid_pre)[1],(valid_recall)[1],(valid_f1)[1]]],win="1_Database",update='append')

        self.viz.line(X=[epoch],Y=[[(valid_pre)[2],(valid_recall)[2],(valid_f1)[2]]],win="2_email",update='append')
        self.viz.line(X=[epoch],Y=[[(valid_pre)[3],(valid_recall)[3],(valid_f1)[3]]],win="3_FTP",update='append')

        self.viz.line(X=[epoch],Y=[[(valid_pre)[4],(valid_recall)[4],(valid_f1)[4]]],win="4_game",update='append')
        self.viz.line(X=[epoch],Y=[[(valid_pre)[5],(valid_recall)[5],(valid_f1)[5]]],win="5_P2P",update='append')

        self.viz.line(X=[epoch],Y=[[(valid_pre)[6],(valid_recall)[6],(valid_f1)[6]]],win="6_Social_Network",update='append')
        self.viz.line(X=[epoch],Y=[[(valid_pre)[7],(valid_recall)[7],(valid_f1)[7]]],win="7_Streaming",update='append')

        self.viz.line(X=[epoch],Y=[[(valid_pre)[8],(valid_recall)[8],(valid_f1)[8]]],win="8_Cridex",update='append')
        self.viz.line(X=[epoch],Y=[[(valid_pre)[9],(valid_recall)[9],(valid_f1)[9]]],win="9_Geodo",update='append')
        
        self.viz.line(X=[epoch],Y=[[(valid_pre)[10],(valid_recall)[10],(valid_f1)[10]]],win="10_Htbot",update='append')
        self.viz.line(X=[epoch],Y=[[(valid_pre)[11],(valid_recall)[11],(valid_f1)[11]]],win="11_Miuref",update='append')
            
        self.viz.line(X=[epoch],Y=[[(valid_pre)[12],(valid_recall)[12],(valid_f1)[12]]],win="12_Neris",update='append')
        self.viz.line(X=[epoch],Y=[[(valid_pre)[13],(valid_recall)[13],(valid_f1)[13]]],win="13_Nsis-ay",update='append')
        
        self.viz.line(X=[epoch],Y=[[(valid_pre)[14],(valid_recall)[14],(valid_f1)[14]]],win="14_Shifu",update='append')
        self.viz.line(X=[epoch],Y=[[(valid_pre)[15],(valid_recall)[15],(valid_f1)[15]]],win="15_Tinba",update='append')
            
        self.viz.line(X=[epoch],Y=[[(valid_pre)[16],(valid_recall)[16],(valid_f1)[16]]],win="16_Virut",update='append')
        self.viz.line(X=[epoch],Y=[[(valid_pre)[17],(valid_recall)[17],(valid_f1)[17]]],win="17_Zeus",update='append')
        

        self.viz.heatmap(valid_confusion_matrix/np.max(valid_confusion_matrix),win="x",
            opts={
                    "rownames" : ["chat",'Database','email','FTP',"game", 'P2P',"Social_Network", 'Streaming',"Cridex",'Geodo','Htbot','Miuref','Neris','Nsis-ay',"Shifu","Tinba","Virut","Zeus"],
                    "columnnames" : ["chat",'Database','email','FTP',"game", 'P2P',"Social_Network", 'Streaming',"Cridex",'Geodo','Htbot','Miuref','Neris','Nsis-ay',"Shifu","Tinba","Virut","Zeus"],
                    "title" : "confusion_matrix"
            })