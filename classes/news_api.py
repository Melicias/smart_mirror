import requests
import json
import configs.config as config

class News_api:

	def __init__(self):

		# api.openweathermap.org/data/2.5/forecast?id=
		self.category_i = 0
		self.api_url_website = "https://newsapi.org/v2/top-headlines?"
		self.api_key = config.news_api['key']
		self.country = config.news_api['country']
		self.language = config.news_api['language']
		self.source = config.news_api['source']
		self.pageSize = config.news_api['pageSize']
		self.category = config.news_api['category'][self.category_i]
		self.category_total = len(config.news_api['category'])
		self.generate_url(False)

		


	def generate_url(self,new_category):

		if(new_category):
			self.category_number()
			self.category = config.news_api['category'][self.category_i]

		self.api_url = self.api_url_website #+ "" + str(self.api_id_city) + "&appid=" + self.api_key;
		self.api_url += "apiKey=" + self.api_key
		if(len(self.source) != 0):
			self.api_url += "&sources=" + self.source
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

	def category_number(self):
		self.category_i += 1
		print(self.category_i)
		if(self.category_total == self.category_i):
			self.category_i = 0

	def get_category(self):
		return self.category

