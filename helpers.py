import csv
import pandas as pd

def write_csv(data):
    with open('playerid.csv', 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)

def read_csv(filename: str):
    if not filename:
        raise ValueError('no file given')
    playerids = pd.read_csv(filepath_or_buffer=filename, names=['id', 'name'])
    return playerids
    