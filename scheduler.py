import schedule
from service.news_service import NewsService
from service.coinmarketcap_service import CoinMarketCapService
from service.twitter_service import TwitterService
from service.bybit_service import BybitService
from service.coingecko_service import CoinGeckoService

news_service = NewsService()
bybit_service = BybitService()
coingecko_service = CoinGeckoService()
coinmarketcap_service = CoinMarketCapService()
twitter_service = TwitterService()

def job():
    news_service.fetch_and_save_data()
    #bybit_service.fetch_and_save_data()
    coingecko_service.fetch_and_save_data()
    coinmarketcap_service.fetch_and_save_data()
    #twitter_service.fetch_and_save_data()


#schedule.every().day.at("08:00").do(job)
#schedule.every().day.at("12:00").do(job)
#schedule.every().day.at("16:00").do(job)
#schedule.every().day.at("20:00").do(job)
