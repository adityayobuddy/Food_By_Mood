# utils/weather_api.py
import requests

def get_weather(city="Delhi"):
    API_KEY = "9ff72d32fc17572d9cbc0f3d57f1aa66"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    data = requests.get(url).json()
    return {
        "temperature": data["main"]["temp"],
        "condition": data["weather"][0]["main"].lower()
    }
