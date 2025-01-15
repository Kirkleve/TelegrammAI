from services.base_service import BaseService
from db_manager import insert_news_data
from logger import logger
from keys import twitter_bearer_token


class TwitterService(BaseService):
    def __init__(self):
        super().__init__("get_twitter_data")
        self.base_url = "https://api.twitter.com/2/tweets/search/recent"
        self.success_count = 0
        self.error_count = 0
        self.query = "#cryptocurrency"  # Тема поиска
        self.max_results = 10  # Максимум твитов за один запрос

    def fetch_and_save_data(self):
        """
        Основной метод для получения данных с Twitter API и их сохранения в базу данных.
        """
        if not self._can_run():
            return

        logger.info(f"Начинаем сбор данных из Twitter API (запрос: {self.query}).")

        headers = {
            "Authorization": f"Bearer {twitter_bearer_token}"
        }
        params = {
            "query": self.query,
            "tweet.fields": "created_at,text",  # Поля твита
            "max_results": self.max_results,  # Количество твитов
        }

        data = self.make_request(self.base_url, headers=headers, params=params)
        if data and isinstance(data, dict) and "data" in data:
            self._process_data(data["data"])
        else:
            self._log_error("Некорректная структура ответа от Twitter API.", data)

        self._finalize()

    def _process_data(self, tweets):
        """
        Обрабатывает список твитов и сохраняет их в базу данных.
        """
        for tweet in tweets:
            title = tweet.get("text", "Без текста")
            description = "Твиттер"
            url = f"https://twitter.com/twitter/status/{tweet.get('id', '')}"  # Формируем URL твита

            try:
                insert_news_data("Twitter", title, description, url)
                self.success_count += 1
            except Exception as e:
                logger.error(f"{self.service_key}: Ошибка при сохранении твита: {title}. {e}")
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
            logger.info(f"Все данные с Twitter API успешно собраны ({self.success_count} записей).")
        else:
            logger.warning(f"Ошибки при сборе данных с Twitter API: Успешно: {self.success_count}, Ошибки: {self.error_count}.")
