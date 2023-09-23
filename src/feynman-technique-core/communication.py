import configparser
import asyncio
from aiohttp import ClientSession
from api import BackendRestApi

config = configparser.ConfigParser()
config.read('./config/config.ini')

FEYNMAN_TECHNIQUE_BACKEND_REST_API_BASE_URL = config['restapi']['feynman-technique-backend']
FEYNMAN_TECHNIQUE_SCRAPER_REST_API_BASE_URL = config['restapi']['feynman-technique-scraper']

async def get_words_async() -> list[str]:
    url = f'{FEYNMAN_TECHNIQUE_BACKEND_REST_API_BASE_URL}/{BackendRestApi.GetWordsOnly}'
    async with ClientSession(trust_env=True) as session:
        async with session.get(url) as response:
            response = await response.read()
            print(response)
    return response
