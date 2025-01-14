import sqlite3

def check_saved_tweets():
    """
    Проверяет содержимое таблицы crypto_news и выводит сохранённые твиты.
    """
    global conn
    try:
        # Подключаемся к базе данных
        conn = sqlite3.connect('crypto_data.db')
        c = conn.cursor()

        # Извлекаем данные, где source = 'Twitter'
        c.execute("SELECT title, published_at FROM crypto_news WHERE source = 'Twitter'")
        rows = c.fetchall()

        if not rows:
            print("В таблице crypto_news нет данных из Twitter.")
        else:
            print(f"Найдено {len(rows)} твитов из Twitter:")
            for idx, row in enumerate(rows, start=1):
                print(f"{idx}. Текст: {row[0]}")
                print(f"Дата публикации: {row[1]}")
                print("-" * 50)

    except Exception as e:
        print(f"Ошибка при проверке твитов: {e}")
    finally:
        if conn:
            conn.close()

# Вызов функции для проверки твитов
if __name__ == "__main__":
    check_saved_tweets()
