import requests
from loguru import logger


def get_city_coordinates(city_name):
    url = f"https://nominatim.openstreetmap.org/search?q={city_name}&format=json"
    try:
        response = requests.get(url)
        data = response.json()

        if data:
            latitude = float(data[0]['lat'])
            longitude = float(data[0]['lon'])
            return {'latitude': latitude, 'longitude': longitude}
        else:
            raise ValueError("No city data found")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting city coordinates: {e}")
        raise Exception("Failed to get city coordinates")