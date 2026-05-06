import requests

API_KEY = "91dffd32e42f55166d13632aa104bfb7"

def get_weather(city):

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url)

    data = response.json()

    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    weather = data["weather"][0]["main"]

    return temp, humidity, weather


def farmer_advice(temp,humidity,weather):

    if weather == "Rain":
        return "Rain expected. Protect crops."

    elif temp > 35:
        return "High temperature. Irrigation recommended."

    elif humidity > 85:
        return "High humidity. Risk of fungal disease."

    else:
        return "Weather normal for farming."