from pathlib import Path
from scapy.layers.dns import DNS
from scapy.layers.inet import TCP
from scapy.packet import Padding
from scapy.utils import rdpcap

PREFIX_TO_APP_ID = {
    # AIM chat
    'aim_chat_3a': 0,
    'aim_chat_3b': 0,
    'aimchat1': 0,
    'aimchat2': 0,
    # Email
    'email1a': 1,
    'email1b': 1,
    'email2a': 1,
    'email2b': 1,
    # Facebook
    'facebook_audio1a': 2,
    'facebook_audio1b': 2,
    'facebook_audio2a': 2,
    'facebook_audio2b': 2,
    'facebook_audio3': 2,
    'facebook_audio4': 2,
    'facebook_chat_4a': 2,
    'facebook_chat_4b': 2,
    'facebook_video1a': 2,
    'facebook_video1b': 2,
    'facebook_video2a': 2,
    'facebook_video2b': 2,
    'facebookchat1': 2,
    'facebookchat2': 2,
    'facebookchat3': 2,
    # FTPS
    'ftps_down_1a': 3,
    'ftps_down_1b': 3,
    'ftps_up_2a': 3,
    'ftps_up_2b': 3,
    # Gmail
    'gmailchat1': 4,
    'gmailchat2': 4,
    'gmailchat3': 4,
    # Hangouts
    'hangout_chat_4b': 5,
    'hangouts_audio1a': 5,
    'hangouts_audio1b': 5,
    'hangouts_audio2a': 5,
    'hangouts_audio2b': 5,
    'hangouts_audio3': 5,
    'hangouts_audio4': 5,
    'hangouts_chat_4a': 5,
    'hangouts_video1b': 5,
    'hangouts_video2a': 5,
    'hangouts_video2b': 5,
    # ICQ
    'icq_chat_3a': 6,
    'icq_chat_3b': 6,
    'icqchat1': 6,
    'icqchat2': 6,
    # Netflix
    'netflix1': 7,
    'netflix2': 7,
    'netflix3': 7,
    'netflix4': 7,
    # SCP
    'scp1': 8,
    'scpdown1': 8,
    'scpdown2': 8,
    'scpdown3': 8,
    'scpdown4': 8,
    'scpdown5': 8,
    'scpdown6': 8,
    'scpup1': 8,
    'scpup2': 8,
    'scpup3': 8,
    'scpup5': 8,
    'scpup6': 8,
    # SFTP
    'sftp1': 9,
    'sftp_down_3a': 9,
    'sftp_down_3b': 9,
    'sftp_up_2a': 9,
    'sftp_up_2b': 9,
    'sftpdown1': 9,
    'sftpdown2': 9,
    'sftpup1': 9,
    # Skype
    'skype_audio1a': 10,
    'skype_audio1b': 10,
    'skype_audio2a': 10,
    'skype_audio2b': 10,
    'skype_audio3': 10,
    'skype_audio4': 10,
    'skype_chat1a': 10,
    'skype_chat1b': 10,
    'skype_file1': 10,
    'skype_file2': 10,
    'skype_file3': 10,
    'skype_file4': 10,
    'skype_file5': 10,
    'skype_file6': 10,
    'skype_file7': 10,
    'skype_file8': 10,
    'skype_video1a': 10,
    'skype_video1b': 10,
    'skype_video2a': 10,
    'skype_video2b': 10,
    # Spotify
    'spotify1': 11,
    'spotify2': 11,
    'spotify3': 11,
    'spotify4': 11,
    # Torrent
    'torrent01': 12,
    # Tor
    'torfacebook': 13,
    'torgoogle': 13,
    'tortwitter': 13,
    'torvimeo1': 13,
    'torvimeo2': 13,
    'torvimeo3': 13,
    'toryoutube1': 13,
    'toryoutube2': 13,
    'toryoutube3': 13,
    # Vimeo
    'vimeo1': 14,
    'vimeo2': 14,
    'vimeo3': 14,
    'vimeo4': 14,
    # Voipbuster
    'voipbuster1b': 15,
    'voipbuster2b': 15,
    'voipbuster3b': 15,
    'voipbuster_4a': 15,
    'voipbuster_4b': 15,
    # Youtube
    'youtube1': 16,
    'youtube2': 16,
    'youtube3': 16,
    'youtube4': 16,
    'youtube5': 16,
    'youtube6': 16,
    'youtubehtml5_1': 16,

}

