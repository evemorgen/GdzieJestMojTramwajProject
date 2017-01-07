import requests

class OpenWeatherMapApiWrapper:
	
	APIKEY = 111111
	
	def getCurrentWeather(self):
		self.currentWeather = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Krakow&APPID='+str(APIKEY))
		
	def getHistoricalWeather(self, start, end):
		self.historicalWeather = requests.get('http://history.openweathermap.org/data/2.5/history/city?q=Krakow,PL&type=hour&start='+str(start)+'&end='+str(end)+'&APPID='+str(APIKEY))

	def getForecast5days(self):
		self.forecast5days = requests.get('api.openweathermap.org/data/2.5/forecast?q=Krakow,PL&APPID='+str(APIKEY))
		