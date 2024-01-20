import argparse
from pre_packet import *
import pandas as pd
from utils import MY_VPN_TRAFFIC_TO_ID,MY_VPN_H1_LABEL,MY_TOR_TRAFFIC_TO_ID,MY_TOR_H1_LABEL,MY_USTC_H1_LABEL,MY_USTC_TRAFFIC_TO_ID,MY_DATACON_H1_LABEL
import cv2
import os
from tqdm import tqdm
import time
from scapy.utils import PcapWriter

def parse_arg() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='preProcess for flow file')

    parser.add_argument('--inputpath', type=str, default='', help='the inpath of the pcap file')
    parser.add_argument('--pre_type', type=str, default='1d', help='the type of process')
    parser.add_argument('--outputpath', type=str, default='', help='the outpath of the pcap file')
    parser.add_argument('--max_len', type=int, default=1600, help='the max length of one packet')
    parser.add_argument('--dataset_type', type=str, default='TOR', help='the type of the dataset([VPN,TOR,USTC])')
    parser.add_argument('--img_size', type=int, default=39, help='the size of img')
    args = parser.parse_args()


    return args


def transfer_to_1d(path:Path,output:Path,max_len:int,dataset_type:str):
    """
    
    Args:
        path:the parent path of the pcap file
        output:the path where the processed pcaps are put in
        max_len:the max length of the padded packet
        dataset_type:use the dataset_type to label
    """
    if os.path.exists(path) is False:
        raise ValueError("Error input path")
    
    path = path if isinstance(path,Path) else Path(path)
    output = output if isinstance(output,Path) else Path(output)

    if os.path.exists(output) is False:
        os.makedirs(output)

    file_list=path.glob('*')
    for filename in file_list:
        print(f"The {filename.name} size is {round(os.stat(filename).st_size/(1024*1024),2)}MB")
        print("when print sucess means one file has done.")

        if filename.suffix in (".pcap"):
            rows=[]
            step=0

            
            packets=read_pcap(filename)

            for i,one in enumerate(packets):
                if omit_packet(one) is False:
                    one=remove_ether(one)
                    one=anoymize_ip(one)
                    one=padding(one,max_len)
                    arr=packet_to_array(one)
                    
                    arr=normalize(arr)



                    if dataset_type in ["VPN","TOR","USTC"]:
                        prefix = filename.name.split('.')[0].lower()
                        h1_label=eval(f"MY_{dataset_type}_H1_LABEL").get(prefix)
                        traffic_label = eval(f"MY_{dataset_type}_TRAFFIC_TO_ID").get(prefix)

                        row = {
                            'h1_label':h1_label,
                            'traffic_label': traffic_label,
                            'packet': arr.tolist()
                        }
                        rows.append(row)

                    elif dataset_type == "DATACON":
                        prefix=filename.name.split(".pcap")[0]
                        h1_label=eval(f"MY_{dataset_type}_H1_LABEL").get(filename.parent.name)

                        row = {
                            'h1_label':h1_label,
                            'packet': arr.tolist()
                        }
                        rows.append(row)

                    else:
                        
                        h1_label=None
                        traffic_label=None
                        row = {
                            'h1_label':h1_label,
                            'traffic_label': traffic_label,
                            'packet': arr.tolist()
                        }
                        rows.append(row)
                    
                    
                    

            if rows and step==0:
                df = pd.DataFrame(rows)
                df.to_csv(output.joinpath(prefix+'.csv'))
            elif rows and step==1:
                df= pd.DataFrame(rows)
                df.to_csv(output.joinpath(prefix+'.csv'),mode='a',header=0)
            
        else:
            continue
        print("success")

def transfer_to_2d(path:Path,output:Path,max_len:int,img_size:int):
    """

    Args:
        path:the parent path of the pcap file
        output:the path where the processed pcaps are put in
        max_len:the max length of the padded packet
        img_size:the height width of the img
    """
    pass




if __name__ =="__main__":
    args = parse_arg()

    if args.pre_type=="1d":
        transfer_to_1d(args.inputpath,args.outputpath,args.max_len,args.dataset_type)
    elif args.pre_type=="2d":
        transfer_to_2d(args.inputpath,args.outputpath,args.max_len,args.img_size)
    else:
        raise ValueError("no this type")
