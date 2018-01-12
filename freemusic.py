import xbmc
import json
import re
import urllib
import urlparse

import requests
from BeautifulSoup import BeautifulSoup as BS
from nanscrapers.common import clean_title, random_agent, replaceHTMLCodes
from ..scraper import Scraper

session = requests.Session()
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36"}

class freemusic(Scraper):
    domains = ['freemusicdownloads']
    name = "Freemusic"
    sources = []

    def __init__(self):
        self.base_link = 'http://down.freemusicdownloads.world/'
        #self.search_link = 'results?search='
        self.sources = []
    
    def scrape_music(self, title, artist, debrid=False):
        try:
            song_search = clean_title(title.lower()).replace(' ','+')
            artist_search = clean_title(artist.lower()).replace(' ','+')
            song_comp = clean_title(title.lower())
            artist_comp = clean_title(artist.lower())
            total = artist_comp +'-'+ song_comp
            start_url = '%sresults?search=%s+%s'    %(self.base_link,artist_search,song_search)
            html = requests.get(start_url, headers=headers, timeout=20).content
            match = re.compile('<h4 class="card-title">(.+?)</h4>.+?href="(.+?)"',re.DOTALL).findall(html)
            for m, link in match:
                match2 = m.replace('\n','').replace('\t','').replace(' ','')
                match3 = match2.lower()
                quals = re.compile(str(total)+'(.+?)>').findall(str(match3)+'>')
                qual1 = str(quals)
                qual = qual1.replace("[", "").replace("]", "")
                if clean_title(title).lower() in clean_title(match2).lower():
                    if clean_title(artist).lower() in clean_title(match2).lower():
                        self.sources.append({'source': 'Youtube', 'quality': qual, 'scraper': self.name, 'url': link, 'direct': True}) 

            return self.sources    
        except Exception, argument:
            return self.sources
            
                    



        