import logging

# Настройка логгера
logger = logging.getLogger("CryptoLogger")
logger.setLevel(logging.DEBUG)  # Установим минимальный уровень логирования

# Форматирование логов
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Обработчик для записи в файл с поддержкой UTF-8
file_handler = logging.FileHandler("crypto_log.txt", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)  # Записывать все сообщения (DEBUG и выше)
file_handler.setFormatter(formatter)

# Обработчик для вывода в консоль
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # Выводить только INFO и выше
console_handler.setFormatter(formatter)

# Добавляем обработчики в логгер
logger.addHandler(file_handler)
logger.addHandler(console_handler)
