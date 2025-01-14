import logging

# Настройка логирования
logging.basicConfig(
    filename="crypto_log.txt",
    level=logging.ERROR,
    format="%(asctime)s - %(message)s"
)

logger = logging.getLogger()