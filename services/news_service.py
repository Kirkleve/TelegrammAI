from services.base_service import BaseService
from db_manager import insert_news_data
from logger import logger
from keys import api_key_news


class NewsService(BaseService):
    def __init__(self):
        super().__init__("get_crypto_news")
        self.base_url = "https://newsapi.org/v2/everything"
        self.success_count = 0
        self.error_count = 0
        self.default_query = "cryptocurrency"
        self.language = "en"  # Язык новостей
        self.page_size = 20  # Максимум новостей за один запрос
        self.pages = 5  # Сколько страниц обрабатывать (максимум 100 новостей)

    def fetch_and_save_data(self):
        """
        Основной метод для получения и сохранения новостей.
        """
        if not self._can_run():
            return

        logger.info(f"Начинаем сбор данных из News API (запрос: {self.default_query}).")

        for page in range(1, self.pages + 1):
            self._fetch_and_save_page(page)

        self._finalize()

    def _fetch_and_save_page(self, page):
        """
        Получает данные для одной страницы и сохраняет их в базу.
        """
        params = {
            'q': self.default_query,  # Запрос темы
            'apiKey': api_key_news,  # Ваш API-ключ
            'language': self.language,  # Язык новостей
            'pageSize': self.page_size,  # Количество новостей на странице
            'page': page,  # Номер страницы
            'sortBy': 'publishedAt'  # Сортировка по дате публикации
        }

        data = self.make_request(self.base_url, params=params)
        if data and isinstance(data, dict) and 'articles' in data:
            self._process_data(data['articles'])
        else:
            self._log_error(f"Некорректная структура ответа от News API для страницы {page}.", data)

    def _process_data(self, articles):
        """
        Обрабатывает список новостей и сохраняет их в базу данных.
        """
        for article in articles:
            title = article.get('title', 'Без названия')
            description = article.get('description', 'Без описания')
            url = article.get('url', '')

            try:
                insert_news_data("NewsAPI", title, description, url)
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
            logger.info(f"Все данные с News API успешно собраны ({self.success_count} записей).")
        else:
            logger.warning(f"Ошибки при сборе данных с News API: Успешно: {self.success_count}, Ошибки: {self.error_count}.")
