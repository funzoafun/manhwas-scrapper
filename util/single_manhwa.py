import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests

load_dotenv()


class Manhwa:
    manhwaUrl: str

    def __init__(self, manhwaurl):
        self.manhwaUrl = manhwaurl

    @property
    def getManhwaSoup(self):
        SCRAPER_URL = 'http://api.webscrapingapi.com/v1'
        manhwa_params = {
            'api_key': os.environ['API_KEy'],
            'url': self.manhwaUrl,
            'render_js': 1
        }
        manhwa_response = requests.get(SCRAPER_URL, params=manhwa_params)
        manhwa_content = manhwa_response.text
        return BeautifulSoup(manhwa_content, 'html.parser')
