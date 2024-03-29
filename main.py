from tqdm import tqdm
import soupmaker as sm
import playerinfo as pi

sofifa_url = 'http://sofifa.com/players?offset='
player_url = 'http://sofifa.com/player/'

def get_player_ids(total: int = 20120):
    for offset in tqdm(range(0, total, 60)):
        soup = sm.soup_maker(url=sofifa_url+str(offset))
        players = pi.get_players_name_and_id(soup=soup)
        if offset == 0:
            pi.store_player_ids(players=players, mode='db', header=True)
        else:
            pi.store_player_ids(players=players, mode='db')

def read_player_ids(mode: str = 'db'):
    return pi.read_player_ids(mode=mode)

def get_player_details(id: int):
    url = player_url+str(id)
    soup = sm.soup_maker(url=url)
    player_attributes = pi.get_player_attributes(soup=soup, id = id)
    return player_attributes

def is_player_attribute_stored(player_id: int) -> bool:
    return pi.is_player_attributed_stored(player_id=player_id)


if _name_ == '__main__':
    get_player_ids()

    
    #player_ids = read_player_ids(mode='db')
    #print(player_ids)
    '''
    player_ids = player_ids['player_id'].tolist()
    player_ids = sorted(player_ids)
    pbar = tqdm(player_ids)
    max_player_id = pi.max_player_attribute_id_stored()
    for player_id in pbar:
        pbar.set_description(f'Processing - {player_id}')
        if player_id > max_player_id:
            get_player_details(player_id)
    #get_player_details(231900)
    '''