# Project-specific utilities to look up network pc pcid and ip address

import socket

def get_ip(pcid: str) -> str:
    # print(f'  Getting IP address for {pcid}...')
    try:
        return socket.gethostbyname(pcid)
    except Exception:
        return None
    
def get_pcid(ip_address: str) -> str:
    # print(f'  Getting PCID for {ip_address}...')
    try:
        hostname = socket.gethostbyaddr(ip_address)[0]
        return hostname.split('.')[0].upper()
    except Exception:
        return None