import csv
import pandas as pd
import db

def write_csv(data):
    with open('playerid.csv', 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)

def read_csv(filename: str):
    if not filename:
        raise ValueError('no file given')
    playerids = pd.read_csv(filepath_or_buffer=filename, names=['id', 'name'])
    return playerids
    
def add_digits_in_string(string):
    """
    Add the digits in a string.
    """
    digits = [int(digit) for digit in string.split('+')]
    return sum(digits)

def read_db(schema: str, table: str) -> pd.DataFrame:
    conn = db.connect_db()
    df = pd.read_sql_table(table_name=table, schema=schema, con=conn)
    conn.close()
    return df 

def write_db(schema: str, table: str, df: pd.DataFrame) -> int:
    conn = db.connect_db()
    df.to_sql(name=table, schema=schema, con=conn, if_exists='append')
    conn.close()
    return 200