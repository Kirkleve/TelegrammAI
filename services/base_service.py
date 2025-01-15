import requests
from logger import logger
from rate_limiter import set_delay

class BaseService:
    def __init__(self, service_key):
        self.service_key = service_key

    def make_request(self, url, headers=None, params=None):
        """
        Выполняет HTTP-запрос с обработкой ошибок.
        """
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            try:
                return response.json()
            except ValueError:
                logger.error(f"{self.service_key}: Ответ API не является корректным JSON.")
                return None
        except requests.exceptions.RequestException as e:
            logger.error(f"{self.service_key}: Ошибка при выполнении запроса: {e}")
            set_delay(self.service_key)
            return None
