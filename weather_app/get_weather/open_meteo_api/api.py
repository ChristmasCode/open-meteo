from retry_requests import retry
import requests_cache
from retry import retry
from requests.exceptions import RequestException

class OpenMeteoApiClient:
    def __init__(self):
        self.cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        self.retry_session = retry(self.cache_session, retries=5, backoff_factor=0.2)

    def get_weather_data(self, latitude, longitude, current_temperature):
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": current_temperature,
            "forecast_days": 1
        }

        try:
            responses = self.retry_session.get(url, params=params)
            responses.raise_for_status()
            return responses.json()
        except RequestException as e:
            raise Exception(f"Error getting weather data: {e}")