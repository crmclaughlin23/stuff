# --- Third Party Packages --- #
import pandas as pd
from natsort import order_by_index, index_natsorted

# --- Shared Packages --- #
from shared_utils.sql import get_engine, read_table, write_to_sql
from shared_config.sql import PROD_SERVER, PYRO_DATABASE

# --- Project Packages --- #
from automation_audit_cure_pcs.config import SOURCE_PATH as source, CLIENT_NAME as client
from automation_audit_cure_pcs.utils.network import get_ip, get_pcid
from automation_audit_cure_pcs.utils.cpc import get_cpc

def run_pipeline() -> None:
    """Run the control-pc-inventory pipeline."""
    print("Running control-pc-inventory pipeline")
    
    # --- Database Connection ---#
    engine = get_engine(PROD_SERVER, PYRO_DATABASE)
    print(f'  Connecting to the {PYRO_DATABASE} database on the {PROD_SERVER} server...')
    
    equip_pcs = read_table(engine, 'SELECT * FROM [Equipment PCs]')
    
    # --- Data Processing ---#
    # Get ip address
    print('  Getting IP Addresses...')
    equip_pcs['New_IP_Address'] = equip_pcs['PCID'].apply(lambda pcid: get_ip(pcid))
    equip_pcs['IP_Address'] = equip_pcs.apply(lambda row: row['New_IP_Address'] if row['New_IP_Address'] is not None else row['IP_Address'], axis=1) # If New IP Address is None, previous IP Address is used

    # Get pcid
    print('  Getting PCIDs...')
    equip_pcs['New_PCID'] = equip_pcs['IP_Address'].apply(lambda ip: get_pcid(ip))
    equip_pcs['PCID'] = equip_pcs.apply(lambda row: row['New_PCID'] if row['New_PCID'] is not None else row['PCID'], axis=1) # If New PCID is None, previous PCID is used

    # Get CPC software version
    print('  Getting CPC Versions...')
    equip_pcs['New_CPC_Version'] = equip_pcs.apply(lambda row: get_cpc(row['IP_Address'], row['PCID'], source, client), axis=1)
    equip_pcs['CPC_Version'] = equip_pcs.apply(lambda row: row['New_CPC_Version'] if row['New_CPC_Version'] is not None else row['CPC_Version'], axis=1) # If New CPC Version is None, previous CPC Version is used

    equip_pcs = equip_pcs.drop(columns=['New_IP_Address', 'New_PCID', 'New_CPC_Version'])

    equip_pcs['Database_Name'] = equip_pcs['Alt_Name'].apply(lambda alt_name: f"CPC_{alt_name.replace(' ', '')}")

    #--- Sorting Table ---#
    print('  Sorting Table...')
    indexer = index_natsorted(equip_pcs['PC'])
    equip_pcs = equip_pcs.reindex(order_by_index(equip_pcs.index, indexer))
    equip_pcs = equip_pcs.reset_index(drop=True)
    
    print(equip_pcs)
    
     #--- Writing DataFrame to Equipment PCs table ---#
    print('  Writing DataFrame to Equipment PCs table...')
    write_to_sql(equip_pcs, 'Equipment PCs', engine)