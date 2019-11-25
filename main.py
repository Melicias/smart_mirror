from classes.weather_api import Weather_api
from classes.news_api import News_api
from newsapi import NewsApiClient

weather_api = Weather_api()
news_api = News_api()
#newsapi = NewsApiClient(api_key='5770ad4f261349b886ca4a187e593fb9')

weather = weather_api.get_data()
news = news_api.get_data()
#top_headlines = newsapi.get_top_headlines(category='technology',
#                                          language='en',
#                                          country='us')

print(weather_api.jprint(weather))



