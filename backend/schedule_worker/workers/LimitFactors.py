import requests
import datetime
from utils import Config
import json

class LimitFactors:
	
	APIKEY = '53b7cffbaec63da155201fca282be50d'
	weekdayPercent = [0.24, 1.88, 4.61, 7.6, 6.41, 6.04, 6.2, 6.12, 6.39, 6.73, 8.01, 8.38, 8.14, 6.69, 5.25, 4.08, 3.12, 2.24, 1.47, 0.4]
	
	def getCurrentWeather(self):
		r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Krakow&APPID='+str(APIKEY))
		self.currentWeather = r.json()

	def getForecast5days(self):
		self.forecast5days = requests.get('api.openweathermap.org/data/2.5/forecast?q=Krakow,PL&APPID='+str(APIKEY))

	def tempFactor(self):
		self.currentTemp = float(self.currentWeather['main']['temp']) - 273.15
		if currentTemp>26:
			return 0.97
		elif currentTemp>18 and currentRain<26:
			return 1
		elif currentTemp>6 and currentRain<18:
			return 0.99
		else:
			return 0.97

	def rainFactor(self):
		currentRain = float(currentWeather['rain']['3h'])/3
		if currentRain<2:
			return 0.98
		elif currentRain>2 and currentRain<4:
			return 0.97
		elif currentRain>4 and currentRain<6:
			return 0.95
		else:
			return 0.91

	def snowFactor(self):
		currentSnow = float(self.currentWeather['snow']['3h'])/3
		if currentSnow<3:
			return 0.95
		elif currentRain>3 and currentRain<5:
			return 0.86
		else:
			return 0.81






