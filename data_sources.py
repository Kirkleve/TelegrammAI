import requests
from pybit.unified_trading import HTTP
from logger import logger
from keys import api_key_bybit, api_secret_bybit

# Создание глобальной сессии Bybit
session = HTTP(api_key=api_key_bybit, api_secret=api_secret_bybit)

def make_request(url, headers=None, params=None):
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при выполнении запроса: {e}")
        return None
