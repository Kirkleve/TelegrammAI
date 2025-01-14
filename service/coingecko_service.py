from data_sources import make_request
from db_manager import insert_price_data
from logger import logger
from rate_limiter import can_run, set_delay

class CoinGeckoService:
    def __init__(self):
        self.service_key = "get_crypto_data_coingecko"
        self.url = 'https://api.coingecko.com/api/v3/coins/markets'
        self.params = {'vs_currency': 'usd', 'ids': 'bitcoin,ethereum'}

    def fetch_and_save_data(self):
        if not can_run(self.service_key):
            logger.warning("Пропуск запуска CoinGecko: ожидание окончания задержки.")
            return

        try:
            data = make_request(self.url, params=self.params)
            if data:
                for item in data:
                    insert_price_data("CoinGecko", item['id'], float(item['current_price']),
                                      float(item.get('high_24h', 0)),
                                      float(item.get('low_24h', 0)),
                                      0)  # CoinGecko не предоставляет open_price
                logger.info("Данные с CoinGecko успешно сохранены.")
                print("Данные CoinGecko сохранены")
        except Exception as e:
            logger.error(f"Ошибка при работе с CoinGecko: {e}")
            set_delay(self.service_key)
