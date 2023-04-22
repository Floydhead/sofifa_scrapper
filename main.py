from tqdm import tqdm
import soupmaker as sm
import playerinfo as pi

if __name__ == '__main__':
    sofifa_url = 'http://sofifa.com/players?offset='

    for offset in tqdm(range(0, 0, 60)):
        soup = sm.soup_maker(url=sofifa_url+str(offset))
        players = pi.get_players_name_and_id(soup=soup)
        if offset == 0:
            pi.store_player_ids(players=players, header=True)
        else:
            pi.store_player_ids(players=players)

    print('players saved')

    playerids = pi.read_player_ids(filename='playerid.csv')
    print(playerids.head())

    player_url = 'http://sofifa.com/player/'

    soup = sm.soup_maker(url=player_url+'243580')
    pi.get_player_attributes(soup=soup)
