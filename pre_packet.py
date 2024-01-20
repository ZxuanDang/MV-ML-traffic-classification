import scapy
from scapy.all import *
from scapy.layers.inet import IP, TCP, UDP
from scapy.layers.dns import DNS
from scapy.layers.l2 import Ether
from scapy.layers.l2 import ARP
from scapy.utils import PcapReader
from scapy.packet import Padding
from scapy.compat import raw
from scapy.utils import rdpcap
from pathlib import Path
import numpy as np
import pandas as pd
from tqdm import tqdm
from typing import Optional,Union
import numpy as np


def remove_ether(packet):

    if Ether in packet:
        return packet[Ether].payload
    return packet

def read_pcap(path:Union[Path,str]):
    """

    Args:
        path: the path where the pcap is.
    
    Return:
        scapy.utils.PcapReader: 
            flow packet reader
    """
    path=path if isinstance(path,Path) else Path(path)
    packets=PcapReader(str(path))
    return packets

def omit_packet(packet:scapy.layers):
    """

    Args:
        packet: one packet 
    Return:
        bool:
            True means omit;False means not. 
    """
    if TCP in packet and (packet[TCP].flags & 0x17):
        layers=packet[TCP].payload.layers()
        if not layers or (Padding in layers and len(layers)==1):
            return True
    if UDP in packet:
        layers=packet[UDP].payload.layers()
        if not layers or (Padding in layers and len(layers)==1):
            return True        
    if DNS in packet:
        return True
    
    if ARP in packet:
        return True

    if not packet.haslayer(IP):
        return True
    
    return False

def anoymize_ip(packet:scapy.layers):
    """
    Args:
        packet: one packet
    Return:
        scapy.layer: packet without real ip
    """
    if IP in packet:
        packet[IP].src='0.0.0.0'
        packet[IP].dst='0.0.0.0'
        return packet
    else:
        raise ValueError("the packet without ip layer, this situation should not appear")  



def pad_udp(packet:scapy.layers):
    """
    Args:
        packet: one packet with udp layer
    Return:
        scapy.layer: packet with padded udp layer
    """
    if UDP in packet:
        packet_after=packet[UDP].payload.copy()
        packet_before=packet.copy()
        packet_before[UDP].remove_payload()
        packet=packet_before/raw(b'\x00'*(12+40))/packet_after
        return packet
    return packet   

def pad_options(packet:scapy.layers):
    """
    Args:
        packet: one packet
    Reture:
        scapy.layer: packet with full options in IP and TCP
    """ 
    if IP in packet:
        packet_after=packet[IP].payload.copy()
        packet_before=packet.copy()
        packet_before[IP].remove_payload()
        packet=packet_before/raw(b'\x00'*(40-len(packet[IP].options)))/packet_after
    if TCP in packet:
        packet_after=packet[TCP].payload.copy()
        packet_before=packet.copy()
        packet_before[TCP].remove_payload()
        packet=packet_before/raw(b'\x00'*(40-len(packet[TCP].options)))/packet_after
    return packet

def padding(packet:scapy.layers, max_len:int):
    """
    Args:
        packet: one packet ready for padding
        max_len: the max length of the padded packet

    Return:
        scapy.layers: the padded packet 
    """
    udp_packet=pad_udp(packet)
    options_packet=pad_options(udp_packet)
    packet_len=len(options_packet)
    if packet_len <= max_len:
        padded_packet=options_packet/raw(b"\x00"*(max_len-packet_len))
    else:
        padded_packet=raw(options_packet)[0:max_len]
    
    return padded_packet

def packet_to_array(packet:scapy.layers):
    """
    Args:
        packet: one packet 
    
    Returns:
        numpy.ndarray: the packet transferred uint8
    """
    arr=np.frombuffer(raw(packet),dtype=np.uint8)
    return arr

def normalize(arr:np.array):
    arr=arr/255
    return arr