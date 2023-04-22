import helpers as h

def get_players_name_and_id(soup):
    table = soup.find('table', {'class': 'table table-hover persist-area'})
    tbody = table.find('tbody')
    player_items = [player.find('td', {'class': 'col-name'}).find('a')['href'] for player in tbody.contents]
    player_items = [(player.split('/')[2], player.split('/')[3]) for player in player_items]
    return player_items

def store_player_ids(players, header: bool=False):
    if header:
        pass
        #write_csv((('id'), ('name')))
    h.write_csv(players)  

def read_player_ids(filename: str):
    playerids = h.read_csv(filename=filename)
    return playerids

def get_player_attributes(soup):
    divs = soup.find_all('div', {'class': 'center'})
    atts = divs[5].find_all('div', {'class': 'block-quarter'})
    #cross = atts[0].find('ul', {'class': 'pl'})
    #print(cross.text)
    for att in atts:
        stats = att.find('ul', {'class': 'pl'}).text
        stats = stats.split('\n')
        for stat in stats:
            print(stat.split(' ').len())