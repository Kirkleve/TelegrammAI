from data_sources import make_request
from db_manager import insert_price_data
from logger import logger
from rate_limiter import can_run, set_delay
from keys import cmc_api_key


class CoinMarketCapService:
    def __init__(self):
        self.service_key = "get_crypto_data_coinmarketcap"
        self.url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        self.headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': cmc_api_key}
        self.params = {'start': '1', 'limit': '10', 'convert': 'USD'}

    def fetch_and_save_data(self):
        if not can_run(self.service_key):
            logger.warning("Пропуск запуска CoinMarketCap: ожидание окончания задержки.")
            return

        try:
            # Выполняем запрос
            data = make_request(self.url, headers=self.headers, params=self.params)

            # Проверяем, что данные корректны
            if isinstance(data, dict) and 'data' in data:
                for item in data['data']:
                    # Проверяем структуру данных для каждой записи
                    symbol = item.get('symbol', 'N/A')
                    price_info = item.get('quote', {}).get('USD', {})
                    price = float(price_info.get('price', 0))
                    high_24h = float(price_info.get('high_24h', 0))
                    low_24h = float(price_info.get('low_24h', 0))

                    insert_price_data("CoinMarketCap", symbol, price, high_24h, low_24h, 0)
                logger.info("Данные с CoinMarketCap успешно сохранены.")
                print("Данные CoinMarketCap сохранены")
            else:
                logger.warning("Некорректная структура ответа от CoinMarketCap.")
        except Exception as e:
            logger.error(f"Ошибка при работе с CoinMarketCap: {e}")
            set_delay(self.service_key)
