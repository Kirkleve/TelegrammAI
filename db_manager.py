import sqlite3

def create_db():
    conn = sqlite3.connect('crypto_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS crypto_prices (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 source TEXT,
                 symbol TEXT,
                 last_price REAL,
                 high_price REAL,
                 low_price REAL,
                 open_price REAL,
                 timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS crypto_news (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 source TEXT,
                 title TEXT,
                 description TEXT,
                 url TEXT,
                 published_at DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def insert_price_data(source, symbol, last_price, high_price, low_price, open_price):
    conn = sqlite3.connect('crypto_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO crypto_prices (source, symbol, last_price, high_price, low_price, open_price) VALUES (?, ?, ?, ?, ?, ?)",
              (source, symbol, last_price, high_price, low_price, open_price))
    conn.commit()
    conn.close()

def insert_news_data(source, title, description, url):
    conn = sqlite3.connect('crypto_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO crypto_news (source, title, description, url) VALUES (?, ?, ?, ?)",
              (source, title, description, url))
    conn.commit()
    conn.close()
