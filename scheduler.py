from services.news_service import NewsService
from services.coinmarketcap_service import CoinMarketCapService
from services.twitter_service import TwitterService
from services.bybit_service import BybitService
from services.coingecko_service import CoinGeckoService
from services.cryptopanic_service import CryptoPanicService

news_service = NewsService()
bybit_service = BybitService()
coingecko_service = CoinGeckoService()
coinmarketcap_service = CoinMarketCapService()
twitter_service = TwitterService()
cryptopanic_service = CryptoPanicService()

def job():
    news_service.fetch_and_save_data()
    bybit_service.fetch_and_save_data()
    coingecko_service.fetch_and_save_data()
    coinmarketcap_service.fetch_and_save_data()
    twitter_service.fetch_and_save_data()
    cryptopanic_service.fetch_and_save_all_data()


#schedule.every().day.at("08:00").do(job)
#schedule.every().day.at("12:00").do(job)
#schedule.every().day.at("16:00").do(job)
#schedule.every().day.at("20:00").do(job)
