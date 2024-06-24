import requests
from datetime import datetime
class NewsController:
    def __init__(self):
        pass

    def get_recommendation_news(self,countries='us',industries='Technology',pages=1) -> list[dict]:
        url = f"https://api.marketaux.com/v1/news/all?api_token=ILqmhd82JOP8Feo9YFwxoFca82e8mzasKWG4jYKe&language=en&industries={industries}&page={pages}&limit=2&countries={countries}"
        response = requests.get(url).json()
        news_list  = []
        for news in response['data']:
            new = {}
            new['title'] = news['title']
            new['description'] = news['description']
            new['url'] = news['url']
            new['snippet'] = news['snippet']
            new['image_url'] = news['image_url']
            published_at_dt = datetime.strptime(news['published_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
            new['published_at'] = published_at_dt.strftime('%Y-%m-%d %H:%M')
            news_list.append(new)
        return news_list

    def get_news_by_symbol(self,symbol,pages=1) -> list[dict]:
        url  = f"https://api.marketaux.com/v1/news/all?api_token=ILqmhd82JOP8Feo9YFwxoFca82e8mzasKWG4jYKe&language=en&limit=5&symbols={symbol}&page={pages}"
        response = requests.get(url).json()
        news_list = []
        for news in response['data']:
            new = {}
            new['title'] = news['title']
            new['description'] = news['description']
            new['url'] = news['url']
            new['snippet'] = news['snippet']
            new['image_url'] = news['image_url']
            published_at_dt = datetime.strptime(news['published_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
            new['published_at'] = published_at_dt.strftime('%Y-%m-%d %H:%M')
            news_list.append(new)
        return news_list

if __name__ == '__main__':
    print(NewsController().get_news_by_symbol("aapl"))
