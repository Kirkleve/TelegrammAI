from data_sources import get_crypto_data_coingecko, get_crypto_data_bybit, get_crypto_data_coinmarketcap, get_twitter_data, get_crypto_news
from db_manager import insert_price_data, insert_news_data, sanitize_text
from logger import logger

def job():
    try:
        print("Получение данных с CoinGecko...")
        coingecko_data = get_crypto_data_coingecko()
        for data in coingecko_data:
            try:
                symbol = data['id']
                last_price = float(data.get('current_price', 0))
                high_price = float(data.get('high_24h', 0))
                low_price = float(data.get('low_24h', 0))
                open_price = 0  # CoinGecko не предоставляет цену открытия

                # Запись данных в базу
                insert_price_data("CoinGecko", symbol, last_price, high_price, low_price, open_price)
                print(f"Сохранены данные из CoinGecko: {symbol} - {last_price} USD")
            except Exception as e:
                print(f"Ошибка при обработке данных из CoinGecko для {data['id']}: {e}")

        print("Получение данных с Bybit...")
        bybit_data = get_crypto_data_bybit()
        for data in bybit_data:
            try:
                symbol = data['symbol']
                last_price = float(data.get('lastPrice', 0))
                high_price = float(data.get('highPrice', 0))
                low_price = float(data.get('lowPrice', 0))
                open_price = float(data.get('openPrice', 0))

                # Запись данных в базу
                insert_price_data("Bybit", symbol, last_price, high_price, low_price, open_price)
                print(f"Сохранены данные из Bybit: {symbol} - {last_price} USD")
            except Exception as e:
                print(f"Ошибка при обработке данных из Bybit для {data['symbol']}: {e}")

        print("Получение данных с CoinMarketCap...")
        cmc_data = get_crypto_data_coinmarketcap()
        for data in cmc_data:
            try:
                symbol = data['symbol']
                last_price = float(data['quote']['USD']['price'])
                high_price = float(data['quote']['USD'].get('high_24h', 0))
                low_price = float(data['quote']['USD'].get('low_24h', 0))
                open_price = 0  # CoinMarketCap не предоставляет цену открытия

                # Запись данных в базу
                insert_price_data("CoinMarketCap", symbol, last_price, high_price, low_price, open_price)
                print(f"Сохранены данные из CoinMarketCap: {symbol} - {last_price} USD")
            except Exception as e:
                print(f"Ошибка при обработке данных из CoinMarketCap для {data['symbol']}: {e}")

        print("Получение новостей о криптовалютах...")
        news_data = get_crypto_news()
        for article in news_data:
            try:
                title = article['title']
                description = article['description']
                url = article['url']

                # Запись новостей в базу с указанием источника
                insert_news_data("NewsAPI", title, description, url)
                print(f"Сохранена новость: {title}")
            except Exception as e:
                print(f"Ошибка при обработке новости: {e}")

        print("Получение данных с Twitter...")
        twitter_data = get_twitter_data()
        for tweet in twitter_data:
            sanitized_text = sanitize_text(tweet.get('text', 'Нет текста'))
            insert_news_data("Twitter", sanitized_text, '', '')

        print("Данные успешно обновлены.")
    except Exception as e:
        logger.error(f"Error in job execution: {e}")
        print("Произошла ошибка при обновлении данных. Проверьте логи.")