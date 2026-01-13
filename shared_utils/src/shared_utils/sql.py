import pandas as pd
from sqlalchemy import create_engine

def get_engine(server: str, database: str) -> str:
    """Return a SQLAlchemy engine for a trusted SQL Server connection."""
    conn_str = (
        f'mssql+pyodbc://{server}/{database}?trusted_connection=yes&'
        f'driver=ODBC+Driver+17+for+SQL+Server'    
    )
    return create_engine(conn_str)

def read_table(engine, query: str) -> pd.DataFrame:
    """Read a SQL table or query into a DataFrame."""
    return pd.read_sql(query, engine)

def write_to_sql(df, table_name, engine_name):
    """Write a DataFrame to a SQL table with error handling."""
    try:
        df.to_sql(name=table_name, con=engine_name, if_exists='replace', index=False)
    except Exception as e:
        print(f'Error writing to database: {e}')