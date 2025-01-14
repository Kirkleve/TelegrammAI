from data_sources import make_request
from db_manager import insert_news_data
from logger import logger
from rate_limiter import can_run, set_delay
from keys import twitter_bearer_token

class TwitterService:
    def __init__(self):
        self.service_key = "get_twitter_data"
        self.url = 'https://api.twitter.com/2/tweets/search/recent'
        self.headers = {'Authorization': f'Bearer {twitter_bearer_token}'}
        self.params = {'query': '#cryptocurrency', 'tweet.fields': 'created_at,text', 'max_results': 10}

    def fetch_and_save_data(self):
        if not can_run(self.service_key):
            logger.warning("Пропуск запуска Twitter: ожидание окончания задержки.")
            return

        try:
            response = make_request(self.url, headers=self.headers, params=self.params)
            tweets = response.get('data', [])
            if tweets:
                for tweet in tweets:
                    insert_news_data("Twitter", tweet['text'], "", "")
                logger.info(f"Сохранено {len(tweets)} твитов.")
                print("Данные Twitter сохранены")
            else:
                logger.warning("Нет новых твитов.")
        except Exception as e:
            logger.error(f"Ошибка при работе с Twitter: {e}")
            set_delay(self.service_key)
