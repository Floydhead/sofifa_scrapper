import csv
import pandas as pd
import db
from sqlalchemy import text

def write_csv(data):
    with open('playerid.csv', 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)

def read_csv(filename: str):
    if not filename:
        raise ValueError('no file given')
    playerids = pd.read_csv(filepath_or_buffer=filename, names=['id', 'name'])
    return playerids
    
def evaluate_string(string):
    return eval(string)

def read_db(schema: str, table: str) -> pd.DataFrame:
    engine = db.connect_db()
    cursor = engine.connect()
    df = pd.read_sql_table(table_name=table, schema=schema, con=cursor)
    cursor.close()
    return df 

def write_db(schema: str, table: str, df: pd.DataFrame, truncate: bool = True) -> int:
    if truncate:
        truncate_db(schema=schema, table=table)
    engine = db.connect_db()
    cursor = engine.connect()
    df.to_sql(name=table, schema=schema, con=engine, if_exists='append', index=False)
    cursor.close()
    return 200

def truncate_db(schema: str, table: str) -> int:
    engine = db.connect_db()
    cursor = engine.connect()
    sql = text(f'TRUNCATE TABLE {schema}.{table}')
    cursor.execute(sql)
    cursor.close()
    return 200

def delete_row_in_db(schema: str, table: str, column_name: str, column_value: str) -> int:
    engine = db.connect_db()
    cursor = engine.connect()
    sql = text(f'DELETE FROM {schema}.{table} WHERE {column_name} = {column_value}')
    #print(sql)
    cursor.execute(sql)
    cursor.commit()
    cursor.close()
    return 200