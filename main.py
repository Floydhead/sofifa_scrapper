from tqdm import tqdm
import soupmaker as sm
import playerinfo as pi

if __name__ == '__main__':
    sofifa_url = 'http://sofifa.com/players?offset='

    for offset in tqdm(range(0, 120, 60)):
        soup = sm.soup_maker(url=sofifa_url+str(offset))
        players = pi.get_players_name_and_id(soup=soup)
        if offset == 0:
            pi.store_player_ids(players=players, mode='db')
        else:
            pi.store_player_ids(players=players, mode='db')

    print('players saved')

    playerids = pi.read_player_ids(mode='db')
    print(playerids.head())

    player_url = 'http://sofifa.com/player/'

    soup = sm.soup_maker(url=player_url+'206085')
    pi.get_player_attributes(soup=soup)
