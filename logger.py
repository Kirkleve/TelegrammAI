import logging

# Настройка логирования
logging.basicConfig(
    filename="crypto_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding='utf-8'
)

logger = logging.getLogger()