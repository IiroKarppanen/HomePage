# importing requests and json
import requests, json
from datetime import datetime as dt, timedelta, timezone, date
import datetime
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
CITY = "New York"
API_KEY = "80a0b6e9e8019ea97ceb2137ba302c7b"

URL = BASE_URL + "q=" + CITY + "&units=metric&appid=" + API_KEY

# HTTP request
response = requests.get(URL)
# checking the status code of the request
if response.status_code == 200:
   # getting data in the json format
   data = response.json()
   # getting the main dict block
   main = data['main']

   wind = data['wind']

   # getting temperature
   temperature = main['temp']
   # getting the humidity
   humidity = main['humidity']
   # getting the pressure
   pressure = main['pressure']
   # weather report
   report = data['weather']

   speed = wind['speed']

   sun = data['sys']

   seconds = data['timezone']
   local_timezone = datetime.timedelta(seconds=seconds)

   utc_time = dt.utcnow()
   local_time = utc_time + local_timezone

   my_timezone = dt.now() - utc_time

   print(my_timezone)

   sunrise = dt.fromtimestamp(sun['sunrise']) + (local_timezone - my_timezone)
   sunset = dt.fromtimestamp(sun['sunset']) + (local_timezone - my_timezone)

   if sunrise < local_time < sunset:
          print("day")
   else:
         print("night")
 
  


