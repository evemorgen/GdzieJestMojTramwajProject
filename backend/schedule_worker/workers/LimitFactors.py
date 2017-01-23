import requests
import datetime
from utils import Config
import json
import math

class LimitFactors:
	
	APIKEY = '53b7cffbaec63da155201fca282be50d'
	AppID - '78kOzFRwOsBUvjs8cSwJ'
	AppCode - 'tVPlWqdtR7lLIgHau3sQrA'
	weekdayPercent = [0.24, 1.88, 4.61, 7.6, 6.41, 6.04, 6.2, 6.12, 6.39, 6.73, 8.01, 8.38, 8.14, 6.69, 5.25, 4.08, 3.12, 2.24, 1.47, 0.4]
	weekendPercent = [0.4, 1.62, 2.84, 4.75, 5.77, 6.50, 7.04, 7.45, 7.73, 7.88, 7.34, 6.78, 6.69, 6.63, 5.9, 5.37, 3.8, 3.17, 2.09, 0.26]
	swietoPercent = [0.26, 1.31, 1.78, 3.34, 4.39, 5.46, 6.36, 7.35, 7.42, 7.89, 7.84, 7.54, 7.56, 7.52, 7.02, 6.66, 4.59, 3.57, 1.81, 0.26]
	weekdayPassengerSum = 1087189
	weekendPassengerSum = 680431
	swietoPassengerSum = 459748
	tramPopularity = 0.5
	numberTramStops = 334
	
	def getCurrentWeather(self):
		r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Krakow&APPID='+str(LimitFactors.APIKEY))
		self.currentWeather = r.json()

	def getRequestingTrafficFlowData(self):
		r = requests.get('https://traffic.cit.api.here.com/traffic/6.2/flow.json?quadkey=12020330&app_code='+str(LimitFactors.AppCode)+'&app_id='+str(LimitFactors.AppIDAppCode))
		self.currentTraffic = r.json()

	def getForecast5days(self):
		self.forecast5days = requests.get('api.openweathermap.org/data/2.5/forecast?q=Krakow,PL&APPID='+str(APIKEY))

	def tempFactor(self):
		self.currentTemp = float(self.currentWeather['main']['temp']) - 273.15
		if currentTemp>26:
			return 0.97
		elif currentTemp>16 and currentRain<26:
			return 1
		elif currentTemp>6 and currentRain<16:
			return 0.99
		else:
			return 0.97

	def rainFactor(self):
		if self.currentWeather['rain']:
			currentRain = float(self.currentWeather['rain']['3h'])/3
			if currentRain<2:
				return 0.98
			elif currentRain>2 and currentRain<4:
				return 0.97
			elif currentRain>4 and currentRain<6:
				return 0.95
			else:
				return 0.91
		else:
			return 1

	def snowFactor(self):
		if self.currentWeather['snow']:
			currentSnow = float(self.currentWeather['snow']['3h'])/3
			if currentSnow<3:
				return 0.95
			elif currentSnow>3 and currentSnow<5:
				return 0.86
			else:
				return 0.81
		else:
			return 1

	def crowdFactor(self):
		now = datetime.datetime.now()
		if now.hour>=24 and now.hour<4:
			numberPeople = 0.2
			self.timeDelayOnStop = numberPeople*(5.0-1.2*math.log(numberPeople))
		else:
			h = new.hour-4
			if now.weekday>=0 and now.weekday<6:
				numberPeople = (LimitFactors.tramPopularity*LimitFactors.weekdayPercent[h]*LimitFactors.weekdayPassengerSum)/(100*LimitFactors.numberTramStops*6)
			elif now.weekday==6:
				numberPeople = (LimitFactors.tramPopularity * LimitFactors.weekendPercent[h] * LimitFactors.weekendPassengerSum) / (100 * LimitFactors.numberTramStops*6)
			else:
				numberPeople = (LimitFactors.tramPopularity * LimitFactors.swietoPercent[h] * LimitFactors.swietoPassengerSum) / (100 * LimitFactors.numberTramStops*6)
		if numberPeople<= 23:
			self.timeDelayOnStop = numberPeople * (5.0 - 1.2 * math.log(numberPeople))
		else:
			self.timeDelayOnStop = 1.2*numberPeople


	


	def currentFactorImpacts(self):
		self.getCurrentWeather()
		return self.snowFactor()*self.crowdFactor()*self.tempFactor()




