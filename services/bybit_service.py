from services.base_service import BaseService
from db_manager import insert_price_data
from logger import logger
from pybit.unified_trading import HTTP
from keys import api_key_bybit, api_secret_bybit

class BybitService(BaseService):
    def __init__(self):
        super().__init__("get_crypto_data_bybit")
        self.session = HTTP(api_key=api_key_bybit, api_secret=api_secret_bybit)
        self.success_count = 0
        self.error_count = 0

    def fetch_and_save_data(self):
        if not self._can_run():
            return

        try:
            response = self.session.get_tickers(category="spot")
            if response and 'result' in response and 'list' in response['result']:
                self._process_data(response['result']['list'])
            else:
                self._log_error("Некорректная структура ответа от Bybit.")
        except Exception as e:
            self._log_error(f"Ошибка при работе с Bybit: {e}")

        self._finalize()

    def _process_data(self, data):
        for item in data:
            symbol = item.get('symbol', 'N/A')
            last_price = float(item.get('lastPrice', 0))
            high_price = float(item.get('highPrice', 0))
            low_price = float(item.get('lowPrice', 0))
            open_price = float(item.get('openPrice', 0))

            try:
                insert_price_data("Bybit", symbol, last_price, high_price, low_price, open_price)
                self.success_count += 1
            except Exception as e:
                logger.error(f"{self.service_key}: Ошибка при сохранении данных {symbol}: {e}")
                self.error_count += 1

    def _log_error(self, message):
        logger.error(f"{self.service_key}: {message}")
        self.error_count += 1

    def _can_run(self):
        return True  # Здесь можно добавить проверку ограничений времени.

    def _finalize(self):
        if self.error_count == 0:
            logger.info(f"Все данные с Bybit успешно собраны ({self.success_count} записей).")
        else:
            logger.warning(f"Ошибки при сборе данных с Bybit: Успешно: {self.success_count}, Ошибки: {self.error_count}.")
