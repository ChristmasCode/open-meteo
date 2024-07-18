from django.shortcuts import render
from .utils import get_city_coordinates
import openmeteo_requests
import requests_cache
from retry_requests import retry

def index(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        coordinates = get_city_coordinates(city)
        if coordinates:
            # Setup the Open-Meteo API client with cache and retry on error
            cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
            retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
            openmeteo = openmeteo_requests.Client(session=retry_session)

            # Get weather data
            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": coordinates['latitude'],
                "longitude": coordinates['longitude'],
                "current": ["temperature_2m", "apparent_temperature", "wind_speed_10m", "wind_direction_10m"],
                "forecast_days": 1
            }
            responses = openmeteo.weather_api(url, params=params)
            response = responses[0]

            # Current values
            current = response.Current()
            current_temperature_2m = current.Variables(0).Value()
            current_apparent_temperature = current.Variables(1).Value()

            context = {
                'city': city,
                'current_temperature': round(current_temperature_2m, 1),
                'current_apparent_temperature': round(current_apparent_temperature, 1)
            }
            return render(request, 'index.html', context)
    return render(request, 'index.html')