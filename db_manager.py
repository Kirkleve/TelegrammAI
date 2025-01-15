import sqlite3
from logger import logger

def create_db():
    """
    Создаёт базу данных и таблицы, если они ещё не существуют.
    """
    conn = sqlite3.connect('crypto_data.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    c = conn.cursor()

    # Таблица для хранения цен
    c.execute('''CREATE TABLE IF NOT EXISTS crypto_prices (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 source TEXT,
                 symbol TEXT,
                 last_price REAL,
                 high_price REAL,
                 low_price REAL,
                 open_price REAL,
                 timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')

    # Таблица для хранения новостей
    c.execute('''CREATE TABLE IF NOT EXISTS crypto_news (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 source TEXT,
                 title TEXT,
                 description TEXT,
                 url TEXT UNIQUE,  -- Уникальное ограничение на URL
                 published_at DATETIME DEFAULT CURRENT_TIMESTAMP)''')

    conn.commit()
    conn.close()


def news_exists(title, url):
    """
    Проверяет, существует ли новость с указанными title и url в базе данных.

    :param title: Заголовок новости.
    :param url: Ссылка на новость.
    :return: True, если новость существует, иначе False.
    """
    conn = sqlite3.connect('crypto_data.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    c = conn.cursor()
    c.execute("SELECT 1 FROM crypto_news WHERE title = ? OR url = ?", (title, url))
    exists = c.fetchone() is not None
    conn.close()
    return exists


def insert_price_data(source, symbol, last_price, high_price, low_price, open_price):
    """
    Вставляет данные о цене криптовалюты в базу данных.

    :param source: Источник данных.
    :param symbol: Символ криптовалюты.
    :param last_price: Последняя цена.
    :param high_price: Максимальная цена.
    :param low_price: Минимальная цена.
    :param open_price: Цена открытия.
    """
    conn = sqlite3.connect('crypto_data.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO crypto_prices (source, symbol, last_price, high_price, low_price, open_price) VALUES (?, ?, ?, ?, ?, ?)",
                  (source, symbol, last_price, high_price, low_price, open_price))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Пропускаем дублирующие записи
    except Exception as e:
        logger.error(f"Ошибка при добавлении данных в базу: {e}")
    finally:
        conn.close()


def insert_news_data(source, title, description, url):
    """
    Вставляет новость в базу данных, если она ещё не существует.

    :param source: Источник данных.
    :param title: Заголовок новости.
    :param description: Описание новости.
    :param url: Ссылка на новость.
    """
    if news_exists(title, url):
        return  # Если новость существует, просто выходим из функции

    conn = sqlite3.connect('crypto_data.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO crypto_news (source, title, description, url) VALUES (?, ?, ?, ?)",
                  (source, title, description, url))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Пропускаем дублирующие записи
    except Exception as e:
        logger.error(f"Ошибка при добавлении новости: {e}")
    finally:
        conn.close()
