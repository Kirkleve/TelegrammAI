from services.base_service import BaseService
from db_manager import insert_price_data
from logger import logger
from keys import cmc_api_key


class CoinMarketCapService(BaseService):
    def __init__(self):
        super().__init__("get_crypto_data_coinmarketcap")
        self.base_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        self.success_count = 0
        self.error_count = 0
        self.currency = 'USD'  # Валюта для котировок
        self.limit = 100  # Количество криптовалют для обработки

    def fetch_and_save_data(self):
        """
        Основной метод для получения данных с CoinMarketCap и их сохранения в базу данных.
        """
        if not self._can_run():
            return

        logger.info(f"Начинаем сбор данных для топ-{self.limit} криптовалют с CoinMarketCap.")

        params = {
            'start': '1',  # С какой позиции начинать (1 = первая криптовалюта)
            'limit': self.limit,  # Количество криптовалют
            'convert': self.currency,  # Валюта
        }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': cmc_api_key,  # Ваш API-ключ
        }

        data = self.make_request(self.base_url, headers=headers, params=params)
        if data and isinstance(data, dict) and 'data' in data:
            self._process_data(data['data'])
        else:
            self._log_error("Некорректная структура ответа от CoinMarketCap.", data)

        self._finalize()

    def _process_data(self, data):
        """
        Обрабатывает данные, полученные с CoinMarketCap, и сохраняет их в базу данных.
        """
        for item in data:
            symbol = item.get('symbol', 'N/A')
            last_price = self._safe_float(item.get('quote', {}).get(self.currency, {}).get('price'))
            high_price = self._safe_float(item.get('quote', {}).get(self.currency, {}).get('high_24h'))
            low_price = self._safe_float(item.get('quote', {}).get(self.currency, {}).get('low_24h'))
            open_price = 0  # CoinMarketCap не предоставляет цену открытия

            try:
                insert_price_data("CoinMarketCap", symbol, last_price, high_price, low_price, open_price)
                self.success_count += 1
            except Exception as e:
                logger.error(f"{self.service_key}: Ошибка при сохранении данных {symbol}: {e}")
                self.error_count += 1

    def _log_error(self, message, data=None):
        logger.error(f"{self.service_key}: {message}")
        if data:
            logger.debug(f"{self.service_key}: Ответ: {data}")
        self.error_count += 1

    def _safe_float(self, value):
        """
        Преобразует значение в float, если это возможно; иначе возвращает 0.
        """
        try:
            return float(value) if value is not None else 0
        except ValueError:
            return 0

    def _can_run(self):
        return True  # Здесь можно добавить проверку ограничений времени.

    def _finalize(self):
        """
        Итоговый отчёт.
        """
        if self.error_count == 0:
            logger.info(f"Все данные с CoinMarketCap успешно собраны ({self.success_count} записей).")
        else:
            logger.warning(f"Ошибки при сборе данных с CoinMarketCap: Успешно: {self.success_count}, Ошибки: {self.error_count}.")
