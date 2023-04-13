import requests.models
from bs4 import BeautifulSoup as bs
import cloudscraper
from tqdm import tqdm
import time
import csv

def soup_maker(url: str):
    scraper = cloudscraper.create_scraper(browser={
        'browser': 'firefox',
        'platform': 'windows',
        'mobile': False
    })
    attempt, r = 0, requests.models.Response()

    while r.status_code != 200 and attempt < 10:
        if attempt > 0:
            print('reattempting')
            time.sleep(5)
        attempt += 1
        r = scraper.get(url=url)
        print(r.status_code)
    
    markup = r.content
    soup = bs(markup, 'lxml')
    return soup

def get_players_name_and_id(soup):
    table = soup.find('table', {'class': 'table table-hover persist-area'})
    tbody = table.find('tbody')
    player_items = [player.find('td', {'class': 'col-name'}).find('a')['href'] for player in tbody.contents]
    player_items = [(player.split('/')[2], player.split('/')[3]) for player in player_items]

    return player_items

def write_csv(data):
    with open('playerid.csv', 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)


def store_player_ids(players, header: bool=False):
    if header:
        write_csv('id', 'name')
    write_csv(players)  


if __name__ == '__main__':
    url = 'http://sofifa.com/players?offset='

    for offset in tqdm(range(0, 25000, 60)):
        soup = soup_maker(url=url+str(offset))
        players = get_players_name_and_id(soup=soup)
        if offset == 0:
            store_player_ids(players=players, header=True)
        else:
            store_player_ids(players=players)