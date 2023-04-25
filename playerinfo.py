import helpers as h
import re
import pandas as pd

def get_players_name_and_id(soup):
    table = soup.find('table', {'class': 'table table-hover persist-area'})
    tbody = table.find('tbody')
    player_items = [player.find('td', {'class': 'col-name'}).find('a')['href'] for player in tbody.contents]
    player_items = [(player.split('/')[2], player.split('/')[3]) for player in player_items]
    player_items = pd.DataFrame(player_items, columns=['player_id', 'player_name'])
    return player_items

def store_player_ids(players: pd.DataFrame, mode: str = 'db', header: bool=False) -> int:
    if mode not in ['db']:
        if header:
            pass
            #write_csv((('id'), ('name')))
        h.write_csv(players)
    else:
        if header:
            h.truncate_db('player_staging', 'playerids')
        h.write_db('player_staging', 'playerids', players)
    return 200

def read_player_ids(mode: str = 'db', filename: str = None) -> pd.DataFrame:
    playerids = pd.DataFrame()
    if mode not in ['db']:
        playerids = h.read_csv(filename=filename)
    else:
        playerids = h.read_db('player_staging', 'playerids')
    return playerids

def get_player_attributes(soup):
    divs = soup.find_all('div', {'class': 'center'})
    atts = divs[5].find_all('div', {'class': 'block-quarter'})

    attributes = {'Crossing': 0,'Finishing': 0,'Heading accuracy': 0,'Short passing': 0,'Volleys': 0
                  ,'Dribbling': 0,'Curve': 0,'FK Accuracy': 0,'Long passing': 0,'Ball control': 0
                  ,'Acceleration': 0,'Sprint speed': 0,'Agility': 0,'Reactions': 0,'Balance': 0
                  ,'Shot power': 0,'Jumping': 0,'Stamina': 0,'Strength': 0,'Long shots': 0
                  ,'Aggression': 0,'Interceptions': 0,'Positioning': 0,'Vision': 0,'Penalties': 0
                  ,'Composure': 0,'Defensive awareness': 0,'Standing tackle': 0,'Sliding tackle': 0
                  ,'GK Diving': 0,'GK Handling': 0,'GK Kicking': 0,'GK Positioning': 0,'GK Reflexes':0
                  }

    for att in atts:
        stats = att.find('ul', {'class': 'pl'}).text
        stats = stats.split('\n')
        for stat in stats:
            if stat == '':
                continue
            stat = stat.split(' ')
            rating, attribute = stat[0], ' '.join(stat[1:])
            if rating.isalpha():
                continue
            else:
                rating = h.evaluate_string(rating)
            attributes[attribute] = rating
    
    df = pd.DataFrame([attributes])
    print(df.head())

    info = divs[4].find('div', {'class': 'info'})
    positions = info.find('div', {'class': 'meta ellipsis'})
    positions = positions.find_all('span')
    for position in positions:
        print(position.text)
