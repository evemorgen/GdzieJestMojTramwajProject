import json
import logging
import datetime
import math
import pprint

from tornado.gen import coroutine
from tornado.httpclient import AsyncHTTPClient
from lib.tornado_yieldperiodic.yieldperiodic import YieldPeriodicCallback

from utils import Config


class DelayFactorWorker(YieldPeriodicCallback):

    def __init__(self):
        self.config = Config()
        self.httpclient = AsyncHTTPClient()

        self.api_key = self.config['weather_api_key']
        self.app_id = self.config['here_app_id']
        self.app_code = self.config['here_app_code']
        self.top_left = self.config['here_box_top_left']
        self.bottom_right = self.config['here_box_bottom_right']
        self.weekday_percent = self.config['weekday_percent']
        self.weekend_percent = self.config['weekend_percent']
        self.holiday_percent = self.config['holiday_percent']
        self.weekday_sum = self.config['weekday_sum']
        self.weekend_sum = self.config['weekend_sum']
        self.holiday_sum = self.config['holiday_sum']
        self.tram_popularity = self.config['tram_popularity']
        self.number_of_stops = self.config['stops_number']
        YieldPeriodicCallback.__init__(self, self.run, 60000, faststart=True)

    @coroutine
    def handle_weather(self, res):
        logging.info('saving current weather')
        self.current_weather = json.loads(res.body.decode('utf-8'))

    @coroutine
    def get_current_weather(self):
        url = 'http://api.openweathermap.org/data/2.5/weather?q=Krakow&APPID=%s' % self.api_key
        yield self.httpclient.fetch(url, self.handle_weather)

    @coroutine
    def handle_traffic(self, res):
        logging.info('saving current traffic')
        self.current_traffic = json.loads(res.body.decode('utf-8'))

    @coroutine
    def get_current_traffic_flow(self, top_left, bottom_right):
        url = 'https://traffic.cit.api.here.com/traffic/6.2/flow.json?&app_code=%s&app_id=%s&bbox=%s;%s' % (
            self.app_code,
            self.app_id,
            top_left,
            bottom_right
        )
        yield self.httpclient.fetch(url, self.handle_traffic)

    @coroutine
    def handle_forecast(self, res):
        logging.info('saving forecast')
        self.current_forecast = json.loads(res.body.decode('utf-8'))
        logging.info(self.current_forecast)

    @coroutine
    def get_forecast_5_days(self):
        url = 'http://api.openweathermap.org/data/2.5/forecast?q=Krakow,PL&APPID=%s' % self.api_key
        yield self.httpclient.fetch(url, self.handle_forecast)

    def calculate_temp_factor(self):
        current_temp = float(self.current_weather['main']['temp']) - 273.15
        if current_temp > 16 and current_temp < 26:
            return 1
        elif current_temp > 6 and current_temp < 16:
            return 0.99
        else:
            return 0.97

    def calculate_rain_factor(self):
        if 'rain' in self.current_weather:
            current_rain = float(self.current_weather['rain']['3h']) / 3
            if current_rain < 2:
                return 0.98
            elif current_rain >= 2 and current_rain < 4:
                return 0.97
            elif current_rain >= 4 and current_rain < 6:
                return 0.95
            else:
                return 0.91
        else:
            return 1

    def calculate_snow_factor(self):
        if 'snow' in self.current_weather:
            current_snow = float(self.current_weather['snow']['3h']) / 3
            if current_snow < 3:
                return 0.95
            elif current_snow >= 3 and current_snow < 5:
                return 0.86
            else:
                return 0.81
        else:
            return 1

    def calculate_crowd_factor(self):
        now = datetime.datetime.now()
        if now.hour >= 24 and now.hour < 4:
            number_of_people = 0.1
            self.stop_delay = number_of_people * (5.0 - 1.2 * math.log(number_of_people))
        else:
            h = now.hour
            day_factor = {
                0: [self.weekday_percent, self.weekday_sum],
                1: [self.weekday_percent, self.weekday_sum],
                2: [self.weekday_percent, self.weekday_sum],
                3: [self.weekday_percent, self.weekday_sum],
                4: [self.weekday_percent, self.weekday_sum],
                5: [self.weekend_percent, self.weekend_sum],
                6: [self.holiday_percent, self.holiday_sum]
            }
            number_of_people = (self.tram_popularity * day_factor[now.weekday()][0][h] * day_factor[now.weekday()][1])
            number_of_people /= (100 * self.number_of_stops * 6)
        if number_of_people <= 1:
            self.delay_on_stop = number_of_people * (5.0 - 1.2 * math.log(number_of_people))
        else:
            self.delay_on_stop = 1.2 * number_of_people * 10
        return self.delay_on_stop

    @coroutine
    def calculate_traffic_factor(self, first_stop, second_stop):
        yield self.get_current_traffic_flow(first_stop, second_stop)
        suma = 0
        count = 1
        routes = self.current_traffic['RWS'][0]['RW']
        for route in routes:
            for cf in route['FIS'][0]['FI']:
                suma += cf['CF'][0]['JF']
                count += 1
        logging.info("traffic info:  %s, %s, %s", suma, count, 1 - suma / count / 10)
        return (1 - suma / count / 10)

    @coroutine
    def calculate_factor(self, tram):
        assert 1 == self.config['rain_weight'] + self.config['snow_weight'] + self.config['temp_weight'] + self.config['traffic_weight']
        stop_1_string = "%s,%s" % (tram.last_stop['x'], tram.last_stop['y'])
        stop_2_string = "%s,%s" % (tram.next_stop['x'], tram.next_stop['y'])
        traffic = yield self.calculate_traffic_factor(stop_1_string, stop_2_string)
        temp = self.calculate_temp_factor()
        rain = self.calculate_rain_factor()
        snow = self.calculate_snow_factor()
        crowd = self.calculate_crowd_factor()
        logging.info("factors: rain: %s, snow: %s, stop time: %s, traffic: %s", rain, snow, crowd, traffic)
        tram.stop_time = crowd
        tram.velocity = tram.normal_velocity * (
            rain * self.config['rain_weight'] +
            snow * self.config['snow_weight'] +
            temp * self.config['temp_weight'] +
            traffic * self.config['traffic_weight']
        )

    @coroutine
    def run(self):
        yield self.get_current_weather()
