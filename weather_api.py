import os
import urllib.request
import json
from datetime import datetime

# https://api.openweathermap.org/data/2.5/onecall?lat=46.7853&lon=-121.7353718&exclude=minutely,hourly,alerts&appid=afba879cbf23c5b78e3946c501e9eb49&units=imperial


BASE_URL = 'https://api.openweathermap.org/data/2.5/onecall?lat='
KEY = os.getenv('OPENWEATHERMAP_API_KEY')
LON = '&lon='
EXCLUDE = '&exclude=minutely,hourly,alerts&appid='
UNITS = '&units=imperial'

def fetch_weather(lat, lon):
  lat_str = str(lat)
  print(lat_str)
  lon_str = str(lon)
  url = BASE_URL + lat_str + LON + lon_str + EXCLUDE + 'afba879cbf23c5b78e3946c501e9eb49' + UNITS

  response = urllib.request.urlopen(url).read()

  json_response = json.loads(response) 

  return json_response









#     import os
# import urllib.request
# import json
# from datetime import datetime

# https://api.openweathermap.org/data/2.5/onecall?lat=46.7853&lon=-121.7353718&exclude=minutely,hourly,alerts&appid=afba879cbf23c5b78e3946c501e9eb49&units=imperial

# BASE_URL = 'http://api.openweathermap.org/data/2.5/weather?q='
# last_result = None
# last_ts = None
# is_up = False

# def fetch_weather(location=None):
#     global is_up, last_result, last_ts
#     if location is None: 
#         location = "Melbourne,Victoria,Australia"
#     api_key = os.getenv('OPENWEATHERMAP_API_KEY')
#     if api_key is None:
#         print("OpenWeatherMap API key not specified")
#         return None
# url = BASE_URL + location + '&units=metric&appid=' + api_key
#     response = urllib.request.urlopen(url).read() 
#     src = json.loads(response) 
#     #Some simple validation
#     if not "main" in src:
#         is_up = False
#         return None
#     result = {
#         'location': {
#             'name': src['name'],
#             'country' : src['sys']['country'],
#             'lat': src['coord']['lat'],
#             'lon': src['coord']['lon'],
#             },
#         'temperature' : src['main']['temp'],
#         'humidity': src['main']['humidity'],
#         'wind' : {
#             'speed' : float(src['wind']['speed']) * 3.6,
#             'deg' : src['wind']['deg'] 
#         },
#         'cloud' : src['clouds']['all'],
#         'pressure' : src['main']['pressure'],
#     }
#     last_result = result
#     last_ts = datetime.now()
#     return result