import requests
from loguru import logger
from requests import RequestException


class UnableToGetCityCoordinatesException(Exception):
    pass

def get_city_coordinates(city_name):
    url = f"https://nominatim.openstreetmap.org/search?q={city_name}&format=json"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for non-2xx status codes
        data = response.json()

        if data:
            if data[0].get('lat') and data[0].get('lon'):
                latitude = float(data[0]['lat'])
                longitude = float(data[0]['lon'])
                return {'latitude': latitude, 'longitude': longitude}
            else:
                raise UnableToGetCityCoordinatesException("No valid city data found")
        else:
            raise UnableToGetCityCoordinatesException("No city data found")
    except RequestException as e:
        logger.error(f"Error getting city coordinates: {e}")
        raise UnableToGetCityCoordinatesException("Failed to get city coordinates")