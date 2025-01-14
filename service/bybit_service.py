from data_sources import session
from db_manager import insert_price_data
from logger import logger
from rate_limiter import can_run, set_delay

class BybitService:
    def __init__(self):
        self.service_key = "get_crypto_data_bybit"

    def fetch_and_save_data(self):
        if not can_run(self.service_key):
            logger.warning("Пропуск запуска Bybit: ожидание окончания задержки.")
            return

        try:
            response = session.get_tickers(category="spot")
            data = response['result']['list']
            for item in data:
                insert_price_data("Bybit", item['symbol'], float(item['lastPrice']),
                                  float(item.get('highPrice', 0)),
                                  float(item.get('lowPrice', 0)),
                                  float(item.get('openPrice', 0)))
            logger.info("Данные с Bybit успешно сохранены.")
            print("Данные Bybit сохранены")
        except Exception as e:
            logger.error(f"Ошибка при работе с Bybit: {e}")
            set_delay(self.service_key)
