from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration
from conductor.client.worker.worker_task import worker_task
from conductor.client.configuration.configuration import AuthenticationSettings
from conductor.client.worker.worker import TaskResult
import requests


SERVER_URL = '<url>'
KEY = '<key>'   
SECRET = '<secret>'


@worker_task(task_definition_name='weather_lookup')
def my_task(city: str) -> TaskResult:

   # Geocode the city
   geo = requests.get(
      "https://geocoding-api.open-meteo.com/v1/search",
      params={"name": city, "count": 1},
   ).json()

   if not geo.get("results"):
      return f"Could not find coordinates for '{city}'."

   loc = geo["results"][0]
   lat, lon = loc["latitude"], loc["longitude"]
   name = loc.get("name", city)
   country = loc.get("country", "")

   # Fetch current weather
   weather = requests.get(
      "https://api.open-meteo.com/v1/forecast",
      params={
         "latitude": lat,
         "longitude": lon,
         "current": "temperature_2m,wind_speed_10m,relative_humidity_2m",
      },
   ).json()

   cur = weather["current"]
   temp = cur["temperature_2m"]
   wind = cur["wind_speed_10m"]
   humidity = cur["relative_humidity_2m"]

   return (
      f"{name}, {country}: {temp}\u00b0C, "
      f"wind {wind} km/h, humidity {humidity}%"
   )


if __name__ == "__main__":
  api_config = Configuration(
     server_api_url=SERVER_URL,
     authentication_settings=AuthenticationSettings(
        key_id=KEY,
        key_secret=SECRET
     ),
  )
  task_handler = TaskHandler(configuration=api_config)
  task_handler.start_processes()
