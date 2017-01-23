from utils import Configimport requests
import datetime
import json
import math
import re

class LimitFactors:
	
	APIKEY = '53b7cffbaec63da155201fca282be50d'
	AppID = '78kOzFRwOsBUvjs8cSwJ'
	AppCode = 'tVPlWqdtR7lLIgHau3sQrA'
	weekdayPercent = [0.24, 1.88, 4.61, 7.6, 6.41, 6.04, 6.2, 6.12, 6.39, 6.73, 8.01, 8.38, 8.14, 6.69, 5.25, 4.08, 3.12, 2.24, 1.47, 0.4]  #od 4 do 23 procentowy rozkład pasażerów
	weekendPercent = [0.4, 1.62, 2.84, 4.75, 5.77, 6.50, 7.04, 7.45, 7.73, 7.88, 7.34, 6.78, 6.69, 6.63, 5.9, 5.37, 3.8, 3.17, 2.09, 0.26]
	swietoPercent = [0.26, 1.31, 1.78, 3.34, 4.39, 5.46, 6.36, 7.35, 7.42, 7.89, 7.84, 7.54, 7.56, 7.52, 7.02, 6.66, 4.59, 3.57, 1.81, 0.26]
	weekdayPassengerSum = 1087189
	weekendPassengerSum = 680431
	swietoPassengerSum = 459748
	tramPopularity = 0.5
	numberTramStops = 334
	leftTopBoxCoordinates = '50.103093,19.870580'   #współrzędne prostokąta obszaru krakowa dla którego będzie obliczany współczynnik ruchu
	rightBottomBoxCoordinates = '50.011471,20.029605'

	
	def getCurrentWeather(self):
		r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Krakow&APPID='+LimitFactors.APIKEY)
		self.currentWeather = r.json()

	def getRequestingTrafficFlowData(self):
		r = requests.get('https://traffic.cit.api.here.com/traffic/6.2/flow.json?&app_code='+LimitFactors.AppCode+'&app_id='+LimitFactors.AppID+'&bbox='+LimitFactors.leftTopBoxCoordinates+';'+LimitFactors.rightBottomBoxCoordinates)
		self.currentTraffic = r.json()

	def getForecast5days(self):
		self.forecast5days = requests.get('api.openweathermap.org/data/2.5/forecast?q=Krakow,PL&APPID='+LimitFactors.APIKEY)

	def tempFactor(self):
		self.currentTemp = float(self.currentWeather['main']['temp']) - 273.15
		if self.currentTemp>26:
			return 0.97
		elif self.currentTemp>16 and self.currentTemp<26:
			return 1
		elif self.currentTemp>6 and self.currentTemp<16:
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
			numberPeople = 0.1
			self.timeDelayOnStop = numberPeople*(5.0-1.2*math.log(numberPeople))
		else:
			h = now.hour-4
			if now.weekday>=0 and now.weekday<6:
				numberPeople = (LimitFactors.tramPopularity*LimitFactors.weekdayPercent[h]*LimitFactors.weekdayPassengerSum)/(100*LimitFactors.numberTramStops*6)
			elif now.weekday==6:
				numberPeople = (LimitFactors.tramPopularity * LimitFactors.weekendPercent[h] * LimitFactors.weekendPassengerSum) / (100 * LimitFactors.numberTramStops*6)
			else:
				numberPeople = (LimitFactors.tramPopularity * LimitFactors.swietoPercent[h] * LimitFactors.swietoPassengerSum) / (100 * LimitFactors.numberTramStops*6)
		if numberPeople<= 1:
			self.timeDelayOnStop = numberPeople * (5.0 - 1.2 * math.log(numberPeople))
		else:
			self.timeDelayOnStop = 1.2*numberPeople

	def trafficFlowFactor(self):
		currentTrafficString = str(self.currentTraffic)
		count = 0;
		sum = 0;
		for m in re.finditer('"JF":', currentTrafficString):		#wyszukanie param "JF": w stringu bo po nim jest liczba oznaczająca Jam Factor
			count = count+1											#The number between 0.0 and 10.0 indicating the expected quality of travel. When there is a road closure,
			tmp = currentTrafficString[m.end()]						# the Jam Factor will be 10. As the number approaches 10.0 the
			if currentTrafficString[m.end()] == '-':				#quality of travel is getting worse. -1.0 indicates that a Jam Factor could not be calculated.
				tmp = '0'
				count = count - 1
			elif currentTrafficString[m.end()+1]=='.':
				tmp = tmp+currentTrafficString[m.end()+1]+currentTrafficString[m.end()+2]
			elif currentTrafficString[m.end()+1]=='0':
				tmp = '10'
			sum=sum+float(tmp)
		self.averageJamfactor = 1-sum/(count*10)					#obliczenie parametru Jam factor dla całego Krakowa

	def currentFactorImpacts(self):
		self.getCurrentWeather()
		self.getRequestingTrafficFlowData()
		return self.snowFactor()*self.crowdFactor()*self.tempFactor()*self.averageJamfactor

	def returntTimeDelayOnStop(self):
		return self.timeDelayOnStop


