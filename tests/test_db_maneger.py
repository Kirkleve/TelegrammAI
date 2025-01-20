from unittest.mock import patch, MagicMock
from db_manager import create_db  # Импортируем функцию для создания базы данных


def test_create_db():
    # Мокаем sqlite3.connect для того, чтобы не открывать реальное подключение
    with patch('sqlite3.connect') as mock_connect:
        # Мокаем успешное подключение (симулируем подключение)
        mock_connect.return_value = MagicMock()

        # Вызовем функцию create_db
        create_db()

        # Проверим, что sqlite3.connect была вызвана один раз с аргументами
        mock_connect.assert_called_once_with('crypto_data.db', detect_types=3)