ID_TO_TRAFFIC = {
    0: 'Chat',
    1: 'Email',
    2: 'File Transfer',
    3: 'Streaming',
    4: 'Torrent',
    5: 'Voip',
    6: 'VPN: Chat',
    7: 'VPN: File Transfer',
    8: 'VPN: Email',
    9: 'VPN: Streaming',
    10: 'VPN: Torrent',
    11: 'VPN: Voip',
}


ID_TO_APP = {
    0: 'AIM Chat',
    1: 'Email',
    2: 'Facebook',
    3: 'FTPS',
    4: 'Gmail',
    5: 'Hangouts',
    6: 'ICQ',
    7: 'Netflix',
    8: 'SCP',
    9: 'SFTP',
    10: 'Skype',
    11: 'Spotify',
    12: 'Torrent',
    13: 'Tor',
    14: 'Vimeo',
    15: 'Voipbuster',
    16: 'Youtube',
}

#############################VPN#####################
MY_VPN_H1_LABEL={

    ##non-VPN:
    
    # Chat
    'aim_chat_3a': 0,
    'aim_chat_3b': 0,
    'aimchat1': 0,
    'aimchat2': 0,
    'facebook_chat_4a': 0,
    'facebook_chat_4b': 0,
    'facebookchat1': 0,
    'facebookchat2': 0,
    'facebookchat3': 0,
    'hangout_chat_4b': 0,
    'hangouts_chat_4a': 0,
    'icq_chat_3a': 0,
    'icq_chat_3b': 0,
    'icqchat1': 0,
    'icqchat2': 0,
    'skype_chat1a': 0,
    'skype_chat1b': 0,

    # Email
    'email1a': 0,
    'email1b': 0,
    'email2a': 0,
    'email2b': 0,
    'gmailchat1':0,
    'gmailchat2':0,
    'gmailchat3':0,

    # File Transfer
    'ftps_down_1a': 0,
    'ftps_down_1b': 0,
    'ftps_up_2a': 0,
    'ftps_up_2b': 0,
    'sftp1': 0,
    'sftp_down_3a': 0,
    'sftp_down_3b': 0,
    'sftp_up_2a': 0,
    'sftp_up_2b': 0,
    'sftpdown1': 0,
    'sftpdown2': 0,
    'sftpup1': 0,
    'skype_file1': 0,
    'skype_file2': 0,
    'skype_file3': 0,
    'skype_file4': 0,
    'skype_file5': 0,
    'skype_file6': 0,
    'skype_file7': 0,
    'skype_file8': 0,

    # Streaming
    'vimeo1': 0,
    'vimeo2': 0,
    'vimeo3': 0,
    'vimeo4': 0,
    'youtube1': 0,
    'youtube2': 0,
    'youtube3': 0,
    'youtube4': 0,
    'youtube5': 0,
    'youtube6': 0,
    'youtubehtml5_1': 0,
    'facebook_video1a':0,
    'facebook_video1b':0,
    # Torrent
    'torrent01': 0,
    # VoIP
    'facebook_audio1a': 0,
    'facebook_audio1b': 0,
    'facebook_audio2a': 0,
    'facebook_audio2b': 0,
    'facebook_audio3': 0,
    'facebook_audio4': 0,
    'hangouts_audio1a': 0,
    'hangouts_audio1b': 0,
    'hangouts_audio2a': 0,
    'hangouts_audio2b': 0,
    'hangouts_audio3': 0,
    'hangouts_audio4': 0,
    'skype_audio1a': 0,
    'skype_audio1b': 0,
    'skype_audio2a': 0,
    'skype_audio2b': 0,
    'skype_audio3': 0,
    'skype_audio4': 0,



    ##VPN:

    # VPN: Chat
    'vpn_aim_chat1a': 1,
    'vpn_aim_chat1b': 1,
    'vpn_facebook_chat1a': 1,
    'vpn_facebook_chat1b': 1,
    'vpn_hangouts_chat1a': 1,
    'vpn_hangouts_chat1b': 1,
    'vpn_icq_chat1a': 1,
    'vpn_icq_chat1b': 1,
    'vpn_skype_chat1a': 1,
    'vpn_skype_chat1b': 1,
    # VPN: File Transfer
    'vpn_ftps_a': 1,
    'vpn_ftps_b': 1,
    'vpn_sftp_a': 1,
    'vpn_sftp_b': 1,
    'vpn_skype_files1a': 1,
    'vpn_skype_files1b': 1,
    # VPN: Email
    'vpn_email2a': 1,
    'vpn_email2b': 1,
    # VPN: Streaming
    'vpn_vimeo_a': 1,
    'vpn_vimeo_b': 1,
    'vpn_youtube_a': 1,
    'vpn_netflix_a':1,
    # VPN: Torrent
    'vpn_bittorrent': 1,
    # VPN VoIP
    'vpn_facebook_audio2': 1,
    'vpn_hangouts_audio1': 1,
    'vpn_hangouts_audio2': 1,
    'vpn_skype_audio1': 1,
    'vpn_skype_audio2': 1,



}

