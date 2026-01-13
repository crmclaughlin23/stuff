# Project-specific utilities to look up which version of CPCClient.exe is installed on the PC

from datetime import datetime
import os

def get_cpc(ip: str, pcid: str, source: str, client: str) -> str | None:
    try:
        client_cpc = os.path.join('\\' + '\\' + str(ip), source, client)

        if not os.path.exists(client_cpc):
            client_cpc = os.path.join('\\' + '\\' + str(pcid), source, client)
             
        if os.path.exists(client_cpc):
            client_date = datetime.fromtimestamp(os.path.getmtime(client_cpc)).strftime('%Y-%m-%d')
            return str(client_date)
    except Exception:
        return None