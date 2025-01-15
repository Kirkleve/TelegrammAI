import logging

class CustomConsoleHandler(logging.StreamHandler):
    """
    Кастомный обработчик для вывода в консоль только итоговых сообщений.
    """
    def emit(self, record):
        # Проверяем уровень записи
        if record.levelname == "INFO" and "Данные сохранены из" in record.msg:
            print(record.msg)
        elif record.levelname == "ERROR":
            print("ОШИБКА ПРОВЕРЬ ИНФОРМАЦИЮ В ЛОГЕРЕ")


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

# Кастомный обработчик для вывода в консоль
console_handler = CustomConsoleHandler()
console_handler.setLevel(logging.INFO)  # Выводить только итоговые сообщения
console_handler.setFormatter(formatter)

# Добавляем обработчики в логгер
logger.addHandler(file_handler)
logger.addHandler(console_handler)
