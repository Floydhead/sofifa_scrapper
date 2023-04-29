import helpers as h
import re
import pandas as pd
import regex as re

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

def get_player_attributes(soup, id: int):
    divs = soup.find_all('div', {'class': 'center'})
    atts = divs[5].find_all('div', {'class': 'block-quarter'})

    attributes = {'player_id': id, 'Crossing': 0,'Finishing': 0,'Heading_accuracy': 0,'Short_passing': 0,'Volleys': 0
                  ,'Dribbling': 0,'Curve': 0,'FK_Accuracy': 0,'Long_passing': 0,'Ball_control': 0
                  ,'Acceleration': 0,'Sprint_speed': 0,'Agility': 0,'Reactions': 0,'Balance': 0
                  ,'Shot_power': 0,'Jumping': 0,'Stamina': 0,'Strength': 0,'Long_shots': 0
                  ,'Aggression': 0,'Interceptions': 0,'Positioning': 0,'Vision': 0,'Penalties': 0
                  ,'Composure': 0,'Defensive_awareness': 0,'Standing_tackle': 0,'Sliding_tackle': 0
                  ,'GK_Diving': 0,'GK_Handling': 0,'GK_Kicking': 0,'GK_Positioning': 0,'GK_Reflexes':0
                  }

    for att in atts:
        if not att or att.text in ['', '\n']:
            continue
        stats = att.find('ul', {'class': 'pl'}).text
        stats = stats.split('\n')
        for stat in stats:
            if stat == '':
                continue
            stat = stat.split(' ')
            rating, attribute = stat[0], '_'.join(stat[1:])
            pattern = r'^[+-]?\d+([+-]\d+)?$'
            if re.match(pattern, rating):
                rating = h.evaluate_string(rating)
            else:
                continue
            if attribute in ['Marking']:
                attribute = 'Defensive_awareness'
            attributes[attribute] = rating
    
    attributes = pd.DataFrame([attributes])
    #print(attributes.head(), "/n", attributes.columns)
    store_player_attributes(attributes=attributes, id=id)
    get_player_positions(soup=soup, id=id)

def get_player_positions(soup, id: int):
    divs = soup.find_all('div', {'class': 'center'})
    info = divs[4].find('div', {'class': 'info'})
    positions = info.find('div', {'class': 'meta ellipsis'})
    positions = positions.find_all('span')
    #for position in positions:
    #    print(position.text)

def store_player_attributes(attributes: pd.DataFrame, id: int):
    delete = h.delete_row_in_db('player_staging', 'player_stats', 'player_id', id)
    if delete == 200:
        h.write_db('player_staging', 'player_stats', attributes)

def is_player_attributed_stored(player_id: int) -> bool:
    player_id_db = max_player_attribute_id_stored()
    if player_id <= player_id_db:
        return True
    else:
        return False

def max_player_attribute_id_stored() -> int:
    player_id_db = h.read_db('player_staging', 'player_stats')['player_id'].to_list()
    player_id_db = max(player_id_db) if len(player_id_db) > 0 else 0
    return player_id_db