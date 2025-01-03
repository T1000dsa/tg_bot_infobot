import requests
from datetime import datetime as dt
import itertools
format_date = '%Y-%m-%d %H:%M:%S'
class Weather:
	"""
	Takes a 3 values: x - city name, mode - weather forecast mode (current and 5 days(per days)) and
	api.
	To use Weather - put in class like this - > 
	Exemplar = Weather('London', '5 days')

	Also you can use named keys like this - >
	Exemplar = Weather(x='London', mode='5 days')
	"""
	def __init__(self, x=None, mode='current', api=None):
		self.__x = x
		self.__api = "fde841fe0d3fdac9babcf624c70c320b" if api is None else api
		self.__mode = mode.lower()
		self.__mods = {
				'current':f'https://api.openweathermap.org/data/2.5/weather?q={self.__x}&appid={self.__api}',
				'5 days':f'https://api.openweathermap.org/data/2.5/forecast?q={self.__x}&appid={self.__api}',
				}
		self.__main_cities = sorted(['Moscow', 'Karachi', 'Kolkata', 'Buenos Aires', 'Lagos', 'Paris', 'Jakarta', 'Berlin',
			'Beijing', 'Delhi', 'Istanbul', 'Tokyo', 'London', 'New York', 'Shanghai', 'São Paulo', 'Mexico City', 'Cairo', 
			'Dhaka', 'Mumbai', 'Osaka', 'Tehran'])
		try:
			self.__url = self.__mods.get(mode)
		except(NameError) as err:
			print('Error!', err)
			raise NameError

	def giveforecast(self) -> tuple[str]:
		"""
		Return weather to the requared city. Create a txt file with results.
		"""
		try:
			responce = requests.get(self.__url, params={'units':'metric', 'lang':'ru'})
			country = responce.json()['sys']['country']
		except(TimeoutError, ConnectionError) as err:
			print('Cant connect to server.', err)

		data_json = responce.json()

		if self.__mode == 'current' and responce.status_code == 200:
			return (self.__x, country, data_json['main']['temp'], data_json['weather'][0]['description'], dt.fromtimestamp(data_json['dt']))
		if self.__mode == '5 days' and responce.status_code == 200:
			return ((self.__x, country, i['main']['temp'], i['weather'][0]['description'],  i['dt_txt']) for i in data_json['list'])
		elif responce.status_code != 200:
			print('Error', responce.status_code)

	def main_cities(self, mode=None):
		mode = self.__mode if mode == None else mode
		data_main_cities = self.__main_cities
		for i in data_main_cities:
			try:
				data_url = self.__mods[mode].replace(str(self.__x), i)
				responce = requests.get(data_url, params={'units':'metric', 'lang':'ru'})
			except(TimeoutError, ConnectionError) as err:
				print('Cant connect to server.', err)
			if mode.lower() == '5 days': #Doesn't work in current version
				yield i, ((x['main']['temp'],  x['dt_txt']) for x in responce.json()['list'])
			if mode.lower() == 'current':
				temp:str = responce.json()['main']['temp']
				main:str = responce.json()['weather'][0]['description']
				country:str = responce.json()['sys']['country']
				date:dt = dt.fromtimestamp(responce.json()['dt'])
				yield (i,country, temp, main, date)