import os
import requests
from urllib.parse import quote # used to ensure space or special characters are properly encoded in the url eg #New York
from dotenv import load_dotenv

load_dotenv()  # Load from .env file
def get_weather_data(city):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    city = quote(city)
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={api_key}&units=metric"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None

