from services.base_service import BaseService
from db_manager import insert_news_data
from logger import logger
from keys import cryptopanic_api_key


class CryptoPanicService(BaseService):
    def __init__(self):
        super().__init__("get_cryptopanic_data")
        self.base_url = "https://cryptopanic.com/api/v1/posts/"
        self.success_count = 0
        self.error_count = 0
        self.filters = ['rising', 'hot', 'bullish', 'bearish', 'important']
        self.currencies = ['BTC', 'ETH', 'XRP', 'SOL', 'DOGE']
        self.languages = ['en', 'ru']

    def fetch_and_save_all_data(self):
        """
        Основной метод для получения всех доступных бесплатных данных с CryptoPanic.
        """
        if not self._can_run():
            return

        logger.info("Начинаем сбор данных из CryptoPanic.")

        # Сбор данных по фильтрам, валютам и языкам
        for filter_name in self.filters:
            self._fetch_and_save(kind='news', extra_params={'filters': filter_name})

        for currency in self.currencies:
            self._fetch_and_save(kind='news', extra_params={'currencies': currency})

        for language in self.languages:
            self._fetch_and_save(kind='news', extra_params={'regions': language})

        self._finalize()

    def _fetch_and_save(self, kind, extra_params=None):
        """
        Выполняет запрос к CryptoPanic для определённого фильтра или языка и сохраняет данные.
        """
        params = {
            'auth_token': cryptopanic_api_key,
            'kind': kind,
            'public': 'true',  # Используем публичное API
        }
        if extra_params:
            params.update(extra_params)

        data = self.make_request(self.base_url, params=params)
        if data and isinstance(data, dict) and 'results' in data:
            self._process_data(data['results'], extra_params)
        else:
            self._log_error(f"Некорректная структура ответа от CryptoPanic (параметры: {extra_params}).", data)

    def _process_data(self, results, params):
        """
        Обрабатывает данные, полученные с CryptoPanic, и сохраняет их в базу данных.
        """
        for post in results:
            title = post.get('title', 'Без названия')
            description = post.get('domain', 'Без описания')
            url = post.get('url', '')

            try:
                insert_news_data("CryptoPanic", title, description, url)
                self.success_count += 1
            except Exception as e:
                logger.error(f"{self.service_key}: Ошибка при сохранении новости: {title}. {e}")
                self.error_count += 1

    def _log_error(self, message, data=None):
        logger.error(f"{self.service_key}: {message}")
        if data:
            logger.debug(f"{self.service_key}: Ответ: {data}")
        self.error_count += 1

    def _can_run(self):
        return True  # Здесь можно добавить проверку ограничений времени.

    def _finalize(self):
        """
        Итоговый отчёт.
        """
        if self.error_count == 0:
            logger.info(f"Все данные с CryptoPanic успешно собраны ({self.success_count} записей).")
        else:
            logger.warning(f"Ошибки при сборе данных с CryptoPanic: Успешно: {self.success_count}, Ошибки: {self.error_count}.")
