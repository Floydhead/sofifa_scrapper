import sqlalchemy
from sqlalchemy import create_engine

def connect_db() -> sqlalchemy.Engine:
    '''
    cnxn_str = ("Driver={SQL Server};"
            "Server=ALIENWAREM15R1\SQLEXPRESS;"
            "Database=ocm;"
            "Trusted_Connection=yes;")
    '''
    cnxn_str = 'mssql+pyodbc://ALIENWAREM15R1\SQLEXPRESS/ocm?driver=SQL+Server+Native+Client+11.0'
    cnxn = create_engine(cnxn_str)
    return cnxn