
import requests

def geocode_address(address):
    url = 'https://nominatim.openstreetmap.org/search'
    params = {
        'q': address,
        'format': 'json',
        'addressdetails': 1,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        results = response.json()
        if results:
            lat = results[0]['lat']
            lon = results[0]['lon']
            return lat, lon
    return None, None
