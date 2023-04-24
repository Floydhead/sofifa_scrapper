import pyodbc

def connect_db() -> pyodbc.Connection:
    cnxn_str = ("Driver={SQL Server Native Client 11.0};"
            "Server=ALIENWAREM15R1\SQLEXPRESS;"
            "Database=ocm;"
            "Trusted_Connection=yes;")
    cnxn = pyodbc.connect(cnxn_str)
    return cnxn