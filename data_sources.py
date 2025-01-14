import requests
import logging
import time
from pybit.unified_trading import HTTP
from keys import api_key_bybit, api_secret_bybit, cmc_api_key, twitter_bearer_token, api_key_news
from logger import logger

session = HTTP(api_key=api_key_bybit, api_secret=api_secret_bybit)


# Bybit API
def get_crypto_data_bybit():
    session = HTTP(api_key=api_key_bybit, api_secret=api_secret_bybit)
    try:
        response = session.get_tickers(category="spot")
        return response['result']['list']
    except Exception as e:
        logging.error(f"Error getting data from Bybit: {e}")
        return []


# CoinGecko API
def get_crypto_data_coingecko():
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    params = {'vs_currency': 'usd', 'ids': 'bitcoin,ethereum'}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"Error getting data from CoinGecko: {e}")
        return []


# Twitter API
def get_twitter_data():
    """
    Получает данные с Twitter API и возвращает список твитов.
    """
    global response
    url = 'https://api.twitter.com/2/tweets/search/recent'
    headers = {
        'Authorization': f'Bearer {twitter_bearer_token}'
    }
    params = {
        'query': '#cryptocurrency',  # Хештег или ключевое слово
        'tweet.fields': 'created_at,text',  # Поля твита
        'max_results': 10  # Количество результатов (максимум 100)
    }

    while True:
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()

            # Обработка успешного ответа
            tweets = response.json().get('data', [])
            print(f"Получено {len(tweets)} твитов.")
            logger.info(f"Получено {len(tweets)} твитов.")
            return tweets

        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:  # Лимит запросов
                reset_time = int(response.headers.get('x-rate-limit-reset', time.time() + 86400))
                wait_time = reset_time - int(time.time())
                print(f"Превышен лимит запросов. Ожидание {wait_time} секунд...")
                logger.warning(f"Превышен лимит запросов. Ожидание {wait_time} секунд...")
                time.sleep(max(wait_time, 0))  # Задержка до сброса лимита
            else:
                logger.error(f"HTTP Error: {e}")
                print(f"HTTP Error: {e}")
                break
        except Exception as e:
            logger.error(f"Ошибка: {e}")
            print(f"Ошибка: {e}")
            break


# coinmarketcap API
def get_crypto_data_coinmarketcap():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': cmc_api_key}
    params = {'start': '1', 'limit': '10', 'convert': 'USD'}
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json().get('data', [])
    except Exception as e:
        logger.error(f"Error getting data from CoinMarketCap: {e}")
        return []


# News API
def get_crypto_news():
    url = 'https://newsapi.org/v2/everything'
    params = {'q': 'cryptocurrency', 'apiKey': api_key_news, 'language': 'en', 'sortBy': 'publishedAt'}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get('articles', [])
    except Exception as e:
        logger.error(f"Error getting news: {e}")
        return []
