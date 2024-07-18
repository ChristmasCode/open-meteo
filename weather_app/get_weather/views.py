from django.shortcuts import render
from .utils import get_city_coordinates
import openmeteo_requests
import requests_cache
from retry_requests import retry
from loguru import logger

def index(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        try:
            coordinates = get_city_coordinates(city)
        except Exception as e:
            # Обработка ошибок, связанных с получением координат города
            logger.info(f"Error getting city coordinates: {e}")
            return render(request, 'index.html', {'error': 'Failed to get city coordinates'})

        if coordinates:
            # Setup the Open-Meteo API client with cache and retry on error
            try:
                cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
                retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
                openmeteo = openmeteo_requests.Client(session=retry_session)
            except Exception as e:
                # Обработка ошибок, связанных с настройкой сессии
                logger.info(f"Error setting up session: {e}")
                return render(request, 'index.html', {'error': 'Failed to set up API client'})

            # Get weather data
            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": coordinates['latitude'],
                "longitude": coordinates['longitude'],
                "current": ["temperature_2m", "apparent_temperature", "wind_speed_10m", "wind_direction_10m"],
                "forecast_days": 1
            }
            try:
                responses = openmeteo.weather_api(url, params=params)
                response = responses[0]
            except Exception as e:
                # Обработка ошибок, связанных с получением данных погоды
                logger.info(f"Error getting weather data: {e}")
                return render(request, 'index.html', {'error': 'Failed to get weather data'})

            # Current values
            try:
                current = response.Current()
                current_temperature_2m = current.Variables(0).Value()
                current_apparent_temperature = current.Variables(1).Value()
            except Exception as e:
                # Обработка ошибок, связанных с извлечением текущих значений
                logger.info(f"Error getting current weather values: {e}")
                return render(request, 'index.html', {'error': 'Failed to get current weather values'})

            context = {
                'city': city,
                'current_temperature': round(current_temperature_2m, 1),
                'current_apparent_temperature': round(current_apparent_temperature, 1)
            }
            return render(request, 'index.html', context)
    return render(request, 'index.html')