# for traffic identification
MY_VPN_TRAFFIC_TO_ID = {
    # Chat
    'aim_chat_3a': 0,
    'aim_chat_3b': 0,
    'aimchat1': 0,
    'aimchat2': 0,
    'facebook_chat_4a': 0,
    'facebook_chat_4b': 0,
    'facebookchat1': 0,
    'facebookchat2': 0,
    'facebookchat3': 0,
    'hangout_chat_4b': 0,
    'hangouts_chat_4a': 0,
    'icq_chat_3a': 0,
    'icq_chat_3b': 0,
    'icqchat1': 0,
    'icqchat2': 0,
    'skype_chat1a': 0,
    'skype_chat1b': 0,


    # Email
    'email1a': 1,
    'email1b': 1,
    'email2a': 1,
    'email2b': 1,
    'gmailchat1':1,
    'gmailchat2':1,
    'gmailchat3':1,

    # File Transfer
    'ftps_down_1a': 2,
    'ftps_down_1b': 2,
    'ftps_up_2a': 2,
    'ftps_up_2b': 2,
    'sftp1': 2,
    'sftp_down_3a': 2,
    'sftp_down_3b': 2,
    'sftp_up_2a': 2,
    'sftp_up_2b': 2,
    'sftpdown1': 2,
    'sftpdown2': 2,
    'sftpup1': 2,
    'skype_file1': 2,
    'skype_file2': 2,
    'skype_file3': 2,
    'skype_file4': 2,
    'skype_file5': 2,
    'skype_file6': 2,
    'skype_file7': 2,
    'skype_file8': 2,

    # Streaming
    'vimeo1': 3,
    'vimeo2': 3,
    'vimeo3': 3,
    'vimeo4': 3,
    'youtube1': 3,
    'youtube2': 3,
    'youtube3': 3,
    'youtube4': 3,
    'youtube5': 3,
    'youtube6': 3,
    'youtubehtml5_1': 3,
    'facebook_video1a':3,
    'facebook_video1b':3,

    # Torrent
    'torrent01': 4,
    
    # VoIP
    'facebook_audio1a': 5,
    'facebook_audio1b': 5,
    'facebook_audio2a': 5,
    'facebook_audio2b': 5,
    'facebook_audio3': 5,
    'facebook_audio4': 5,
    'hangouts_audio1a': 5,
    'hangouts_audio1b': 5,
    'hangouts_audio2a': 5,
    'hangouts_audio2b': 5,
    'hangouts_audio3': 5,
    'hangouts_audio4': 5,
    'skype_audio1a': 5,
    'skype_audio1b': 5,
    'skype_audio2a': 5,
    'skype_audio2b': 5,
    'skype_audio3': 5,
    'skype_audio4': 5,
    # VPN: Chat
    'vpn_aim_chat1a': 6,
    'vpn_aim_chat1b': 6,
    'vpn_facebook_chat1a': 6,
    'vpn_facebook_chat1b': 6,
    'vpn_hangouts_chat1a': 6,
    'vpn_hangouts_chat1b': 6,
    'vpn_icq_chat1a': 6,
    'vpn_icq_chat1b': 6,
    'vpn_skype_chat1a': 6,
    'vpn_skype_chat1b': 6,
    # VPN: File Transfer
    'vpn_ftps_a': 7,
    'vpn_ftps_b': 7,
    'vpn_sftp_a': 7,
    'vpn_sftp_b': 7,
    'vpn_skype_files1a': 7,
    'vpn_skype_files1b': 7,
    # VPN: Email
    'vpn_email2a': 8,
    'vpn_email2b': 8,
    # VPN: Streaming
    'vpn_vimeo_a': 9,
    'vpn_vimeo_b': 9,
    'vpn_youtube_a': 9,
    'vpn_netflix_a':9,
    # VPN: Torrent
    'vpn_bittorrent': 10,
    # VPN VoIP
    'vpn_facebook_audio2': 11,
    'vpn_hangouts_audio1': 11,
    'vpn_hangouts_audio2': 11,
    'vpn_skype_audio1': 11,
    'vpn_skype_audio2': 11,
    



}



