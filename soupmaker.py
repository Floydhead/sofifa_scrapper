import time
import requests.models
from bs4 import BeautifulSoup as bs
import cloudscraper

def soup_maker(url: str):
    scraper = cloudscraper.create_scraper(browser={
        'browser': 'firefox',
        'platform': 'windows',
        'mobile': False
    })
    attempt, r = 0, requests.models.Response()

    while r.status_code != 200 and attempt < 10:
        time.sleep(0.35)
        if attempt > 0:
            #print('reattempting')
            pass
        attempt += 1
        r = scraper.get(url=url)
        #print(r.status_code)
    
    markup = r.content
    soup = bs(markup, 'lxml')
    return soup