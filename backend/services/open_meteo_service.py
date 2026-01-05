import requests

URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=-38.74"
    "&longitude=-72.59"
    "&current=temperature_2m,pressure_msl,wind_speed_10m"
)

def fetch_current():
    r = requests.get(URL, timeout=10)
    r.raise_for_status()
    return r.json()["current"]
