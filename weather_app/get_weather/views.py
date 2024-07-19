from django.shortcuts import render
from .open_meteo_api.api import OpenMeteoApiClient
from .utils import get_city_coordinates, UnableToGetCityCoordinatesException
from loguru import logger


def handle_get_coordinates_error(e):
    logger.info(f"Error getting city coordinates: {e}")
    return {'error': 'Failed to get city coordinates'}


def handle_get_weather_error(e):
    logger.info(f"Error getting weather data: {e}")
    return {'error': 'Failed to get weather data'}


def index(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        try:
            coordinates = get_city_coordinates(city)

            if not coordinates:
                return render(request, 'index.html')

            api_client = OpenMeteoApiClient()
            current_temperature = ["temperature_2m", "apparent_temperature"]
            weather_data = api_client.get_weather_data(coordinates['latitude'], coordinates['longitude'], current_temperature)
            current = weather_data['current_weather']
            current_temperature_2m = current['temperature_2m']
            current_apparent_temperature = current['apparent_temperature']
        except UnableToGetCityCoordinatesException as e:
            return render(request, 'index.html', handle_get_coordinates_error(e))
        except Exception as e:
            return render(request, 'index.html', handle_get_weather_error(e))

        context = {
            'city': city,
            'current_temperature': round(current_temperature_2m, 1),
            'current_apparent_temperature': round(current_apparent_temperature, 1)
        }
        return render(request, 'index.html', context)
