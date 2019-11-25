import requests
import json
import configs.config as config

class News_api:

	def __init__(self):

		# api.openweathermap.org/data/2.5/forecast?id=
		self.api_url_website = "https://newsapi.org/v2/top-headlines?";
		self.api_key = config.news_api['key'];
		self.country = config.news_api['country'];
		self.language = config.news_api['language'];
		self.category = config.news_api['category'];
		self.pageSize = config.news_api['pageSize'];

		self.api_url = self.api_url_website #+ "" + str(self.api_id_city) + "&appid=" + self.api_key;
		self.api_url += "apiKey=" + self.api_key
		if(len(self.country) != 0):
			self.api_url += "&country=" + self.country
		if(len(self.language) != 0):
			self.api_url += "&language=" + self.language
		if(len(self.category) != 0):
			self.api_url += "&category=" + self.category
		if(self.pageSize != 0):
			self.api_url += "&pageSize=" + str(self.pageSize)


	def get_data(self):

		response = requests.get(self.api_url)
		return response.json()