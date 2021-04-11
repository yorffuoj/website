import logging
import requests
import json

BASE_URL = "https://api.jcdecaux.com/vls/v1/stations/"
CONTRACT = "toulouse"
API_KEY = "54b6f2be9a8f6d369691075425d0e11b4611a9d5"

logger = logging.getLogger(__name__)


def get_all_stations(url=BASE_URL, contract=CONTRACT, api_key=API_KEY):
    logger.info(f"Request all stations from {contract} to JCDecaux API")
    url = url if url.endswith("/") else url + "/"
    stations_url = f"{url}?contract={contract}&apiKey={api_key}"
    req = requests.get(stations_url)
    return json.loads(req.text)


def get_station(number, url=BASE_URL, contract=CONTRACT, api_key=API_KEY):
    logger.info(f"Request station number {number} from {contract} to JCDecaux API")
    url = url if url.endswith("/") else url + "/"
    stations_url = f"{url}{number}?contract={contract}&apiKey={api_key}"
    req = requests.get(stations_url)
    return json.loads(req.text)
