from data_sources import make_request
from db_manager import insert_news_data
from logger import logger
from rate_limiter import can_run, set_delay
from keys import api_key_news

class NewsService:
    def __init__(self):
        self.service_key = "get_crypto_news"
        self.url = 'https://newsapi.org/v2/everything'
        self.params = {'q': 'cryptocurrency', 'apiKey': api_key_news, 'language': 'en', 'sortBy': 'publishedAt'}

    def fetch_and_save_data(self):
        if not can_run(self.service_key):
            logger.warning("Пропуск запуска News API: ожидание окончания задержки.")
            return

        try:
            data = make_request(self.url, params=self.params)
            if isinstance(data, dict) and 'articles' in data:
                for article in data['articles']:
                    title = article.get('title', 'Без названия')
                    description = article.get('description', 'Описание отсутствует')
                    url = article.get('url', '')
                    insert_news_data("NewsAPI", title, description, url)
                    logger.info(f"Новость сохранена: {title}")
                    print("Данные News сохранены")
            else:
                logger.warning("Некорректная структура ответа от News API.")
        except Exception as e:
            logger.error(f"Ошибка при работе с News API: {e}")
            set_delay(self.service_key)