#############################TOR#####################
MY_TOR_H1_LABEL={
    ############non-Tor######
    #Chat
    'aim_chat':0,  
    'icqchat':0,  
    'aimchat':0,
    'icq_chat':0,
    'skypechat':0,
    'skype_chat':0,
    'facebookchat':0,
    'hangout_chat':0,
    'hangoutschat':0,
    'facebook_chat':0,



    #Email
    'email_imap_filetransfer':0,



    #streaming
    'spotify':0,
    'spotify2':0,
    'spotify2-1':0,
    'spotify2-2':0,
    'spotifyandrew':0,
    'youtube_flash_workstation':0,
    'youtube_html5_workstation':0,
    'vimeo_workstation':0,


    #browing
    'browsing':0,
    'browsing2':0,
    'browsing2-1':0,
    'browsing2-2':0,
    'browsing_ara':0,
    'browsing_ara2':0,
    'browsing_ger':0,
    'ssl_browsing':0,

    #FTP
    'ftp_filetransfer':0,
    'sftp_filetransfer':0,




    #VoIP
    'hangout_audio':0,
    'facebook_audio':0,
    'facebook_voice_workstation':0,
    'hangouts_voice_workstation':0,
    'skype_audio':0,
    'skype_voice_workstation':0,



    #P2P
    'p2p_vuze':0,
    'p2p_vuze2-1':0,
    'p2p_multiplespeed':0,
    'p2p_multiplespeed2-1':0,


    ###########Tor##########
    #Tor:Chat
    'chat_gate_aim_chat':1,
    'chat_gate_icq_chat':1,
    'chat_aimchatgateway':1,
    'chat_icqchatgateway':1,
    'chat_gate_skype_chat':1,
    'chat_skypechatgateway':1,
    'chat_gate_hangout_chat':1,
    'chat_gate_facebook_chat':1,
    'chat_facebookchatgateway':1,
    'chat_hangoutschatgateway':1,

    #Tor:Email
    'mail_gate_email_imap_filetransfer':1,

    #Tor:streming
    'audio_spotifygateway':1,
    'video_youtube_flash_gateway':1,
    'video_youtube_html5_gateway':1,
    'tor_spotify2-1':1,
    'tor_spotify2-2':1,
    'audio_tor_spotify':1,
    'audio_tor_spotify2':1,
    'video_vimeo_gateway':1,

    #Tor:browing
    "browsing_gate_ssl_browsing":1,
    'browsing_tor_browsing_mam2':1,
    'browsing_ssl_browsing_gateway':1,
    'browsing_tor_browsing_mam':1,
    'browsing_tor_browsing_ger':1,
    'browsing_tor_browsing_ara':1,

    #Tor:FTP
    'file-transfer_gate_sftp_filetransfer':1,
    'file-transfer_gate_ftp_transfer':1,

    #Tor:VoIP
    'voip_gate_hangout_audio':1,
    'voip_hangouts_voice_gateway':1,
    'voip_gate_skype_audio':1,
    'voip_gate_facebook_audio':1,
    'voip_skype_voice_gateway':1,
    'voip_facebook_voice_gateway':1,

    #Tor:P2P
    'p2p_tor_p2p_vuze':1,
    'p2p_tor_p2p_multiplespeed':1,
    'tor_p2p_vuze-2-1':1,
    'tor_p2p_multiplespeed2-1':1,

}

