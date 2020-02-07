import requests
import json
from datetime import datetime
import configs.config as config

#Falta verificar o response.status_code / se da erro (url errado)
#
class Weather_api:

	def __init__(self):
		# api.openweathermap.org/data/2.5/forecast?id=
		self.api_url_website = "http://api.openweathermap.org/data/2.5/forecast?id=";
		self.api_id_city = config.weather_api['city_id'];
		self.api_key = config.weather_api['key'];

		self.api_url = self.api_url_website + "" + str(self.api_id_city) + "&appid=" + self.api_key;


	def get_data(self):
		response = requests.get(self.api_url)
		return self.montar_array(response.json())

	#return data
	#data -> 0 -> string with city name and country
	#     -> 1 -> json with the first 9 
	#     -> 2 -> json with weather by days (5 days)
	def montar_array(self, json):
		data = []
		#city/country
		data.append(json['city']['name'])
		if(json['city']['country'] != "none"):
			data[0] += " " + json['city']['country']

		# get first 9 elements from json and save it on data[1]
		data.append(self.organize_first_nine(json['list'][0:9]))
		data.append([])
		
		weather_in_a_day = []
		#organize weather by days on a array
		for weather in json['list']:
			if(len(weather_in_a_day) != 0):
				#check if its the same day and if it is, add the weather to the array
				if(datetime.fromtimestamp(weather["dt"]).day == datetime.fromtimestamp(weather_in_a_day[0]["dt"]).day):
					weather_in_a_day.append(weather)
				else:
					#if its a different day, call organize_weather_day and delete all data from the weather_in_array so it can be filled for the next day
					#add mid-night from the next day
					weather_in_a_day.append(weather)
					data[2].append(self.organize_weather_day(weather_in_a_day))
					del weather_in_a_day[:]
					weather_in_a_day.append(weather)
			else:
				#empty array, add first element
				weather_in_a_day.append(weather)

		return data


	#return weather_in_hours
	#weather_in_hours -> 0 -> day
	#         		  -> 1 -> temperature
	#         		  -> 2 -> min
	#         		  -> 3 -> max
	#          		  -> 4 -> wind
	#         		  -> 5 -> humidity
	#         		  -> 6 -> clouds
	#         		  -> 7 -> rain
	#         		  -> 8 -> picture
	def organize_weather_day(self, weather):
		weather_in_hours = ["",0,0,0,0,0,0,0,[]]

		date = datetime.fromtimestamp(weather[0]['dt'])
		weather_in_hours[0] = str(date.day) + "-" + str(date.month)# + "-" + str(date.year)
		mini = []
		maxi = []
		pic = []
		pic_id = []

		for w in weather:
			weather_in_hours[1] += w['main']['temp']
			mini.append(w['main']['temp_min'])
			maxi.append(w['main']['temp_max'])
			weather_in_hours[4] += w['wind']['speed']
			weather_in_hours[5] += w['main']['humidity']
			weather_in_hours[6] += w['clouds']['all']
			if("rain" in w):
				weather_in_hours[7] += w['rain']['3h']
			if(date.hour >= 9 and date.hour <= 18):
				pic.append(w['weather'])
				pic_id.append(w['weather'][0]['id'])

		weather_in_hours[1] = round((weather_in_hours[1]/len(weather_in_hours)) - 273.15,2)
		weather_in_hours[2] = round((max(maxi)) - 273.15,2)
		weather_in_hours[3] = round((min(mini)) - 273.15,2)
		weather_in_hours[4] = weather_in_hours[4]/len(weather_in_hours)
		weather_in_hours[5] = weather_in_hours[5]/len(weather_in_hours)
		weather_in_hours[6] = weather_in_hours[6]/len(weather_in_hours)
		if(weather_in_hours[7] != 0):
			weather_in_hours[7] = weather_in_hours[7]/len(weather_in_hours)

		if(len(pic) == 0):
			weather_in_hours[8] = weather[0]['weather']
		else:
			weather_in_hours[8] = pic[self.most_frequent(pic_id)]

		return weather_in_hours

	
	def most_frequent(self,List): 
	    counter = 0
	    num = List[0]
	    i = 0
	    ret = 0
	    
	    for l in List:
	        curr_frequency = List.count(l) 
	        if(curr_frequency > counter): 
	            counter = curr_frequency 
	            num = l
	            ret = i
	        ++i 
	  
	    return ret



	#data 			  -> 0 -> hour
	#         		  -> 1 -> temperature
	#          		  -> 2 -> wind
	#         		  -> 3 -> humidity
	#         		  -> 4 -> clouds
	#         		  -> 5 -> rain
	#         		  -> 6 -> picture
	def organize_first_nine(self,ww):
		data = [[],[],[],[],[],[],[],[],[]]

		i=0
		for w in ww:
			date = datetime.fromtimestamp(w['dt'])
			data[i].append(str(date.hour) + ":00")
			data[i].append(w['main']['temp']-273.15)
			data[i].append(self.check_if_key_exists(w,'winds','speed'))
			data[i].append(w['main']['humidity'])
			data[i].append(self.check_if_key_exists(w,'clouds','all'))
			data[i].append(self.check_if_key_exists(w,'rain','3h'))
			data[i].append(w['weather'][0]['icon'])
			i=i+1

		return data


	def check_if_key_exists(self,data,key,key2):
		try:
		    return data[key][key2]
		except KeyError:
		    return ""


	def jprint(self, obj):
	    # create a formatted string of the Python JSON object
	    text = json.dumps(obj, sort_keys=True, indent=4)
	    return text
