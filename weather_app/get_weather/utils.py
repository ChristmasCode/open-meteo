import requests


def get_city_coordinates(city_name):
    url = f"https://nominatim.openstreetmap.org/search?q={city_name}&format=json"
    response = requests.get(url)
    data = response.json()

    if data:
        latitude = float(data[0]['lat'])
        longitude = float(data[0]['lon'])
        return {'latitude': latitude, 'longitude': longitude}
    else:
        return None