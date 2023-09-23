import configparser
from aiohttp import ClientSession, TCPConnector
from api import BackendRestApi

config = configparser.ConfigParser()
config.read('./config/config.ini')

FEYNMAN_TECHNIQUE_BACKEND_REST_API_BASE_URL = config['restapi']['feynman-technique-backend']
FEYNMAN_TECHNIQUE_SCRAPER_REST_API_BASE_URL = config['restapi']['feynman-technique-scraper']

async def get_words_async() -> list[str]:
    url = f'{FEYNMAN_TECHNIQUE_BACKEND_REST_API_BASE_URL}{BackendRestApi.GetWordsOnly}'
    #TODO: enable SSL verification
    # ssl_context = ssl.create_default_context(cafile=certifi.where())
    async with ClientSession(connector=TCPConnector(ssl=False)) as session:
        async with session.get(url, allow_redirects=True) as response:
            response = await response.read()
            print(response)
    return response
