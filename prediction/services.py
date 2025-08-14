import requests
from datetime import date as date_cls

class OpenMeteoClient:
    """Simple client using free Open-Meteo APIs (no API key required).
    1) Geocode a place name to lat/lon.
    2) Query daily precipitation_probability for the given date.
    """

    GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
    FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

    @classmethod
    def geocode(cls, location: str):
        r = requests.get(cls.GEOCODE_URL, params={"name": location, "count": 1})
        r.raise_for_status()
        data = r.json()
        if not data.get('results'):
            return None
        top = data['results'][0]
        return {
            'name': top.get('name'),
            'lat': top.get('latitude'),
            'lon': top.get('longitude'),
            'country': top.get('country'),
        }

    @classmethod
    def daily_rain_probability(cls, lat: float, lon: float, day: date_cls):
        ymd = day.isoformat()
        params = {
            'latitude': lat,
            'longitude': lon,
            'daily': 'precipitation_probability_max',
            'timezone': 'auto',
            'start_date': ymd,
            'end_date': ymd,
        }
        r = requests.get(cls.FORECAST_URL, params=params)
        r.raise_for_status()
        payload = r.json()
        daily = payload.get('daily', {})
        probs = daily.get('precipitation_probability_max') or []
        if not probs:
            return None, payload
        return float(probs[0]), payload
