import sqlalchemy
from sqlalchemy import create_engine
import mysql.connector


def connect_db(type: str) -> sqlalchemy.Engine:
    cnxn_str = None
    cnxn = None
    if type.lower() in ['mssql', 'sql server', 'sqlserver']:
        '''
        cnxn_str = ("Driver={SQL Server};"
                "Server=ALIENWAREM15R1\SQLEXPRESS;"
                "Database=ocm;"
                "Trusted_Connection=yes;")
        '''
        cnxn_str = 'mssql+pyodbc://ALIENWAREM15R1\SQLEXPRESS/ocm?driver=SQL+Server+Native+Client+11.0'
        cnxn = create_engine(cnxn_str)
    elif type.lower() in ['tidb']:
        '''
        cnxn_str = {
            'host': 'gateway01.eu-central-1.prod.aws.tidbcloud.com',
            'port': 4000,
            'user': '3iXN8QmPjFL5RLQ.root',
            'password': 'IpV3U3PaSIUtmGQY',
            'database': 'ocm'
        }
        '''
        cnxn_str='mysql+mysqlconnector://3iXN8QmPjFL5RLQ.root:IpV3U3PaSIUtmGQY@gateway01.eu-central-1.prod.aws.tidbcloud.com:4000/ocm'
        cnxn = create_engine(cnxn_str)
    return cnxn