MY_TOR_TRAFFIC_TO_ID={

    #Chat
    'aim_chat':0,  
    'icqchat':0,  
    'aimchat':0,
    'icq_chat':0,
    'skypechat':0,
    'skype_chat':0,
    'facebookchat':0,
    'hangout_chat':0,
    'hangoutschat':0,
    'facebook_chat':0,

    #Tor:Chat
    'chat_gate_aim_chat':1,
    'chat_gate_icq_chat':1,
    'chat_aimchatgateway':1,
    'chat_icqchatgateway':1,
    'chat_gate_skype_chat':1,
    'chat_skypechatgateway':1,
    'chat_gate_hangout_chat':1,
    'chat_gate_facebook_chat':1,
    'chat_facebookchatgateway':1,
    'chat_hangoutschatgateway':1,

    #Email
    'email_imap_filetransfer':2,
    #Tor:Email
    'mail_gate_email_imap_filetransfer':3,


    #streaming
    'spotify':4,
    'spotify2':4,
    'spotify2-1':4,
    'spotify2-2':4,
    'spotifyandrew':4,
    'youtube_flash_workstation':4,
    'youtube_html5_workstation':4,
    'vimeo_workstation':4,
    #Tor:streming
    'audio_spotifygateway':5,
    'video_youtube_flash_gateway':5,
    'video_youtube_html5_gateway':5,
    'tor_spotify2-1':5,
    'tor_spotify2-2':5,
    'audio_tor_spotify':5,
    'audio_tor_spotify2':5,
    'video_vimeo_gateway':5,

    #browing
    'browsing':6,
    'browsing2':6,
    'browsing2-1':6,
    'browsing2-2':6,
    'browsing_ara':6,
    'browsing_ara2':6,
    'browsing_ger':6,
    'ssl_browsing':6,
    #Tor:browing
    "browsing_gate_ssl_browsing":7,
    'browsing_tor_browsing_mam2':7,
    'browsing_ssl_browsing_gateway':7,
    'browsing_tor_browsing_mam':7,
    'browsing_tor_browsing_ger':7,
    'browsing_tor_browsing_ara':7,

    #FTP
    'ftp_filetransfer':8,
    'sftp_filetransfer':8,

    #Tor:FTP
    'file-transfer_gate_sftp_filetransfer':9,
    'file-transfer_gate_ftp_transfer':9,


    #VoIP
    'hangout_audio':10,
    'facebook_audio':10,
    'facebook_voice_workstation':10,
    'hangouts_voice_workstation':10,
    'skype_audio':10,
    'skype_voice_workstation':10,

    #Tor:VoIP
    'voip_gate_hangout_audio':11,
    'voip_hangouts_voice_gateway':11,
    'voip_gate_skype_audio':11,
    'voip_gate_facebook_audio':11,
    'voip_skype_voice_gateway':11,
    'voip_facebook_voice_gateway':11,

    #P2P
    'p2p_vuze':12,
    'p2p_vuze2-1':12,
    'p2p_multiplespeed':12,
    'p2p_multiplespeed2-1':12,
    #Tor:P2P
    'p2p_tor_p2p_vuze':13,
    'p2p_tor_p2p_multiplespeed':13,
    'tor_p2p_vuze-2-1':13,
    'tor_p2p_multiplespeed2-1':13,
}

#############################USTC###################
MY_USTC_H1_LABEL={
##################benign########################
    #Chat
    "skype":0,
    #Database
    'mysql':0,
    #Email
    'gmail':0,
    'outlook':0,

    #FTP
    'ftp':0,
    'smb-1':0,
    'smb-2':0,

    #Game
    'worldofwarcraft':0,
    #P2P
    'bittorrent':0,

    #Social_Network
    'weibo-1':0,
    'weibo-2':0,
    'weibo-3':0,
    'weibo-4':0,

    #Streaming
    'facetime':0,

 
##################malware#######################
   #Cridex
    'cridex':1,

    #Geodo
    'geodo':1,

    #Htbot
    'htbot':1,

    #Miuef
    'miuref':1,

    #Neris
    'neris':1,

    #Nsis-ay
    'nsis-ay':1,
    #Shifu
    'shifu':1,
    #Tinba
    'tinba':1,
    #Virut
    'virut':1,
    #Zeus
    'zeus':1,
}
MY_USTC_TRAFFIC_TO_ID={
    #Chat
    "skype":0,
    #Database
    'mysql':1,
    #Email
    'gmail':2,
    'outlook':2,

    #FTP
    'ftp':3,
    'smb-1':3,
    'smb-2':3,

    #Game
    'worldofwarcraft':4,
    #P2P
    'bittorrent':5,

    #Social_Network
    'weibo-1':6,
    'weibo-2':6,
    'weibo-3':6,
    'weibo-4':6,

    #Streaming
    'facetime':7,

    #Cridex
    'cridex':8,

    #Geodo
    'geodo':9,

    #Htbot
    'htbot':10,

    #Miuref
    'miuref':11,

    #Neris
    'neris':12,

    #Nsis-ay
    'nsis-ay':13,
    #Shifu
    'shifu':14,
    #Tinba
    'tinba':15,
    #Virut
    'virut':16,
    #Zeus
    'zeus':17,

}

#############################DataCon###################
MY_DATACON_H1_LABEL={
    "white":0,

    "black":1,
}