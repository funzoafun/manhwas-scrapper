import os
import requests
import bs4
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()


class AllManhwas:
    SCRAPER_URL = 'http://api.webscrapingapi.com/v1'
    providerUrl: str
    apiKey = os.environ['API_KEY']

    def __init__(self, providerUrl):
        self.providerUrl = providerUrl

    @property
    def getManhwaContent(self):
        params = {
            'api_key': self.apiKey,
            'url': self.providerUrl,
            'render_js': 1
        }
        manhwa_response = requests.get(self.SCRAPER_URL, params=params)
        return manhwa_response.text

    @property
    def getManhwaSoup(self):
        content = self.getManhwaContent
        return BeautifulSoup(content, 'html.parser')

    @property
    def getAllManhwasList(self):
        soup = self.getManhwaSoup
        all_link_tags = soup.findAll('a', {'class': 'series'})
        allLinks = []
        for link in all_link_tags:
            allLinks.append(link.get('href'))

        return allLinks
