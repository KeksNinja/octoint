import requests
from octorest import OctoRest

from octoint.main_config import CONFIG
from octoint.main_utils import octoint_logger

rest_api_logger = octoint_logger(__name__)


def make_client():
    CONFIG.reload_config()
    api_key = CONFIG.api_key
    url = CONFIG.address

    try:
        client = OctoRest(url=url, apikey=api_key)
        return client
    except requests.exceptions.ConnectionError as e:
        rest_api_logger.error(f'could not connect\n{e}')
        exit()
