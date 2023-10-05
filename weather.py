#!/usr/bin/env python3
"""
    Author: Pek, Jonetta
    Date: 5 October 2023
    Purpose: Program that retrieves weather data for different cities from OpenWeather API
"""


import requests
import credentials


API_KEY = credentials.openweather_apikey


def get_coordinates():
    COORD_URL = 'http://api.openweathermap.org/geo/1.0/direct?'
    city = input('Enter a city name:\n>>>')
    query_string = {
        'appid': API_KEY, 
        'q':city
    }
    response = requests.get(url=COORD_URL, params=query_string) 
    if response.status_code == 200:
        data = response.json()
        return data[0]['lat'], data[0]['lon'], city
    else: 
        print('An error occurred while retrieving coordinates data.')


def get_data():
    """
    payload example:
        {'base': 'stations',
         'clouds': {'all': 88},
         'cod': 200,
         'coord': {'lat': 2.1833, 'lon': 33.6833},
         'dt': 1696517118,
         'id': 235186,
         'main': {'feels_like': 301.25,
                  'grnd_level': 893,
                  'humidity': 38,
                  'pressure': 1008,
                  'sea_level': 1008,
                  'temp': 301.8,
                  'temp_max': 301.8,
                  'temp_min': 301.8},
        'name': 'Amuria',
        'sys': {'country': 'UG', 'sunrise': 1696476665, 'sunset': 1696520181},
        'timezone': 10800,
        'visibility': 10000,
        'weather': [{'description': 'overcast clouds',
                    'icon': '04d',
                    'id': 804,
                    'main': 'Clouds'}],
        'wind': {'deg': 33, 'gust': 3.06, 'speed': 1.33}}
    """
    WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather'
    lat, lon, city = get_coordinates()
    query_string = {
        'appid': API_KEY,
        'lat':lat,
        'lon': lon
    }
    response = requests.get(url=WEATHER_URL, params=query_string)
    if response.status_code == 200:
        return response.json(), city
    else: 
        print('An error occurred while retrieving weather data.')

def get_temp(data: dict):
    return data['main']['temp']


def get_weather(data: dict):
    return data['weather'][0]['description']

def main():
    data, city = get_data()
    print(f'City: {city.capitalize()}\nWeather: {get_weather(data)}\nTemperature: {round(get_temp(data)-273, 2)} Celsius')

if __name__ == '__main__':
    main()