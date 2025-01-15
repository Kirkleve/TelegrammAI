from services.base_service import BaseService
from db_manager import insert_price_data
from logger import logger


class CoinGeckoService(BaseService):
    def __init__(self):
        super().__init__("get_crypto_data_coingecko")
        self.base_url = 'https://api.coingecko.com/api/v3/coins/markets'
        self.success_count = 0
        self.error_count = 0
        self.currency = 'usd'  # Валюта для котировок
        self.per_page = 50  # Количество криптовалют за один запрос
        self.pages = 2  # Для топ-100 потребуется 2 страницы

    def fetch_and_save_data(self):
        """
        Основной метод для получения данных с CoinGecko и их сохранения в базу данных.
        """
        if not self._can_run():
            return

        logger.info(f"Начинаем сбор данных для топ-{self.per_page * self.pages} криптовалют с CoinGecko.")

        for page in range(1, self.pages + 1):
            self._fetch_and_save_page(page)

        self._finalize()

    def _fetch_and_save_page(self, page):
        """
        Получает данные для одной страницы криптовалют и сохраняет их в базу.
        """
        params = {
            'vs_currency': self.currency,
            'order': 'market_cap_desc',  # По убыванию рыночной капитализации
            'per_page': self.per_page,  # Количество записей на странице
            'page': page,  # Номер страницы
        }

        data = self.make_request(self.base_url, params=params)
        if data and isinstance(data, list):
            logger.info(f"Обработка страницы {page}: {len(data)} записей.")
            self._process_data(data)
        else:
            self._log_error(f"Некорректная структура ответа от CoinGecko для страницы {page}.", data)

    def _process_data(self, data):
        """
        Обрабатывает данные, полученные с CoinGecko, и сохраняет их в базу данных.
        """
        for item in data:
            symbol = item.get('id', 'N/A')
            last_price = self._safe_float(item.get('current_price'))
            high_price = self._safe_float(item.get('high_24h'))
            low_price = self._safe_float(item.get('low_24h'))
            open_price = 0  # CoinGecko не предоставляет цену открытия

            try:
                insert_price_data("CoinGecko", symbol, last_price, high_price, low_price, open_price)
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
            logger.info(f"Все данные с CoinGecko успешно собраны ({self.success_count} записей).")
        else:
            logger.warning(f"Ошибки при сборе данных с CoinGecko: Успешно: {self.success_count}, Ошибки: {self.error_count}.")
